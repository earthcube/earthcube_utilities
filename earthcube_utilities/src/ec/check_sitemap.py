from io import StringIO

from ec.sitemap.sitemap import Sitemap
import argparse

def sitemap_checker(args):
    sitemap = Sitemap(args.sitemapurl)
    if  not args.nocheck :
        sitemap.check_urls()

    return sitemap.get_url_report()

def start():
    parser = argparse.ArgumentParser()
    parser.add_argument("sitemapurl", help='sitemapurl')
    parser.add_argument("--output", type=argparse.FileType('rw'), help='output file')
    parser.add_argument("--no-url-check", dest="nocheck" ,help='output file', default=False)
    args = parser.parse_args()

    result = sitemap_checker(args)
    if args.output:
        args.output.write(result)
    else:
        print(result)
if __name__ == '__main__':

    result = start()

