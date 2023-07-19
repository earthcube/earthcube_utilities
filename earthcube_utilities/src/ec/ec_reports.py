import functools
import click
import logging
import json
import sys
from pydash.collections import find
from pydash import is_empty
from ec.gleanerio.gleaner import getSitemapSourcesFromGleaner, getGleaner
from ec.reporting.report import generateGraphReportsRepo, reportTypes, missingReport, generateIdentifierRepo
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
        self.graphendpoint = graphendpoint
        self.output = output
        self.upload = upload
        self.debug = debug

    # lets put checks as methods in here.
    # that way some checks if we can connect can be done in one place
    def hasS3(self) -> bool:
         if   ( is_empty(self.s3server) or is_empty(self.bucket) ):
             log.fatal(f" must provide a gleaner config or (s3endpoint and s3bucket)]")
             raise Exception("must provide a gleaner config or (s3endpoint and s3bucket)]")
         return True
    def hasS3Upload(self) -> bool:
         if  not self.upload and ( is_empty(self.s3server) or is_empty(self.bucket) ):
             log.fatal(f" must provide a gleaner config or (s3endpoint and s3bucket)]")
             raise Exception("must provide a gleaner config or (s3endpoint and s3bucket)]")
         return True
    def hasGraphendpoint(self, option:bool=False, message="must provide graphendpoint") -> bool:
         """ if option is not true, so if summon only, then empty is graphendpoint is ok
            """
         if   option or is_empty(self.graphendpoint) :
             log.fatal(message)
             raise Exception(message)
         return True

def common_params(func):
    @click.option('--cfgfile', help='gleaner config file', type=click.Path(exists=True))
    @click.option('--s3server', help='s3 server address')
    @click.option('--s3bucket', help='s3 bucket')
    @click.option('--graphendpoint', help='graph endpoint')
    @click.option('--upload/--no-upload', help='upload to s3 bucket', default=True)
    @click.option('--output', help='dump to file', type=click.File('wb'))
    @click.option('--debug/--no-debug', default=False, envvar='REPO_DEBUG')
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@click.group()
@common_params
def cli( cfgfile,s3server, s3bucket, graphendpoint, upload, output, debug):
   obj = EcConfig(cfgfile,s3server, s3bucket, graphendpoint, upload, output, debug)

@cli.command()

@click.option('--source', help='One or more repositories (--source a --source b)', multiple=True)
@click.option('--milled/--no-milled', help='include milled', default=False)
@click.option('--summononly', help='check summon only', is_flag=True, default=False)
@common_params
def missing_report(cfgfile,s3server, s3bucket, graphendpoint, upload, output, debug, source, milled, summononly):
    # name missing-report
    ctx = EcConfig(cfgfile, s3server, s3bucket, graphendpoint, upload, output, debug)
    output = ctx.output
    upload = ctx.upload
    bucket = ctx.bucket
    s3server = ctx.s3server
    graphendpoint = ctx.graphendpoint  # not in gleaner file, at presen
    ctx.hasS3()
    ctx.hasGraphendpoint(option=summononly, message="must provide graphendpoint if you are checking the graph" )

    log.info(f"s3server: {s3server} bucket:{bucket} graph:{graphendpoint}")
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
            report = missingReport(source_url, bucket, source_name, s3Minio, graphendpoint, milled=milled, summon=summononly)
            report = json.dumps(report,  indent=2)
            if output:  # just append the json files to one filem, for now.
                log.info(f"report for {source_name} appended to file")
                output.write(bytes(report, 'utf-8'))
            if upload:
                s3Minio.putReportFile(bucket, source_name, "missing_report.json", report)
        except Exception as e:
            log.error(f"could not write missing report for {source_name} to s3server:{s3server}:{bucket} error:{e}",
                          source_name, s3server, bucket, e)
    return

@cli.command()
@click.option('--source', help='One or more repositories (--source a --source b)', multiple=True)
@click.option('--detailed', help='run the detailed version of the reports',is_flag=True, default=False)
@common_params
def graph_stats(cfgfile,s3server, s3bucket, graphendpoint, upload, output, debug, source, detailed):
    ctx = EcConfig(cfgfile, s3server, s3bucket, graphendpoint, upload, output, debug)
    output = ctx.output
    no_upload = ctx.upload
    graphendpoint = ctx.graphendpoint
    s3server = ctx.s3server
    s3bucket = ctx.bucket

    ctx.hasS3Upload()
    ctx.hasGraphendpoint(message=" must provide graphendpoint")
    if upload:
        s3Minio = s3.MinioDatastore(s3server, None)
    """query an endpoint, store results as a json file in an s3 store"""
    log.info(f"Querying {graphendpoint} for graph statisitcs  ")
### more work needed before detailed works
    if "all" in source:
        if detailed:
            report_json = generateGraphReportsRepo("all", graphendpoint, reportList=reportTypes["all_detailed"])
        else:
            report_json = generateGraphReportsRepo("all", graphendpoint,reportList=reportTypes["all"])
            if output:  # just append the json files to one filem, for now.
                log.info(f" report for ALL appended to file")
                output.write(report_json)
            if upload:
                bucketname, objectname = s3Minio.putReportFile(s3bucket, "all", "graph_report.json", report_json)
    else:
        for s in source:
            if detailed:
                report_json = generateGraphReportsRepo(s, graphendpoint, reportList=reportTypes["repo_detailed"])
            else:
                report_json = generateGraphReportsRepo(s, graphendpoint, reportList=reportTypes["repo"])
            if output:  # just append the json files to one filem, for now.
                log.info(f" report for {s} appended to file")
                output.write(bytes(report_json, 'utf-8'))
            if upload:
                bucketname, objectname = s3Minio.putReportFile(s3bucket, s, "graph_report.json", report_json)
    return

@cli.command()
@click.option('--source', help='One or more repositories (--source a --source b)', multiple=True)
@click.option('--json', help='output json format', is_flag=True, default=True)
@common_params
def identifier_stats(cfgfile,s3server, s3bucket, graphendpoint, upload, output, debug, source, json):
    filename = 'identifier_metadata_summary'
    if cfgfile:
        s3endpoint,  bucket, glnr=getGleaner(cfgfile)
        minio = glnr.get("minio")
        # passed paramters override the config parameters
        s3server = s3server if s3server else s3endpoint
        bucket = s3bucket if s3bucket else bucket
    else:
        s3server = s3server
        bucket = s3bucket

    if is_empty(s3server) or is_empty(bucket):
        logging.fatal(f" must provide a gleaner config or (s3endpoint and s3bucket)]")
        raise Exception(" must provide a gleaner config or (s3endpoint and s3bucket)]")

## output is file
    if json:
        filename = filename + '.json'
    else:
        filename = filename + '.csv'

    logging.info(f" s3server: {s3server} bucket:{bucket}")

    s3Minio = s3.MinioDatastore(s3server, None)
    if source:
        sources = source
    else:
        sources = getSitemapSourcesFromGleaner(cfgfile)
        sources = list(filter(lambda source: source.get('active'), sources))
        sources = list(map(lambda r: r.get('name'), sources))
    for repo in sources:
        try:
            identifier_stats = generateIdentifierRepo(repo, bucket, s3Minio)
            if json:
                o = identifier_stats.to_json(orient='records', indent=2)
            else:
                o = identifier_stats.to_csv(index=False)

            if output:
                logging.info(f" report for {repo} appended to file")
                output.write(bytes(o, 'utf-8'))
            if upload:
                s3Minio.putReportFile(bucket, repo, filename, o)

        except Exception as e:
            logging.info('Missing keys: ', e)
    return

# @cli.command()
# # @click.option('--cfgfile', help='gleaner config file', default='gleaner', type=click.Path(exists=True))
# # no default for s3 parameters here. read from gleaner. if provided, these override the gleaner config
# # @click.option('--s3server', help='s3 server address')
# # @click.option('--s3bucket', help='s3 bucket')
# @click.option('--source', help='One or more repositories (--source a --source b)', multiple=True)
# @click.option('--json', help='output json format', is_flag=True, default=True)
# @click.option('--detailed', help='run the detailed version of the reports',is_flag=True, default=False)
# @click.option('--milled/--no-milled', help='include milled', default=False)
# @click.option('--summononly', help='check summon only',is_flag=True, default=False)
# # @click.pass_obj
# @common_params
# @click.pass_context
# def run_all (ctx, cfgfile,s3server, s3bucket, graphendpoint, upload, output, debug, source, json,detailed, milled, summononly ):
# # this probably needs to run to a try catch block where ratehr than method doing a sys.exit, they
# # toss an exception, so if one report fails, the others run.
#     try:
#         ctx.forward(missing_report)
#         # ctx.invoke( missing_report, cfgfile=cfgfile,s3server=s3server,
#         #             s3bucket=s3bucket,
#         #             graphendpoint=graphendpoint,
#         #             upload=upload, output=output,
#         #             debug=debug,
#         #             source=source,
#         #             milled=milled,
#         #             summononly=summononly
#         #             )
#     except Exception as e:
#         log.error("missing report failed ")
#     try:
#         identifier_stats(cfgfile, s3server, s3bucket, graphendpoint, upload, output, debug, source, json)
#     except Exception as e:
#         log.error("identifier stats failed")
#     try:
#
#         graph_stats(cfgfile, s3server, s3bucket, graphendpoint, upload, output, debug, source, detailed)
#     except Exception as e:
#         log.error("graph stats failed")

if __name__ == '__main__':
    cli()
    sys.exit(0)
