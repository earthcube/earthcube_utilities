#from ec.py just enough to run some of the basic sparql queries, using sparqldataframe in the end ;M Bobak
#from utils:
import os
dflt_endpoint = "https://graph.geocodes.ncsa.illinois.edu/blazegraph/namespace/earthcube/sparql" #and summary
import mb

##get_  _txt   fncs:
# are composed from the middle/variable word, and called in: v4qry
#def get_relateddatafilename_txt(url="https://raw.githubusercontent.com/earthcube/facetsearch/toolMatchNotebookQuery/client/src/sparql_blaze/sparql_relateddatafilename.txt"):
def get_relateddatafilename_txt(url="https://raw.githubusercontent.com/MBcode/ec/master/NoteBook/sparql_relateddatafilename.txt"):
    return get_ec_txt(url)  #need var to be {?q} so dont have to write extra logic below

def get_webservice_txt(url="https://raw.githubusercontent.com/earthcube/facetsearch/master/client/src/sparql_blaze/sparql_gettools_webservice.txt"):
    return get_ec_txt(url)

def get_download_txt(url="https://raw.githubusercontent.com/earthcube/facetsearch/master/client/src/sparql_blaze/sparql_gettools_download.txt"):
    return get_ec_txt(url)

def get_notebook_txt(url="https://raw.githubusercontent.com/MBcode/ec/master/NoteBook/sparql_gettools_notebook.txt"):
    return get_ec_txt(url)

#in feat_summary:
#def get_query_txt(url="https://raw.githubusercontent.com/earthcube/facetsearch/master/client/src/sparql_blaze/sparql_query.txt"):
def get_query_txt(url="https://raw.githubusercontent.com/MBcode/ec/master/NoteBook/sparql-query.txt"):
    return get_ec_txt(url)

#def get_summary_query_txt(url="https://raw.githubusercontent.com/earthcube/facetsearch/master/client/src/sparql_blaze/sparql_query.txt"): #had limit at end
def get_summary_query_txt(url="http://mbobak.ncsa.illinois.edu/ec/nb/sparql_blaze.txt"):
    #return get_ec_txt(url)  #start to use this in the sparql-nb txt_query
    return """PREFIX bds: <http://www.bigdata.com/rdf/search#>
 PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
 PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
 prefix schema: <https://schema.org/>
 SELECT distinct ?g ?pubname ?placenames ?kw  ?datep
        (MAX(?score1) as ?score)  ?name ?description ?resourceType
          WHERE {
            ?lit bds:search "${q}" .
            ?lit bds:matchAllTerms false .
            ?lit bds:relevance ?score1 .
            ?lit bds:minRelevance 0.14 .
            ?g ?p ?lit .
        ?g schema:name ?name .
        ?g schema:description ?description .
 BIND (IF (exists {?g a schema:Dataset .}  , "data", "tool") AS ?resourceType).
 OPTIONAL {?g schema:date ?datep .}
 OPTIONAL {?g schema:publisher ?pubname .}
 OPTIONAL {?g schema:place ?placenames .}
 OPTIONAL {?g schema:keywords ?kw .} }
 GROUP BY ?g ?pubname ?placenames ?kw ?datep ?disurl ?score ?name ?description  ?resourceType
         ORDER BY DESC(?score)"""

#replace this and other on server w/raw git url, before they are used here
def get_subj2urn_txt(url="http://mbobak.ncsa.illinois.edu/ec/nb/sparql_subj2urn.txt"):
    #return get_ec_txt(url)
    return """prefix sschema: <https://schema.org/>
            SELECT distinct    ?g WHERE {
            graph ?g { <${g}> a schema:Dataset }}"""

def get_graphs_txt(url="http://mbobak.ncsa.illinois.edu/ec/nb/sparql_graphs.txt"):
    #return get_ec_txt(url)
    return "SELECT distinct ?g  WHERE {GRAPH ?g {?s ?p ?o}}"

def get_graph_txt(url="http://mbobak.ncsa.illinois.edu/ec/nb/get_graph.txt"):
    #return get_ec_txt(url)
    #return "SELECT distinct ?s ?p ?o  WHERE { graph ?g {?s ?p ?o} filter(?g = <${g}>)}"
    return "SELECT distinct ?s ?p ?o  WHERE { graph ?g {?s ?p ?o} filter(?g = <${q}>)}" #there will be a better way
    #return "describe <${q}>)}" #similar but can't do this    #also want where can ask for format as jsonld for ui
    #consider ret CONSTRUCT from a direct match vs filter
    #I'm ok w/filter given the changing URNs taking a subset should still return something

#def get_summary_txt(url="http://mbobak.ncsa.illinois.edu/ec/nb/get_summary.txt"):
def get_summary_txt(url="https://raw.githubusercontent.com/earthcube/ec/master/summary/get_summary.txt"):
    "this is to make a summary, not to do a qry on the summary"
    return get_ec_txt(url)

#----
def qs2graph(q,sqs):
    return sqs.replace('${q}',q)
def urn2graph(urn,sqs):
    #return sqs.replace('<${g}>',urn)
    return sqs.replace('<${g}>',f'"{urn}"')
#def sti(sqs, matchVar, replaceValue): #assume only1(replacement)right now,in the SPARQL-Qry(file)String(txt)
#    "sparql template instantiation, 2qry2df"
#    return sqs.replace(matchVar,replaceValue)
def v2iqt(var,sqs):  #does the above fncs
    if '<${g}>' in sqs: #var=urn
        #return sqs.replace('<${g}>',var)
        #return sqs.replace('<${g}>',f'"{var}"')
        return sqs.replace('<${g}>',f'<{var}>')
    if '${q}' in sqs:   #var=q
        return sqs.replace('${q}',var)
    else:
        return sqs #when nothing to replace, like in get_graphs
    #could add relatedData case, but changed to 'q' for now
    #really if only 1 var, could always just change it
    #_someday could send in dict to replace if >1

#def iqt2df(iqt,endpoint="https://graph.geodex.org/blazegraph/namespace/nabu/sparql"):
#def iqt2df(iqt,endpoint="https://graph.geocodes.earthcube.org/blazegraph/namespace/earthcube/sparql"):
#def iqt2df(iqt,endpoint=dflt_endpoint):
def iqt2df(iqt,endpoint=None):
    "instantiated-query-template/txt to df"
    if not iqt:
        return "need isntantiated query text"
    import sparqldataframe, simplejson
 #  if sparql_inited==None:
 #      si= init_sparql()  #still need to init
 #      #qs= iqt #or si  #need q to instantiate
    #add2log(iqt)
    global dflt_endpoint
    if not endpoint:
        endpoint=dflt_endpoint
 #  add2log(f'query:{iqt}')
 #  add2log(f'endpoint:{endpoint}')
    df = sparqldataframe.query(endpoint, iqt)
    return df

def v4qry(var,qt):
    "var + query-type 2 df"
    if not var:
        var=""
    sqs = eval("get_" + qt + "_txt()") #get_  _txt   fncs, are above
    if not mb.is_str(sqs):
        print('f4qry get_ {qt} _txt() gave; {sqs}, so aborting')
        return ""
    iqt = v2iqt(var,sqs)
    #add2log(iqt) #logged in next fnc
    adf = iqt2df(iqt)
    return adf

def search_query(q): #same as txt_query below
    return v4qry(q,"query")

#functionality that is see on dataset page:

def search_relateddatafilename(q):
    return v4qry(q,"relateddatafilename")

def search_download(urn):
    return v4qry(urn,"download")

def search_webservice(urn):
    return v4qry(urn,"webservice")

def search_notebook(urn):
    return v4qry(urn,"notebook")

#
def subj2urn(doi):
    "<<doi a so:Dataset>>'s graph"
    return v4qry(doi,"subj2urn")

def get_graphs():
    "return all the g URNs"
    return v4qry("","graphs")

def get_graph(g):
    "return all triples from g w/URN"
    return v4qry(g,"graph")

def get_summary(g=""): #g not used but could make a version that gets it for only 1 graph
    "return summary version of all the graphs quads"
    return v4qry(g,"summary")

#def get_summary_query(g=""): #g not used but could make a version that gets it for only 1 graph
#search_query above, should now use this
def summary_query(g=""): #this is finally used in: txt_query_summary
    "replacement txt_query of new summary namespace" #or summary2/etc check
    return v4qry(g,"summary_query") #could call this the fast_query



#summary_endpoint = dflt_endpoint.replace("earthcube","summary")
 #for now, but will have to check, at times
 #no 2nd change, all vars should be the same from the summary
