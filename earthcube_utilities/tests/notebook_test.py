import unittest

from ec.notebook.geocodes import get_from_geocodes
class NotebookTestCase(unittest.TestCase):
    def test_get_from_geocodes(self):
        #jsonld = get_from_geocodes("urn:gleaner.io:earthcube:geocodes_demo_datasets:257108e0760f96ef7a480e1d357bcf8720cd11e4")
        jsonld = get_from_geocodes("urn:gleaner:summoned:opentopography:0024e35144d902d8b413ffd400ede6a27efe2146")

        self.assertIsNot("[]", jsonld)  # add assertion here


if __name__ == '__main__':
    unittest.main()
