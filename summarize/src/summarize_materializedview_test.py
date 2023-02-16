import unittest

import pandas

import summarize.src.summarize_materializedview


class SummarizeMaterializedViewTestCase(unittest.TestCase):
    def test_summaryDF2ttl(self):
        file = '../resources/testing/summarydf_short.csv'
        # with open(file, 'r') as f:
        #     testdf = f.read()
        testdf = pandas.read_csv(file)
        results = summarize.src.summarize_materializedview.summaryDF2ttl(testdf, "test")
        self.assertEqual(2, results.count("a :Dataset ;"))  # add assertion here


if __name__ == '__main__':
    unittest.main()
