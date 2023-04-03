#!  python3
import argparse
from io import StringIO, BytesIO
import logging
import os
import sys

from ec.graph.sparql_query import queryWithSparql
from ec.reporting.report import  generateGraphReportsRepo, reportTypes
from ec.datastore import s3
from ec.logger import config_app

log = config_app()

def basicCounts(args):
    """query an endpoint, store results as a json file in an s3 store"""
    log.info(f"Querying {args.graphendpoint} for graph statisitcs  ")
### more work needed before detailed works
    if args.repo == "all":
         # report_json = generateGraphReportsRepo("all",
         #      args.graphendpoint, reportTypes=reportTypes)

        if (args.detailed):
            report_json = generateGraphReportsRepo("all", args.graphendpoint, reportList=reportTypes["all_detailed"] )
        else:
            report_json = generateGraphReportsRepo("all",
                                                       args.graphendpoint,reportList=reportTypes["all"])
    else:
        # report_json = generateGraphReportsRepo(args.repo,
        #   args.graphendpoint,reportTypes=reportTypes)

        if (args.detailed):
            report_json = generateGraphReportsRepo(args.repo, args.graphendpoint,reportList=reportTypes["repo_detailed"] )
        else:
            report_json = generateGraphReportsRepo(args.repo,
                                                       args.graphendpoint, reportList=reportTypes["repo"] )
    s3Minio = s3.MinioDatastore( args.s3server, None)
    #data = f.getvalue()
    bucketname, objectname = s3Minio.putReportFile(args.s3bucket,args.repo,"graph_report.json",report_json)
    return 0
def start():
    """
        Run the generate_repo_stats program.
        query an endpoint, store results as a json file in an s3 store.
        Arguments:
            args: Arguments passed from the command line.
        Returns:
            An exit code.

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--graphendpoint', dest='graphendpoint',
                        help='graph endpoint' ,default="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/")
    parser.add_argument('--s3', dest='s3server',
                        help='s3 server address (localhost:9000)', default='localhost:9000')
    parser.add_argument('--s3bucket', dest='s3bucket',
                        help='s3 server address (localhost:9000)', default='gleaner')
    parser.add_argument('--repo', dest='repo',
                        help='repository', default='all')

    parser.add_argument("--detailed",action='store_true',
                        dest="detailed" ,help='run the detailed version of the reports', default=False)

    args = parser.parse_args()

    exitcode = basicCounts(args)

if __name__ == '__main__':
    start()
