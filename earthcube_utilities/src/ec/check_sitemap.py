from io import StringIO

from ec.sitemap.sitemap import Sitemap
import argparse
from distutils.util import strtobool
def sitemap_checker(args):
    """Sitemap checker. Default option  checks if url is sitemap exist"""
    sitemap = Sitemap(args.sitemapurl, no_progress_bar=args.no_progress)
    if  not args.nocheck :
        sitemap.check_urls()

    return sitemap.get_url_report()

def start():
    """
        Run the sitemap_checker program.
        Sitemap checker. Default option  checks if url is sitemap exist.
        Arguments:
            args: Arguments passed from the command line.
        Returns:
            result of check as csv.

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("sitemapurl", help='sitemapurl')
    parser.add_argument("--output", type=argparse.FileType('w'), help='output file')
    parser.add_argument("--no-url-check",action='store_true', dest="nocheck" ,help='output file', default=False)
    parser.add_argument("--no-progress", action='store_false',   dest="no_progress" ,help='no progress bar', default=True)
    args = parser.parse_args()

    result = sitemap_checker(args)
    if args.output:
        args.output.write(result)
    else:
        print(result)
if __name__ == '__main__':

    result = start()

