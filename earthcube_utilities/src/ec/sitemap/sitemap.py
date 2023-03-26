import logging
from io import StringIO

import advertools as adv
from pandarallel import pandarallel


import requests, sys, os
import yaml
from tqdm import tqdm

def _urlExists(sitemapurl):
    try:
        r = requests.get(sitemapurl)
        if r.status_code == 404:
            logging.error("Sitemap URL is 404")
            return False
    except:
        return False
    return True
def _urlResponse(item_loc: str):
    """return response code, content type, """
    try:
        r = requests.head(item_loc)
        if r.status_code != 200:
            return [r.status_code, None]
        else:
            content_type = r.headers.get("Content-Type")
            return [r.status_code, content_type]
    except:
        return [400, None]
class Sitemap():
    sitemapurl = None
    sitemap_df = None
    errors=[]
    def __init__(self, sitemapurl, repoName="", no_progress_bar=False):
        self.sitemapurl = sitemapurl
        self.no_progress_bar = no_progress_bar
        if _urlExists(sitemapurl):
            self.sitemap_df = adv.sitemap_to_df(sitemapurl)
        else:
            self.errors.append(f"sitemap url invalid: {sitemapurl}")

    def validUrl(self):
        return _urlExists(self.sitemapurl)
    def uniqueItems(self):
         return self.sitemap_df.sitemap.unique()

    def uniqueUrls(self):
         return self.sitemap_df["loc"].unique()

    def check_urls(self):
        # add valid to dataframe
        df = self.sitemap_df

        # df[["url_response","content_type"]]= df.progress_apply(lambda row:
        #                        _urlResponse(row.get('loc')),
        #                        axis=1)
        df["url_response"]=None
        df["content_type"]=None

        pandarallel.initialize(progress_bar=self.no_progress_bar)
        df["url_response"],df["content_type"]=  zip(*df.parallel_apply(lambda row:
                           _urlResponse(row.get('loc')),
                           axis=1))

    def get_url_report(self):
        out= StringIO()
        self.sitemap_df.to_csv(out, index=False,
                columns=['loc','lastmod','url_response', 'content_type']
              #                 columns=['loc','lastmod',"url_response/content_type"]
                               )
        return out.getvalue()

class SitemapForSource(Sitemap):
    source= None

    def __init__(self, source):
        self.self.source = source
        if source["sourcetype"] !=  "sitemap":
            return Exception("source is Not a sitemap")
        super.__init__(source.url, reponame= source.name)

    def get_status(self):
        s = self.source
        return  { 'name': s.name , 'code': _urlResponse( s.get("url") ), 'description': "res", 'url': s.get("description"), 'type': s.get("sourcetype")}