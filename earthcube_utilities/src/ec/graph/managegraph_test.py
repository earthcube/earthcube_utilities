import unittest

import manageGraph


class BrazgraphTestCase(unittest.TestCase):
    def test_createAndDelete(self):
        bg =  manageGraph.ManageBlazegraph("https://graph.geodex.org/blazegraph", "test")
        create = bg.createNamespace()
        self.assertEqual(True, create)  # add assertion here
        destroy = bg.deleteNamespace()
        self.assertEqual(True, destroy)


if __name__ == '__main__':
    unittest.main()
