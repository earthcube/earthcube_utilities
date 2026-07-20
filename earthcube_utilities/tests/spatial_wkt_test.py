import unittest

from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery

from ec.spatial_wkt import getSpatialQuery, QUERIES

GEO = "http://www.opengis.net/ont/geosparql#"

BOX_DATA = """
@prefix schema: <https://schema.org/> .
<urn:ds1> a schema:Dataset ;
  schema:spatialCoverage [ schema:geo <urn:geo1> ] .
<urn:geo1> a schema:GeoShape ; schema:box "10.5 -120.0 12.5 -118.0" .
"""

LATLON_DATA = """
@prefix schema: <https://schema.org/> .
<urn:ds2> a schema:Dataset ;
  schema:spatialCoverage [ schema:geo <urn:geo2>, <urn:geo3> ] .
<urn:geo2> a schema:GeoCoordinates ; schema:latitude 10.5 ; schema:longitude -120.0 .
<urn:geo3> a schema:GeoCoordinates ; schema:latitude 11.5 ; schema:longitude -119.0 .
"""


class SpatialWktTestCase(unittest.TestCase):
    def test_queries_parse(self):
        """all spatial queries load from resources; construct queries are valid sparql"""
        for name in QUERIES:
            for mode in ["construct", "insert"]:
                query = getSpatialQuery(name, mode)
                self.assertTrue(len(query) > 0)
            prepareQuery(getSpatialQuery(name, "construct"))

    def run_construct(self, name, data):
        g = Graph()
        g.parse(data=data, format="turtle")
        result = Graph()
        for triple in g.query(getSpatialQuery(name, "construct")):
            result.add(triple)
        return result

    def test_box2polygon(self):
        result = self.run_construct("box2polygon", BOX_DATA)
        wkt = [str(o) for s, p, o in result if str(p) == f"{GEO}asWKT"]
        self.assertEqual(len(wkt), 1)
        self.assertEqual(wkt[0],
                         "POLYGON((-120.0 10.5, -118.0 10.5, -118.0 12.5, -120.0 12.5, -120.0 10.5))")

    def test_latlon2multipoint(self):
        result = self.run_construct("latlon2multipoint", LATLON_DATA)
        wkt = [str(o) for s, p, o in result if str(p) == f"{GEO}asWKT"]
        self.assertEqual(len(wkt), 1)
        self.assertEqual(wkt[0], "MULTIPOINT((-120.0 10.5), (-119.0 11.5))")


if __name__ == '__main__':
    unittest.main()
