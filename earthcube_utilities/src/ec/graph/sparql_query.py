"""
This basically wraps sparqldataframe,
and contains a way to get resources that are the sparql queries,
and few helpers to basic queries
"""
import pandas
from  pydash import  ends_with, replace_end, sort
import sparqldataframe
from string import Template
try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

import ec.graph.sparql_files as sparqlfiles

"""
QUery with a spaql query

parameters are an object so to pass in a reponame:
{"repo": self.repo}

or to pass in a graph
{"g": self.repo}
"""

def queryWithSparql( template_name : str, endpoint : str,parameters:object={}) -> pandas.DataFrame:
    """ Query a SPARQL endpoint, and return a Pandas Dataframe

    Parameters:
       template_name: name of templates in the ec.graph.sparql_files directory
       endpoint: SPARQL endpoint url
       parameters: object with the names to fill in template eg {"repo": "reponame"}
    """
    query = _getSparqlFileFromResources(f"{template_name}")
    q_template = Template(query)
    thsGraphQuery = q_template.substitute(parameters)
    q_df = sparqldataframe.query(endpoint, thsGraphQuery)
    return q_df

## this will need to be done to package specifications.
# https://stackoverflow.com/questions/6028000/how-to-read-a-static-file-from-inside-a-python-package
def _getSparqlFileFromResources(filename) -> str:
    """ retrieves sparql file from the sparql_files folder when in a package"""
    resourcename = f"{filename}.sparql"
    resource = pkg_resources.read_text(sparqlfiles, resourcename)
    return resource
    # with open(f"./resources/{filename}", "r") as stream:
    #     try:
    #         return stream.read()
    #     except Exception as exc:
    #         print(exc)
def listSparqlFilesFromResources() -> str:
    """ retrieves sparql file from the sparql_files folder when in a package"""
    resource = pkg_resources.contents(sparqlfiles)
    files = filter( lambda f: ends_with(f, ".sparql"), resource)
    files = map(lambda f: replace_end(f,".sparql",""), files)
    files = sort(list(files))
    return files

def getAGraph(  g, endpoint: str) -> pandas.DataFrame:
    """Query a SPARQL endpoint and return a Pandas Dataframe for a geocodes object"""
    query = _getSparqlFileFromResources('get_triples_for_a_graph')
    q_template = Template(query)
    thsGraphQuery = q_template.substitute(g=g)
    g_df = sparqldataframe.query(endpoint, thsGraphQuery)

    return g_df