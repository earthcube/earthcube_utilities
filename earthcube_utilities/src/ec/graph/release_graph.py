import csv
from io import StringIO
from string import Template

import pandas
from rdflib import Namespace, Dataset,Graph, ConjunctiveGraph
from rdflib.namespace import RDF

from  ec.graph.sparql_query import _getSparqlFileFromResources
from ec.datastore.s3 import MinioDatastore

"""
prefix schema: <https://schema.org/>
SELECT distinct ?g ?subj  ?resourceType ?name ?description  ?pubname
        (GROUP_CONCAT(DISTINCT ?placename; SEPARATOR=", ") AS ?placenames)
        (GROUP_CONCAT(DISTINCT ?kwu; SEPARATOR=", ") AS ?kw) ?datep ?sosType

        WHERE {
          graph ?g {
             ?subj schema:name ?name .
             ?subj schema:description ?description .
                values ?sosType {
                schema:Dataset
    
                }

            Minus {?subj a schema:Person } .
            
            #BIND (?type AS ?resourceType) .

            optional {?subj schema:distribution/schema:url|schema:subjectOf/schema:url ?url .}
            OPTIONAL {?subj schema:datePublished ?date_p .}
            OPTIONAL {?subj schema:publisher/schema:name|schema:sdPublisher|schema:provider/schema:name ?pub_name .}
            OPTIONAL {?subj schema:spatialCoverage/schema:name ?place_name .}
            OPTIONAL {?subj schema:keywords ?kwu .}

             BIND ( IF ( BOUND(?date_p), ?date_p, "1900-01-01") as ?datep ) .
            BIND ( IF ( BOUND(?pub_name), ?pub_name, "No Publisher") as ?pubname ) .
            BIND ( IF ( BOUND(?place_name), ?place_name, "No spatialCoverage") as ?placename ) .
             }

        }
      #  GROUP BY ?g ?subj ?resourceType ?name ?description ?pubname ?placenames ?kw ?datep    ?sosType 
       GROUP BY ?g ?subj  ?name ?description ?pubname ?placenames ?kw ?datep    ?sosType 
"""
# notes... we can group concat where a field is possibly none. we have to use a bind.
# from placenames and keywords
summary_sparql = """
prefix schema: <https://schema.org/>
SELECT distinct ?g ?subj  ?resourceType ?name ?description  ?pubname
        (GROUP_CONCAT(DISTINCT ?placename; SEPARATOR=", ") AS ?placenames)
        (GROUP_CONCAT(DISTINCT ?kws; SEPARATOR=", ") AS ?kw) 
        ?datep ?sosType

        WHERE {
          graph ?g {
             ?subj schema:name ?name .
             ?subj schema:description ?description .
                values ?sosType {
                schema:Dataset

                }

?subj a ?type . 
            BIND (?type AS ?resourceType) .

            optional {?subj schema:distribution/schema:url|schema:subjectOf/schema:url ?url .}
            OPTIONAL {?subj schema:datePublished ?date_p .}
            OPTIONAL {?subj schema:publisher/schema:name|schema:sdPublisher|schema:provider/schema:name ?pub_name .}
            OPTIONAL {?subj schema:spatialCoverage/schema:name ?placename .}
            OPTIONAL {?subj schema:keywords ?kwu } .

            # BIND ( IF ( BOUND(?date_p), ?date_p, "1900-01-01") as ?datep ) .
         #   BIND ( IF ( BOUND(?pub_name), ?pub_name, "No Publisher") as ?pubname ) .
            BIND ( IF ( BOUND(?place_name), ?place_name, "No spatialCoverage") as ?placename ) .
             BIND ( IF ( BOUND(?kwu), ?kwu, "") as ?kws ) .
             }

        }
      #  GROUP BY ?g ?subj ?resourceType ?name ?description ?pubname ?placenames ?kw ?datep    ?sosType 
       GROUP BY ?g ?subj  ?name ?description ?pubname ?placenames ?kw ?datep    ?sosType 
        """
test_types="""
prefix schema: <https://schema.org/>
SELECT distinct ?place_name ?g ?type ?sosType ?date_p (GROUP_CONCAT(DISTINCT ?resourceType ; SEPARATOR=", ") AS ?sc) (count(distinct ?s ) as ?scount)
WHERE {
graph ?g  {

       ?s a ?type .
             values ?sosType {
            schema:Dataset

            } 
             Minus {?s a schema:Person } .
                  BIND (IF (exists {?s a schema:Dataset .} ||exists{?s a schema:DataCatalog .} , "data", "tool") AS ?resourceType) 
         OPTIONAL {?s schema:datePublished ?date_p .}
         OPTIONAL {?s schema:spatialCoverage/schema:name ?place_name .}
          OPTIONAL {?s schema:publisher/schema:name|schema:sdPublisher|schema:provider/schema:name ?pub_name .}
       }
 
}

GROUP By ?type ?resourceType ?sosType ?date_p ?place_name
ORDER By DESC(?scount)
"""
SCHEMAORG_http = Namespace("http://schema.org/")
SCHEMAORG_https = Namespace("https://schema.org/")
class ReleaseGraph:
    dataset = Dataset(default_union=True)
    dataset.bind('schema_http',SCHEMAORG_http)
    dataset.bind('schema', SCHEMAORG_https)
    #dataset = ConjunctiveGraph()
    filename = ""

    def load_release(self, file_or_url):
        self.dataset.parse(file_or_url, format='nquads')
    def read_release(self, s3server, s3bucket, source, date="latest"):
        s3 = MinioDatastore(s3server, None)
        url = s3.getLatestRelaseUrl(s3bucket, source)
        self.filename = url[ url.rfind('/') +1 :]
        self.load_release(url)

    def summarize(self):
        # get the summary sparql query, run it sparql data frome to put it in a dataframe
        #might just feed the result rows to pandas
        # all_summary_query returns no rows ;)
       # resource = ec.graph.sparql_query._getSparqlFileFromResources("all_summary_query")
       # resource = ec.graph.sparql_query._getSparqlFileFromResources("all_repo_count_datasets")
        # result = self.dataset.query(resource)

        #result = self.dataset.query(test_types, initNs={'schema_o': SCHEMAORG_http, 'schema':SCHEMAORG_https })
        query = _getSparqlFileFromResources('all_summary_query')
        result = self.dataset.query(summary_sparql, result='sparql', initNs={'schema_old': SCHEMAORG_http, 'schema': SCHEMAORG_https})
        #result = self.dataset.query(summary_sparql)
        csvres = result.serialize(format="csv")
        csvres = csvres.decode()
        csv_io = StringIO(csvres)
        df = pandas.read_csv(csv_io)
        return df

    def query_release(self, template_name='all_summary_query',parameters={}):
        query = _getSparqlFileFromResources(f"{template_name}")
        # get the summary sparql query, run it sparql data frome to put it in a dataframe
        #might just feed the result rows to pandas
        # all_summary_query returns no rows ;)
       # resource = ec.graph.sparql_query._getSparqlFileFromResources("all_summary_query")
       # resource = ec.graph.sparql_query._getSparqlFileFromResources("all_repo_count_datasets")
        # result = self.dataset.query(resource)
        q_template = Template(query)
        thsGraphQuery = q_template.substitute(parameters)
        #result = self.dataset.query(test_types, initNs={'schema_o': SCHEMAORG_http, 'schema':SCHEMAORG_https })
        result = self.dataset.query(thsGraphQuery, result='sparql', initNs={'schema_old': SCHEMAORG_http, 'schema': SCHEMAORG_https})
        #result = self.dataset.query(summary_sparql)
        csvres = result.serialize(format="csv")
        csvres = csvres.decode()
        csv_io = StringIO(csvres)
        df = pandas.read_csv(csv_io)
        return df
# types works, summary does not.
