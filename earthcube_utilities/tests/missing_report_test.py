"""missingReport's graph_urns path.

Offline: the rest of tests/ wants live minio and blazegraph, these stub both.
"""
import unittest
from unittest import mock

import ec.reporting.report as report_module
from ec.reporting.report import missingReport

SITEMAP_URLS = ["https://example.org/a", "https://example.org/b"]
# sha is whatever follows the last colon
URNS = [
    "urn:ec-geocodes:iris:aaaaaaaa",
    "urn:ec-geocodes:iris:bbbbbbbb",
]


class _Datastore:
    """Enough of bucketDatastore for missingReport."""

    endpoint = "oss.example.org"

    def __init__(self, summoned_shas=None):
        self._summoned_shas = summoned_shas if summoned_shas is not None else ["aaaaaaaa", "bbbbbbbb"]

    def listSummonedUrls(self, bucket, repo):
        return [{"url": u} for u in SITEMAP_URLS]

    def listSummonedSha(self, bucket, repo):
        return list(self._summoned_shas)

    def listMilledSha(self, bucket, repo):
        return []


class _Sitemap:
    def __init__(self, url, **kwargs):
        self.url = url

    def validUrl(self):
        return True

    def uniqueUrls(self):
        return list(SITEMAP_URLS)


class MissingReportGraphUrnsTestCase(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch.object(report_module.ec.sitemap, "Sitemap", _Sitemap)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_supplied_urns_are_used_and_no_sparql_is_attempted(self):
        with mock.patch.object(report_module.ec.graph.sparql_query, "queryWithSparql") as q:
            response = missingReport("https://example.org/sitemap.xml", "b", "iris",
                                     _Datastore(), milled=False, summon=False,
                                     graph_urns=URNS)

        q.assert_not_called()
        self.assertEqual(2, response["graph_urn_count"])
        self.assertEqual(0, response["missing_summon_graph_count"])

    def test_a_sha_missing_from_the_urns_is_reported(self):
        datastore = _Datastore(summoned_shas=["aaaaaaaa", "bbbbbbbb", "cccccccc"])

        response = missingReport("https://example.org/sitemap.xml", "b", "iris",
                                 datastore, milled=False, summon=False,
                                 graph_urns=URNS)

        self.assertEqual(2, response["graph_urn_count"])
        self.assertEqual(1, response["missing_summon_graph_count"])
        self.assertEqual(["cccccccc"], response["missing_summon_graph"])

    def test_an_empty_urn_list_is_not_the_same_as_none(self):
        """A release with no named graphs reports zero, it does not fall back
        to querying an endpoint."""
        with mock.patch.object(report_module.ec.graph.sparql_query, "queryWithSparql") as q:
            response = missingReport("https://example.org/sitemap.xml", "b", "iris",
                                     _Datastore(), milled=False, summon=False,
                                     graph_urns=[])

        q.assert_not_called()
        self.assertEqual(0, response["graph_urn_count"])
        self.assertEqual(2, response["missing_summon_graph_count"])

    def test_without_urns_it_still_queries_the_endpoint(self):
        with mock.patch.object(report_module.ec.graph.sparql_query, "queryWithSparql") as q:
            q.return_value = {"g": URNS}
            response = missingReport("https://example.org/sitemap.xml", "b", "iris",
                                     _Datastore(), graphendpoint="http://graph/sparql",
                                     milled=False, summon=False)

        q.assert_called_once()
        self.assertEqual("repo_select_graphs", q.call_args[0][0])
        self.assertEqual("http://graph/sparql", q.call_args[0][1])
        self.assertEqual(2, response["graph_urn_count"])

    def test_summon_returns_before_either_path(self):
        with mock.patch.object(report_module.ec.graph.sparql_query, "queryWithSparql") as q:
            response = missingReport("https://example.org/sitemap.xml", "b", "iris",
                                     _Datastore(), summon=True)

        q.assert_not_called()
        self.assertNotIn("graph_urn_count", response)
        self.assertEqual(2, response["summoned_count"])


if __name__ == '__main__':
    unittest.main()
