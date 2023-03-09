import unittest

import manageGraph as mg


class BrazgraphTestCase(unittest.TestCase):
    def test_createAndDelete(self):
        bg =  mg.ManageBlazegraph("https://graph.geodex.org/blazegraph", "test")
        create = bg.createNamespace()
        self.assertIn(create, ["Created","Exists"])  # add assertion here
        destroy = bg.deleteNamespace()
        self.assertEqual("Deleted", destroy)

# this could probably be best done with a setup, to read file, and create temp namespace and teardown,
    # but that can wait
    def test_insert_milled(self):
        # this is to test the files uploaded from milled
        bg =  mg.ManageBlazegraph("https://graph.geodex.org/blazegraph", "test")
        create = bg.createNamespace()
        try:
            #self.assertEqual(True, create)  # add assertion here
           # file = 'resources/test_triples/milled/0d8f2661071bdf56c91569ddfa0a5b8dea1a526d.rdf'
            file = '../../../resources/test_triples/milled/0d8f2661071bdf56c91569ddfa0a5b8dea1a526d.rdf'
            with open(file, 'rb+') as f:
                lines = f.read()
            inserted = bg.insert(lines,"text/plain")
            self.assertEqual(True, inserted)
        except:
            self.fail("failed")
        finally:
            destroy = bg.deleteNamespace()

    def test_insert_nq(self):
        # this is to test the files uploaded from milled
        bg =  mg.ManageBlazegraph("https://graph.geodex.org/blazegraph", "test")
        create = bg.createNamespace()
        try:
            #self.assertEqual(True, create)  # add assertion here
           # file = 'resources/test_triples/milled/0d8f2661071bdf56c91569ddfa0a5b8dea1a526d.rdf'
            file = '../../../resources/test_triples/nq/iris.txt'
            with open(file, 'rb+') as f:
                lines = f.read()
            inserted = bg.insert(lines)
            self.assertEqual(True, inserted)
        except:
            self.fail("failed")
        finally:
            destroy = bg.deleteNamespace()
        #self.assertEqual(True, destroy)

if __name__ == '__main__':
    unittest.main()
