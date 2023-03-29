import json
import os
import shutil
import tempfile
import unittest
from os import path

import pyld.jsonld

from ec.collection.rocrate_collection  import SosRocrate,readDecoderRoCrate
from ec.sos_json.utils import formatted_jsonld


class RoCreateTestCase(unittest.TestCase):
    json1=None
    json2=None

    def setUp(self) -> None:
        file = "../resources/0024e35144d902d8b413ffd400ede6a27efe2146.jsonld"

        with open(file) as f:
            jsonld = f.read()
        jsonld = formatted_jsonld(jsonld, form="frame", schemaType="Dataset")
        jsonld = json.loads(jsonld)
        #jsonld = pyld.jsonld.flatten(jsonld, {"@vocab":"https://schema.org/"})
        self.json1 = jsonld

    def test_readcreate(self):
        collectiondir = "../resources/collection/simple/"
        crate_dir = collectiondir
        tempcreate = path.join(tempfile.gettempdir(),"read_crate.crate")

        zip_source = shutil.make_archive( tempcreate, "zip", crate_dir)
        crate = readDecoderRoCrate(zip_source)
        for e in crate.get_entities():
            print(e.id, e.type)


    def test_createCreate(self):

        crate = SosRocrate()
        crate.name = "test"
        crate.addSosCreator(crate, "aUser")
        crate.addSosPublisher(crate,name="publsher")
        crate.addSosURL(url="http://example.com", name="a url")
        tempcreate = path.join(tempfile.gettempdir(), "write_crate.crate")
        crate.write(tempcreate)
        self.assertTrue( os.path.exists(tempcreate) )

        # needs to openf file and find "@id": "example.com"
        with open( path.join(tempcreate, "ro-crate-metadata.json")) as f:
            file_content =f.read()
            self.assertIsNotNone(file_content)

    def test_createCreateURLAndJsonLD(self):

        crate = SosRocrate()
        crate.name = "test"
        crate.addSosCreator(crate, "aUser")
        crate.addSosPublisher(crate,name="publsher")
        crate.addSosDatasetAsFile(self.json1, "https://portal.opentopography.org/lidarDataset?opentopoID=OTLAS.052015.32611.1")
        tempcreate = path.join(tempfile.gettempdir(), "write_crate_2.crate")
        crate.write(tempcreate)
        self.assertTrue( os.path.exists(tempcreate) )

        # needs to openf file and find "@id": "example.com"
        with open( path.join(tempcreate, "ro-crate-metadata.json")) as f:
            file_content =f.read()
            self.assertIsNotNone(file_content)
    def test_createCreateAddJsonldAsDataset(self):

        crate = SosRocrate()
        crate.name = "test"
        crate.addSosCreator(crate, "aUser")
        crate.addSosPublisher(crate,name="publsher")
        crate.addSosURL(crate,url="http://example.com", name="a url")
        # crate.addSosDatasetAsEntity(crate,json.dumps(jsonld), "urn1")
        crate.addSosDatasetAsDataset(self.json1, "https://portal.opentopography.org/lidarDataset?opentopoID=OTLAS.052015.32611.1")
        with  tempfile.TemporaryDirectory() as tmpdir:
            tempcreate = path.join(tmpdir, "write_dataset.crate")
            crate.write(tempcreate)
            self.assertTrue( os.path.exists(tempcreate) )
            crate.write_zip(tempcreate)

            # needs to openf file and find "@id": "urn1/"
            with open( path.join(tempcreate, "ro-crate-metadata.json")) as f:
                file_content =f.read()
                self.assertIsNotNone(file_content)

    def test_createCreateAddJsonldAsContextEntity(self):
        """this does not get added to hasParts... aka does not get Identifieed as a Dataset"""
        crate = SosRocrate()
        crate.name = "test"
        crate.addSosCreator(crate, "aUser")
        crate.addSosPublisher(crate,name="publsher")
        crate.addSosURL(crate,url="http://example.com", name="a url")
       # crate.addSosDatasetAsEntity(crate,json.dumps(jsonld), "urn1")
        crate.addSosDatasetAsCtxEntity(self.json1, "urn1")
        with  tempfile.TemporaryDirectory() as tmpdir:
            tempcreate = path.join(tmpdir, "write_ctx.crate")
            crate.write(tempcreate)
            self.assertTrue( os.path.exists(tempcreate) )
            crate.write_zip(tempcreate)

# needs to openf file and find "@id": "urn1/"
            with open( path.join(tempcreate, "ro-crate-metadata.json")) as f:
                file_content =f.read()
                self.assertIsNotNone(file_content)


if __name__ == '__main__':
    unittest.main()
