import unittest
from approvaltests.approvals import verify

import pandas

import summarize.src.summarize_materializedview


class SummarizeMaterializedViewTestCase(unittest.TestCase):


    def test_summaryDF2ttl(self):
        file = '../resources/testing/summarydf_short.csv'
        # with open(file, 'r') as f:
        #     testdf = f.read()
        testdf = pandas.read_csv(file)
        results, g = summarize.src.summarize_materializedview.summaryDF2ttl(testdf, "test")
        self.assertEqual(2, results.count("a :Dataset ;"))  # add assertion here
        # this is an approval test.
        # in the approved_files directory there will be a file .approved.txt
        # if the test fails, but the results are correct,
        # mv summarize/src/approved_files/SummarizeMaterializedViewTestCase.test_summaryDF2ttl.recieved.txt summarize/src/approved_files/SummarizeMaterializedViewTestCase.test_summaryDF2ttl.approved.txt
        # rerun test
        nt = g.serialize(format='longturtle')
        verify(results)

if __name__ == '__main__':
    unittest.main()
