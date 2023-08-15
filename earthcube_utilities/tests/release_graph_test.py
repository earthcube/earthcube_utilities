import unittest
from ec.graph.release_graph import ReleaseGraph
from approvaltests import verify, verify_as_json

from ec.summarize import summaryDF2ttl

s3server = "oss.geocodes-aws-dev.earthcube.org"
s3bucket = "test"

class ReelaseTestCase(unittest.TestCase):
    def test_read_release(self):
        rg = ReleaseGraph()
        rg.read_release(s3server, s3bucket, "geocodes_demo_data")

        self.assertEqual(len(rg.dataset), 1201)  # add assertion here

    def test_summarize(self, source='iris'):
        rg = ReleaseGraph()
       # rg.read_release(s3server, s3bucket, "geocodes_demo_data")
        rg.load_release( "./resources/releases/summonediris_https_fixed_release.nq")
        self.assertEqual( 465, len(rg.dataset))
        df = rg.summarize()
        self.assertEqual(28, len(df))
        results,g = summaryDF2ttl(df,source)
        nt = g.serialize(format='longturtle')
        verify(nt)

if __name__ == '__main__':
    unittest.main()
