import unittest

from datastore.s3 import MinioDatastore
from pydash.collections import find

class S3TestCase(unittest.TestCase):
    def test_get_latest_releases(self):
        bucket="gleaner-wf"
        endpoint = "oss.geocodes-dev.earthcube.org"
        s3client = MinioDatastore(endpoint, None)
        paths = s3client.getRelasePaths(bucket)
        self.assertIsNone(paths)

    def test_get_release(self):
        bucket = "gleaner-wf"
        endpoint = "oss.geocodes-dev.earthcube.org"
        repo = 'opentopgraphy'
        s3client = MinioDatastore(endpoint, None)
        paths = s3client.getRelasePaths(bucket)
        path = find(paths, lambda p: repo in p)
        file = s3client.getLatestRelaseFile(bucket, repo)
        self.assertIsNone(file)
    def test_get_jsonld(self):
        bucket = "gleaner-wf"
        endpoint = "oss.geocodes-dev.earthcube.org"
        repo = 'opentopography'
        urn = '001f05192c5328e54b25ab23779e13c95b995cd1'
        s3client = MinioDatastore(endpoint, None)

        list = s3client.getJsonLD(bucket, repo, urn)
        self.assertIsNone(list)
    def test_list_jsonld(self):
        bucket = "gleaner-wf"
        endpoint = "oss.geocodes-dev.earthcube.org"
        repo = 'opentopography'

        s3client = MinioDatastore(endpoint, None)

        alist = list( s3client.listJsonld(bucket, repo) )
        self.assertIsNotNone(alist)
    def test_listSummonedUrls(self):
        bucket = "gleaner-wf"
        endpoint = "oss.geocodes-dev.earthcube.org"
        repo = 'opentopography'
        s3client = MinioDatastore(endpoint, None)

        list = s3client.listSummonedUrls(bucket, repo)
        self.assertIsNone(list)

if __name__ == '__main__':
    unittest.main()
