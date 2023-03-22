import json
import unittest

from datastore.s3 import MinioDatastore
from ec.reporting.report import generateAGraphReportsRepo, generateGraphReportsRepo, putGraphReports4RepoReport

# shortened list of report types for testing
reportTypes ={
    "all": [{"code":"triple_count", "name": "all_count_triples"},
            {"code":"graph_count_by_repo", "name": "all_repo_count_graphs"},
            ],
    "repo":[
        {"code":"kw_count", "name": "repo_count_keywords"},
{"code":"dataset_count", "name": "repo_count_datasets"},
    ]
}
class ReportingTestCase(unittest.TestCase):
    def test_generate_a_graph_repo(self):
        report = generateAGraphReportsRepo("opentopography","triple_count" , "https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/sparlq")
        self.assertIsNot(None,report)
    def test_generate_a_graph_repo_all(self):
        report = generateAGraphReportsRepo("all", "triple_count", "https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/sparlq")
        self.assertIsNot(None,report)
        self.assertEquals(1, report.size)

    def test_generate_graph_all(self):
        """ run a list of report types."""
        report_json = generateGraphReportsRepo("all",
                                          "https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/sparlq",
                                          reportTypes=reportTypes)
        self.assertIsNot(None,report_json)
        report = json.loads(report_json)
        self.assertEquals(2, len(report["reports"]) )

    def test_generate_graph_repo(self):
        """ run a list of report types."""
        report_json = generateGraphReportsRepo("opentopography",
                                          "https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/sparlq",
                                          reportTypes=reportTypes)
        self.assertIsNot(None,report_json)
        report = json.loads(report_json)
        self.assertEquals(2, len(report["reports"]) )

    def test_put_report(self):
        bucket = "gleaner"
        endpoint = "oss.geocodes-dev.earthcube.org"
        repo="opentopography"
        date="latest"
        report_json = generateGraphReportsRepo("all",
                                          "https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/sparlq",
                                          reportTypes=reportTypes,
                                               )
        s3client = MinioDatastore(endpoint, None)

        bucket_name, object_name = putGraphReports4RepoReport(repo,   report_json, s3client, reportname="putest.json", date='latest')
        self.assertEquals(bucket_name, bucket)
        self.assertIsNotNone(object_name)
if __name__ == '__main__':
    unittest.main()
