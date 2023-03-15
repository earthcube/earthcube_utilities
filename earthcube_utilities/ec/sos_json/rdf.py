import pandas
from rdflib import URIRef, BNode, Literal, Graph, Dataset

import graph

# this context will need to be expanded.
from sos_json.sos import compact_jld_str, formatted_jsonld

jsonld_context = context = { "@vocab": "https://schema.org/"}

def is_http(u):
    if not isinstance(u, str) :
        print("might need to set LD_cache") #have this where predicate called
        return None
    #might also check that the str has no spaces in it,&warn/die if it does
    return u.startswith("http")

def createRDFNode(nodeValue):
    "fix_url and quote otherwise"
    if not isinstance(nodeValue,str):
        if  (nodeValue is None) or  (pandas.isnull(nodeValue)):
            return Literal("")
        return Literal(nodeValue)
    else:
        if nodeValue.startswith("<ht"):
            return URIRef(nodeValue)
        elif nodeValue.startswith("_:B"):
            return BNode(nodeValue.replace("_:B", "B"))
        elif nodeValue.startswith("t1"):
            return BNode(nodeValue.replace("t1", "Bt1"))
        elif is_http(nodeValue):
            return URIRef(nodeValue)
        elif nodeValue.startswith("doi:"):
            return URIRef(nodeValue)
        elif nodeValue.startswith("DOI:"):
            return URIRef(nodeValue)
        #elif obj:
        elif nodeValue is None:
            return Literal("")
        elif pandas.isnull(nodeValue):
            return Literal("")
        else:
            # import json
            # return json.dumps(url)
           return Literal(nodeValue)
    #else:
    #    return url

def df2rdfgraph(df):
    "print out df as .nt file"

    g = Graph()
    g.bind("schema", "https://schema.org/")
    for index, row in df.iterrows():
        s=df["s"][index]
        s=createRDFNode(s)
        p=df["p"][index]
        p=createRDFNode(p)
        o=df["o"][index]
        o=createRDFNode(o)
        g.add((s, p, o))

        #need to finish up w/dumping to a file
    return  g


def get_rdfgraph(urn, endpoint ): #get graph
    df=graph.sparqlquery.getAGraph(urn, endpoint)
    g=df2rdfgraph(df)
    return g


def load_release(releaseurl):
    g= Dataset()
    g.parse(releaseurl, format='nquads')
    return g
#  using https://github.com/cadmiumkitty/rdfpandas
    #g = Graph()
#    g.parse(releaseurl, format='nt')
#    df = to_dataframe(g)


# returns a framd JSON
# form= framed|compact
def get_rdf2jld(urn, endpoint, form="jsonld", schemaType="Dataset"):
    "get jsonld from endpoint"
    g = get_rdfgraph(urn, endpoint)
    # auto_compact=False might change
    jld_str = g.serialize(format="json-ld")

    return formatted_jsonld(jld_str)


def get_rdf2jld_str(urn, endpoint):
    "get jsonld from endpoint"
    g= get_rdfgraph(urn, endpoint)
    jld_str = g.serialize(format="json-ld")
    return compact_jld_str(jld_str)