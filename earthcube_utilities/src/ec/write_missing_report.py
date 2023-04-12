#!  python3
import argparse
import logging
import json
from ec.gleanerio.gleaner import getSitemapSourcesFromGleaner
from ec.reporting.report import missingReport
from ec.datastore import s3

def writeMissingReport(args):
    s3Minio = s3.MinioDatastore(args.s3server, None)
    sources = getSitemapSourcesFromGleaner(args.cfgfile)
    sources = list(filter(lambda source: source.get('active'), sources))

    for i in sources:
        url = i.get('url')
        repo = i.get('name')

        try:
            report = missingReport(url, args.s3bucket, repo, s3Minio, args.graphendpoint)
            report = json.dumps(report)
            s3Minio.putReportFile(args.s3bucket, repo, "missing_report.json", report)
        except Exception as e:
            logging.error(e)

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
    parser.add_argument('--graphendpoint', dest = 'graphendpoint',
                        help = 'graph endpoint', default = "https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/")
    parser.add_argument('--s3', dest = 's3server',
                        help = 's3 server address (localhost:9000)', default = 'localhost:9000')
    parser.add_argument('--s3bucket', dest = 's3bucket',
                        help = 's3 server address (localhost:9000)', default = 'gleaner')
    parser.add_argument('--cfgfile', dest = 'cfgfile',
                        help = 'gleaner config file', default = 'gleaner')

    args = parser.parse_args()
    exitcode = writeMissingReport(args)

if __name__ == '__main__':
    start()