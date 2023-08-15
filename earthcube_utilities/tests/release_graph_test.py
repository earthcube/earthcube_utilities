import unittest
from ec.graph.release_graph import ReleaseGraph

s3server = "oss.geocodes-dev.earthcube.org"
s3bucket = "gleaner"

class ReelaseTestCase(unittest.TestCase):
    def test_read_release(self):
        rg = ReleaseGraph()
        rg.read_release(s3server, s3bucket, "geocodes_demo_data")

        self.assertEqual(len(rg.dataset), 1604)  # add assertion here

    def test_summarize(self):
        rg = ReleaseGraph()
       # rg.read_release(s3server, s3bucket, "geocodes_demo_data")
        rg.load_release( "./resources/releases/summonediris_https_fixed_release.nq")
        df = rg.summarize()
        self.assertEqual(len(df), 1604)

if __name__ == '__main__':
    unittest.main()
