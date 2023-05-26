import functools
import os
from typing import Tuple

import click
import logging
import json
import sys

from pydash.collections import find
from pydash import is_empty
import pandas as pd
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
    s3Minio = s3.MinioDatastore(s3server, None)

    if path:
        count = s3Minio.countPath(s3bucket, path)
        res = f"Count for path {path}: {count}"
        print(res)
    else:
        message = "Please provide path to source. E.g. --path milled/iris"
        log.fatal(message)
        raise Exception(message)

@cli.command()
@click.option('--path', help='Path to source')
@click.option('--source', help='One repositories')
@common_params
def urls(cfgfile, s3server, s3bucket, graphendpoint, upload, output, debug, source, path):
    ctx = EcConfig(cfgfile, s3server, s3bucket, graphendpoint, upload, output, debug)
    s3Minio = s3.MinioDatastore(s3server, None)
    res = s3Minio.listSummonedUrls(s3bucket, source)
    return res

@cli.command()
@click.option('--source', help='One repositories')
@common_params
def download(cfgfile, s3server, s3bucket, graphendpoint, upload, output, debug, source):
    ctx = EcConfig(cfgfile, s3server, s3bucket, graphendpoint, upload, output, debug)
    s3Minio = s3.MinioDatastore(s3server, None)
    urns = s3Minio.listSummonedSha(s3bucket, source)
    mypath = source
    if not os.path.isdir(mypath):
        os.makedirs(mypath)
    for urn in urns:
        outFileName = f"{mypath}/{urn}.jsonld"
        print(outFileName)
        outFile = open(outFileName, "wb")
        o = s3Minio.getJsonLD(s3bucket, source, urn)
        outFile.write(o)
        outFile.close()
    return

if __name__ == '__main__':
    cli()
    sys.exit(0)