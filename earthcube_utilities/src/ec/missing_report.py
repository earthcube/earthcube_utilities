#!  python3
import click
import logging
import json
import sys

from pydash.collections import find
from pydash import is_empty
from ec.gleanerio.gleaner import getSitemapSourcesFromGleaner, getGleaner
from ec.reporting.report import missingReport
from ec.datastore import s3

@click.command()
@click.option('--cfgfile', help='gleaner config file', type=click.Path(exists=True))
@click.option('--graphendpoint', help='graph endpoint'
              )
# no default for s3 parameters here. read from gleaner. if provided, these override the gleaner config
@click.option('--s3server', help='s3 server address')
@click.option('--s3bucket', help='s3 bucket')
@click.option('--no_upload', help='do not upload to s3 bucket',is_flag=True, default=False)
@click.option('--output', help='dump to file', type=click.File('wb'))
@click.option('--source', help='gone or more repositories (--source a --source b)', multiple=True)
@click.option('--milled', help='include milled', is_flag=True,default=False)
@click.option('--summon', help='check summon only',is_flag=True, default=False)

def writeMissingReport(cfgfile, graphendpoint, s3server, s3bucket, no_upload, output, source, milled, summon):
    if cfgfile:
        s3endpoint, bucket, glnr = getGleaner(cfgfile)
        minio = glnr.get("minio")
        # passed paramters override the config parameters
        s3server = s3server if s3server else s3endpoint
        bucket = s3bucket if s3bucket else bucket
    else:
        s3server = s3server
        bucket = s3bucket
    graphendpoint = graphendpoint  # not in gleaner file, at present
    if is_empty(s3server) or is_empty(bucket):
        logging.fatal(f" must provide a gleaner config or (s3endpoint and s3bucket)]")
        return 1
    if is_empty(graphendpoint) and not summon:
        logging.fatal(f" must provide graphendpoint if you are checking milled")
        return 1
    logging.info(f" s3server: {s3server} bucket:{bucket} graph:{graphendpoint}")
    s3Minio = s3.MinioDatastore(s3server, None)
    sources = getSitemapSourcesFromGleaner(cfgfile)
    sources = list(filter(lambda source: source.get('active'), sources))
    sources_to_run = source  # optional if null, run all

    for i in sources:
        source_url = i.get('url')
        source_name = i.get('name')
        if sources_to_run is not None and len(sources_to_run) >0:
            if not find (sources_to_run, lambda x: x == source_name ):
                continue
        try:
            report = missingReport(source_url, bucket, source_name, s3Minio, graphendpoint, milled=milled, summon=summon)
            report = json.dumps(report,  indent=2)
            if output:  # just append the json files to one filem, for now.
                logging.info(f" report for {source_name} appended to file")
                output.write(report)
            if not no_upload:
                s3Minio.putReportFile(bucket, source_name, "missing_report.json", report)
        except Exception as e:
            logging.error(f"could not write missing report for {source_name} to s3server:{s3server}:{bucket} error:{e}",
                          source_name, s3server, bucket, e)
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
    exitcode = writeMissingReport()
    sys.exit(exitcode)


if __name__ == '__main__':
    start()

