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
import logging as log  #have some dgb prints, that will go to logs soon/but I find it slow to have to cat the small logs everytime
log.basicConfig(filename='tsum.log', encoding='utf-8', level=log.DEBUG,
                format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

#get_summary4repo still uses port for fuseki, will (be)switching to blaze soon
#port=3030 #do not this this is used anymore, so should rm
port=9999 #but all our blaze urls use trafik so don't need the port, unless local
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
    #make sure I can send the qry into the new qry.py ec.py subset's fncs, skipping it's usual lookup
    #ec.get_summary(qry) vs "" as it is now
    #def get_summary(g=""): #g not used but could make a version that gets it for only 1 graph
    #vs changing this could dump qry's txt to: get_summary.txt which qry.py will load; 
    # but would have to do at the right time, so time, to make the qry fncs more general
    # or more like the ui, to get the above qry in github, and have the ec/qry utils use that*
    # https://raw.githubusercontent.com/earthcube/ec/master/summary/get_summary.txt
#import earthcube_utilities as ec #check that it has been updated for newer work/later
#import ../earthcube_utilities as ec  #assuming it is one level above #now just get qry.py part of ec.py
#from utils:
#dflt_endpoint = "https://graph.geocodes.ncsa.illinois.edu/blazegraph/namespace/earthcube/sparql" #and summary
#ec.dflt_endpoint = tmp_endpoint
#df=ec.get_summary("")
import qry as ec #check that it has been updated for newer work/later

#dbg=True
dbg=False

cwd=os.getcwd()
cwd_leaf = ec.path_leaf(cwd)
#instead of conversion by file-query or tmp-server right here, dv wants to use the main endpoint
#so that will include creating and destroying namespaces there, which can be done w/libs, like:
#should probably do this in pkg, wish not so distant/might lnk for now
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

#=output will be in format
#all are tabbed after context
#a                       :Dataset ;
# then :so-keyword ;   last w/.
#column names:
# "subj" , "g" , "resourceType" , "name" , "description" , "pubname" , "placenames" , "kw" , "datep" ,
#next time just get a mapping file/have qry w/so keywords as much a possilbe
##in dc/summarize.py have a version that would do this all from repo.nq &be done w/it
## if we didn't need to do some much checking below, could do w/sparql only
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
                log.debug(f'dbg:{row}')
            gu=df["g"][index]
            #skip the small %of dups, that even new get_summary.txt * has
            there = urns.get(gu)
            if not there:
                urns[gu]=1
            elif there:
                #log.debug(f'already:{there},so would break loop')
                continue #from loop
            #rt=row['resourceType']
            rt_=row['resourceType']
            rt=rt_.replace("https://schema.org/","")
            if dbg:
                log.debug(f'rt:{rt}')
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
            #log.debug(f'        a {rt} ;')
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

endpoint='https://graph.geocodes.ncsa.illinois.edu/blazegraph/namespace' 

def get_summary4repo(repo):
    "so can call interactively to look at the df"
    ##tmp_endpoint=f'http://localhost:3030/{repo}/sparql' #fnq repo
    #tmp_endpoint=f'http://localhost:{port}/{repo}/sparql' #fnq repo #fuseki
    #repo="iris_nabu" #just for 1st test
    #tmp_endpoint=f'https://graph.geocodes.ncsa.illinois.edu/blazegraph/namespace/{repo}/sparql' #1st blaze call  *
    tmp_endpoint=f'{endpoint}/{repo}/sparql' #1st blaze call  *
    log.info(f'get_summary4repo try:{tmp_endpoint}') #if >repo.ttl, till prints, will have to rm this line &next2:
    log.info(f'try:{tmp_endpoint}') #if >repo.ttl, till prints, will have to rm this line &next2:
    #try:https://graph.geocodes.ncsa.illinois.edu/blazegraph/namespace/iris_nabu/sparql
    #seems to work, now make in /iris/ but have to get the iris.nq up there 1st to run the qry
    ec.dflt_endpoint = tmp_endpoint
    df=ec.get_summary("")
    return df

def get_summary_from_namespace(args):
    "so can call interactively to look at the df"
    #if not run on local(for now:ncsa)machine: 
  # host=os.getenv('HOST') #checking against new store, for now
  # log.info(f'host={host}')
  # log.info(f'host={host}')
    #tmp_endpoint=f'https://graph.geocodes.ncsa.illinois.edu/blazegraph/namespace/{namespace}/sparql'
    tmp_endpoint=args.endpoint
    #if host != "geocodes.ncsa.illinois.edu":
    #    log.info("using external call") #but could do this locally as well
    #    tmp_endpoint=f'https://graph.geocodes.ncsa.illinois.edu/{namespace}/sparql'
    #else: #even internally can have connection problems
    #    tmp_endpoint=f'http://localhost:9999/{namespace}/sparql' 
    log.info(f'get_summary_from_namespace try:{tmp_endpoint}') 
    log.info(f'try:{tmp_endpoint}') 
    ec.dflt_endpoint = tmp_endpoint
    df=ec.get_summary("")
    return df


#def make_graph(ns, url="https://graph.geodex.org/blazegraph"): #put tmp namespaces here, for now
def make_graph(ns, url="https://graph.geocodes.ncsa.illinois.edu/blazegraph"): 
    mg=manageGraph.ManageBlazegraph(url, ns) 
    log.info(f'have graph instance:{mg}, for url:{url}')
    import urllib.request
    code=urllib.request.urlopen(url).getcode()
    log.info(f'w/code:{code}') #good here but getting 404 during insert
    log.info(f'have graph instance:{mg}, for url:{url}')
    return mg

graphs={} #so can look up graph by namespace, to rm later, w/o having to keep track

def make_graph_ns(ns):
    mg= make_graph(ns)
    #should check if the namespace was already there
    mg.createNamespace() #dflt=quads, can add False for triples later
    log.info(f'created ins:{mg} w/namespace:{ns}')
    graphs[ns]=mg
    return mg

def rm_graph_ns(ns):
    mg=graphs.get(ns)
    log.info(f'deleting ins:{mg} w/namespace:{ns}')
    mg.deleteNamespace()

#-
def file_size(fn):
    size= os.path.getsize(fn)
    log.info(f'size:{size}')
    return size
#-
summary_namespace="summary2"

# what I thought might be managegraph methods, now as functions here:
#   def call_summarize(self):
#       log.info(f'call tsum on:{self.namespace}')
def call_summarize(repo):
    log.info("per repo={repo} through blaze-namespace")
    df=get_summary4repo(repo)
    summaryDF2ttl(df)

#till get upload into tmp_ns could switch from fuseki2blaze by hitting
# https://graph.geocodes.ncsa.illinois.edu/blazegraph/#namespaces iris_nabu *
#just to see it work, and create iris.ttl
# for this temp test, don't change the create/delete location bc don't want to loose this test ns yet

#   def summarize(self, ns="summary"):
#       self.createNamespace()
#       self.upload_nq_file()
#       self.call_summarize() #creates repo.ttl
#       self.deleteNamespace()
#       self.upload_ttl_file(ns)  #uploads it
#def summarize(repo, final_ns="summary"):
def summarize_repo(repo, final_ns="summary"):
    repo_file=f'{repo}.nq'
    repo_file_size=file_size(repo_file)
    if repo_file_size < 99:
        log.warning(f'repo:{repo_file} only:{repo_file_size} bytes, so not ok to summarize')
    tmp_ns="test"
    if repo:
        tmp_ns=repo
        log.info(f'ns={tmp_ns}=repo={repo}')
    else:
        log.warning(f'WARNING ns={tmp_ns}') #log after I finish debugging this
    mg= make_graph_ns(tmp_ns)
    log.info(f'mg.upload_nq_file(){repo}')
    mg.upload_nq_file() #will need to get ns=repo.nq up to ns so can be summarized in next step
    #the insert should error if it didn't get in there
    call_summarize(repo) #creates repo.ttl
    #could check to see file is there/ok
    mg.deleteNamespace()  #could keep around during debugging just to check ;makes it, but isn't getting filled yet
    summary_file=f'{repo}.ttl'
    summary_size=file_size(summary_file)
    if summary_size > 99:
        log.info(f'would: upload {repo}.ttl from here/after checking? to {summary_namespace}')
        print(f'now: upload {repo}.ttl (after checking) to, eg: {endpoint}/{summary_namespace}')
     #Best to do this by hand, w/ ttl2blaze.sh after having looked at it/them
     #  log.info(f'upload {repo}.ttl from here/after checking? to {summary_namespace}')
     #  mgs=make_graph_ns(summary_namespace)  #how are we giving this, and I think we should check over it 1st
     #  mgs.upload_ttl_file(summary_file)  #uploads it, to a differetn namespace of your choice, eg 'summary' #was getting 400
    else:
        log.warning(f'summary:{summary_file} only:{summary_size} long, so not ok to upload')
    #but should really check this before doing it

if __name__ == '__main__':
    import sys

    parser = argparse.ArgumentParser()

    parser.add_argument("repo",  help='repository name')
    parser.add_argument('--endpoint', dest='endpoint',
                        help='use blazegraph endpoint, fully defined, as data source; eg https://graph.geocodes.ncsa.illinois.edu/blazegraph/namespace/{repo}/sparql')
    parser.add_argument('--summary_namespace', dest='summary_namespace',
                        help='the namespace on the endpoint that the final summary will be uploaded to')
    if(len(sys.argv)==1):
        print("you need to enter the name of a repo to summarize")
    else:
        args = parser.parse_args() #would fail here, if no arg w/o printing help
        tmp_endpoint=args.endpoint
        if tmp_endpoint:
            endpoint=tmp_endpoint
        print(f'summarizing using (temp) endpoint={endpoint}')
        log.info(f'summarizing using (temp) endpoint={endpoint}')
        if args.summary_namespace:
            summary_namespace=args.summary_namespace
        log.info(f'summary_namespace={summary_namespace}')
        if(len(sys.argv)>1):
            repo = args.repo
            # repo = sys.argv[1]
            #tmp_endpoint=f'http://localhost:3030/{repo}/sparql' #fnq repo
            #print(f'try:{tmp_endpoint}') #if >repo.ttl, till prints, will have to rm this line &next2:
            #ec.dflt_endpoint = tmp_endpoint
            #df=ec.get_summary("")
            log.info(f'port={port},arg1={repo}')
       #    if  args.endpoint : #when: os.getenv('tmp_summary_port') #if 9999 will use blaze
       #        log.info("bulk 1st load from blaze")
       #        df=get_summary_from_namespace( args)
       #    else:
       #        #log.info("per repo through fuseki")
       #        log.info("per repo through blaze-namespace")
       #        df=get_summary4repo(repo)
       #    summaryDF2ttl(df)
       #for now skip 1st shot summarization of all repo's from main blaze namespace, eg. earthcube
       #and just:
            #summarize_repo(repo) #get potential final upload ns in later; 
            summarize_repo(repo, summary_namespace) 
            #though I'd rather be able to check file before it gets loaded to final summary namespace
        else:
            #log.info("need to give repo to run, or if:tmp_summary_port=9999 a namespace for initial bulk load")
            parser.print_help()
