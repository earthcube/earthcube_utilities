import unittest
from click.testing import CliRunner
from ec.ec_reports import missing_report, graph_stats

class ReportingTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.runner = CliRunner()
        self.cfgfile = "/Users/ylyang/gleaner"
        self.s3server = "oss.geocodes.ncsa.illinois.edu"
        self.bucket = "yybucket"
        self.graphendpoint = "https://graph.geocodes.ncsa.illinois.edu/blazegraph/namespace/yyearthcube2/sparql"
        self.upload = False

    def test_ec_missing_report(self):
        output = "ec_missing_report_test"
        debug = False
        source = "iris"
        milled = False
        summononly = True
        result = self.runner.invoke(missing_report,
                               [self.cfgfile, self.s3server, self.bucket, self.graphendpoint, self.upload,
                                output, debug, source, milled, summononly])
        self.assertTrue(result)

    def test_ec_graph_stats(self):
        output = "ec_missing_report_test"
        debug = False
        source = "iris"
        result = self.runner.invoke(graph_stats,
                                    [self.cfgfile, self.s3server, self.bucket, self.graphendpoint, self.upload,
                                     output, debug, source])
        self.assertTrue(result)

    def test_ec_identifier_stats(self):
        output = "ec_identifier_stats_test"
        debug = False
        source = "iris"
        json = True
        result = self.runner.invoke(graph_stats,
                                    [self.cfgfile, self.s3server, self.bucket, self.graphendpoint, self.upload,
                                     output, debug, source, json])
        self.assertTrue(result)