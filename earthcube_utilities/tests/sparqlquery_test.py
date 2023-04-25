import unittest
from approvaltests import verify

# pycharm does not like the top level package name... but this is what makes it work
# from ec.graph.sparql_query import getFileFromResources,getAGraph, queryWithSparql
from ec.graph.sparql_query import _getSparqlFileFromResources,getAGraph, queryWithSparql, listSparqlFilesFromResources


class Graph_SparqlDataframe_TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.endpoint = "https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/"
        cls.repo = "opentopography"
        cls.g = "urn:gleaner:summoned:opentopography:0024e35144d902d8b413ffd400ede6a27efe2146"
        cls.gbad = "urn:gleaner:summoned:random:uuid"

    def test_getFile(self):
        f = _getSparqlFileFromResources("select_one")
        self.assertEqual(f, "SELECT * { ?s ?p ?o } LIMIT 1")  # add assertion here
    def test_listile(self):
        f =list(listSparqlFilesFromResources())
        verify(f)  # add assertion here

    def test_getGraph(self ):
        result = getAGraph(self.g, self.endpoint)
        self.assertIsNotNone(result)
        self.assertTrue(result.size > 0)

    def test_getGraphBadURI(self ):
        result = getAGraph(self.gbad, self.endpoint)
        self.assertIsNotNone(result)
        self.assertTrue(result.size == 0)

    def test_queryWithSparqlRepo(self ):
        result = queryWithSparql("repo_count_datasets", self.endpoint, parameters= {"repo": self.repo})
        self.assertIsNotNone(result)
        self.assertTrue(result.size > 0)

    def test_queryWithSparqlNoParameters(self ):
        result = queryWithSparql("select_one", self.endpoint)
        self.assertIsNotNone(result)
        self.assertTrue(result.size > 0)
if __name__ == '__main__':
    unittest.main()
