import logging
from io import StringIO
from string import Template

import pandas
import sparqldataframe
from rdflib import URIRef, BNode, Literal, Graph,Namespace, RDF
import json

from  ec.graph.sparql_query import queryWithSparql

context = "@prefix : <https://schema.org/> ."

### BLAZEGRAPH
'''original fetch all from temporary namespace'''
def get_summary4repo(endpoint: str) -> pandas.DataFrame:
    df = queryWithSparql("all_summary_query", endpoint)
    return df
    # file = '../resources/sparql/summary_query.txt'
    # with open(file, 'r') as f:
    #     lines = f.read()
    # df = sparqldataframe.query(endpoint,lines)
    # return df

''' fetch all from graph namespace'''
def get_summary4graph(endpoint : str) -> pandas.DataFrame:
    df= queryWithSparql("all_summary_query",endpoint)
    return df
    # file = '../resources/sparql/all_summary_query.sparql'
    # with open(file, 'r') as f:
    #     lines = f.read()
    # df = sparqldataframe.query(endpoint,lines)
    # return df

''' fetch subset  from graph namespace'''
def get_summary4repoSubset(endpoint: str, repo : str) -> pandas.DataFrame:

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
####
def summaryDF2ttl(df: pandas.DataFrame, repo: str) -> tuple[dict, str]:
    "summarize sparql qry (or main quad store)s ret DataFrame, as triples in ttl format w/g as the new subj"
    urns = {}
    def is_str(v):
        return type(v) is str
    g = Graph()
    ## ##########
    # Not officially a standard schema format.
    # we might want to use our own namespace in the future
    ###########
    g.bind("ecsummary", "https://schema.org/")
    ecsummary = Namespace("https://schema.org/")

    #use StringIO() so we don't have to write a file
    # this will go away with RDF Graph generation
    f = StringIO()
    f.write(f'{context}\n')
    for index, row in df.iterrows():
        logging.debug(f'dbg:{row}')
        gu=df["g"][index]
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
        #if no publisher urn.split(':')
        #to use:repo in: ['urn', 'gleaner', 'summoned', 'opentopography', '58048498c7c26c7ab253519efc16df237866e8fe']
        #as of the last runs, this was being done per repo, which comes in on the CLI, so could just use that too*
        if pubname=="No Publisher":
            ul=gu.split(':')
            if len(ul)>4: #could check, for changing urn more, but for now:
                #pub_repo=ul[3]
                pub_repo=ul[4]
                if is_str(pub_repo):
                    pubname=pub_repo
                else: #could just use cli repo
#                        global repo
                    pubname=repo
# date
        datep=row['datep']
        if datep == "No datePublished":
            datep=None
        placename=row['placenames']


        ##############
        # output
        # write to f StringIO()
        # for RDF graph, using sub, verp object
        ###############
        s=row['subj']
        f.write(" \n")
        f.write(f'<{gu}>\n')
# RDF.TYPE
        if rt == "tool":
            f.write(f'        a :SoftwareApplication ;\n')
            g.add((graph_subject,RDF.type, Literal("SoftwareApplication")) )
        else:
            f.write(f'        a :Dataset ;\n')
            g.add((graph_subject, RDF.type, Literal("Dataset")))
# ecsummary.name
        f.write(f'        :name {name} ;\n')
        if (pandas.isnull( row.get('name'))):
            g.add((graph_subject, ecsummary.name, Literal("")))
        else:
            g.add( (graph_subject, ecsummary.name, Literal( row.get('name') ) ) )

# ecsummary.description
        f.write(f'        :description ""{sdes}"" ;\n')
        g.add((graph_subject, ecsummary.description, Literal(description)))

# ecsummary.keywords
        f.write(f'        :keywords {kw} ;\n')
        g.add((graph_subject, ecsummary.keywords, Literal(kw_)))
# ecsummary.publisher
        f.write(f'        :publisher "{pubname}" ;\n')
        g.add((graph_subject, ecsummary.publisher, Literal(pubname)))
# ecsummary.place
        f.write(f'        :place "{placename}" ;\n')
        g.add((graph_subject, ecsummary.place, Literal(placename)))
# ecsummary date
        if datep:
            f.write(f'        :date "{datep}" ;\n') #might be: "No datePublished" ;should change in qry, for dv's lack of checking
            g.add((graph_subject, ecsummary.date, Literal(datep)))
# ecsummary subjectOf
        f.write(f'        :subjectOf <{s}> .\n')
        g.add((graph_subject, ecsummary.subjectOf, URIRef(s)))

# ecsummary.distribution
        du= row.get('url') # check now/not yet
        if is_str(du):
            f.write(f'        :distribution <{du}> .\n')
            g.add((graph_subject, ecsummary.distribution, URIRef(s)))
# spatial

# ecsummary.latitude
        mlat= row.get('maxlat') # check now/not yet
        if is_str(mlat):
            f.write(f'        :latitude {mlat} .\n')
            g.add((graph_subject, ecsummary.latitude, Literal(mlat)))
        mlon= row.get('maxlon') # check now/not yet
        if is_str(mlon):
            f.write(f'        :longitude {mlon} .\n')
            g.add((graph_subject, ecsummary.longitude, Literal(mlon)))

# ecsummary.encodingFormat
        encodingFormat= row.get('encodingFormat') # check now/not yet
        if is_str(encodingFormat):
            f.write(f'        :encodingFormat {encodingFormat} .\n')
            g.add((graph_subject, ecsummary.encodingFormat, Literal(encodingFormat)))
        #see abt defaults from qry or here, think dv needs date as NA or blank/check
        #old:
        #got a bad:         :subjectOf <metadata-doi:10.17882/42182> .
        #incl original subj, just in case for now
        #lat/lon not in present ui, but in earlier version

        #### end for ####
    return f.getvalue() , g
# g is an RDF graph that can be dumped using
# output_string = g.serialize(format='longturtle')
# output_string = g.serialize(format="json-ld")
# or other formats


