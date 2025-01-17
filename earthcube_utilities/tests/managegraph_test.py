import unittest

from os import getenv
import ec.graph.manageGraph as mg



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
            file = '../resources/test_triples/milled/0d8f2661071bdf56c91569ddfa0a5b8dea1a526d.rdf'
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
            file = '../resources/test_triples/nq/iris.txt'
            with open(file, 'rb+') as f:
                lines = f.read()
            inserted = bg.insert(lines)
            self.assertEqual(True, inserted)
        except:
            self.fail("failed")
        finally:
            destroy = bg.deleteNamespace()
        #self.assertEqual(True, destroy)

class GraphDbTestCase(unittest.TestCase):
    def test_createAndDelete(self):
        password = getenv("GRAPHPASSWORD")
        if password is None:
            raise Exception("GRAPHPASSWORD missing")
        user = getenv("GRAPHUSER", "admin")
        if user is None:
            raise Exception("GRAPHUSER missing")
        bg = mg.ManageGraphdb("http://132.249.238.155/", "test", user,password )
        create = bg.createNamespace()
        self.assertIn(create, ["Created", "Exists"])  # add assertion here
        destroy = bg.deleteNamespace()
        self.assertEqual("Deleted", destroy)
    def test_insert_milled(self):
        # this is to test the files uploaded from milled
        password = getenv("GRAPHPASSWORD")
        if password is None:
            raise Exception("GRAPHPASSWORD missing")
        user = getenv("GRAPHUSER", "admin")
        if user is None:
            raise Exception("GRAPHUSER missing")
        bg = mg.ManageGraphdb("http://132.249.238.155/", "test", user, password)
        create = bg.createNamespace()
        self.assertIn(create, ["Created", "Exists"])
        try:
            #self.assertEqual(True, create)  # add assertion here
           # file = 'resources/test_triples/milled/0d8f2661071bdf56c91569ddfa0a5b8dea1a526d.rdf'
            file = '../resources/test_triples/milled/0d8f2661071bdf56c91569ddfa0a5b8dea1a526d.rdf'
            with open(file, 'rb+') as f:
                lines = f.read()
            inserted = bg.insert(lines,"text/plain")
            self.assertEqual(True, inserted)
        except:
            self.fail("failed")
        finally:
            destroy = bg.deleteNamespace()

    def test_load_from_release(self):
        password = getenv("GRAPHPASSWORD")
        if password is None:
            raise Exception("GRAPHPASSWORD missing")
        user = getenv("GRAPHUSER", "admin")
        if user is None:
            raise Exception("GRAPHUSER missing")
        bg = mg.ManageGraphdb("http://132.249.238.155/", "test", user, password)
        create = bg.createNamespace()
        self.assertIn(create, ["Created", "Exists"])
        try:
            # self.assertEqual(True, create)  # add assertion here
            # file = 'resources/test_triples/milled/0d8f2661071bdf56c91569ddfa0a5b8dea1a526d.rdf'
            file = 'https://oss.geocodes-aws-dev.earthcube.org/test/graphs/latest/geocodes_demo_datasets_release.nq'

            inserted = bg.loadReleaseFromUrl(url=file,source='test')
            self.assertEqual(True, inserted)
        except:
            self.fail("failed")
        finally:
            destroy = bg.deleteNamespace()

if __name__ == '__main__':
    unittest.main()
