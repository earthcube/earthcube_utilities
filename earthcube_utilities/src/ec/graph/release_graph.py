import csv
from io import StringIO
from string import Template

import pandas
from rdflib import Namespace, Dataset,Graph, ConjunctiveGraph
from rdflib.namespace import RDF

from  ec.graph.sparql_query import _getSparqlFileFromResources
from ec.datastore.s3 import MinioDatastore


# notes... we can group concat where a field is possibly none. we have to use a bind.
# from placenames and keywords

SCHEMAORG_http = Namespace("http://schema.org/")
SCHEMAORG_https = Namespace("https://schema.org/")
class ReleaseGraph:
   # dataset = Dataset(default_union=True,store="Oxigraph")
    dataset = Dataset(default_union=True)
    dataset.bind('schema_http',SCHEMAORG_http)
    dataset.bind('schema', SCHEMAORG_https)
    #dataset = ConjunctiveGraph()
    filename = ""

    def load_release(self, file_or_url, format='nquads' ):
        self.dataset.parse(file_or_url, format=format)
    def read_release(self, s3server, s3bucket, source, date="latest", options={}):
        s3 = MinioDatastore(s3server, options)
        url = s3.getLatestRelaseUrl(s3bucket, source)
        self.filename = url[ url.rfind('/') +1 :]
        self.load_release(url)

    def summarize(self):
        print("SUMMARIZE from RELEASE not reliable. produces different results than blazegrapn (no min/max depth")
        # get the summary sparql query, run it sparql data frome to put it in a dataframe
        #might just feed the result rows to pandas
        # all_summary_query returns no rows ;)
       # resource = ec.graph.sparql_query._getSparqlFileFromResources("all_summary_query")
       # resource = ec.graph.sparql_query._getSparqlFileFromResources("all_repo_count_datasets")
        # result = self.dataset.query(resource)

        #result = self.dataset.query(test_types, initNs={'schema_o': SCHEMAORG_http, 'schema':SCHEMAORG_https })
        query = _getSparqlFileFromResources('all_summary_query')
       # result = self.dataset.query(summary_sparql, result='sparql', initNs={'schema_old': SCHEMAORG_http, 'schema': SCHEMAORG_https})
        result = self.dataset.query(query, result='sparql')

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
