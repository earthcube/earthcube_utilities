import logging
from io import StringIO

import advertools as adv
import pandas
from numpy import ndarray
from pandarallel import pandarallel
from pandas import DataFrame

import requests, sys, os
import yaml
from pandas.core.arrays import ExtensionArray
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
    """ This holds information about a sitemap, and allows for testing of the
    URLS in the sitemap to see if they exist.
    If the sitemap URL does not exist, then it will return a Sitemap, with an
    len(errors) > 0.

    """
    sitemapurl = None
    _validSitemap = True
    sitemap_df = pandas.DataFrame()
    errors=[]
    _checkedUrls=False
    def __init__(self, sitemapurl, repoName="", no_progress_bar=False):
        self.sitemapurl = sitemapurl
        self.no_progress_bar = no_progress_bar
        if _urlExists(sitemapurl):
            self.sitemap_df = adv.sitemap_to_df(sitemapurl)
            self._validSitemap = True
        else:
            self.errors.append(f"sitemap url invalid: {sitemapurl}")
            # the other option is to return None.

    def validUrl(self) -> bool:
        """ does the provided sitemap URL exist."""
        return self._validSitemap

    def errors(self):
        return self.errors
    def uniqueItems(self):
        """list of unqiue sitemaps records"""
        return self.sitemap_df.sitemap.unique()

    def uniqueUrls(self) :
        """Returns a pandas series of the URLS'"""
        return self.sitemap_df["loc"].unique()

    def check_urls(self) -> DataFrame:
        """This will run head on the list of url's in the pandas dataframe.
        It will append columns ("url_response","content_type") to the sitemap_df
        """

        # add columns to the dataframe. clear out any previous values
        df = self.sitemap_df
        df["url_response"]=None
        df["content_type"]=None

        if not self._validSitemap:
            self._checkedUrls = True
            return df

        pandarallel.initialize(progress_bar=self.no_progress_bar)
        df["url_response"],df["content_type"]=  zip(*df.parallel_apply(lambda row:
                           _urlResponse(row.get('loc')),
                           axis=1))
        self._checkedUrls =True
        return df

    def get_url_report(self) -> str:
        """returns a csv of the 'loc','lastmod','url_response', 'content_type' """
        if not self._checkedUrls:
            self.check_urls()
        out= StringIO()
        self.sitemap_df.to_csv(out, index=False,
                columns=['loc','lastmod','url_response', 'content_type']
              #                 columns=['loc','lastmod',"url_response/content_type"]
                               )
        return out.getvalue()

class GleanerioSourceSitemap(Sitemap):
    """ For a provided GleanerIO source record, create a Sitemap object to utilize"""
    source= None

    def __init__(self, source):
        self.self.source = source
        if source["sourcetype"] !=  "sitemap":
            return Exception("source is Not a sitemap")
        super.__init__(source.url, reponame= source.name)

    def get_status(self):
        s = self.source
        return  { 'name': s.name , 'code': _urlResponse( s.get("url") ), 'description': "res", 'url': s.get("description"), 'type': s.get("sourcetype")}