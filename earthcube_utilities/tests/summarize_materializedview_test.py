import unittest
from approvaltests.approvals import verify

import pandas

from ec.summarize.summarize_materializedview import summaryDF2ttl, summaryDF2quad


class SummarizeMaterializedViewTestCase(unittest.TestCase):


    def test_summaryDF2ttl(self):
        file = "../resources/testing/summarydf_short.csv"
        with open(file, 'r') as f:
            tesdf = f.read()
        testdf = pandas.read_csv(file)
        results, g = summaryDF2ttl(testdf, "test")
        self.assertEqual(2, results.count("a ecsummary:Dataset ;"))  # add assertion here
        # this is an approval test.
        # in the approved_files directory there will be a file .approved.txt
        # if the test fails, but the results are correct,
        # mv summarize/src/approved_files/SummarizeMaterializedViewTestCase.test_summaryDF2ttl.recieved.txt summarize/src/approved_files/SummarizeMaterializedViewTestCase.test_summaryDF2ttl.approved.txt
        # rerun test
        nt = g.serialize(format='longturtle')
        verify(nt)
    def test_summaryDF2quad(self):
        file = "../resources/testing/summarydf_short.csv"
        with open(file, 'r') as f:
            tesdf = f.read()
        testdf = pandas.read_csv(file)
        results, g = summaryDF2quad(testdf, "test")
        self.assertEqual(2, results.count("<https://schema.org/Dataset>"))  # add assertion here
        # this is an approval test.
        # in the approved_files directory there will be a file .approved.txt
        # if the test fails, but the results are correct,
        # mv summarize/src/approved_files/SummarizeMaterializedViewTestCase.test_summaryDF2ttl.recieved.txt summarize/src/approved_files/SummarizeMaterializedViewTestCase.test_summaryDF2ttl.approved.txt
        # rerun test
        nt = g.serialize(format='nquads')
        verify(nt)

if __name__ == '__main__':
    unittest.main()
