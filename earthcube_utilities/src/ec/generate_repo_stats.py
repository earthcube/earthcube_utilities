#!  python3
import argparse
from io import StringIO, BytesIO
import logging
import os
import sys

from ec.graph.sparql_query import queryWithSparql

from ec.datastore import s3

logging.basicConfig(format='%(levelname)s : %(message)s', level=os.environ.get("LOGLEVEL", "INFO"), stream=sys.stdout)
log = logging.getLogger()

def basicCounts(args):
    """query an endpoint, store results as a json file in an s3 store"""
    log.info(f"Querying {args.graphendpoint} for dataset counts  ")
    counts = queryWithSparql( "all_repo_count_datasets",  args.graphendpoint)

    json = counts.to_json( orient = 'records')
    log.info(f"wrting results to  {args.s3server} {args.s3bucket}\\all\\dataset_count.json for dataset counts  ")
    s3Minio = s3.MinioDatastore( args.s3server, None)
    #data = f.getvalue()
    bucketname, objectname = s3Minio.putReportFile(args.s3bucket,"all","dataset_count.json",json)
    return 0
def start():
    parser = argparse.ArgumentParser()
    parser.add_argument('--graphendpoint', dest='graphendpoint',
                        help='graph endpoint' ,default="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/")
    parser.add_argument('--s3', dest='s3server',
                        help='s3 server address (localhost:9000)', default='localhost:9000')
    parser.add_argument('--s3bucket', dest='s3bucket',
                        help='s3 server address (localhost:9000)', default='gleaner')
    args = parser.parse_args()

    exitcode = basicCounts(args)

if __name__ == '__main__':
    start()
