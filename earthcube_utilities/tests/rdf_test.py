import os
import unittest

import pytest
from approvaltests import verify

from jsonrdf.rdf import df2rdfgraph,get_rdfgraph, compact_jld_str
import pandas

class RDFTestCase(unittest.TestCase):

    ## this test hits and endpoint, so it needs a
    @pytest.mark.skipif(
        os.getenv('RUNNINGACTION') == "True",
        reason="Needs a service to check"
    )
    def test_get_rdf(self):
        g = get_rdfgraph("urn:gleaner:summoned:opentopography:0024e35144d902d8b413ffd400ede6a27efe2146", "https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/")
        self.assertIsNotNone(g)

        verify(f"length of graph is: {len(g)} triples")


    def test_dfnt(self):
        file = '../resources/0024e35144d902d8b413ffd400ede6a27efe2146_triples.csv'
        # with open(file, 'r') as f:
        #     testdf = f.read()
        testdf = pandas.read_csv(file)
        g = df2rdfgraph(testdf)
        self.assertIsNotNone(g)
        verify(f"length of graph is: {len(g)} triples")

    def test_compactJsonld(self):
        file = '../resources/0024e35144d902d8b413ffd400ede6a27efe2146_triples.csv'
        # with open(file, 'r') as f:
        #     testdf = f.read()
        testdf = pandas.read_csv(file)
        g = df2rdfgraph(testdf)
        jsonld = g.serialize(format="json-ld")
        self.assertIsNotNone(jsonld)
        cmpt = compact_jld_str(jsonld)
        verify(f"length of jsonld is: {len(cmpt)}")

if __name__ == '__main__':
    unittest.main()
