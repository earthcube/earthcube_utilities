import argparse
import json
import logging
import sys
import pandas as pd
from pydash import is_empty

from ec.gleanerio.gleaner import getSitemapSourcesFromGleaner, getGleaner
from ec.datastore import s3

def summarizeIdentifierMetadata(args):
    if (args.cfgfile):
        s3endpoint,  bucket, glnr= getGleaner(args.cfgfile)
        minio = glnr.get("minio")
        # passed paramters override the config parameters
        s3server = args.s3server if args.s3server else s3endpoint
        bucket = args.s3bucket if args.s3bucket else bucket
    else:
        s3server = args.s3server
        bucket = args.s3bucket

    if is_empty(s3server) or is_empty(bucket):
        logging.fatal(f" must provide a gleaner config or (s3endpoint and s3bucket)]")
        return 1

    logging.info(f" s3server: {s3server} bucket:{bucket}")

    s3Minio = s3.MinioDatastore(s3server, None)
    sources = getSitemapSourcesFromGleaner(args.cfgfile)
    sources = list(filter(lambda source: source.get('active'), sources))
    for repo in sources:
        jsonlds = s3Minio.listJsonld(bucket, repo.get('name'), include_user_meta = True)
        objs = map(lambda f: s3Minio.s3client.stat_object(f.bucket_name, f.object_name), jsonlds)
        o_list = list(map(lambda f: {'Identifiertype': f.metadata['X-Amz-Meta-Identifiertype'],
                                     'Matchedpath': checkMatchpath(f),
                                     'Uniqueid': f.metadata['X-Amz-Meta-Uniqueid']
                                     }, objs))
        df = pd.DataFrame(o_list)

        try:
            o = df.groupby(['Identifiertype', 'Matchedpath']).count()
            if (args.output):
                logging.info(f" report for {repo.get('name')} appended to file")
                args.output.writelines('\n\nSource name: ' + repo.get('name') + o.to_string())
            if not args.no_upload:
                o = json.loads(o.to_json(orient = 'index'))
                o = json.dumps(o, indent = 2)
                s3Minio.putReportFile(bucket, repo.get('name'), "identifier_metadata_summary.json", o)
        except Exception as e:
            logging.info('Missing keys: ', e)
    return 0

def checkMatchpath(f):
    try:
        return f.metadata['X-Amz-Meta-Matchedpath']
    except:
        return 'Matchedpath does not exist'

def start():
    """
        Run the summarize_identifier_metadata program.
        Get a list of active repositories from the gleaner file.
        For each repository, summarize identifierTypes and matchedPath, then write these information to a file and upload it to s3.
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
    # no default for s3 parameters here. read from gleaner. if provided, these override the gleaner config
    parser.add_argument('--s3', dest='s3server',
                        help='s3 server address ')
    parser.add_argument('--s3bucket', dest='s3bucket',
                        help='s3 bucket ')
    parser.add_argument('--no_upload', dest='no_upload', action='store_true', default=False,
                        help='do not upload to s3 bucket ')
    parser.add_argument('--output', type=argparse.FileType('w'), default='identifier_metadata_summary.txt',
                        dest='output', help='dump to file')

    args = parser.parse_args()
    exitcode = summarizeIdentifierMetadata(args)
    sys.exit(exitcode)

if __name__ == '__main__':
    start()