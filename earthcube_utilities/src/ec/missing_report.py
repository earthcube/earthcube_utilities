#!  python3
import argparse
import logging
import json
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

    for i in sources:
        url = i.get('url')
        repo = i.get('name')

        try:
            report = missingReport(url, bucket, repo, s3Minio, graphendpoint)
            report = json.dumps(report,  indent=2)
            s3Minio.putReportFile(bucket, repo, "missing_report.json", report)
        except Exception as e:
            logging.error(f"could not write missing report for {repo} to s3server:{s3server}:{bucket} error:{e}", repo,s3server,bucket, e)

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
    parser.add_argument('--output',  type=argparse.FileType('w'), dest="output", help="dump to file")


    args = parser.parse_args()
    exitcode = writeMissingReport(args)

if __name__ == '__main__':
    start()
