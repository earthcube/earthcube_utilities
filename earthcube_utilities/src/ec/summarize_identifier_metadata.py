import argparse
import logging
import sys

from pydash.collections import find
from pydash import is_empty
import pandas as pd

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

    if args.json:
        filename = args.output.rsplit(".", 1)[0] + '.json'
    else:
        filename = args.output.rsplit(".", 1)[0] + '.csv'
    if args.output:
        output_file = open(filename, 'w')

    logging.info(f" s3server: {s3server} bucket:{bucket}")

    s3Minio = s3.MinioDatastore(s3server, None)
    #sources = getSitemapSourcesFromGleaner(args.cfgfile)
    # sources = list(filter(lambda source: source.get('active'), sources))
    # sources = list(map(lambda r: r.get('name'), sources))
    # repos = args.source
    if args.source:
        sources = args.source
    else:
        sources = getSitemapSourcesFromGleaner(args.cfgfile)
        sources = list(filter(lambda source: source.get('active'), sources))
        sources = list(map(lambda r: r.get('name'), sources))
    for repo in sources:
        # if repos is not None and len(repos) >0:
        #     if not find (repos , lambda x: x == repo ):
        #         continue
        jsonlds = s3Minio.listJsonld(bucket, repo, include_user_meta=True)
        objs = map(lambda f: s3Minio.s3client.stat_object(f.bucket_name, f.object_name), jsonlds)
        o_list = list(map(lambda f: {'Source': repo,
                                     'Identifiertype': f.metadata.get('X-Amz-Meta-Identifiertype'),
                                     'Matchedpath': f.metadata.get('X-Amz-Meta-Matchedpath'),
                                     'Uniqueid': f.metadata.get('X-Amz-Meta-Uniqueid'),
                                     'Example': f.metadata.get('X-Amz-Meta-Uniqueid')
                                     }, objs))

        df = pd.DataFrame(o_list)
        try:
            identifier_stats = df.groupby(['Source', 'Identifiertype', 'Matchedpath'], group_keys=True, dropna=False)\
                .agg({'Uniqueid': 'count', 'Example':lambda x: x.iloc[0:5].tolist()}).reset_index()
            if args.json:
                o = identifier_stats.to_json(orient='records', indent=2)
            else:
                o = identifier_stats.to_csv(index=False)

            if args.output:
                logging.info(f" report for {repo} appended to file")
                output_file.write(o)
            if not args.no_upload:
                s3Minio.putReportFile(bucket, repo, filename, o)

        except Exception as e:
            logging.info('Missing keys: ', e)
    return 0

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
                        help='gleaner config file')
    # no default for s3 parameters here. read from gleaner. if provided, these override the gleaner config
    parser.add_argument('--s3', dest='s3server',
                        help='s3 server address ')
    parser.add_argument('--s3bucket', dest='s3bucket',
                        help='s3 bucket ')
    parser.add_argument('--no_upload', dest='no_upload', action='store_true', default=False,
                        help='do not upload to s3 bucket ')
    parser.add_argument('--output', default='identifier_metadata_summary.csv',
                        dest='output', help='dump to file')
    parser.add_argument('--json', dest='json', action='store_false', default=True,
                        help='output json format')
    parser.add_argument('--source', action='append', help="one or more repositories (--source a --source b)")

    args = parser.parse_args()
    exitcode = summarizeIdentifierMetadata(args)
    sys.exit(exitcode)

if __name__ == '__main__':
    start()
