#!/usr/bin/env python3

import argparse
import logging
import os
from ec.graph.manageGraph import ManageBlazegraph as mg
from ec.graph.sparql_query import _getSparqlFileFromResources
from ec.summarize.summarize_materializedview import summaryDF2ttl, get_summary4graph,get_summary4repoSubset
from ec.gleanerio.gleaner import endpointUpdateNamespace,getNabu, reviseNabuConfGraph, runNabu
from rdflib import Dataset, Namespace
from urllib.parse import urlparse
from ec.graph.release_graph import ReleaseGraph

def isValidURL(toValidate):
    o = urlparse(toValidate)
    if o.scheme and o.netloc:
        return True
    else:
        return False

def summarizeReleaseOnly():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", dest='url', help='url of file',
                        default="https://oss.geocodes-dev.earthcube.org/gleaner-wf/graphs/latest/summonediris_2023-03-13-11-02-47_release.nq"

                        )

    parser.add_argument("--repo", dest='repo', help='repo name used in the  urn')

    parser.add_argument('--s3base', dest='s3base',
                        help='basurl of',
                        default="https://oss.geocodes-dev.earthcube.org/"
                        )
    parser.add_argument('--s3bucket', dest='s3bucket',
                        help='basurl of',
                        default="gleaner-wf"

                        )
    parser.add_argument('--graphendpoint', dest='graphendpoint',
                        help='graph endpoint with namespace',
                        default="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/sparql"
                        )
    parser.add_argument('--nographsummary', action='store_true', dest='nographsummary',
                        help='send triples to file', default=False)
    parser.add_argument('--summary_namespace', dest='summary_namespace',
                        help='summary_namespace defaults to {repo_summary}',
                        )
    args = parser.parse_args()

    repo = args.repo
    if args.summary_namespace:
        if isValidURL(args.summary_namespace):
            msg = 'For summary_namespace, Please enter the namespace only.'
            print(msg)
            logging.error(msg)
            return 1
        summary = args.summary_namespace
    else:
        summary = f"{repo}_summary"
    endpoint= args.graphendpoint
    graphendpoint = mg.graphFromEndpoint(endpoint)
    SCHEMAORG_http = Namespace("http://schema.org/")
    SCHEMAORG_https = Namespace("https://schema.org/")
    g =   Dataset(default_union=True)
    g.bind('schema_http',SCHEMAORG_http)
    g.bind('schema', SCHEMAORG_https)


    g.parse(args.url, format='nquads')
    ## HOW TO SUMMARIZE from RDF QUadss?
    # this will need to be modularlized, ad reqworked.

    # file = '../resources/sparql/all_summary_query.sparql'
    # with open(file, 'r') as f:
    #     lines = f.read()
    # sumresults = g.query(lines)
    sum_query = _getSparqlFileFromResources("all_summary_query")
    sumresults = g.query(sum_query, result='sparql', initNs={'schema_old': SCHEMAORG_http, 'schema': SCHEMAORG_https})
    if len(sumresults) == 0:
        print("No result. Issue with RDF lib... use a triplestore")
        exit(1)
    r = sumresults.serialize(format="csv")
## this returns no rows.
    # WE CAN USE BLAZEGRAPH, so no use going direct


    try:  # temp has been created
        # created = tempnsgraph.createNamespace()
        # if ( created=='Failed'):
        #     logging.fatal("coould not create namespace")
 #       sumnsgraph = mg(graphendpoint, summary)
        # created = sumnsgraph.createNamespace()
        # if ( created=='Failed'):
        #     logging.fatal("coould not create summary namespace")
        # endpoints for file
        # tempendpoint =endpointUpdateNamespace(endpoint,f"{repo}_temp")

        summaryendpoint =endpointUpdateNamespace(endpoint,summary)

        # newNabucfg = reviseNabuConf(cfg,tempendpoint )
        # runNabu(newNabucfg,repo, args.glcon )

        if repo is not None:
            summarydf = get_summary4repoSubset(endpoint, repo)
        else:
            # this really needs to be paged ;)
            summarydf = get_summary4graph(endpoint)
            repo = ""

        nt,g = summaryDF2ttl(summarydf,repo) # let's try the new generator

        summaryttl = g.serialize(format='longturtle')
        # write to s3  in future
        # with open(os.path.join("output",f"{repo}.ttl"), 'w') as f:
        #      f.write(summaryttl)
        if not args.nographsummary:
            inserted = sumnsgraph.insert(bytes(summaryttl, 'utf-8'),content_type="application/x-turtle" )
            if inserted:
                logging.info(f"Inserted into graph store{sumnsgraph.namespace}" )
            else:
                logging.error(f" dumping file {repo}.ttl  Repo {repo} not inserted into {sumnsgraph.namespace}")

                with open(os.path.join("output",f"{repo}.ttl"), 'w') as f:
                     f.write(summaryttl)
                return 1
        else:
            logging.info(f" dumping file {repo}.ttl  nographsummary: {args.nographsummary} ")

            with open(os.path.join("output", f"{repo}.ttl"), 'w') as f:
                f.write(summaryttl)
    except Exception as ex:
        logging.error(f"error {ex}")
        print(f"Error: {ex}")
        return 1
    # finally:
    #     # need to figure out is this is run after return, I think it is.
    #     logging.debug(f"Deleting Temp namespace {tempnsgraph.namespace}")
    #     deleted = tempnsgraph.deleteNamespace()


if __name__ == '__main__':
    """ Summarize a from a gleaner 'release' set of n-quads file

    Description:
       untested
    """
    # these need to be better
    # url
    # OR
    # s3base, s3bucket
    #   if not repo, read all nq files in graphs/latest
    #
    # graph endpoint,


    exitcode= summarizeReleaseOnly()
    exit(exitcode)
