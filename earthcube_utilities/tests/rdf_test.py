import json
import os
import unittest

import pytest
from approvaltests import verify, verify_as_json

from ec.sos_json.rdf import df2rdfgraph,get_rdfgraph, load_release
from ec.sos_json.utils import compact_jld_str, formatted_jsonld
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

    def test_load_release(self):
        relasefile = "../resources/summonediris_2023-03-13-11-02-47_release.nq"
        #relasefile = "https://oss.geocodes-dev.earthcube.org/gleaner-wf/graphs/latest/summonediris_2023-03-13-11-02-47_release.nq"
        df = load_release(relasefile)
        self.assertIsNotNone(df)
        self.assertTrue(len(df) > 0)

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

    def test_formatted_compact_Jsonld(self):
        file = '../resources/0024e35144d902d8b413ffd400ede6a27efe2146_triples.csv'
        # with open(file, 'r') as f:
        #     testdf = f.read()
        testdf = pandas.read_csv(file)
        g = df2rdfgraph(testdf)
        jsonld = g.serialize(format="json-ld")
        self.assertIsNotNone(jsonld)
        cmpt = formatted_jsonld(jsonld, form="compact")
        verify(f"length of jsonld is: {len(cmpt)}")

    def test_formatted_framedJsonld(self):
        file = '../resources/0024e35144d902d8b413ffd400ede6a27efe2146_triples.csv'
        # with open(file, 'r') as f:
        #     testdf = f.read()
        testdf = pandas.read_csv(file)
        g = df2rdfgraph(testdf)
        jsonld = g.serialize(format="json-ld")
        self.assertIsNotNone(jsonld)
        framed = formatted_jsonld(jsonld, form="frame")
        #verify(f"length of jsonld is: {len(framed)}")
        compare = json.loads(framed)
        verify_as_json(compare)

    def test_dupe_at_id_Jsonld(self):
        """demonstrates that @type is expanded to at type=['Dataset','PropertyValue']"""
        file = '../resources/0024e35144d902d8b413ffd400ede6a27efe2146_orig.jsonld'
        with open(file, 'r') as f:
             jsonld = f.read()
        self.assertIsNotNone(jsonld)

        cmpt = formatted_jsonld(jsonld, form="frame")
        compare = json.loads(cmpt)
        # verify(f"length of jsonld is: {len(cmpt)}")
        verify_as_json(compare)
    def test_relative_at_if_Jsonld(self):
        file = '../resources/0024e35144d902d8b413ffd400ede6a27efe2146_v2.jsonld'
        with open(file, 'r') as f:
            jsonld = f.read()
        self.assertIsNotNone(jsonld)

        cmpt = formatted_jsonld(jsonld, form="compact")
        compare = json.loads(cmpt)
       # verify(f"length of jsonld is: {len(cmpt)}")
        verify_as_json(compare)


if __name__ == '__main__':
    unittest.main()
