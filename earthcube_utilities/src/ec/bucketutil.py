import functools
import os
import click
import logging
import json
import sys

from pydash.collections import find
from pydash import is_empty
import pandas as pd
from ec.gleanerio.gleaner import getSitemapSourcesFromGleaner, getGleaner
from ec.objects.utils import parts_from_urn
from ec.datastore import s3
from ec.logger import config_app
import datetime
import pytz

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
            self.glnr = glnr
        else:
            self.s3server = s3server
            self.bucket = s3bucket

        self.graphendpoint = graphendpoint
        self.output= output
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
    @click.option('--debug/--no-debug', default=False,
                  envvar='REPO_DEBUG')
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@click.group()
@common_params
def cli( cfgfile,s3server, s3bucket, graphendpoint, upload, output, debug):
   obj = EcConfig(cfgfile,s3server, s3bucket, graphendpoint, upload, output, debug)

@cli.command()
@click.option('--path', help='Path to source',)
@click.option('--source', help='One or more repositories (--source a --source b)', multiple=True)
@common_params
def count(cfgfile, s3server, s3bucket, graphendpoint, upload, output, debug, source, path):
    ctx = EcConfig(cfgfile,s3server, s3bucket, graphendpoint, upload, output, debug)
    s3Minio = s3.MinioDatastore(ctx.s3server, None)

    if path:
        count = s3Minio.countPath(ctx.bucket, path)
        res = f"Count for path {path}: {count}"
        sys.stdout.write(json.dumps(res))
    elif source:
        counts = list()
        for s in source:
            path = f"/{s3Minio.paths.get('summon')}/{s.get('name')}"
            count = s3Minio.countPath(ctx.bucket, path)
            res = f"Count for source {s.get('name')}: {count}"
            counts.append(res)
        sys.stdout.write( json.dumps(counts) )
    elif cfgfile:
        sources = getSitemapSourcesFromGleaner(cfgfile)
        counts = list()
        for s in sources:
            path = f"/{s3Minio.paths.get('summon')}/{s.get('name')}"
            count = s3Minio.countPath(ctx.bucket, path)
            res = f"Count for source {s.get('name')}: {count}"
            counts.append(res)
        sys.stdout.write( json.dumps(counts) )
    else:
        message = "Please provide path to source. E.g. --path milled/iris or a config and optional sources"
        log.fatal(message)
        raise Exception(message)
    return

@cli.command()
# @click.option('--path', help='Path to source')
# need to add a method to the s3 to handle the path approach... or not needed
@click.option('--source', help='A repository')
@common_params
def urls(cfgfile, s3server, s3bucket, graphendpoint, upload, output, debug, source):
    """Retreive the URL harvested for a give bucket. T
    There may be duplicate URL's, if an HTML has more than one JSONLD"""
    ctx = EcConfig(cfgfile, s3server, s3bucket, graphendpoint, upload, output, debug)
    s3Minio = s3.MinioDatastore(ctx.s3server, None)
    if source:
        res = s3Minio.listSummonedUrls(ctx.bucket, source)
        sys.stdout.write( json.dumps(res))
    else:
        log.fatal("we need a source and a s3 endpoints")


@cli.command()
@click.option('--urn', help='One or more urns (--urn urna --urn urnb)', multiple=True)
@common_params
def download(cfgfile, s3server, s3bucket, graphendpoint, upload, output, debug, urn):
    """For a given URN(s), download the files and the Metadata"""
    ctx = EcConfig(cfgfile, s3server, s3bucket, graphendpoint, upload, output, debug)
    s3Minio = s3.MinioDatastore(ctx.s3server, None)

    for sha in urn:
        # need to parse the source and actual sha/id out of the urn
        # and then do the path and creat path
        parts = parts_from_urn(sha)
        mypath = parts.get('source')
        id = parts.get('id')
        if not os.path.isdir(mypath):
            os.makedirs(mypath)
        outFileName = f"{mypath}/{id}.jsonld"
        log.info(outFileName)
        outFile = open(outFileName, "wb")
        o = s3Minio.getJsonLD(ctx.bucket, mypath, id)
        outFile.write(o)
        outFile.close()
        outFileName = f"{mypath}/{id}.jsonld.txt"
        log.info(outFileName)
        outFile = open(outFileName, "wb")
        o = s3Minio.getJsonLDMetadata(ctx.bucket, mypath, id)
        outFile.write( bytes(json.dumps(o), 'utf8'))
        outFile.close()
    return

@cli.command()
@click.option('--url', help='the X-Amz-Meta-Url in metadata')
@common_params
def sourceurl(cfgfile, s3server, s3bucket, graphendpoint, upload, output, debug, url):
    """ for a given url, find the sha of the file"""
    ctx = EcConfig(cfgfile, s3server, s3bucket, graphendpoint, upload, output, debug)
    s3Minio = s3.MinioDatastore(ctx.s3server, None)
    sources = getSitemapSourcesFromGleaner(cfgfile)
    sources = list(filter(lambda source: source.get('active'), sources))
    sources = list(map(lambda r: r.get('name'), sources))
    o_list = list()
    for repo in sources:
        jsonlds = s3Minio.listJsonld(s3bucket, repo, include_user_meta=True)
        objs = map(lambda f: s3Minio.s3client.stat_object(f.bucket_name, f.object_name), jsonlds)
        o_list.extend(list(filter(lambda f: f.metadata.get('X-Amz-Meta-Url') == url, objs)))
    sys.stdout.write( json.dumps( o_list))


@cli.command()
@click.option('--url', help='the X-Amz-Meta-Url in metadata')
@click.option('--milled', help='include milled', default=False)
@click.option('--summon', help='include summon', default=True)
@common_params
def duplicates(cfgfile, s3server, s3bucket, graphendpoint, upload, output, debug, summon, milled, url):
    """ Find Possible Duplicates based on the URL that was used to summon JSONLD.
    Note, the may be ok, if a given URL has more than one JSONLD in the HTML.
    """
    # this is more complex. It is about finding duplicate url's,
    # returning the counts, if there is more than one, and the full urn's for thr duplicated
    # probably best done in pandas?
    ctx = EcConfig(cfgfile, s3server, s3bucket, graphendpoint, upload, output, debug)
    s3Minio = s3.MinioDatastore(ctx.s3server, None)
    paths = list()
    if summon:
        paths = list(s3Minio.listPath(s3bucket, 'summoned/', recursive=False))
    if milled:
        paths.extend(list(s3Minio.listPath(s3bucket, 'milled/', recursive=False)))
    for path in paths:
        jsonlds = s3Minio.listPath(s3bucket, path.object_name)
        objs = map(lambda f: s3Minio.s3client.stat_object(f.bucket_name, f.object_name), jsonlds)
        o_list = list(map(lambda f: {'Url': f.metadata.get('X-Amz-Meta-Url'),
                                     'Date': f.last_modified,
                                     'Name': f.object_name
                                     }, objs))
        df = pd.DataFrame(o_list)
        try:
            res = df.groupby(['Url'], group_keys=True, dropna=False) \
            .agg({'Name': 'count', 'Name': lambda x: x.iloc[0:5].tolist(), 'Date': lambda x: x.iloc[0:5].tolist()},
                 ).reset_index()
            print(res)
        except Exception as e:
            logging.info('Missing keys: ', e)
    return 0

@cli.command()
@common_params
def stats(cfgfile, s3server, s3bucket, graphendpoint, upload, output, debug):
    ctx = EcConfig(cfgfile, s3server, s3bucket, graphendpoint, upload, output, debug)
    s3Minio = s3.MinioDatastore(ctx.s3server, None)
    sources = getSitemapSourcesFromGleaner(cfgfile)
    sources = list(filter(lambda source: source.get('active'), sources))
    sources = list(map(lambda r: r.get('name'), sources))

    pathMilled = f"/{s3Minio.paths.get('milled')}/"
    pathSummon = f"/{s3Minio.paths.get('summon')}/"
    stats = {'milled': {'total': 0, 'repo': {}}, 'summon': {'total': 0, 'repo': {}}}
    for repo in sources:
        countMilled = s3Minio.countPath(s3bucket, pathMilled + repo)
        countSummon = s3Minio.countPath(s3bucket, pathSummon + repo)
        if countMilled > 0:
            stats['milled']['repo'] |= {repo: countMilled}
            stats['milled']['total'] += countMilled
        if countSummon > 0:
            stats['summon']['repo'] |= {repo: countSummon}
            stats['summon']['total'] += countSummon
    print(json.dumps(stats, sort_keys = True, indent = 4))

@cli.command()
@click.option('--url', help='the X-Amz-Meta-Url in metadata')
@common_params
def cull(cfgfile, s3server, s3bucket, graphendpoint, upload, output, debug, url):
    """ for a given url, find the sha of the file"""
    ctx = EcConfig(cfgfile, s3server, s3bucket, graphendpoint, upload, output, debug)
    s3Minio = s3.MinioDatastore(ctx.s3server, None)
    utc = pytz.UTC
    sources = getSitemapSourcesFromGleaner(cfgfile)
    sources = list(filter(lambda source: source.get('active'), sources))
    sources = list(map(lambda r: r.get('name'), sources))

    for repo in sources:
        jsonlds = s3Minio.listJsonld(s3bucket, repo, include_user_meta=True)
        objs = map(lambda f: s3Minio.s3client.stat_object(f.bucket_name, f.object_name), jsonlds)
        o_list = list(map(lambda f: {'Source': repo,
                                     'Url': f.metadata.get('X-Amz-Meta-Url'),
                                     'Date': f.last_modified,
                                     'Name': f.object_name
                                     }, objs))
        df = pd.DataFrame(o_list)
        try:
            res = df[df.duplicated(subset=['Url'])]
            res = res[res['Date'] < utc.localize(datetime.datetime.now() - datetime.timedelta(days=7))]
            removeObjectList = res['Name'].values.tolist()
            for r in removeObjectList:
                 s3Minio.removeObject(s3bucket, r)
        except Exception as e:
            logging.info('Missing keys: ', e)

if __name__ == '__main__':
    cli()
    sys.exit(0)
