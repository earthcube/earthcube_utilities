import json
import unittest

from ec.sos_json.utils import validateJson2Schema, isValidJSON
try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

class MyTestCase(unittest.TestCase):
    def test_validateJson2Schema(self):
        file="../resources/0024e35144d902d8b413ffd400ede6a27efe2146.jsonld"
        with open(file, 'r') as f:
            testdata = f.read()
        validjson = isValidJSON(testdata)
        self.assertEqual(True, validjson)
        # pass JSON data a object
        json_data = json.loads(testdata)
        validates,message = validateJson2Schema(json_data)
        self.assertEqual(True, validates)  # add assertion here
        self.assertEqual("Given JSONLD data is Valid", message)


if __name__ == '__main__':
    unittest.main()
