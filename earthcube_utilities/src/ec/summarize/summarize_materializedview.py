import logging
from io import StringIO
from string import Template
from typing import Union

import pandas
import sparqldataframe
from rdflib import URIRef, BNode, Literal, Graph,Namespace, RDF
import rdflib
import json

from  ec.graph.sparql_query import queryWithSparql

HTTPS_SCHEMA_ORG = "https://schema.org/"
HTTP_SCHEMA_ORG = "http://schema.org/"
BASE_SHCEMA_ORG = HTTPS_SCHEMA_ORG
context = f"@prefix : <{BASE_SHCEMA_ORG}> ."

### BLAZEGRAPH
'''original fetch all from temporary namespace'''
def get_summary4repo(endpoint: str) -> pandas.DataFrame:
    logging.info("Running Summary Query to Get all records")
    df = queryWithSparql("all_summary_query", endpoint)
    return df
    # file = '../resources/sparql/summary_query.txt'
    # with open(file, 'r') as f:
    #     lines = f.read()
    # df = sparqldataframe.query(endpoint,lines)
    # return df

''' fetch all from graph namespace'''
def get_summary4graph(endpoint : str) -> pandas.DataFrame:
    logging.info("Running Summary Query to Get all records")
    df= queryWithSparql("all_summary_query",endpoint)
    return df
    # file = '../resources/sparql/all_summary_query.sparql'
    # with open(file, 'r') as f:
    #     lines = f.read()
    # df = sparqldataframe.query(endpoint,lines)
    # return df

''' fetch subset  from graph namespace'''
def get_summary4repoSubset(endpoint: str, repo : str) -> pandas.DataFrame:
    logging.info(f"Running Summary Query to Get {repo} records")
    df = queryWithSparql("repo_summary_query",endpoint, parameters={"repo":repo})
    return df
    # file = '../resources/sparql/repo_summary_query.sparql'
    # with open(file, 'r') as f:
    #     lines = f.read()
    # #query = getFileFromResources(f"{template_name}")
    # #q_template = Template(query)
    # q_template = Template(lines)
    # thsGraphQuery = q_template.substitute(repo=repo)
    #
    # df = sparqldataframe.query(endpoint,thsGraphQuery)
    # return df

###
# from dataframe

# need a from release flag for rdflib terms ...
# (rdflib.term.Variable('datep'), None) (rdflib.term.Variable('description'), rdflib.term.Literal('Global stacks of up to a million event-windowed seismograms using short-term to long-term averages (STA/LTA) in different frequency bands for vertical broadband data (1990-2012) available from the IRIS DMC.  Long period versions include vertical and horizontal component data.\r\n')) (rdflib.term.Variable('g'), rdflib.term.URIRef('urn:ec-geocodes:iris:7c61b564beb0be54aca8085c1d0a3b311ffe0cbb')) (rdflib.term.Variable('kw'), rdflib.term.Literal('seismic,seismology,geophysics,globalstacks')) (rdflib.term.Variable('name'), rdflib.term.Literal('Global stacks of millions of seismograms')) (rdflib.term.Variable('placenames'), rdflib.term.Literal('No spatialCoverage')) (rdflib.term.Variable('pubname'), None) (rdflib.term.Variable('resourceType'), rdflib.term.URIRef('https://schema.org/Dataset')) (rdflib.term.Variable('sosType'), rdflib.term.URIRef('https://schema.org/Dataset')) (rdflib.term.Variable...
####

def summaryDF2ttl(df: pandas.DataFrame, repo: str, from_release=False) -> tuple[ Union[str,bytes], Graph]:
    "summarize sparql query returns turtle string and rdf lib Graph"
    urns = {}
    def is_str(v):
        return type(v) is str
    g = Graph()
    ## ##########
    # Not officially a standard schema format.
    # we might want to use our own namespace in the future
    ###########
    g.bind("ecsummary", BASE_SHCEMA_ORG)
    ecsummary = Namespace(BASE_SHCEMA_ORG)
    sosschema = Namespace(BASE_SHCEMA_ORG)

    for index, row in df.iterrows():
        logging.debug(f'dbg:{row}')
        gu=row["g"]

        graph_subject = URIRef(gu)
        #skip the small %of dups, that even new get_summary.txt * has
        if not urns.get(gu):
            urns[gu]=1
        else:
            #print(f'already:{there},so would break loop')
            continue #from loop


        rt_=row.get('resourceType')
        rt=rt_.replace("https://schema.org/","")
        logging.debug(f'rt:{rt}')

        name=json.dumps(row.get('name')) #check for NaN/fix
        if not name:
            name=f'""'
        if not is_str(name):
            name=f'"{name}"'
        if name=="NaN": #this works, but might use NA
            name=f'"{name}"'
# description
        description=row['description']
        if is_str(description):
            sdes=json.dumps(description)
            #sdes=description.replace(' / ',' \/ ').replace('"','\"')
            #sdes=sdes.replace(' / ',' \/ ').replace('"','\"')
          # sdes=sdes.replace('"','\"')
        else:
            sdes=f'"{description}"'
# keywords
        kw_=row['kw']
        if is_str(kw_):
            kw=json.dumps(kw_)
        else:
            kw=f'"{kw_}"'
# publisher
        pubname=row['pubname']
        if   pandas.isna(pubname) or  pubname=="No Publisher":
            pubname = repo
        #if no publisher urn.split(':')
        #to use:repo in: ['urn', 'gleaner', 'summoned', 'opentopography', '58048498c7c26c7ab253519efc16df237866e8fe']
        #as of the last runs, this was being done per repo, which comes in on the CLI, so could just use that too*


# date
        datep=row['datep']
        if datep == "No datePublished":
            datep=pandas.NA
        # Query should not return "No datePublished" is not a valid Date "YYYY-MM-DD" so
        # UI Date Select failed, because it expects an actual date
        #   Empty values might be handled in the UI...,
        #   or the repository valiation reporting


        placename=row['placenames']


        ##############
        # output
        # write to f StringIO()
        # for RDF graph, using sub, verp object
        ###############
        s=row['subj']
# RDF.TYPE

#         if rt == "tool":
#             g.add((graph_subject,RDF.type, sosschema.SoftwareApplication) )
#         else:
#             g.add((graph_subject, RDF.type, sosschema.Dataset))

        # original aummary query wrote out strings, then converted back to schema uri... just skip that step
        # RDF.TYPE
        rt = row['sosType']
        g.add((graph_subject, RDF.type, URIRef(rt)))

# ecsummary.name
        if (pandas.isnull( row.get('name'))):
            g.add((graph_subject, ecsummary.name, Literal("")))
        else:
            g.add( (graph_subject, ecsummary.name, Literal( row.get('name') ) ) )

# ecsummary.description
        g.add((graph_subject, ecsummary.description, Literal(description)))

# ecsummary.keywords
        g.add((graph_subject, ecsummary.keywords, Literal(kw_)))
# ecsummary.publisher
        if pandas.notna(pubname):
            g.add((graph_subject, ecsummary.publisher, Literal(pubname)))
# ecsummary.place
        g.add((graph_subject, ecsummary.place, Literal(placename)))
# ecsummary date
        if pandas.notna(datep):
            #might be: "No datePublished" ;should change in qry, for dv's lack of checking
            # Query should not return "No datePublished" is not a valid Date "YYYY-MM-DD" so
            # UI Date Select failed, because it expects an actual date
            #   Empty values might be handled in the UI...,
            #   or the repository valiation reporting
            g.add((graph_subject, ecsummary.date, Literal(datep)))
# ecsummary subjectOf
        g.add((graph_subject, ecsummary.subjectOf, URIRef(s)))

# ecsummary.distribution
        du= row.get('url') # check now/not yet
        if is_str(du):
            g.add((graph_subject, ecsummary.distribution, URIRef(s)))
# spatial

# ecsummary.latitude
        mlat= row.get('maxlat') # check now/not yet
        if is_str(mlat):
            g.add((graph_subject, ecsummary.latitude, Literal(mlat)))
        mlon= row.get('maxlon') # check now/not yet
        if is_str(mlon):
            g.add((graph_subject, ecsummary.longitude, Literal(mlon)))

# ecsummary.encodingFormat
        encodingFormat= row.get('encodingFormat') # check now/not yet
        if is_str(encodingFormat):
            g.add((graph_subject, ecsummary.encodingFormat, Literal(encodingFormat)))
        #see abt defaults from qry or here, think dv needs date as NA or blank/check
        #old:
        #got a bad:         :subjectOf <metadata-doi:10.17882/42182> .
        #incl original subj, just in case for now
        #lat/lon not in present ui, but in earlier version

        #### end for ####
    return g.serialize(format='longturtle'), g
# g is an RDF graph that can be dumped using
# output_string = g.serialize(format='longturtle')
# output_string = g.serialize(format="json-ld")
# or other formats


