import unittest

import summarize_repo

class MyTestCase(unittest.TestCase):
    def test_endpointUpdate(self):
        endpoint = summarize_repo.endpointUpdateNamespace("https://example.com/blazegraph/namespace/earhtcube/sparql")
        self.assertEqual( "https://example.com/blazegraph/namespace/temp/sparql",endpoint)  # add assertion here
        endpoint = summarize_repo.endpointUpdateNamespace("https://example.com/blazegraph/namespace/earhtcube/sparql", namepsace="temp_summary")
        self.assertEqual("https://example.com/blazegraph/namespace/temp_summary/sparql", endpoint)

    def test_nabuCfg(self):
        with open('../resources/testing/nabu', 'r') as f:
            endpoint, cfg = summarize_repo.getNabu(f)
        self.assertEqual("https://graph.geodex.org/blazegraph/namespace/earthcube/sparql", endpoint)

    def test_reviseNabuCfg(self):
        with open('../resources/testing/nabu', 'r') as f:
            endpoint, cfg = summarize_repo.getNabu(f)
            endpoint = summarize_repo.endpointUpdateNamespace(
                "https://example.com/blazegraph/namespace/earhtcube/sparql")
            cfgnew = summarize_repo.reviseNabuConf(cfg, endpoint)

        self.assertEqual("https://example.com/blazegraph/namespace/temp/sparql", cfgnew['sparql']['endpoint'])

if __name__ == '__main__':
    unittest.main()
