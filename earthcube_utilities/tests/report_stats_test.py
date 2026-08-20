"""generateReportStats and its two input helpers.

Deliberately offline. The rest of tests/ talks to live minio and blazegraph
endpoints; these do not, which is the point of splitting the i/o out of
generateReportStats in the first place.
"""
import json
import unittest

from ec.reporting.report import generateReportStats, sourcesFromCSV

# a gleanerconfig.yaml sources entry, trimmed to the keys the report reads
IRIS = {
    "name": "iris",
    "propername": "IRIS",
    "domain": "https://ds.iris.edu",
    "url": "https://ds.iris.edu/sitemap.xml",
    "logo": "https://ds.iris.edu/logo.png",
}
OPENTOPO = {
    "name": "opentopography",
    "propername": "OpenTopography",
    "domain": "https://opentopography.org",
    "url": "https://opentopography.org/sitemap.xml",
}

CSV = (
    "Name,ProperName,Domain,URL,Community,Description,Active\r\n"
    "iris,IRIS,https://ds.iris.edu,https://ds.iris.edu/sitemap.xml,geocodes,Seismology,TRUE\r\n"
    "bcodmo,BCO-DMO,https://bco-dmo.org,https://bco-dmo.org/sitemap.xml,deepoceans,Ocean data,TRUE\r\n"
    "retired,Retired,https://retired.example,https://retired.example/sitemap.xml,geocodes,Gone,FALSE\r\n"
)


class GenerateReportStatsTestCase(unittest.TestCase):

    def test_maps_gleanerconfig_fields_onto_the_report(self):
        report = json.loads(generateReportStats([IRIS], {"iris": 28}, "geocodes"))

        self.assertEqual([{
            "source": "iris",
            "title": "IRIS",
            "website": "https://ds.iris.edu",
            "sitemap": "https://ds.iris.edu/sitemap.xml",
            "image": "iris.png",
            "community": "geocodes",
            "description": "",
            "records": "28",
        }], report)

    def test_description_is_blank_not_null_for_a_gleanerconfig_source(self):
        """gleanerconfig has no description field. The key stays, so a consumer
        reading it gets "" rather than undefined."""
        report = json.loads(generateReportStats([IRIS], {}, "geocodes"))

        self.assertEqual("", report[0]["description"])

    def test_description_is_kept_when_the_source_carries_one(self):
        source = dict(IRIS, description="Seismology")
        report = json.loads(generateReportStats([source], {}, "geocodes"))

        self.assertEqual("Seismology", report[0]["description"])

    def test_a_source_with_no_count_reports_zero(self):
        report = json.loads(generateReportStats([IRIS, OPENTOPO], {"iris": 28}, "geocodes"))

        self.assertEqual("28", report[0]["records"])
        self.assertEqual("0", report[1]["records"])

    def test_community_comes_from_the_argument_not_the_source(self):
        """The old code took it from the sheet's Community column, which held a
        comma separated list and was matched by substring."""
        report = json.loads(generateReportStats([IRIS], {}, "deepoceans"))

        self.assertEqual("deepoceans", report[0]["community"])

    def test_order_is_preserved(self):
        report = json.loads(generateReportStats([OPENTOPO, IRIS], {}, "geocodes"))

        self.assertEqual(["opentopography", "iris"], [r["source"] for r in report])

    def test_no_sources_is_an_empty_array(self):
        self.assertEqual([], json.loads(generateReportStats([], {}, "geocodes")))


class SourcesFromCSVTestCase(unittest.TestCase):
    """sourcesFromCSV keeps the sheet path working for the ec_reports CLI, so
    it has to normalise onto the same keys generateReportStats reads."""

    def setUp(self):
        import ec.reporting.report as report_module
        self._readSourceCSV = report_module.readSourceCSV
        import csv as _csv
        report_module.readSourceCSV = lambda url: list(
            _csv.DictReader(CSV.splitlines()))

    def tearDown(self):
        import ec.reporting.report as report_module
        report_module.readSourceCSV = self._readSourceCSV

    def test_normalises_sheet_columns_onto_gleanerconfig_keys(self):
        sources = sourcesFromCSV("ignored", "geocodes")

        self.assertEqual({
            "name": "iris",
            "propername": "IRIS",
            "domain": "https://ds.iris.edu",
            "url": "https://ds.iris.edu/sitemap.xml",
            "description": "Seismology",
        }, sources[0])

    def test_a_named_community_does_not_filter_on_active(self):
        """Preserved quirk: only the 'all' branch ever looked at Active, so an
        inactive row still lands in a named community's report."""
        sources = sourcesFromCSV("ignored", "geocodes")

        self.assertEqual(["iris", "retired"], [s["name"] for s in sources])

    def test_all_takes_every_active_source(self):
        sources = sourcesFromCSV("ignored", "all")

        self.assertEqual(["iris", "bcodmo"], [s["name"] for s in sources])

    def test_a_community_filter_still_selects_on_the_community_column(self):
        sources = sourcesFromCSV("ignored", "deepoceans")

        self.assertEqual(["bcodmo"], [s["name"] for s in sources])

    def test_normalised_sources_render(self):
        report = json.loads(generateReportStats(
            sourcesFromCSV("ignored", "geocodes"), {"iris": 3}, "geocodes"))

        self.assertEqual("Seismology", report[0]["description"])
        self.assertEqual("3", report[0]["records"])


if __name__ == '__main__':
    unittest.main()
