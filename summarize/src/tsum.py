#!/usr/bin/env python3
#mbobak summarize a nq file, for quick queries, and quad now as subj to point to graph-url
 #this is almost like nq2ttl, but is sumarizing via the qry
import pandas as pd
import os
import argparse
fn="iris.csv" #"xdomes.csv"
#df=pd.read_csv(fn, comment='#') #not filling out well yet
#df=pd.read_csv("s.csv") #head of summary.csv, from ec.py's get_summary("")
#df=pd.read_csv("summary_urn.csv") #head of summary.csv, from ec.py's get_summary("")
#df=pd.read_csv("s2.csv") #from similar summarizition but of my stoere, that uses URLs for graph
 #after reading csv via qry, which could be done w/rdflib like in 2nq.py but w/ec like qry
#subj g resourceType name description pubname placenames kw datep
#context = "@prefix : <http://schema.org/> ." #might get larger, eg.incl dcat
context = "@prefix : <https://schema.org/> ." #https for now
#started by tweaking fnq of fn.nq then dump to fn.csv which could read here
# but can use ec.py utils, to just load summary.qry and get df right away
# then iterate over it  ;load ec like I do w/check.py and use
#could have summary in here, or give a get_summary_txt then get_summary(fnq)
#after this get max lat/lon and put as latitude/longnitude, then get centriod
 #consider a version of the query where the vars are already the so:keywords
 #but after changinge ResourceType to 'a', .. oh, this doesn't have : so special case anyway
#used this query on all of geodec using ec.py's get_summary and dumped to summary.csv
#Nov  5 17:24 get_summary.txt -> get_summary_good.txt
#still using txt file on my server right now instead
#=port setup for fuseki, but might now also do 1st one shot from blaze on 9999; ~as above
port=3030
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
#df=pd.read_csv("summary-gc1.csv") #head of summary.csv, from ec.py's get_summary("")
#df=pd.read_csv(f'{repo}.csv') #head of summary.csv, from ec.py's get_summary("")
#seeing error in csv, might be time to get it directly, as repo's are small enough, to try over
#repo="linked.earth" #get from cli now
#testing_endpoint=f'http://ideational.ddns.net:3030/{repo_name}/sparql'
#tmp_endpoint=f'http://localhost:3030/{repo}/sparql' #fnq repo
#print(f'try:{tmp_endpoint}') #if >repo.ttl, till prints, will have to rm this line &next2:
#< not IN_COLAB
#< rdf_inited,rdflib_inited,sparql_inited=True,True,True
#import ec
#import earthcube_utilities as ec #check that it has been updated for newer work/later
import qry as ec #check that it has been updated for newer work/later
#import ../earthcube_utilities as ec  #assuming it is one level above
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
#dbg=True
dbg=False

def summaryDF2ttl(df):
    "summarize sparql qry (or main quad store)s ret DataFrame, as triples in ttl format w/g as the new subj"
    urns = {}
    import json
    def is_str(v):
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
                #sdes=description.replace(' / ',' \/ ').replace('"','\"')
                #sdes=sdes.replace(' / ',' \/ ').replace('"','\"')
              # sdes=sdes.replace('"','\"')
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
           #print(f'        :name "{name}" ;')
            f.write(f'        :name {name} ;\n')
           #print(f'        :description """{description}""" ;')
           #print(f'        :description """{sdes}""" ;')
            f.write(f'        :description ""{sdes}"" ;\n')
           #print(f'        :keyword "{kw}" ;')
           #print(f'        :keyword {kw} ;') #not what schema.org &the new query uses
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

if __name__ == '__main__':
    import sys

    parser = argparse.ArgumentParser()

    parser.add_argument("repo",  help='repository name')
    parser.add_argument('--endpoint', dest='endpoint',
                        help='use blazegraph endpoint, fully defined, as data source; eg https://graph.geocodes.ncsa.illinois.edu/blazegraph/namespace/{repo}/sparql')
    args = parser.parse_args()
    if(len(sys.argv)>1):
        # repo = sys.argv[1]
        repo = args.repo
        #tmp_endpoint=f'http://localhost:3030/{repo}/sparql' #fnq repo
        #print(f'try:{tmp_endpoint}') #if >repo.ttl, till prints, will have to rm this line &next2:
        #ec.dflt_endpoint = tmp_endpoint
        #df=ec.get_summary("")
        print(f'port={port},arg1={repo}')
        if  args.endpoint : #when: os.getenv('tmp_summary_port') #if 9999 will use blaze
            print("bulk 1st load from blaze")
            df=get_summary_from_namespace( args)
        else:
            print("per repo through fuseki")
            df=get_summary4repo(repo)
        summaryDF2ttl(df)
    else:
        #print("need to give repo to run, or if:tmp_summary_port=9999 a namespace for initial bulk load")
        parser.print_help()
