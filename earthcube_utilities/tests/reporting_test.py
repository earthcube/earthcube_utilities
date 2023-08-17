import json
import unittest
from approvaltests import verify, verify_as_json

from ec.datastore.s3 import MinioDatastore

import ec.reporting.report
from ec.reporting.report import generateAGraphReportsRepo, generateGraphReportsRepo

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

    def setUp(self) -> None:
        self.bucket = "gleaner"
        self.endpoint = "oss.geocodes-dev.earthcube.org"
        self.repo = "opentopography"
        self.date = "latest"
        self.s3client = MinioDatastore(self.endpoint, None)
        self.sitemapurl="https://opentopography.org/sitemap.xml"
        self.graphendpoint="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/sparql"

    def test_generate_a_graph_repo(self):
        report = generateAGraphReportsRepo("opentopography","triple_count" , self.graphendpoint)
        self.assertIsNot(None,report)
    def test_generate_a_graph_repo_all(self):
        report = generateAGraphReportsRepo("all", "triple_count",self.graphendpoint)
        self.assertIsNot(None,report)
        self.assertEquals(1, report.size)

    def test_generate_graph_all(self):
        """ run a list of report types."""
        report_json = generateGraphReportsRepo("all",
                                          self.graphendpoint,
                                          reportList=reportTypes['all'])
        self.assertIsNot(None,report_json)
        report = json.loads(report_json)
        self.assertEquals(2, len(report["reports"]) )

    def test_generate_graph_repo(self):
        """ run a list of report types."""
        report_json = generateGraphReportsRepo("opentopography",
                                               self.graphendpoint,
                                          reportList=reportTypes['repo'])
        self.assertIsNot(None,report_json)
        report = json.loads(report_json)
        self.assertEquals(2, len(report["reports"]) )

    def test_put_report(self):
        bucket = "citesting"
        endpoint = "oss.geocodes-dev.earthcube.org"
        repo="geocodes_demo_datasets"
        date="latest"
        report_json = '{"test":"test"}'
        s3client = MinioDatastore(endpoint, None)

        bucket_name, object_name = s3client.putReportFile(bucket, repo, "putest.json",  report_json,
                                                              date='latest'
                                                              )
        self.assertEquals(bucket_name, bucket)
        self.assertIsNotNone(object_name)

    def test_compareSitemap2Summoned(self):
        results = ec.reporting.report.compareSitemap2Summoned(self.sitemapurl,self.bucket,self.repo, self.s3client)
        verify_as_json(results)


    def test_compareSummoned2Milled(self):
        results = ec.reporting.report.compareSummoned2Milled( self.bucket, self.repo, self.s3client)
        verify_as_json(results)
    def test_compareSummoned2Graph(self):
        results = ec.reporting.report.compareSummoned2Graph(self.bucket, self.repo, self.s3client, self.graphendpoint)
        verify_as_json(results)
    def test_missingReport(self):
        results = ec.reporting.report.missingReport(self.sitemapurl,self.bucket, self.repo, self.s3client, self.graphendpoint)
        verify_as_json(results)
    def test_missingReport_badsitemap(self):
        with self.assertRaises(ValueError):
            ec.reporting.report.missingReport("https://example.com/sitemap.xml",self.bucket, self.repo, self.s3client, self.graphendpoint)



if __name__ == '__main__':
    unittest.main()
