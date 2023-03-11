import argparse
from io import StringIO, BytesIO

from graph.sparqlquery import queryWithSparql

from s3 import s3


def basicCounts(args):
    counts = queryWithSparql( "all_repo_count_datasets",  args.graphendpoint)

    json = counts.to_json( orient = 'records')
    s3Minio = s3.MinioDatastore( args.s3server, None)
    #data = f.getvalue()
    bucketname, objectname = s3Minio.putReportFile(args.s3bucket,"all","dataset_count.json",json)
    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--graphendpoint', dest='graphendpoint',
                        help='graph endpoint' ,default="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/")
    parser.add_argument('--s3', dest='s3server',
                        help='s3 server address (localhost:9000)', default='localhost:9000')
    parser.add_argument('--s3bucket', dest='s3bucket',
                        help='s3 server address (localhost:9000)', default='gleaner')
    args = parser.parse_args()

    exitcode = basicCounts(args)