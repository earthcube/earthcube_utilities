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

def graphStats(args):
    """query an endpoint, store results as a json file in an s3 store"""
    log.info(f"Querying {args.graphendpoint} for graph statisitcs  ")
### more work needed before detailed works
    if args.source == "all":
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
            report_json = generateGraphReportsRepo(args.source, args.graphendpoint,reportList=reportTypes["repo_detailed"] )
        else:
            report_json = generateGraphReportsRepo(args.source,
                                                       args.graphendpoint, reportList=reportTypes["repo"] )
    s3Minio = s3.MinioDatastore( args.s3server, None)
    #data = f.getvalue()

    if (args.output):  # just append the json files to one filem, for now.
        logging.info(f" report for {args.source} appended to file")
        args.output.write(report_json)
    if not args.no_upload:
        bucketname, objectname = s3Minio.putReportFile(args.s3bucket,args.source,"graph_report.json",report_json)
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
    parser.add_argument('--source', dest='source',
                        help='repository', default='all')

    parser.add_argument("--detailed",action='store_true',
                        dest="detailed" ,help='run the detailed version of the reports', default=False)
    parser.add_argument('--no_upload', dest = 'no_upload',action='store_true', default=False,
                        help = 'do not upload to s3 bucket ')
    parser.add_argument('--output',  type=argparse.FileType('w'), dest="output", help="dump to file")

    args = parser.parse_args()

    exitcode = graphStats(args)
    exit(exitcode)

if __name__ == '__main__':
    start()
