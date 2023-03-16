import unittest

from s3.s3 import MinioDatastore

class S3TestCase(unittest.TestCase):
    def test_get_latest_releases(self):
        bucket="gleaner-wf"
        endpoint = "oss.geocodes-dev.earthcube.org"
        s3client = MinioDatastore(endpoint, None)
        urls = s3client.getRelaseUrls(bucket)


if __name__ == '__main__':
    unittest.main()
