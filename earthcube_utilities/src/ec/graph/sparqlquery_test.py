import unittest
import sparqlquery


class Graph_SparqlDataframe_TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.endpoint = "https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/"
        cls.repo = "opentopography"
        cls.g = "urn:gleaner:summoned:opentopography:0024e35144d902d8b413ffd400ede6a27efe2146"
        cls.gbad = "urn:gleaner:summoned:random:uuid"

    def test_getFile(self):
        f = sparqlquery.getFileFromResources("sparql/select_one.txt")
        self.assertEqual(f, "SELECT * { ?s ?p ?o } LIMIT 1")  # add assertion here

    def test_getGraph(self ):
        result = sparqlquery.getAGraph(self.g, self.endpoint)
        self.assertIsNotNone(result)
        self.assertTrue(result.size > 0)

    def test_getGraphBadURI(self ):
        result = sparqlquery.getAGraph(self.gbad, self.endpoint)
        self.assertIsNotNone(result)
        self.assertTrue(result.size == 0)

    def test_queryWithSparqlRepo(self ):
        result = sparqlquery.queryWithSparql("repo_count_datasets", {"repo": self.repo}, self.endpoint)
        self.assertIsNotNone(result)
        self.assertTrue(result.size > 0)

if __name__ == '__main__':
    unittest.main()
