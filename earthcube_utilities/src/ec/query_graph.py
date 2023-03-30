#!  python3
import argparse
from io import StringIO, BytesIO
import logging
import os
import sys

from ec.graph.sparql_query import queryWithSparql,listSparqlFilesFromResources

from ec.datastore import s3

logging.basicConfig(format='%(levelname)s : %(message)s', level=os.environ.get("LOGLEVEL", "INFO"), stream=sys.stdout)
log = logging.getLogger()

def basicQuery(args):
    """query an endpoint, return json file in an s3 store"""
    log.info(f"Querying {args.graphendpoint} using {args.query}")
    counts = queryWithSparql(args.query,  args.graphendpoint)

    csv_result = counts.to_csv( quoting=1, index=False)
    if (args.output):
        args.output.write(csv_result)
    else:
        print (csv_result)
    return 0
def start():
    description="A tool to use the queeries in the earthcube utilities"
    epilog = "Queries \n" + "\n".join(listSparqlFilesFromResources())

    parser = argparse.ArgumentParser(description=description, epilog=epilog)

    parser.add_argument("query", help='select_one')
    parser.add_argument('--graphendpoint', dest='graphendpoint',
                        help='graph endpoint' ,default="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/")
    parser.add_argument("--output", type=argparse.FileType('w'), help='output file')

    args = parser.parse_args()
    exitcode = basicQuery(args)


if __name__ == '__main__':
    start()
