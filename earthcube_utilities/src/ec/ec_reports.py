import functools
import os
from typing import Tuple

import click
import logging
import json
import sys

from pydash.collections import find
from pydash import is_empty
from ec.gleanerio.gleaner import getSitemapSourcesFromGleaner, getGleaner
from ec.reporting.report import missingReport
from ec.datastore import s3

from ec.reporting.report import  generateGraphReportsRepo, reportTypes
from ec.datastore import s3
from ec.logger import config_app

log = config_app()
class EcConfig(object):
    """ Parameters that might be common to commands"""
    def __init__(self, cfgfile=None, s3server=None, s3bucket=None, graphendpoint=None, upload=None, output=None,debug=False):
        if cfgfile:
            s3endpoint, bucket, glnr = getGleaner(cfgfile)
            minio = glnr.get("minio")
            # passed paramters override the config parameters
            self.s3server = s3server if s3server else s3endpoint
            self.bucket = s3bucket if s3bucket else bucket
        else:
            self.s3server = s3server
            self.bucket = s3bucket
        # this is not always... no upload should ignore here and catch in command
        ## sys.exit() is bad idead to have check in this class.
        # if  upload and ( is_empty(self.s3server) or is_empty(self.bucket) ):
        #     log.fatal(f" must provide a gleaner config or (s3endpoint and s3bucket)]")
        #     sys.exit(1)
 #       self.s3server=s3server
 #       self.s3bucket=s3bucket
        self.graphendpoint = graphendpoint
        self.ouput= output
        self.upload = upload

        self.debug = debug


    # lets put checks as methods in here.
    # that way some checks if we can connect can be done in one place
    def hasS3(self) -> bool:
         if   ( is_empty(self.s3server) or is_empty(self.bucket) ):
             log.fatal(f" must provide a gleaner config or (s3endpoint and s3bucket)]")
             sys.exit(1)
         return True
    def hasS3Upload(self) -> bool:
         if  not self.upload and ( is_empty(self.s3server) or is_empty(self.bucket) ):
             log.fatal(f" must provide a gleaner config or (s3endpoint and s3bucket)]")
             sys.exit(1)
         return True
    def hasGraphendpoint(self, option:bool=False, message="must provide graphendpoint") -> bool:
         """ if option is not true, so if summon only, then empty is graphendpoint is ok
            """
         if  not option or is_empty(self.graphendpoint) :
             log.fatal(message)
             sys.exit(1)
         return True

def common_params(func):
    @click.option('--cfgfile', help='gleaner config file', type=click.Path(exists=True))
    @click.option('--s3server', help='s3 server address')
    @click.option('--s3bucket', help='s3 bucket')
    @click.option('--graphendpoint', help='graph endpoint')
    @click.option('--upload/--no-upload', help='upload to s3 bucket', default=True)
    @click.option('--output', help='dump to file', type=click.File('wb'))
    @click.option('--debug/--no-debug', default=False,
                  envvar='REPO_DEBUG')
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@click.group()
#click.option('--cfgfile', help='gleaner config file', default='gleaner', type=click.Path(exists=True))

# @click.option('--cfgfile', help='gleaner config file', type=click.Path(exists=True))
# @click.option('--s3server', help='s3 server address')
# @click.option('--s3bucket', help='s3 bucket')
#
# @click.option('--graphendpoint', help='graph endpoint',
#               default='https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/')
#
# @click.option('--upload/--no-upload', help='upload to s3 bucket', default=True)
# @click.option('--output', help='dump to file', type=click.File('wb'))
#
# @click.option('--debug/--no-debug', default=False,
#               envvar='REPO_DEBUG')
@common_params
def cli( cfgfile,s3server, s3bucket, graphendpoint, upload, output, debug):
   obj = EcConfig(cfgfile,s3server, s3bucket, graphendpoint, upload, output, debug)
#    #pass
# def cli( ):
#     pass

@cli.command()
# @click.option('--cfgfile', help='gleaner config file', default='gleaner', type=click.Path(exists=True))
# no default for s3 parameters here. read from gleaner. if provided, these override the gleaner config
#@click.option('--s3server', help='s3 server address')
#@click.option('--s3bucket', help='s3 bucket')
@click.option('--source', help='One or more repositories (--source a --source b)', multiple=True)
@click.option('--milled/--no-milled', help='include milled', default=False)
@click.option('--summon/--no-sommon', help='check summon only', default=False)
#@click.pass_obj
@common_params
def missing_report(ctx,  cfgfile,s3server, s3bucket, graphendpoint, upload, output, debug, source, milled, summon):
    # name missing-report
    ctx.obj = EcConfig(cfgfile, s3server, s3bucket, graphendpoint, upload, output, debug)
    output = ctx.ouput
    no_upload = ctx.no_upload
    # if cfgfile:
    #     s3endpoint, bucket, glnr = getGleaner(cfgfile)
    #     minio = glnr.get("minio")
    #     # passed paramters override the config parameters
    #     s3server = s3server if s3server else s3endpoint
    #     bucket = s3bucket if s3bucket else bucket
    # else:
    #     s3server = s3server
    #     bucket = s3bucket
    bucket = ctx.bucket
    s3server= ctx.s3server
    graphendpoint = ctx.graphendpoint  # not in gleaner file, at presen

    ctx.hasS3()
    ctx.hasGraphendpoint(option=milled,
                                           message=" must provide graphendpoint if you are checking milled" )


    log.info(f" s3server: {s3server} bucket:{bucket} graph:{graphendpoint}")
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
                log.info(f" report for {source_name} appended to file")
                output.write(report)
            if not no_upload:
                s3Minio.putReportFile(bucket, source_name, "missing_report.json", report)
        except Exception as e:
            log.error(f"could not write missing report for {source_name} to s3server:{s3server}:{bucket} error:{e}",
                          source_name, s3server, bucket, e)
    sys.exit(0)
@cli.command()
# @click.option('--cfgfile', help='gleaner config file', default='gleaner', type=click.Path(exists=True))
# no default for s3 parameters here. read from gleaner. if provided, these override the gleaner config
#@click.option('--s3server', help='s3 server address')
#@click.option('--s3bucket', help='s3 bucket')
@click.option('--source', help='One or more repositories (--source a --source b)', multiple=True)
@click.option('--detailed', help='run the detailed version of the reports',is_flag=True, default=False)
#@click.pass_obj
@common_params
def graph_stats( cfgfile,s3server, s3bucket, graphendpoint, upload, output, debug, source, detailed):
    ctx = EcConfig(cfgfile, s3server, s3bucket, graphendpoint, upload, output, debug)
    output= ctx.ouput
    no_upload = ctx.upload
    graphendpoint = ctx.graphendpoint
    s3server = ctx.s3server
    s3bucket = ctx.bucket

    ctx.hasS3Upload()
    ctx.hasGraphendpoint(
                         message=" must provide graphendpoint")
    if  upload:
        s3Minio = s3.MinioDatastore(s3server, None)
    """query an endpoint, store results as a json file in an s3 store"""
    log.info(f"Querying {graphendpoint} for graph statisitcs  ")
### more work needed before detailed works
    if  "all" in source:
         # report_json = generateGraphReportsRepo("all",
         #      args.graphendpoint, reportTypes=reportTypes)

        if (detailed):
            report_json = generateGraphReportsRepo("all", graphendpoint, reportList=reportTypes["all_detailed"] )
        else:
            report_json = generateGraphReportsRepo("all",
                                                       graphendpoint,reportList=reportTypes["all"])
            if (output):  # just append the json files to one filem, for now.
                log.info(f" report for ALL appended to file")
                output.write(report_json)
            if  upload:
                bucketname, objectname = s3Minio.putReportFile(s3bucket, "all", "graph_report.json", report_json)
    else:
        # report_json = generateGraphReportsRepo(args.repo,
        #   args.graphendpoint,reportTypes=reportTypes)
        for s in source:
            if (detailed):
                report_json = generateGraphReportsRepo(s,graphendpoint,reportList=reportTypes["repo_detailed"] )
            else:
                report_json = generateGraphReportsRepo(s,
                                                          graphendpoint, reportList=reportTypes["repo"] )
            if (output):  # just append the json files to one filem, for now.
                log.info(f" report for {s} appended to file")
                output.write(report_json)
            if  upload:
                bucketname, objectname = s3Minio.putReportFile(s3bucket,s,"graph_report.json",report_json)
    sys.exit(0)

if __name__ == '__main__':
    cli()
