#!/usr/bin/env python3
#mbobak summarize a nq file, for quick queries, and quad now as subj to point to graph-url
 #this is almost like nq2ttl, but is sumarizing via the qry
import pandas as pd
import os
import sys
import argparse
context = "@prefix : <https://schema.org/> ." #https for now
#qry.py does get_summary_txt for get_summary.txt from raw git link, but same as qry below
#=port setup for fuseki, but might now also do 1st one shot from blaze on 9999; for 1st shot off main namespace
 #dv wants to skip local throw away fuseki in memory instance, and create namespace on blaze endpoint summarize
  #from it, then delete it, then upload back to the final summary namespace

#get_summary4repo still uses port for fuseki, will (be)switching to blaze soon
port=3030 #do not this this is used anymore, so should rm
#ftsp=os.getenv('fuseki_tmp_summary_port')
ftsp=os.getenv('tmp_summary_port') #if 9999 will use blaze
if ftsp:
    print(f'changing port from {port} to {ftsp}')
    port=ftsp

qry="""
prefix schema: <https://schema.org/>
SELECT distinct ?subj ?g ?resourceType ?name ?description  ?pubname
        (GROUP_CONCAT(DISTINCT ?placename; SEPARATOR=", ") AS ?placenames)
        (GROUP_CONCAT(DISTINCT ?kwu; SEPARATOR=", ") AS ?kw) ?datep
        #(GROUP_CONCAT(DISTINCT ?url; SEPARATOR=", ") AS ?disurl)
        WHERE {
          graph ?g {
             ?subj schema:name ?name .
             ?subj schema:description ?description .
            Minus {?subj a schema:ResearchProject } .
            Minus {?subj a schema:Person } .
 #BIND (IF (exists {?subj a schema:Dataset .} ||exists{?subj a schema:DataCatalog .} , "data", "tool") AS ?resourceType).
                   ?subj a ?resourceType .
            optional {?subj schema:distribution/schema:url|schema:subjectOf/schema:url ?url .}
            OPTIONAL {?subj schema:datePublished ?date_p .}
            OPTIONAL {?subj schema:publisher/schema:name|schema:sdPublisher|schema:provider/schema:name ?pub_name .}
            OPTIONAL {?subj schema:spatialCoverage/schema:name ?place_name .}
            OPTIONAL {?subj schema:keywords ?kwu .}
            BIND ( IF ( BOUND(?date_p), ?date_p, "No datePublished") as ?datep ) .
            BIND ( IF ( BOUND(?pub_name), ?pub_name, "No Publisher") as ?pubname ) .
            BIND ( IF ( BOUND(?place_name), ?place_name, "No spatialCoverage") as ?placename ) .
             }
        }
        GROUP BY ?subj ?pubname ?placenames ?kw ?datep   ?name ?description  ?resourceType ?g
        """
        #using more constrained qry now in get_summary.txt * now above
#import earthcube_utilities as ec #check that it has been updated for newer work/later
import qry as ec #check that it has been updated for newer work/later
    #make sure I can send the qry into the new qry.py ec.py subset's fncs, skipping it's usual lookup
    #ec.get_summary(qry) vs "" as it is now
    #def get_summary(g=""): #g not used but could make a version that gets it for only 1 graph
    #vs changing this could dump qry's txt to: get_summary.txt which qry.py will load; 
    # but would have to do at the right time, so time, to make the qry fncs more general
    # or more like the ui, to get the above qry in github, and have the ec/qry utils use that*
    # https://raw.githubusercontent.com/earthcube/ec/master/summary/get_summary.txt

#import ../earthcube_utilities as ec  #assuming it is one level above #now just get qry.py part of ec.py
#from utils:
#dflt_endpoint = "https://graph.geocodes.ncsa.illinois.edu/blazegraph/namespace/earthcube/sparql" #and summary
#ec.dflt_endpoint = tmp_endpoint
#df=ec.get_summary("")

#all are tabbed after context
#a                       :Dataset ;
# then :so-keyword ;   last w/.
#column names:
# "subj" , "g" , "resourceType" , "name" , "description" , "pubname" , "placenames" , "kw" , "datep" ,
#next time just get a mapping file/have qry w/so keywords as much a possilbe
##in dc/summarize.py have a version that would do this all from repo.nq &be done w/it
## if we didn't need to do some much checking below, could do w/sparql only
#dbg=True
dbg=False

cwd=os.getcwd()
cwd_leaf = ec.path_leaf(cwd)
#instead of conversion by file-query or tmp-server right here, dv wants to use the main endpoint
#so that will include creating and destroying namespaces there, which can be done w/libs, like:
#should probably do this in pkg, wish not so distant/might lnk for now
sys.path.append("..")
sys.path.append("../..")
#above not needed, but below needed in case run from src or .. w/ summarize_repo.sh
if cwd_leaf == "src":
    sys.path.append("../../earthcube_utilities/src/ec/graph")
if cwd_leaf == "summarize":
    sys.path.append("../earthcube_utilities/src/ec/graph")
import manageGraph
#----from when I thought I might do it from w/in that class
#will instantiange a graph/namespace instance in summarize code to do the logic below
    # an instance of this is made,
    #don't have to anymore assume: w/the namespace=repo as one of it's instatiation args
#   def call_summarize(self):
#       print(f'call tsum on:{self.namespace}')

#   def summarize(self, ns="summary"):
#       self.createNamespace()
#       self.upload_nq_file()
#       self.call_summarize() #creates repo.ttl
#       self.deleteNamespace()
#       self.upload_ttl_file(ns)  #uploads it
#----
#instead of calling summaryDF2ttl and having it make the the instance, follow above method
 #and where it says call_summarize, that would be the summaryDF2ttl call
  #or that would be   '' = get_summary4repo    +       ''
#==have methods above as a few funcs below/near __main__

def summaryDF2ttl(df):
    "summarize sparql qry (or main quad store)s ret DataFrame, as triples in ttl format w/g as the new subj"
    urns = {}
    import json

    def is_str(v): #i don't need this to be private, bc it is a generic util
        return type(v) is str

    with open(f'{repo}.ttl', "w") as f:

        f.write(f'{context}\n')
        for index, row in df.iterrows():
            if dbg:
                print(f'dbg:{row}')
            gu=df["g"][index]
            #skip the small %of dups, that even new get_summary.txt * has
            there = urns.get(gu)
            if not there:
                urns[gu]=1
            elif there:
                #print(f'already:{there},so would break loop')
                continue #from loop
            #rt=row['resourceType']
            rt_=row['resourceType']
            rt=rt_.replace("https://schema.org/","")
            if dbg:
                print(f'rt:{rt}')
            name=json.dumps(row['name']) #check for NaN/fix
            if not name:
                name=f'""'
            if not is_str(name):
                name=f'"{name}"'
            if name=="NaN": #this works, but might use NA
                name=f'"{name}"'
            description=row['description']
            if is_str(description):
                sdes=json.dumps(description)
            else:
                sdes=f'"{description}"'
            kw_=row['kw']
            if is_str(kw_):
                kw=json.dumps(kw_)
            else:
                kw=f'"{kw_}"'
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
            datep=row['datep']
            if datep == "No datePublished":
                datep=None
            placename=row['placenames']
            s=row['subj']
            f.write(" \n")
            f.write(f'<{gu}>\n')
            #print(f'        a {rt} ;')
            if rt == "tool":
                f.write(f'        a :SoftwareApplication ;\n')
            else:
                f.write(f'        a :Dataset ;\n')
            f.write(f'        :name {name} ;\n')
            f.write(f'        :description ""{sdes}"" ;\n')
            f.write(f'        :keywords {kw} ;\n')
            f.write(f'        :publisher "{pubname}" ;\n')
            f.write(f'        :place "{placename}" ;\n')
            if datep:
                f.write(f'        :date "{datep}" ;\n') #might be: "No datePublished" ;should change in qry, for dv's lack of checking
            f.write(f'        :subjectOf <{s}> .\n')
            #du= row.get("disurl") #not seeing yet
            du= row.get('url') # check now/not yet
            if is_str(du):
                f.write(f'        :distribution <{du}> .\n')
            mlat= row.get('maxlat') # check now/not yet
            if is_str(mlat):
                f.write(f'        :latitude {mlat} .\n')
            mlon= row.get('maxlon') # check now/not yet
            if is_str(mlon):
                f.write(f'        :longitude {mlon} .\n')
            encodingFormat= row.get('encodingFormat') # check now/not yet
            if is_str(encodingFormat):
                f.write(f'        :encodingFormat {encodingFormat} .\n')
        #see abt defaults from qry or here, think dv needs date as NA or blank/check
        #old:
        #got a bad:         :subjectOf <metadata-doi:10.17882/42182> .
        #incl original subj, just in case for now
        #lat/lon not in present ui, but in earlier version

def get_summary4repo(repo):
    "so can call interactively to look at the df"
    #tmp_endpoint=f'http://localhost:3030/{repo}/sparql' #fnq repo
    tmp_endpoint=f'http://localhost:{port}/{repo}/sparql' #fnq repo
    print(f'try:{tmp_endpoint}') #if >repo.ttl, till prints, will have to rm this line &next2:
    ec.dflt_endpoint = tmp_endpoint
    df=ec.get_summary("")
    return df

def get_summary_from_namespace(args):
    "so can call interactively to look at the df"
    #if not run on local(for now:ncsa)machine: 
    host=os.getenv('HOST') #checking against new store, for now
    print(f'host={host}')
    #tmp_endpoint=f'https://graph.geocodes.ncsa.illinois.edu/blazegraph/namespace/{namespace}/sparql'
    tmp_endpoint=args.endpoint
    #if host != "geocodes.ncsa.illinois.edu":
    #    print("using external call") #but could do this locally as well
    #    tmp_endpoint=f'https://graph.geocodes.ncsa.illinois.edu/{namespace}/sparql'
    #else: #even internally can have connection problems
    #    tmp_endpoint=f'http://localhost:9999/{namespace}/sparql' 
    print(f'try:{tmp_endpoint}') 
    ec.dflt_endpoint = tmp_endpoint
    df=ec.get_summary("")
    return df

def make_graph(ns, url="https://graph.geodex.org/blazegraph"): 
    mg=manageGraph.ManageBlazegraph(url, ns) #put tmp namespaces here, for now
    print(f'have graph instance:{mg}')
    return mg

def make_graph_ns(ns):
    mg= make_graph(ns)
    mg.createNamespace()
    print(f'with namespace:{ns}')
    return mg

# what I thought might be managegraph methods, now as functions here:
#   def call_summarize(self):
#       print(f'call tsum on:{self.namespace}')
def call_summarize(repo):
    print("per repo={repo} through blaze-namespace")
    df=get_summary4repo(repo)
    summaryDF2ttl(df)

#   def summarize(self, ns="summary"):
#       self.createNamespace()
#       self.upload_nq_file()
#       self.call_summarize() #creates repo.ttl
#       self.deleteNamespace()
#       self.upload_ttl_file(ns)  #uploads it
#def summarize(repo, final_ns="summary"):
def summarize_repo(repo, final_ns="summary"):
    tmp_ns="test"
    if repo:
        tmp_ns=repo
        print(f'ns=repo={repo}')

    #mg=manageGraph.ManageBlazegraph("https://graph.geodex.org/blazegraph", tmp_ns) #put tmp namespaces here, for now
    #print(f'have graph instance:{mg}')
    #mg.createNamespace()
    mg= make_graph_ns(tmp_ns)

#  #self.upload_nq_file() #is this done by glcon nabu? probably for the big_namespace
    mg.upload_nq_file() #will need to get repo.nq up so can be summarized in next step
    call_summarize(repo) #creates repo.ttl
    #could check to see file is there/ok
    mg.deleteNamespace()
    mg.upload_ttl_file()  #uploads it
    print(f'will upload {repo}.ttl from here')

if __name__ == '__main__':
    import sys

    parser = argparse.ArgumentParser()

    parser.add_argument("repo",  help='repository name')
    parser.add_argument('--endpoint', dest='endpoint',
                        help='use blazegraph endpoint, fully defined, as data source; eg https://graph.geocodes.ncsa.illinois.edu/blazegraph/namespace/{repo}/sparql')
    if(len(sys.argv)==1):
        print("you need to enter the name of a repo to summarize")
    else:
        args = parser.parse_args() #would fail here, if no arg w/o printing help
        if(len(sys.argv)>1):
            repo = args.repo
            # repo = sys.argv[1]
            #tmp_endpoint=f'http://localhost:3030/{repo}/sparql' #fnq repo
            #print(f'try:{tmp_endpoint}') #if >repo.ttl, till prints, will have to rm this line &next2:
            #ec.dflt_endpoint = tmp_endpoint
            #df=ec.get_summary("")
            print(f'port={port},arg1={repo}')
       #    if  args.endpoint : #when: os.getenv('tmp_summary_port') #if 9999 will use blaze
       #        print("bulk 1st load from blaze")
       #        df=get_summary_from_namespace( args)
       #    else:
       #        #print("per repo through fuseki")
       #        print("per repo through blaze-namespace")
       #        df=get_summary4repo(repo)
       #    summaryDF2ttl(df)
       #for now skip 1st shot summarization of all repo's from main blaze namespace, eg. earthcube
       #and just:
            summarize_repo(repo) #get potential final upload ns in later; 
            #though I'd rather be able to check file before it gets loaded to final summary namespace
        else:
            #print("need to give repo to run, or if:tmp_summary_port=9999 a namespace for initial bulk load")
            parser.print_help()
