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

if __name__ == '__main__':
    unittest.main()
