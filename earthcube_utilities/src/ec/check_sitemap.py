from io import StringIO

from ec.sitemap.sitemap import Sitemap
import argparse

from ec.logger import config_app

log = config_app()

def sitemap_checker(args):
    log.debug(" Sitemap")
    sitemap = Sitemap(args.sitemapurl, no_progress_bar=args.no_progress)
    if  not args.nocheck :
        sitemap.check_urls()

    return sitemap.get_url_report()

def start():
    parser = argparse.ArgumentParser()
    parser.add_argument("sitemapurl", help='sitemapurl')
    parser.add_argument("--output", type=argparse.FileType('w'), help='output file')
    parser.add_argument("--no-url-check",action='store_true', dest="nocheck" ,help='output file', default=False)
    parser.add_argument("--no-progress", action='store_false',   dest="no_progress" ,help='no progress bad', default=True)
    args = parser.parse_args()

    result = sitemap_checker(args)
    if args.output:
        log.info(" Sitemap written to file"  )
        args.output.write(result)
    else:
        print(result)

if __name__ == '__main__':

    result = start()

