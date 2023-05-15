import pandas
from rdflib import Dataset,Graph
from rdflib.namespace import RDF

import ec.graph.sparql_query
from ec.datastore.s3 import MinioDatastore


class ReleaseGraph:
    dataset = Dataset()
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
        resource = ec.graph.sparql_query._getSparqlFileFromResources("all_repo_count_datasets")
        result = self.dataset.query(resource)
        df = pandas.DataFrame(result)
        return df

