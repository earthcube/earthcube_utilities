from ec.sitemap.sitemap import Sitemap


import unittest

class S3TestCase(unittest.TestCase):
    def test_sitemap(self):
        sm = Sitemap("https://earthcube.github.io/GeoCODES-Metadata/metadata/Dataset/allgood/sitemap.xml")
        self.assertTrue(sm.validUrl())

    def test_sitemap_invalid(self):
        # with self.assertRaises(Exception) as context:
        #     Sitemap("https://dfdgsagfs")
        # self.assertTrue("Sitemap URL is 404" in str( context.exception))
        sm = Sitemap("https://dfdgsagfs")
        self.assertTrue(len(sm.errors) >0)

    def test_check_urls(self):
        sm = Sitemap("https://earthcube.github.io/GeoCODES-Metadata/metadata/Dataset/allgood/sitemap.xml")
        sm.check_urls()
        self.assertTrue("url_response" in sm.sitemap_df.columns)