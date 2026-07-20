#!  python3
"""
Tool to add geosparql WKT geometry elements to a graph.

Uses the queries in ec/graph/sparql_files/spatial to convert
schema.org spatial coverage (schema:box, schema:latitude/longitude)
into geo:hasGeometry/geo:asWKT triples.

Two modes:
   construct: run the CONSTRUCT query against an endpoint, write the
      resulting triples to a file (nquads by default)
   insert: run the INSERT (SPARQL UPDATE) query against an endpoint.
      This modifies the graph store, so it requires credentials:
      a username/password (blazegraph, graphdb) or an access token (qlever)
"""
import argparse
import logging
import os
import sys

import requests
from rdflib import Dataset, URIRef

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

import ec.graph.sparql_files as sparqlfiles

logging.basicConfig(format='%(levelname)s : %(message)s', level=os.environ.get("LOGLEVEL", "INFO"), stream=sys.stdout)
log = logging.getLogger()

QUERIES = ["box2polygon", "latlon2multipoint"]

# rdflib parser format for the content types an endpoint may return for CONSTRUCT
_CONTENT_TYPE_FORMATS = {
    "application/n-triples": "nt",
    "text/plain": "nt",
    "text/turtle": "turtle",
    "application/x-turtle": "turtle",
    "application/rdf+xml": "xml",
    "application/n-quads": "nquads",
    "text/x-nquads": "nquads",
}


def getSpatialQuery(name: str, mode: str) -> str:
    """read a query from ec/graph/sparql_files/spatial. mode is construct or insert"""
    resource = pkg_resources.files(sparqlfiles).joinpath("spatial", f"{name}_{mode}.rq")
    return resource.read_text()


def constructTriples(query: str, endpoint: str) -> Dataset:
    """run a CONSTRUCT query, parse the response into an rdflib Dataset"""
    headers = {
        "Content-Type": "application/sparql-query",
        "Accept": "application/n-triples, text/plain;q=0.9, text/turtle;q=0.8, application/rdf+xml;q=0.7",
    }
    r = requests.post(endpoint, data=query.encode("utf-8"), headers=headers)
    if r.status_code != 200:
        raise Exception(f"construct query failed: status {r.status_code} endpoint {endpoint} reason {r.reason} {r.text[:500]}")
    content_type = r.headers.get("Content-Type", "").split(";")[0].strip()
    rdf_format = _CONTENT_TYPE_FORMATS.get(content_type, "nt")
    ds = Dataset()
    ds.parse(data=r.text, format=rdf_format)
    return ds


def construct(args) -> int:
    """construct wkt triples and write them out"""
    query = getSpatialQuery(args.query, "construct")
    log.info(f"running {args.query}_construct against {args.graphendpoint}")
    ds = constructTriples(query, args.graphendpoint)
    triple_count = len(ds)
    if triple_count == 0:
        log.warning("query returned no triples")
    if args.graph:
        out = Dataset()
        g = out.graph(URIRef(args.graph))
        for s, p, o, _ in ds:
            g.add((s, p, o))
        ds = out
    data = ds.serialize(format=args.format)
    if args.output:
        args.output.write(data)
        args.output.close()
        log.info(f"wrote {triple_count} triples to {args.output.name}")
    else:
        print(data)
    return 0


def insert(args) -> int:
    """run the INSERT update against an endpoint. requires credentials"""
    query = getSpatialQuery(args.query, "insert")
    endpoint = args.updateendpoint if args.updateendpoint else args.graphendpoint
    headers = {"Content-Type": "application/sparql-update"}
    auth = None
    params = {}
    if args.accesstoken:
        # qlever uses an access token for updates
        headers["Authorization"] = f"Bearer {args.accesstoken}"
        params["access-token"] = args.accesstoken
    elif args.username and args.password:
        auth = (args.username, args.password)
    else:
        log.error("insert requires credentials: --accesstoken, or --username/--password (or GRAPHUSER/GRAPHPASSWORD environment variables)")
        return 1
    log.info(f"running {args.query}_insert against {endpoint}")
    r = requests.post(endpoint, data=query.encode("utf-8"), headers=headers, params=params, auth=auth)
    if r.status_code not in (200, 204):
        log.error(f"insert failed: status {r.status_code} reason {r.reason} {r.text[:500]}")
        return 1
    log.info(f"insert succeeded: {r.status_code}")
    return 0


def start():
    """
        Run the spatial_wkt program.
        Adds geosparql WKT geometry triples for schema.org spatial coverage.
    """
    description = "Create geosparql WKT geometry elements from schema.org spatial coverage (schema:box, lat/lon)."
    parser = argparse.ArgumentParser(description=description)
    subparsers = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("query", choices=QUERIES, help="spatial query to run")
    common.add_argument('--graphendpoint', dest='graphendpoint',
                        help='graph endpoint',
                        default="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/sparql")

    construct_parser = subparsers.add_parser("construct", parents=[common],
                                             help="construct the wkt triples and write them to a file")
    construct_parser.add_argument("--output", type=argparse.FileType('w'), help='output file (default: stdout)')
    construct_parser.add_argument("--format", default="nquads", choices=["nquads", "nt", "turtle"],
                                  help='output format (default: nquads)')
    construct_parser.add_argument("--graph", help='named graph URI to place the triples in (nquads output)')
    construct_parser.set_defaults(func=construct)

    insert_parser = subparsers.add_parser("insert", parents=[common],
                                          help="insert the wkt triples into the graph (requires credentials)")
    insert_parser.add_argument("--updateendpoint", help='update endpoint, if different from the query endpoint')
    insert_parser.add_argument("--accesstoken", default=os.environ.get("GRAPH_ACCESS_TOKEN"),
                               help='access token for updates (qlever). default: GRAPH_ACCESS_TOKEN environment variable')
    insert_parser.add_argument("--username", default=os.environ.get("GRAPHUSER"),
                               help='username for updates. default: GRAPHUSER environment variable')
    insert_parser.add_argument("--password", default=os.environ.get("GRAPHPASSWORD"),
                               help='password for updates. default: GRAPHPASSWORD environment variable')
    insert_parser.set_defaults(func=insert)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == '__main__':
    start()
