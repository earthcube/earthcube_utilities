#!  python3
import argparse
import logging
import json
import sys

from pydash.collections import find
from pydash import is_empty
from ec.gleanerio.gleaner import getSitemapSourcesFromGleaner, getGleaner
from ec.reporting.report import missingReport
from ec.datastore import s3

def writeMissingReport(args):
    if (args.cfgfile):
        s3endpoint,  bucket, glnr= getGleaner(args.cfgfile)
        minio = glnr.get("minio")
        # passed paramters override the config parameters
        s3server = args.s3server if args.s3server  else  s3endpoint
        bucket = args.s3bucket if args.s3bucket else bucket
    else:
        s3server = args.s3server
        bucket = args.s3bucket
    graphendpoint = args.graphendpoint  # not in gleaner file, at present
    if is_empty(graphendpoint) or is_empty(s3server) or is_empty(bucket):
        logging.fatal(f" must provide graphendpoint and [a gleaner config or (s3endpoint and s3bucket)]")
        return 1
    logging.info(f" s3server: {s3server} bucket:{bucket} graph:{graphendpoint}")
    s3Minio = s3.MinioDatastore(s3server, None)
    sources = getSitemapSourcesFromGleaner(args.cfgfile)
    sources = list(filter(lambda source: source.get('active'), sources))
    repos=args.source

    for i in sources:
        url = i.get('url')
        repo = i.get('name')
        if repos is not None and len(repos) >0:
            if not find (repos , lambda x: x == repo ):
                continue
        try:
            report = missingReport(url, bucket, repo, s3Minio, graphendpoint, milled=args.milled, summon=args.summon)
            report = json.dumps(report,  indent=2)
            if (args.output): # just append the json files to one filem, for now.
                logging.info(f" report for {repo} appended to file")
                args.output.write(report)
            if not args.no_upload:
                s3Minio.putReportFile(bucket, repo, "missing_report.json", report)
        except Exception as e:
            logging.error(f"could not write missing report for {repo} to s3server:{s3server}:{bucket} error:{e}", repo,s3server,bucket, e)
            return 1
    return 0

def start():
    """
        Run the write_missing_report program.
        Get a list of active repositories from the gleaner file.
        For each repository, generate missing reports and write these information to a json file and upload it to s3.
        Arguments:
            args: Arguments passed from the command line.
        Returns:
            An exit code.
    """
    parser = argparse.ArgumentParser()
    # source of sources, and default s3 store.
    #   at present, graph endpoint is no longer in gleaner
    parser.add_argument('--cfgfile', dest='cfgfile',
                        help='gleaner config file', default='gleaner')
    parser.add_argument('--graphendpoint', dest = 'graphendpoint',
                        help = 'graph endpoint', default = "https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/")
# no default for s3 parameters here. read from gleaner. if provided, these override the gleaner config
    parser.add_argument('--s3', dest = 's3server',
                        help = 's3 server address ')
    parser.add_argument('--s3bucket', dest = 's3bucket',
                        help = 's3 bucket ')
    parser.add_argument('--no_upload', dest = 'no_upload',action='store_true', default=False,
                        help = 'do not upload to s3 bucket ')
    parser.add_argument('--output',  type=argparse.FileType('w'), dest="output", help="dump to file")
    parser.add_argument('--source', action='append', help="one or more repositories (--source a --source b)")
    parser.add_argument('--milled', action='store_true', default=False, help="include milled")
    parser.add_argument('--summon', action='store_true', default=False, help="check summon only")


    args = parser.parse_args()
    exitcode = writeMissingReport(args)
    sys.exit(exitcode)

if __name__ == '__main__':
    start()
