import os
import shutil
import tempfile
import unittest
from os import path

import collection.rocate_collection


class RoCreateTestCase(unittest.TestCase):
    def test_readcreate(self):
        collectiondir = "../resources/collection/simple/"
        crate_dir = collectiondir
        tempcreate = path.join(tempfile.gettempdir(),"read_crate.crate")

        zip_source = shutil.make_archive( tempcreate, "zip", crate_dir)
        crate = collection.rocate_collection.readSosRoCrates3(zip_source)
        for e in crate.get_entities():
            print(e.id, e.type)
    def test_createCreate(self):
        file = "../resources/0024e35144d902d8b413ffd400ede6a27efe2146.jsonld"
        with open(file) as f:
            jsonld = f.read()
        crate = collection.rocate_collection.SosRocrate()
        crate.name = "test"
        crate.addSosCreator(crate, "aUser")
        crate.addSosPublisher(crate,name="publsher")
        crate.addSosURL(crate,url="http://example.com", name="a url")
        tempcreate = path.join(tempfile.gettempdir(), "write_crate.crate")
        crate.write(tempcreate)
        self.assertTrue( os.path.exists(tempcreate) )

        with open( path.join(tempcreate, "ro-crate-metadata.json")) as f:
            file_content =f.read()
            self.assertIsNotNone(file_content)


if __name__ == '__main__':
    unittest.main()
