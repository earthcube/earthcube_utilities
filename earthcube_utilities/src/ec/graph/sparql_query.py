"""
This basically wraps sparqldataframe,
and contains a way to get resources that are the sparql queries,
and few helpers to basic queries
"""
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

def queryWithSparql( template_name, endpoint,parameters={}):
    query = getFileFromResources(f"{template_name}")
    q_template = Template(query)
    thsGraphQuery = q_template.substitute(parameters)
    q_df = sparqldataframe.query(endpoint, thsGraphQuery)
    return q_df

## this will need to be done to package specifications.
# https://stackoverflow.com/questions/6028000/how-to-read-a-static-file-from-inside-a-python-package
def getFileFromResources(filename):
    resourcename = f"{filename}.sparql"
    resource = pkg_resources.read_text(sparqlfiles, resourcename)
    return resource
    # with open(f"./resources/{filename}", "r") as stream:
    #     try:
    #         return stream.read()
    #     except Exception as exc:
    #         print(exc)

def getAGraph(  g, endpoint):
    query = getFileFromResources('get_triples_for_a_graph')
    q_template = Template(query)
    thsGraphQuery = q_template.substitute(g=g)
    g_df = sparqldataframe.query(endpoint, thsGraphQuery)

    return g_df