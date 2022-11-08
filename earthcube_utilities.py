#M Bobak, for ncsa.uiuc NSF EarthCube effort, GeoCODES search&resource use w/in NoteBooks
# some on (new)direction(s) at: https://mbcode.github.io/ec
#=this is also at gitlab now, but won't get autoloaded until in github or allow for gitlab_repo
 #but for cutting edge can just get the file from the test server, so can use: get_ec()
dbg=None #can use w/logging as well soon, once there is more need&time
rdf_inited,rdflib_inited,sparql_inited=None,None,None
endpoint=None
#keep these more in sync ;could have a dict for each setup
repo_name="geocodes_demo_datasets" #for testing
#testing_bucket="citesting" #or bucket_name
#testing_bucket="test3" #or bucket_name
testing_bucket="mbci2" #using this vs what send in in places/fix this
ci_url=f'https://oss.geocodes-dev.earthcube.org/{testing_bucket}'
bucket_url=f'https://oss.geocodes-dev.earthcube.org/{testing_bucket}' #use in oss
#testing_endpoint="http://ideational.ddns.net:3030/geocodes_demo_datasets/sparql"
testing_endpoint=f'http://ideational.ddns.net:3030/{repo_name}/sparql'
#testing_endpoint="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/{besting_bucket}/sparql"
first_endpoint = "https://graph.geodex.org/blazegraph/namespace/nabu/sparql"
prod_endpoint = "https://graph.geocodes.earthcube.org/blazegraph/namespace/earthcube/sparql"
#dflt_endpoint = "https://graph.geocodes.earthcube.org/blazegraph/namespace/earthcube/sparql"
dflt_endpoint_old = "https://graph.geocodes.earthcube.org/blazegraph/namespace/earthcube/sparql"
mb_endpoint = "http://24.13.90.91:9999/bigdata/namespace/nabu/sparql"
ncsa_endpoint_old = "http://mbobak.ncsa.illinois.edu:9999/blazegraph/namespace/nabu/sparql"
ncsa_endpoint_ = "https://mbobak.ncsa.illinois.edu:9999/blazegraph/namespace/nabu/sparql"
ncsa_endpoint = "https://mbobak.ncsa.illinois.edu:9999/bigdata/namespace/ld/sparql"
gc1_endpoint = "https://graph.geocodes-1.earthcube.org/blazegraph/namespace/earthcube/sparql"
dev_https_endpoint="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/https/sparql"
#dflt_endpoint = ncsa_endpoint
#dflt_endpoint = "https://graph.geodex.org/blazegraph/namespace/nabu/sparql"
dflt_endpoint = gc1_endpoint
summary_endpoint = dflt_endpoint.replace("earthcube","summary")
#from 'sources' gSheet: can use for repo:file_leaf naming/printing
base_url2repo ={"https://raw.githubusercontent.com/earthcube/GeoCODES-Metadata/main/metadata/Dataset/json": "geocodes_demo_datasets",
        "https://raw.githubusercontent.com/earthcube/GeoCODES-Metadata/main/metadata/Dataset/allgood": "geocodes_demo_datasets",
        "https://raw.githubusercontent.com/earthcube/GeoCODES-Metadata/main/metadata/Dataset/bad": "geocodes_demo_bad",
                "http://mbobak.ncsa.illinois.edu/ec/minio/test3/summoned/geocodes_demo_datasets": "test3"
        } #won't match if '/' at end of key
#can load sitemaps from gSheet, or even better github, here are a few now, in the order the get_graph_per_repo puts them out
 # https://raw.githubusercontent.com/MBcode/ec/master/test/sitemaps.csv #had to take bad ones out again
named_sitemaps={ #putting version of this in my ec/test as sitemaps.csv
"ssdb.iodp": "https://ssdb.iodp.org/dataset/sitemap.xml",
"usap-dc": "https://www.usap-dc.org/view/dataset/sitemap.xml",
#"xdomes": "https://xdomes.tamucc.edu/srr/sensorML/sitemap.xml",
"iris": "http://ds.iris.edu/files/sitemap.xml",
#"balto": "http://balto.opendap.org/opendap/site_map.txt ",
"DesignSafe": "https://www.designsafe-ci.org/sitemap.xml ",
#"neon": "https://geodex.org/neon_prodcodes_sm.xml",
"opentopography": "https://portal.opentopography.org/sitemap.xml",
"earthchem": "https://ecl.earthchem.org/sitemap.xml",
"lipidverse": "https://lipdverse.org/sitemap.xml",
"magic": "https://www2.earthref.org/MagIC/contributions.sitemap.xml",
#"neotomadb": "http://data.neotomadb.org/sitemap.xml",
"cchdo": "https://cchdo.ucsd.edu/sitemap.xml",
"unavco": "https://www.unavco.org/data/doi/sitemap.xml",
"hydroshare": "https://www.hydroshare.org/sitemap-resources.xml",
"bco-dmo": "https://www.bco-dmo.org/sitemap.xml",
"opencoredata": "http://opencoredata.org/sitemap.xml",
"iedadata": "http://get.iedadata.org/doi/xml-sitemap.php",
"ucar": "https://data.ucar.edu/sitemap.xml",
"unidata": "https://www.unidata.ucar.edu/sitemap.xml",
"linked.earth": "http://wiki.linked.earth/sitemap.xml",
"r2r": "https://service-dev.rvdata.us/api/sitemap/",
"geocodes_demo_dataset": "https://raw.githubusercontent.com/earthcube/GeoCODES-Metadata/gh-pages/metadata/Dataset/sitemap.xml",
"amgeo": "https://amgeo-dev.colorado.edu/sitemap.xml",
"rr": "https://object.cloud.sdsc.edu/v1/AUTH_85f46aa78936477d8e71b186269414e8/gleaner-summoned"
}
sitemaps=list(named_sitemaps.values())
repos=list(named_sitemaps.keys())

def test_sitemaps(sitemaps=named_sitemaps):
    sitemaps=list(named_sitemaps.values())
    print(f'getting lengths for:{sitemaps}')
    sc=sitemaps_count(sitemaps) #but needs to handle timeouts before running that full list
    return sc  #this will work w/dflt list now

def ld_ls_jsonld(repo,base_path=None):
    #if not base_path:
    #    return "go to base ld-cache dir"
    return ls_(f'{repo}/*.jsonld')

def ld_jsonld_counts(repos=repos):
    rd={}
    for repo in repos:
        l=ld_ls_jsonld(repo)
        ln=len(l)
        print(f'{repo} has {ln}')
        rd[repo]=ln
    return rd

local=None
def laptop(): #could call: in_binder
    "already have libs installed"
    global rdf_inited,rdflib_inited,sparql_inited
    rdf_inited,rdflib_inited,sparql_inited=True,True,True
    print("rdf_inited,rdflib_inited,sparql_inited=True,True,True")
    return "rdf_inited,rdflib_inited,sparql_inited=True,True,True"

def local():
    "do in binder till can autoset if not in colab"
    #put in a binder version of sparql_nb template, for now
    local=laptop()

def now():
    from datetime import datetime
    now = datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
    return dt_string

def head(l, n=5):
    return l[:n]

def tail(l, n=5):
    return l[-n:]

def is_str(v):
    return type(v) is str

def is_list(v):
    return type(v) is list

#pagemil parameterized colab/gist can get this code via:
#with httpimport.github_repo('MBcode', 'ec'):   
#  import ec
#version in template used the earthcube utils
import os
import sys
import json
IN_COLAB = 'google.colab' in sys.modules

def falsep(val):
    return val == False

def not_true(val):
  return val and (val != False)

#if not_true(IN_COLAB):
if falsep(IN_COLAB):
    print("not IN_COLAB")
    #local()
    laptop()

def ndtq(name=None,datasets=None,queries=None,tools=None):
  "get collection args for colab or binder"
  import json
  if IN_COLAB: #this has to come from top level
    n=json.loads(name)
    d=json.loads(datasets)
    t=json.loads(tools)
    Q=json.loads(queries)
  else:
    ds = ipyparams.params['collection']
    print(ds)
    dso = json.loads(ds)
    # if this cell fails the first run.
    #run a second time, and it works.
    n=dso.get('name')
    d=dso.get('datasets')
    t=dso.get('tools')
    Q=dso.get('queries')
  print(f'n={n},d={d},q={Q},t={t}')
  return n,d,t,Q

#more loging
#def install_recipy():
#    cs='pip install recipy'
#    os.system(cs)
#install_recipy()
#import recipy
def first(l):
    "get the first in an iterable"
    from collections.abc import Iterable
    if isinstance(l,list):
        return l[0]
    elif isinstance(l,Iterable):
        return list(l)[0]
    else:
        return l

def flatten(xss): #stackoverflow
    "make list of lists into 1 flat list"
    return [x for xs in xss for x in xs]

#from qry.py
def get_txtfile(fn):
    "ret str from file"
    with open(fn, "r") as f:
        return f.read()

def get_jsfile2dict(fn):
    "get jsonfile as dict"
    #s=get_txtfile(fn)
    #return json.loads(s)
    with open(fn, "r") as f:
        return json.load(f)

def put_txtfile(fn,s,wa="w"):
    "filename to dump string to"
    #with open(fn, "w") as f:
    with open(fn, "a") as f:
        return f.write(s)

def list2txtfile(fn,l,wa="w"):
    with open(fn, "a") as f:
        for elt in l:
            f.write(f'{elt}\n')
    return len(l)

def date2log(): #could use now to put on same line, but this breaks it apart
    cs="date>>log"
    os.system(cs)

def add2log(s):
    "logging" #will use lib
    date2log()
    fs=f'[{s}]\n'
    put_txtfile("log",fs,"a")

def print2log(s):
    print(s)
    add2log(s)

def os_system(cs):
    "run w/o needing ret value"
    os.system(cs)
    add2log(cs)

def os_system_(cs):
    "system call w/return value"
    s=os.popen(cs).read()
    add2log(cs)
    return s

def curl_url(url):
    cs=f'curl {url}'
    return os_system_(cs)

def whoami():
    return os_system_("whoami")

def urn_leaf(s): #like urn_tail
    "last part of : sep string" 
    leaf = s if not s else s.split(':')[-1]
    return leaf

#start adding more utils, can use to: fn=read_file.path_leaf(url) then: !head fn
def path_leaf(path):
    "everything after the last /"
    import ntpath
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def path_base_leaf(path):
    "like path_leaf but gives base 1st"
    import ntpath
    head, tail = ntpath.split(path)
    if not tail:
        tail = ntpath.basename(head)
    return head, tail

def replace_base(path,mydict=base_url2repo,sep=":"): #for context like: repo:filename
    "use URI to context:, eg. repo:leaf.rdf"
    base,leaf=path_base_leaf(path)
    new_base=mydict.get(base)
    if new_base:
        return f'{new_base}{sep}{leaf}'
    else:
        return path

def file_ext(fn):
    "the ._part of the filename"
    st=os.path.splitext(fn)
    add2log(f'fe:st={st}')
    return st[-1]

def file_base(fn):
    "the base part of base.txt"
    st=os.path.splitext(fn)
    add2log(f'fb:st={st}')
    return st[0]

def file_leaf_base(path):
    "base of the leaf file"
    pl=path_leaf(path)
    return file_base(pl)

#sparql.ipynb:    "ds_url=ec.collect_ext(ds_urls,ext)\n",
def collect_ext(l,ext):
  return list(filter(lambda x: file_ext(x)==ext,flatten(l)))

def collect_ext_(l,ext):
  return list(filter(lambda x: file_ext(x)==ext,l))

def collect_pre(l,pre):
  return list(filter(lambda x: x.startswith(pre),flatten(l)))

def collect_pre_(l,pre):
  return list(filter(lambda x: x.startswith(pre),l))

def collect_str(l,s):
  return list(filter(lambda x: s in x ,flatten(l)))

def collect_str_(l,s):
  return list(filter(lambda x: s in x ,l))

#could think a file w/'.'s in it's name, had an .ext
 #so improve if possible; hopefully not by having a list of exts
  #but maybe that the ext is say 6char max,..
#only messed up filename when don't send in w/.ext and has dots, but ok w/.ext

def has_ext(fn):
    return (fn != file_base(fn))

def wget(fn):
    #cs= f'wget -a log {fn}'  #--quiet
    cs= f'wget --tries=2 -a log {fn}' 
    os_system(cs)
    return path_leaf(fn) #new

def wget2(fn,fnl): #might make optional in wget
    "wget url, save to " #eg. sitemap to repo.xml
    cs= f'wget -O {fnl} --tries=2 -a log {fn}' 
    os_system(cs) 
    return get_txtfile(fnl) #not necc,but useful

def mkdir(dir):
    cs=f'mkdir {dir}'
    return os_system(cs)

def pre_rm(url):
    "rm (possibly alredy) downloaded version of url"
    fnb=path_leaf(url)
    cs=f'rm {fnb}'
    os_system(cs)
    return fnb

def get_ec(url="http://geocodes.ddns.net/ec/nb/ec.py"):
    pre_rm(url)
    wget(url)
    return "import ec"

    #often want to get newest ec.py if debugging
    # but don't need to get qry-txt each time, but if fails will use latest download anyway

def get_ec_txt(url):
    fnb= pre_rm(url)
    wget(url)
    return get_txtfile(fnb)

#testing:
jar=os.getenv("jar") #move this to top, near global endpoint
if not jar:
    if local:
        jar="~/bin/jar" #have set by local, setup will have to get otherwise
    else:
        jar="."

def blabel_l(fn): 
    "get rid of BlankNodes, needs setup_j"
    fb=file_base(fn) 
    ext=file_ext(fn)
    cs=f'java -Xmx4155M -jar {jar}/blabel.jar  LabelRDFGraph -l -i {fn} -o {fb}_l{ext}'
    os_system(cs)

def read_sd_(fn):
    "read_csv space delimited"
    import pandas as pd
    return pd.read_csv(fn,delimiter=" ")

def read_sd(fn):
    "read_file space delimited"
    fn_=fn.replace("urn:","")
    if dbg:
        print(f'read_sd:{fn_}')
    #return read_file(fn_,".txt")
    import pandas as pd
    try:
        df=pd.read_csv(fn, sep='\n',header=None,comment='#')
    except:
        df = str(sys.exc_info()[0])
    return df

def read_json_(fn):
    "read_json and flatten for df_diff"
    #import pandas as pd
    #return pd.read_json(fn) #finish or skip for:
    return read_file(fn,".json") #getting "<class 'NameError'>"

#def read_json(url):
def read_json(urn):
    "request json, ret dict"
    import urllib.request
    import json
    url=urn.replace("urn:","")
    if dbg:
        print(f'read_json:{url}')
    with urllib.request.urlopen(url) as response:
        #try:
        res = response.read()
        if res:
            return json.loads(res)
        else:
            return None

def is_df(df):
    import pandas as pd
    return isinstance(df, pd.DataFrame)

#https://stackoverflow.com/questions/48647534/python-pandas-find-difference-between-two-data-frames
def df_diff(df1,df2): #doesn't work as well as I would like in all situations, work on/fix/finish
    import pandas as pd
    if not is_df(df1):
        print("df_diff:1st arg:wrong type:{df1}")
        return pd.DataFrame() #False
    if not is_df(df2):
        print("df_diff:2nd arg:wrong type:{df2}")
        return pd.DataFrame() #False
    if dbg:
        print(f'df_diff:{df1},{df2}')
    return pd.concat([df1,df2]).drop_duplicates(keep=False)

def diff_sd(fn1,fn2):
    "df_diff 2 space delimited files"
    df1=read_sd(fn1)
    df2=read_sd(fn2)
    dfdiff=df_diff(df1,df2)
    if dfdiff.empty:
        return True
    else:
        return dfdiff

def diff_flat_json(fn1,fn2):
    "df_diff 2 space delimited files"
    df1=read_json(fn1)
    df2=read_json(fn2)
    return df_diff(df1,df2) #or skip for:

def get_json_eq(fn1,fn2):
    print(f'get_json_eq:{fn1},{fn2}') #dbg
    d1=read_json(fn1)
    d2=read_json(fn2)
    if not d1:
        print("d1 missing")
    if not d2:
        print("d2 missing")
    return d1 == d2

def get_json_diff(fn1,fn2):
    d1=read_json(fn1)
    d2=read_json(fn2)
    #(https://pypi.org/project/deepdiff/)  or (https://dictdiffer.readthedocs.io/en/latest/)
    return d1 == d2 #finish, as will have to install in NBs too

#def list_diff(li1,li2):
def list_diff_not_in(li1,li2):
    "those in l1 not in l2"
    s = set(li2)
    return [x for x in li1 if x not in s]
#>>> list_diff_not_in(["a","b","c"],["a","b"])
#['c']
def list_diff_dropoff(li1,li2):
    ldiff= list_diff_not_in(li1,li2)
    #print(f'li1={li1}')
    #print(f'li2={li2}')
    #print(f'ldiff={ldiff}')
    return ldiff
    #return list_diff_not_in(li1,li2)

#testing cmp w/gold-stnd should now comes from github 
 #also can send alt bucket ..., now citesting, but be able to set: testing_bucket
#now endpoint loaded from ld-cache to work out mechanics of these fncs, 
 #will get from live workflow one we are sure it will be up during testing ;can be reset from script

def find_urn_diffs(endpoint="http://ideational.ddns.net:3030/geocodes_demo_datasets/sparql", 
        gold="https://raw.githubusercontent.com/earthcube/GeoCODES-Metadata/mb_sample/metadata/Dataset/standard/milled/geocodes_demo_datasets/URNs.txt"):
       #gold="https://raw.githubusercontent.com/MBcode/ec/master/test/standard/milled/geocodes_demo_datasets/URNs.txt"):
    "get_graphs_list and saved gold-list, and diff" #~do a set diff
    print("in find_urn_diffs,read_sd gold")
    #df_gold=read_sd(gold)
    df_gold=read_file(gold,".txt")
    print(f'gold:{df_gold}')
    #get_graphs w/convience gives list
    #return df_diff(df_gold, )
    global testing_endpoint
    if endpoint == testing_endpoint:
        test_endpoint=endpoint
    else: #use global so can set by script
        test_endpoint=testing_endpoint
    #test_list=get_graphs_list(test_endpoint)
    test_list=get_graphs_tails(test_endpoint)
    print(f'test:{test_list}')
    gold_list=df_gold['g'].tolist()
    print(f'gold:{gold_list}')
    tl=len(test_list)
    tg=len(gold_list)
    print(f'got:{tl},expected:{tg}') #consider also listing sitmap counts
    #return list_diff(test_list,gold_list)
    return list_diff_not_in(gold_list,test_list)

#if have url for gold-stnd bucket, and have missing urn
#milled_bucket="" #either the test milled, or from production then from diff buckets, ;still missing URNs from end2end start it off

#check_urn_ rdf|jsonld look up from LD-cache of latest run, and compare w/gold-stnd in github
  #tested separately, &ok on 1st pass;  ret True if ok=the same as gold-stnd
  #if the file was not there, might send whole file back as diff, or fail/check, but would like it2say not there/finish
   #might also call from spot_crawl_dropoff, which would already know that the file was there for sure

def check_urn_rdf(urn,
        test_bucket="https://oss.geocodes-dev.earthcube.org/citesting/milled/geocodes_demo_datasets/",
        gold="https://raw.githubusercontent.com/earthcube/GeoCODES-Metadata/mb_sample/metadata/Dataset/standard/milled/geocodes_demo_datasets/"):
       #gold="https://raw.githubusercontent.com/MBcode/ec/master/test/standard/milled/geocodes_demo_datasets/"):
    "check a URNs milled-rdf diff btw urls for current+gold-stnd buckets"
    import pandas as pd
    #gold_rdf=f'{test_bucket}{urn}.rdf' #test_rdf=f'{milled_bucket}{urn}.rdf'
    gold_rdf=f'{gold}{urn}.rdf'
    test_rdf=f'{test_bucket}{urn}.rdf'
    #could blabel_l them both if need be
    #df_gold=pd.read_csv(gold_rdf)
    #df_test=pd.read_csv(test_rdf)
    #return df_diff(df_gold,df_test)
    return diff_sd(gold_rdf,test_rdf) #the read should skip the header

def check_urn_jsonld(urn,
     #test_bucket="https://oss.geocodes-dev.earthcube.org/citesting/summoned/geocodes_demo_datasets/", ;use testing_bucket fix
                     #test_bucket="https://oss.geocodes-dev.earthcube.org/test3/summoned/geocodes_demo_datasets/",
        test_bucket=f'https://oss.geocodes-dev.earthcube.org/{testing_bucket}/summoned/geocodes_demo_datasets/',
        gold="https://raw.githubusercontent.com/earthcube/GeoCODES-Metadata/mb_sample/metadata/Dataset/standard/summoned/geocodes_demo_datasets/"):
       #gold="https://raw.githubusercontent.com/MBcode/ec/master/test/standard/summoned/geocodes_demo_datasets/"):
    "check a URNs summonded-jsonld diff btw urls for current+gold-stnd buckets"
    #rm urn: if necessary
    gold_rdf=f'{gold}{urn}.jsonld'
    test_rdf=f'{test_bucket}{urn}.jsonld'
    print(f'check_urn_jsonld:{urn}')
    #return diff_sd(gold_rdf,test_rdf)
    #return diff_flat_json(gold_rdf,test_rdf)
    return get_json_eq(gold_rdf,test_rdf) #if not= then use dict-diff lib to show the diffs

#might make a check_urn_ld_cache(urn,bucket=,test_set=,test_base=): #and it knows summoned .jsonld, milled .rdf
def check_urn_ld_cache(urn,bucket="citesting",test_set="geocodes_demo_datasets",test_base="https://oss.geocodes-dev.earthcube.org/"):
    "given URN, compare latest run LD_cache with gold-std" #check_urn_ fncs hold default gold url
    global testing_bucket
    if(testing_bucket != "citesting"): #to change test_bucket ...
        test_bucket=test_bucket.replace("citesting",testing_bucket)
    else:
        test_bucket=bucket
    test_rdf=f'{test_base}{test_bucket}/milled/{test_set}/' #{urn}.rdf added later
    print(f'new rdf:{test_rdf}')
    #rdf_check= list(check_urn_rdf(urn,test_rdf)) #bool not iterable
    rdf_check= check_urn_rdf(urn,test_rdf)
    test_jsonld=f'{test_base}{test_bucket}/summoned/{test_set}/' #{urn}.jsonld added later
    print(f'new jsonld:{test_jsonld}')
    jsonld_check= check_urn_jsonld(urn,test_jsonld) 
    #return rdf_check.append(jsonld_check) #mapping over these, they would come back in pairs
    return rdf_check, jsonld_check 

#endpoint loaded like nabu, to work on all this functionality, then can make sure it keeps it up like the ld-cache
def get_urn_diffs(endpoint="http://ideational.ddns.net:3030/geocodes_demo_datasets/sparql", 
        gold="https://raw.githubusercontent.com/earthcube/GeoCODES-Metadata/mb_sample/metadata/Dataset/standard/milled/geocodes_demo_datasets/"):
       #gold="https://raw.githubusercontent.com/MBcode/ec/master/test/standard/milled/geocodes_demo_datasets/"):
    "see which URN/graphs are in endpoint, and compare with expected"
    gold_URNs= gold + "URNs.txt"
    print(f'find_urn_diffs:{endpoint},{gold_URNs}')
    dfu=find_urn_diffs(endpoint,gold_URNs)
    return dfu

#spot_ crawl_dropoff below, will use new LD_cache_ .. files and call these helper functions in the end
 #non spot will still need integrity checks like in original ingestTesting.md &some shacl

#'validation'  ;check consituent fncs before switch over to this one
def check_urn_diffs(endpoint="http://ideational.ddns.net:3030/geocodes_demo_datasets/sparql", 
        test_bucket="https://oss.geocodes-dev.earthcube.org/citesting/milled/geocodes_demo_datasets/",
        gold="https://raw.githubusercontent.com/earthcube/GeoCODES-Metadata/mb_sample/metadata/Dataset/standard/milled/geocodes_demo_datasets/"):
       #gold="https://raw.githubusercontent.com/MBcode/ec/master/test/standard/milled/geocodes_demo_datasets/"):
       "looks at endpoint for missing URNs, then check LD-cache for each"
       dfu=get_urn_diffs(endpoint,gold)
       #ld_checks= list(map(lambda urn: check_urn_ld_cache(urn,test_bucket),dfu)) #could send more or less:
       ld_checks= list(map(check_urn_ld_cache,dfu))
       return ld_checks
#vs
#'validation'
def check_urn_diffs_(endpoint="http://ideational.ddns.net:3030/geocodes_demo_datasets/sparql", 
        test_bucket="https://oss.geocodes-dev.earthcube.org/citesting/milled/geocodes_demo_datasets/",
        gold="https://raw.githubusercontent.com/earthcube/GeoCODES-Metadata/mb_sample/metadata/Dataset/standard/milled/geocodes_demo_datasets/"):
       #gold="https://raw.githubusercontent.com/MBcode/ec/master/test/standard/milled/geocodes_demo_datasets/"):
    "find_urn_diffs and for each missing check_urn_rdf|jsonld" #get_graphs diff w/expected URNs, then check each missing
    gold_URNs= gold + "URNs.txt"
    print(f'find_urn_diffs:{endpoint},{gold_URNs}')
    dfu=find_urn_diffs(endpoint,gold_URNs)
    #dfu=find_urn_diffs(endpoint) #use it's default for a bit, bc read_sd prob w/github raw right now ;change2 read_file
    global testing_bucket
    if(testing_bucket != "citesting"): #to change test_bucket ...
        use_test_bucket=test_bucket.replace("citesting",testing_bucket)
        print(f'need2setup2pass changed test_bucket:{use_test_bucket}')
        #maybe have test_ url made of test_base + bucket + (summonde4.jsonld,milled4.rdf) + test_set
        test_base="https://oss.geocodes-dev.earthcube.org/"
        test_set="geocodes_demo_datasets" #could set this as a global as well
        test_rdf=f'{test_base}{use_test_bucket}/milled/{test_set}/'
        print(f'new rdf:{test_rdf}')
        test_jsonld=f'{test_base}{use_test_bucket}/summoned/{test_set}/'
        print(f'new jsonld:{test_jsonld}')
        #rdf_checks= list(map(lambda urn: check_urn_rdf(urn,endpoint,rdf_checks),dfu))
        rdf_checks= list(map(lambda urn: check_urn_rdf(urn,test_rdf),dfu))
        #jsonld_checks= list(map(lambda urn: check_urn_jsonld(urn,endpoint,jsonld_checks),dfu)) 
        jsonld_checks= list(map(lambda urn: check_urn_jsonld(urn,test_jsonld),dfu)) 
    else: # the other way   #got similar output w/missing bucket,so needs more test situations/closer look
        #will need lambdas if want to pass any change to the defaults on
        print(f'check_urn_rdf of:{dfu}')
        rdf_checks= list(map(check_urn_rdf,dfu))
        jsonld_checks= list(map(check_urn_jsonld,dfu)) #could do after, only if a problem, or just check them all now
        print(f'get:{rdf_checks}')
    return rdf_checks.append(jsonld_checks) 
    #return rdf_checks #test the check fncs w/any (array of) URNs that exist

#=merge using:
def merge_dict_list(d1,d2):
    from collections import defaultdict
    dd = defaultdict(list)
    for d in (d1, d2): # you can list as many input dicts as you want here
        for key, value in d.items():
            dd[key].append(value)
    return dd

def repos2counts(repos):
    "from cached sitemaps,etc"
    repo_df_loc={}
    for repo in repos:
        repo_df_loc[repo]=repo2site_loc_df(repo)
    repo_counts={}
    #for repo in repos:
    for repo in repo_df_loc:
        repo_counts[repo]=len(repo_df_loc[repo])
    #for now on ld-cache-counts:
    repo_ld_counts={}
    repo_fnum=wget2("http://geocodes.ddns.net/ec/test/repo_fnum.txt","summoned.txt")
    repo_fnum_list=repo_fnum.split('\n')
    for repo_num in repo_fnum_list:
        repo_num_list=repo_num.split(' ')
        if len(repo_num_list)>1:
            #print(repo_num_list)
            repo_=repo_num_list[0]
            fnum=repo_num_list[1]
            rl=repo_.split('/')
            if len(rl)>2:
                #print(rl)
                rn=rl[2]
                repo_ld_counts[rn]=fnum
    #for now on final-counts: #next from graph.csv and run system cmd on it,then strip extra spaces
    repoCounts=wget2("http://geocodes.ddns.net/ec/test/graph_counts.txt","graph.txt")
    final_counts={}
    rl2_list=repoCounts.split('\n')
    for  rl2 in rl2_list:
        num_repo=rl2.split(' ')
        if len(num_repo)>1:
            #print(num_repo)
            count=num_repo[0]
            repo=num_repo[1].lstrip('milled:').lstrip('summoned:') #in case either
            final_counts[repo]=count
    return repo_counts,repo_ld_counts,final_counts,      repo_df_loc 

def post_untar(url,uncompress="tar -zxvf "): #could be "unzip -qq "
    "uncompress downloaded version of url"
    fnb=path_leaf(url)
    cs=f'{uncompress} {fnb}'
    os_system(cs)
    return fnb

def install_url(url): #use type for uncompress later
    pre_rm(url)
    wget(url)
    fnb=post_untar(url) #
    return fnb.rstrip(".tar.gz").rstrip(".zip") #handle either type

def install_java():
    ca= "apt-get install -y openjdk-8-jdk-headless -qq > /dev/null"
    os_system(cs)  #needed for jena..
    os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
    # !java -version #check java version

def install_jena(url="https://dlcdn.apache.org/jena/binaries/apache-jena-4.5.0.tar.gz"):
    return install_url(url)

def install_fuseki(url="https://dlcdn.apache.org/jena/binaries/apache-jena-fuseki-4.5.0.tar.gz"):
    return install_url(url)

def install_any23(url="https://dlcdn.apache.org/any23/2.7/apache-any23-cli-2.7.tar.gz"):
    return install_url(url)

def setup_blabel(url="http://geocodes.ddns.net/ld/bn/blabel.jar"):
    wget(url)

def setup_j(jf=None):
    install_java()
    path=os.getenv("PATH")
    jena_dir=install_jena()
    any23_dir=install_any23()
    if jf:
        fuseki_dir=install_jena()
        addpath= f':{jena_dir}/bin:{fuseki_dir}/bin:{any23_dir}/bin'
    else:
        addpath= f':{jena_dir}/bin:{any23_dir}/bin'
    os.environ["PATH"]= path + addpath 
    setup_blabel() #which also needs java
    return addpath

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

def get_query_txt(url="https://raw.githubusercontent.com/MBcode/ec/master/NoteBook/sparql-query.txt"):
    return get_ec_txt(url)

def get_subj2urn_txt(url="http://geocodes.ddns.net/ec/nb/sparql_subj2urn.txt"):
    #return get_ec_txt(url)
    return """prefix sschema: <https://schema.org/>
            SELECT distinct    ?g WHERE {
            graph ?g { <${g}> a schema:Dataset }}"""

def get_graphs_txt(url="http://geocodes.ddns.net/ec/nb/sparql_graphs.txt"):
    #return get_ec_txt(url)
    return "SELECT distinct ?g  WHERE {GRAPH ?g {?s ?p ?o}}"

def get_graph_txt(url="http://geocodes.ddns.net/ec/nb/get_graph.txt"):
    #return get_ec_txt(url)
    #return "SELECT distinct ?s ?p ?o  WHERE { graph ?g {?s ?p ?o} filter(?g = <${g}>)}"
    return "SELECT distinct ?s ?p ?o  WHERE { graph ?g {?s ?p ?o} filter(?g = <${q}>)}" #there will be a better way
    #return "describe <${q}>)}" #similar but can't do this    #also want where can ask for format as jsonld for ui
    #consider ret CONSTRUCT from a direct match vs filter

def get_summary_txt(url="http://geocodes.ddns.net/ec/nb/get_summary.txt"):
    return get_ec_txt(url)

## so/eg. this last one is where get_graph(g) calls v4qry(g,"graph")

def add_ext(fn,ft):
    if ft==None or ft=='' or ft=='.' or len(ft)<2:
        return None
    fn1=path_leaf(fn) #just the file, not it's path
    fext=file_ext(fn1) #&just it's .ext
    r=fn1
    if fext==None or fext=='':
        fnt=fn1 + ft
        #cs= f'mv {fn1} {fnt}' 
        cs= f'sleep 2;mv {fn1} {fnt}' 
        os_system(cs)
        r=fnt
    return r

def wget_ft(fn,ft):
    wget(fn)
    fnl=fn
    if ft!='.' and ft!='' and ft!=None and len(ft)>2:
        fnl=add_ext(fn,ft) #try sleep right before the mv
    #does it block/do we have2wait?, eg. time.sleep(sec)
    #fnl=path_leaf(fn) #just the file, not it's path
    if os.path.isfile(fnl):
        fs=os.path.getsize(fnl) #assuming it downloads w/that name
    else:
        fs=None
    #if fs>999 and fs<999999999: #try upper limit later
    #if fs>699:
    #    cs=f'unzip {fnl}'
    #    os.system(cs)
    #unzip even if small broken file
    if ft=='.zip': #should check if zip
        cs=f'unzip {fnl}'
        os_system(cs)
        fnb=file_base(fnl)
#       if os.path.isdir(fnb):
#           cs=f'ln -s . content' #so can put . before what you paste
#           os_system(cs)
    return fs

#rdflib_inited=None
def init_rdflib():
    #cs='pip install rdflib networkx'
    #cs='pip install rdflib networkx extruct' 
    #cs='pip install rdflib rdflib-jsonld networkx extruct' 
    cs='pip install rdflib rdflib-jsonld networkx extruct python-magic' 
    os_system(cs)
    rdflib_inited=cs

#-from crawlLD.py
#def crawl_LD(url) ;could get other than jsonld, &fuse
def url2jsonLD(url):
    "get jsonLD from w/in url"
    add2log(f'url2jsonLD({url})')
    if rdflib_inited==None:
        init_rdflib()
    import extruct
    import requests
    from w3lib.html import get_base_url
    r = requests.get(url)
    base_url_ = get_base_url(r.text, r.url)
    #ld = extruct.extract(r.text, base_url=base_url_ ,syntaxes=['json-ld'] )
    md = extruct.extract(r.text, base_url=base_url_ ,syntaxes=['json-ld'] )
    if md: #still geting as if all MetaData, so select out json-ld
        #ld = md.get('json-ld')
        lda = md.get('json-ld')
        #print(f'lda={lda}')
        ld=lda[0] #ret first here
        #print(f'ld={ld}')
    else: 
        ld =""
    add2log(ld)
    return ld

def url2jsonLD_fn(url,fn):
    "url2jsonLD_file w/forced filename"
    ld=url2jsonLD(url)
    LD=json.dumps(ld, indent= 2)
    fnj = fn + ".jsonld" #only if not there
    return put_txtfile(fnj,LD)

def url2jsonLD_file(url):
    "get jsonLD from w/in url, save to file"
    ld=url2jsonLD(url)
    fnb=file_leaf_base(url)
    LD=json.dumps(ld, indent= 2)
    put_txtfile(fnb,LD)
    return fnb

#def fn2jsonld(fn, base_url=None):
def fn2jsonld(fn, base_url=None):
    "url=base_url+fn save to fn"
    import re
#   if not base_url:
#       base_url = os.getenv('BASE_URL')
    #print(base_url)
    #print(fn)
#    url= base_url + fn
    url=fn
    #print(url)
    #ld=url2jsonLD(url)
    md=url2jsonLD(url)
    if md:
        ld = md.get('json-ld')
    else: 
        ld =""
    #print(len(ld))
    cfn=re.sub(r'(\n\s*)+\n+', '\n', fn.strip())
    fn = cfn + ".jsonld"
    #print(fn)
    if ld:
        with open(fn  ,'w') as f:
            #pp.pprint(ld,f)
            #f.write(pprint.pformat(ld[0]))
            f.write(json.dumps(ld[0], indent= 2))
    return ld
#-
#already done above,but take parts2fix below
def getjsonLD(url):
    "url2 .jsonld"
    import re
    import json
    ld=url2jsonLD(url) #get json
    #fnb=file_base(url)
    fnb=file_leaf_base(url)
    cfn=re.sub(r'(\n\s*)+\n+', '\n', fnb.strip())
    #fnj=fnb+".jsonld" 
    #put_txtfile(fnj,ld)
    fnj=cfn+".jsonld" 
    add2log(f'getjsonLD:{fnb},{fnj}')
    #LD=json.dumps(ld[0], indent= 2)
    LD=json.dumps(ld, indent= 2)
    put_txtfile(fnj,LD)
    #put_txtfile(fnj,LD.decode("utf-8"))
    return fnj

#get fnb + ".nt" and put_txtfile that str
#def 2nt  from any rdf frmt to a .nt file, bc easiest to concat
def xml2nt(fn,frmt="xml"):  #could also use rapper here, see: rdfxml2nt
    "turn .xml(rdf) to .nt"
    if rdflib_inited==None:
        init_rdflib()
    fnb=file_base(fn)
    from rdflib import Graph
    g = Graph()
    #g.parse(fn, format="xml")
    g.parse(fn, format=frmt) #allow for "json-ld"..
    #UnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 1: invalid start byte ;fix
    #s=g.serialize(format="ntriples").decode("u8") #works via cli,nb had ntserializer prob
    s=g.serialize(format="ntriples") #try w/o ;no, but works in NB w/just a warning
    fnt=fnb+".nt" #condsider returning this
    put_txtfile(fnt,s)
    add2log(f'xml2nt:{fnt},len:{s}')
    #return len(s) 
    return fnt 

def to_nt_str(fn,frmt="json-ld"):  
    "turn .xml(rdf) to .nt"
    fnb=file_base(fn)
    from rdflib import Graph
    g = Graph()
    g.parse(fn, format=frmt) #allow for other formats
    s=g.serialize(format="ntriples") 
    return s

def jsonld2nt(fn,frmt="json-ld"):
    "turn .jsonld to .nt"
    add2log(f'jsonld2nt:{fn},{frmt}')
    return xml2nt(fn,frmt)

def url2nt(url):
    "get .jsonLD file,&create a .nt version"
    #ld=url2jsonLD(url)
    #s1=len(ld)
    fnj=getjsonLD(url)
    fnt=jsonld2nt(fnj)
    #fnt=jsonld2nt(fnb)
    #s2=jsonld2nt(fnb)
    #add2log(f'url2nt,jsonld:{s1},nt:{s2}')
    #return s2
    #add2log(f'url2nt,jsonld:{s1},{fnt}')
    add2log(f'url2nt,{fnj},{fnt}')
    return fnt

def append2everyline(fn,aptxt,fn2=None):
    with open(fn) as fp:
        lines= fp.read().splitlines()
    if(fn2==None):
        fn2=fn.replace(".nt",".nq") #main use for triples to quads
    with open(fn2, "w") as fp:
        for line in lines:
            line= line.strip('.') #get rid of this from triples
            print(line + " " + aptxt, file=fp)
    return fn2

def url2nq(url):
    "crawl url ret .jsonld .nt .nq"
    fn= url2nt(url)
    apptxt= f'<{url}> .'
    return append2everyline(fn, apptxt)

def setup_s3fs(): #do this by hand for now
    #cs='pip install s3fs' #assume done rarely, once/session 
    #cs='pip install s3fs xmltodict' #want to switch to just request of url&parse xml:bucket_files.py
    cs='pip install s3fs xmltodict htmllistparse' #last for rehttpfs
    os_system(cs)

#if mounted minio like htm, that could have some benefits, incl getting over maxkeys, see what lib/s needed

def ls(dir): #there are other py commands to do this
    cs=f'ls {dir}'
    return os_system_(cs)

def ls_(path):
    lstr=ls(path)
    return lstr.split("\n")

#def mount_htm(ld_url=f'http://mbobak.ncsa.illinois.edu/ld/{repo_name}'):
def mount_htm(ld_url="http://mbobak.ncsa.illinois.edu/ld",repo=None):
    "mount any htm url, but default to current repo"
    if not repo:
        global repo_name
        repo = repo_name
    repo_cache=f'{ld_url}/{repo}'
    os_system(f'mkdir {repo}') #could mount higher so can mix repos
    cs=f'nohup rehttpfs {repo_cache} {repo} &' #macfuse has a problem but works on linux
    print(cs) #dbg
    os_system(cs)
    l=ls(repo)
    print(f'ls:{l}')
    return repo
    
def mount_repo(repo=None,ld_url="http://mbobak.ncsa.illinois.edu/ld"):
    "mount repo from my ld_cache"
    return mount_htm(ld_url,repo)

def mount_ld(repo="ld",ld_url="http://mbobak.ncsa.illinois.edu"):
    "mount ld_cache for all repos"
    return mount_htm(ld_url,repo)

def get_oss_(minio_endpoint_url="https://oss.geocodes-dev.earthcube.org/"): #old version
    import s3fs
    oss = s3fs.S3FileSystem( anon=True, key="", secret="",
          client_kwargs = {"endpoint_url": minio_endpoint_url})
    return oss
#def get_oss(minio_endpoint_url="https://oss.geocodes-dev.earthcube.org/"):
#def get_oss(minio_endpoint_url="https://oss.geocodes-dev.earthcube.org/",login=False):
def get_oss(minio_endpoint_url="https://oss.geocodes-dev.earthcube.org/",anon=True):
    import s3fs
    global S3KEY,S3SECRET
    #if login:
    if not anon:
        s3key=S3KEY
        s3secret=S3SECRET
    else:
        s3key=""
        s3secret=""
    oss = s3fs.S3FileSystem(
            #anon=True,
          anon=anon,
          key=s3key,
          secret=s3secret,
          #client_kwargs = {"endpoint_url":"https://oss.geodex.org"}
          #client_kwargs = {"endpoint_url":"https://oss.geocodes-dev.earthcube.org/"}
          client_kwargs = {"endpoint_url": minio_endpoint_url}
       )
    return oss
#in nb got: 
#ImportError: cannot import name 'PROTOCOL_TLS' from 'urllib3.util.ssl_' (/usr/local/lib/python3.7/dist-packages/urllib3/util/ssl_.py)
#but mostly run on machine where crawl/insert is done w/ spot_test.py for reports

#if not: fs = s3fs.S3FileSystem(anon=True), anon=False:
#def get_oss_login(minio_endpoint_url="https://oss.geodex.org", login=True):
def get_oss_login(minio_endpoint_url="https://oss.geodex.org", anon=False):
    #return get_oss(minio_endpoint_url,login)
    return get_oss(minio_endpoint_url,anon)


#def oss_ls(path='test3/summoned'):
def oss_ls(path='test3/summoned',full_path=True,minio_endpoint_url="https://oss.geocodes-dev.earthcube.org/"):
    oss=get_oss(minio_endpoint_url) #global oss
    import s3fs
    epl= oss.ls(path)
    if full_path:
        return list(map(lambda ep: f'{minio_endpoint_url}{ep}', epl))
    else:
        return epl
#>>> oss_ls('test3/summoned',False) #now need false to get this output
#['test3/summoned/geocodes_demo_datasets', 'test3/summoned/opentopography']
#>>> oss_ls('test3/summoned/geocodes_demo_datasets') #did not have base of url, so fixed w/map above, as default output type
#['test3/summoned/geocodes_demo_datasets/257108e0760f96ef7a480e1d357bcf8720cd11e4.jsonld', 'test3/summoned/geocodes_demo_datasets/261c022db9edea9e4fc025987f1826ee7a704f06.jsonld', 'test3/summoned/geocodes_demo_datasets/7435cba44745748adfe80192c389f77d66d0e909.jsonld', 'test3/summoned/geocodes_demo_datasets/9cf121358068c7e7f997de84fafc988083b72877.jsonld', 'test3/summoned/geocodes_demo_datasets/b2fb074695be7e40d5ad5d524d92bba32325249b.jsonld', 'test3/summoned/geocodes_demo_datasets/c752617ea91a725643d337a117bd13386eae3203.jsonld', 'test3/summoned/geocodes_demo_datasets/ce020471830dc75cb1639eae403a883f9072bb60.jsonld', 'test3/summoned/geocodes_demo_datasets/fcc47ef4c3b1d0429d00f6fb4be5e506a7a3b699.jsonld', 'test3/summoned/geocodes_demo_datasets/fe3c7c4f7ca08495b8962e079920c06676d5a166.jsonld']
#>>> 

def setup_sitemap(): #do this by hand for now
    cs='pip install ultimate_sitemap_parser' #assume done rarely, once/session 
    os_system(cs) #get rid of top one soon
    cs='pip install advertools' #assume done rarely, once/session 
    os_system(cs)

def sitemap_tree(url): #will depricate
    "len .all_pages for count"
    #print("assume: setup_sitemap()")
    from usp.tree import sitemap_tree_for_homepage
    tree = sitemap_tree_for_homepage(url)
    return tree

#switch over libs from tree to df

def sitemap_df(url):
    import  advertools as adv
    df=adv.sitemap_to_df(url)
    return df

def sitemap_all_pages(url):
    #tree=sitemap_tree(url)
    #return tree.all_pages()
    df=sitemap_df(url)
    return df['loc']

def repo2site_loc_df(repo):
    "get df[loc] from repos sitemap" #use cached sitemap
    base_url="http://geocodes.ddns.net/ec/crawl/sitemaps/"
    url=f'{base_url}{repo}.xml'
    return sitemap_all_pages(url)

def sitemaps_all_loc(sitemaps):
    "list(iterable) to get all DFs of LOCs"
    return map(sitemap_all_pages,sitemaps)
    #also be able to work w/dictionaries,  repo_name sitmap in, count out

def sitemap_list_(url):
    pages=sitemap_all_pages(url)
    pl=list(pages)
    return pl #get rid of need for these libs

def sitemap_list(url):
    "use fast xml lib"
    return sitemap_urls(url)

def sitemap_len(url):
    "try fast xml version"
    ul=sitemap_urls(url)
    return len(ul)
#now using this over https://github.com/MBcode/ec/blob/master/test/counts.md named_sitemaps
#sitemaps=list(named_sitemaps.values())
#counts=list(map(sitemap_len_,sitemaps)) #now resistent to errors, get:
#[25226, 18634, 704, 28, 5654, 17654, 0, 4263, 920, 0, 211, 45159, 0, 910, 2522, 0]
#can also run: that prints them out as it goes along
#sc=sitemaps_count(sitemaps)

def sitemap_len_(url):
    "for counts" # maybe allow filtering types later
    pages=sitemap_all_pages(url)
    pl=list(pages)
    return len(pl)

def sitemaps_count(sitemaps):
    sitemap_count = {}
    for sitemap in sitemaps:
        count=sitemap_len(sitemap)
        print(f'{sitemap} has {count} records')
        sitemap_count[sitemap]=count
    return sitemap_count

def crawl_sitemap(url):
    "url w/o sitemap.xml, might try other lib"
    #tree=sitemap_tree(url)
    pages=sitemap_all_pages(url)
    #for page in tree.all_pages():
    for page in pages:
        url2nq(page)
        #url2nq(page.url)
        #print(f'url2nq({page.url})') #dbg

#if already crawled and just need to convert

#since  no request to pull base_url from, will have to setenv it
#def nt2nq(fn,dir="nt"): #default ~hardcode, bc not sent in loop
def nt2nq(fn,dir=""): #use this dflt in ec.py in case no ./nt
    import os
    base_url= os.getenv('BASE_URL')
    if (not base_url):
        print("for now, need to: setenv BASE_URL ...")
    fnb=file_base(fn)
    #url=base_url + fnb.lstrip("nt") + "/" #hard coded 'dir'
    url=base_url + fnb.lstrip(dir) + "/"
    aptxt= f'<{url}> .'
    return append2everyline(fn,aptxt)

def all_nt2nq(dir):
    import glob
    get= dir + "/*.nt"
    ntfiles = glob.glob(get)
    for fn in ntfiles:
        #nt2nq(fn)
        print(nt2nq(fn))

#https://stackoverflow.com/questions/39274216/visualize-an-rdflib-graph-in-python
def rdflib_viz(url,ft=None): #or have it default to ntriples ;'turtle'
    if rdflib_inited==None:
        init_rdflib()
    import rdflib
    from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
    import networkx as nx
    import matplotlib.pyplot as plt 
    g = rdflib.Graph()
    if ft!=None:
        result = g.parse(url) #if didn't do mv, could send in format= 
    else:
        result = g.parse(url,format=ft)
    G = rdflib_to_networkx_multidigraph(result) 
    #stackoverflow.com/questions/3567018/how-can-i-specify-an-exact-output-size-for-my-networkx-graph
    #plt.figure(3,figsize=(12,12)) 
    plt.figure(3,figsize=(18,18)) 
    # Plot Networkx instance of RDF Graph
    pos = nx.spring_layout(G, scale=2)
    edge_labels = nx.get_edge_attributes(G, 'r')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    nx.draw(G, with_labels=True) 
    #if not in interactive mode for
    plt.show()

#still use above, although ontospy also allows for some viz
f_nt=None

#could load .nt as a tsv file, to look at if interested
def read_rdf(fn,ext=".tsv"):  #too bad no tabs though../fix?
    return read_file(fn,ext)
#consider using https://pypi.org/project/rdfpandas/

#if I ever get a chance, I'm going to go back to my more understandable /ld/repo/name format
#def urn2uri_(urn):  #looking for a more stable indicator
def urn2uri(urn): 
    "URN to backup store"
    if urn==None:
        return f'no-urn:{urn}'
    elif urn.startswith('urn:'):
        #url=urn.replace("urn:","http://141.142.218.86/",1).replace(":","/") ;gives///
        url=urn.replace(":","/").replace("urn","http://141.142.218.86",1)
        url += ".rdf"
        return url

#after ro_crate subset have all SO/dcat version 
#
def get_gID(): #could have arg that defaults to gName
  subj = "gID:" + gName.replace(".","") 
  return subj 

def get_collectionID(collectionName):
  subj=get_gID()
  collection= f'<{subj}/collection/{collectionName}>'
  return collection 

def set_collectionName(collectionName):
  rs= prefixes+ "prefix gID: https://sites.google.com/site/ \n " 
  subj = "gID:" + gName.replace(".","") #get_gID()
  search = f'<gID:search/{q}>'
  rs+= f'<{subj}> <so:searchAction> {search} \n '
  rs+= f'{search} <so:search> "{q}" \n '
  collection= f'<{subj}/collection/{collectionName}>' #get_collectionID(collectionName)
  rs+= f'<{subj}> <so:collection> {collection} \n '
  return rs 

#def set_collection_rows(collection,rows): #needs collection generated from set_collectionName right now
def set_collection_rows(collectionName,rows):
  row=rows[0] #will iterate over for all rows soon, a: row2d..
  u2=row2urn_url(row)
  urn,url=u2[0],u2[1] #will do other urls soon too
  uri=urn2uri(urn)
  collection=get_collectionID(collectionName) #if sent name vs final collection
  rs+= f'{collection} dcat:Dataset <{uri}> \n '
  rs+= f'<{uri}> dcat:Distribution <{u2[1]}> \n '
  return rs 

#This was in the gist above, but broke out parts above, so could call below w/less code
#if we want more of a breakdown, so can ask for user/agent's collections then it's ....
def rows2collection_(rows,collectionName):
  rs= prefixes+ "prefix gID: https://sites.google.com/site/ \n " 
  subj = "gID:" + gName.replace(".","") 
  search = f'<gID:search/{q}>'
  rs+= f'<{subj}> <so:searchAction> {search} \n '
  rs+= f'{search} <so:search> "{q}" \n '
  collection= f'<{subj}/collection/{collectionName}>'
  rs+= f'<{subj}> <so:collection> {collection} \n '
  row=rows[0] #will iterate over for all rows soon, a: row2d..
  u2=row2urn_url(row)
  urn,url=u2[0],u2[1] #will do other urls soon too
  uri=urn2uri(urn)
  rs+= f'{collection} dcat:Dataset <{uri}> \n '
  rs+= f'<{uri}> dcat:Distribution <{u2[1]}> \n '
  return rs 

#def rows2collection_nt(rows,collectionName): #could reuse above in parts & transform
def rows2collection(rows,collectionName): #redo above 1st
  rs1=set_collectionName(collectionName)
  rs2=set_collection_rows(collectionName,rows)
  return rs1+rs2 

#assertThese=rows2collection(rows,"my1")
#assertThese 

#
minio_backup= "http://141.142.218.86" #can also reset this global
#use w/oss
minio_prod= "https://oss.geodex.org" #minio
minio_dev_= "https://oss.geocodes.earthcube.org"
minio_dev="https://oss.geocodes-dev.earthcube.org/"
minio=minio_prod #but need to reset for amgeo in dev, would rather have all in one space, eg.just above

#summoned=jsonld milled=rdf=which is really .nt ;though gets asserted as quads /?
#def urn2uri(urn): #from wget_rdf, replace w/this call soon
def urn2urls(urn): #from wget_rdf, replace w/this call soon
    "way we map URNs ~now" #check on this w/the URN changes 
    if urn==None:
        return f'no-urn:{urn}'
    #if(urn!=None and urn.startswith('urn:')):
    elif urn.startswith('urn:'):
        #global f_nt
       #url=urn.replace(":","/").replace("urn","https://oss.geodex.org",1) #minio
        url=urn.replace(":","/").replace("urn",minio,1) #minio
      # urlroot=path_leaf(url) #file w/o path
        urlj= url + ".jsonld" #get this as well so can get_jsfile2dict the file
      # urlj.replace("milled","summoned")
        url += ".rdf"
        #cs= f'wget -a log {url}' 
        #os_system(cs)
        #cs= f'wget -a log {urlj}' 
        #os_system(cs)
        #return url, urlroot, urlj
        return url, urlj

#only urls of rdf not downloadable yet
def urn2fnt(urn):
    rdf_urls=urn2urls(urn)
    fnt=file_base(path_leaf(rdf_urls[0])) + ".nt"
    return fnt

def rdf2nt(urlroot_):
    "DFs rdf is really .nt, also regularize2dcat"
    urlroot=urlroot_.replace(".rdf","") #to be sure
    global f_nt
    fn1 = urlroot + ".rdf"
    fn2 = urlroot + ".nt" #more specificially, what is really in it
    #cs= f'mv {fn1} {fn2}' #makes easier to load into rdflib..eg: #&2 read into df
    cs= f'cat {fn1}|sed "/> /s//>\t/g"|sed "/ </s//\t</g"|sed "/doi:/s//DOI:/g"|cat>{fn2}'
    os_system(cs)   #fix .nt so .dot is better ;eg. w/doi
    f_nt=fn2
    return fn2
##
def is_node(url): #not yet
    return (url.startswith("<") or url.startswith("_:B"))

#def is_tn(url):
def tn2bn(url):
    "make blaze BNs proper for .nt"
    if url.startswith("t1"):
        return url.replace("t1","_:Bt1")
    else:
        return url

def cap_http(url):
    "<url>"
    if is_http(url):
        return f'<{url}>'
    else:
        return url

def cap_doi(url):
    "<doi>"
    if url.startswith("doi:"):
        return f'<{url}>'
    elif url.startswith("DOI:"):
        return f'<{url}>'
    else:
        return url

def fix_url3(url):
    "cap http/doi tn2bn"
    url=tn2bn(url)
    url=cap_http(url)
    url=cap_doi(url)
    #could put is_node check here
    return url

#def fix_url_(url,obj=True): #should only get a chance to quote if the obj of the triple
def fix_url(url):
    "fix_url and quote otherwise"
    if is_node(url):
        return url
    elif url.startswith("t1"):
        return url.replace("t1","_:Bt1")
    elif is_http(url):
        return f'<{url}>'
    elif url.startswith("doi:"):
        return f'<{url}>'
    elif url.startswith("DOI:"):
        return f'<{url}>'
    #elif obj:
    else:
        import json
        return json.dumps(url)
    #else:
    #    return url

def df2nt(df,fn=None):
    "print out df as .nt file"
    import json
    if fn:
        put_txtfile(fn,"")
    for index, row in df.iterrows():
        #s=row['s']
        s=df["s"][index]
        s=fix_url(s)
        s=fix_url(s)
        p=df["p"][index]
        p=fix_url(p)
        o=df["o"][index]
        o=fix_url(o)
        if o=="NaN":
            o=""
        str3=f'{s} {p} {o} .\n'
        if dbg:
            print(str3)
        if fn:
            put_txtfile(fn,str3,"a")
        #need to finish up w/dumping to a file
    return df

def get_rdf(urn,viz=None):
    "start of replacement for wget_rdf" #that doesn't need the ld cache
    df=get_graph(urn)
    df2nt(df)
    if viz: #should fix this below 
        fn2=urn_leaf(urn) + ".nt" #try tail
        rdflib_viz(fn2) #find out if can viz later as well via hidden .nt file
    return df #already returns the same as wget_rdf

def get_rdf2nt(urn):
    "get and rdf2nt" #rdf2nt was getting around df's naming, will be glad to get away from that cache
    df=get_rdf(urn)
    fn2=urn_leaf(urn) # + ".nt" 
    append2allnt(fn2)
    fn2 = fn2 + ".nt"
    return df2nt(df,fn2) #seems to work w/a test urn
    #return df2nt(df)
##
#take urn2uri out of this, but have to return a few vars
def wget_rdf(urn,viz=None):
    if not viz:
        return get_rdf2nt(urn) #use get_graph version for now
    if urn==None:
        return f'no-urn:{urn}'
    #if(urn!=None and urn.startswith('urn:')):
    elif urn.startswith('urn:'):
        global f_nt
 #      url=urn.replace(":","/").replace("urn","https://oss.geodex.org",1)
 #      urlroot=path_leaf(url) #file w/o path
 #      urlj= url + ".jsonld" #get this as well so can get_jsfile2dict the file
 #      urlj.replace("milled","summoned")
 #      url += ".rdf"
        #url, urlroot, urlj = urn2uri(urn) #so can reuse this, also getting sys change/fining missing in minio
        url, urlj = urn2urls(urn) #so can reuse this, also getting sys change/fining missing in minio
        urlroot=path_leaf(url) #file w/o path
        cs= f'wget -a log {url}' 
        os_system(cs)
        cs= f'wget -a log {urlj}' 
        os_system(cs)
      # fn1 = urlroot + ".rdf"
      # fn2 = urlroot + ".nt" #more specificially, what is really in it
      # #cs= f'mv {fn1} {fn2}' #makes easier to load into rdflib..eg: #&2 read into df
      # cs= f'cat {fn1}|sed "/> /s//>\t/g"|sed "/ </s//\t</g"|sed "/doi:/s//DOI:/g"|cat>{fn2}'
      # os_system(cs)   #fix .nt so .dot is better ;eg. w/doi
      # f_nt=fn2
        rdf2nt(urlroot)
        #from rdflib import Graph
        #g = Graph()
        #g.parse(fn2)
        if viz: #can still get errors
            fn2=urn_leaf(urn) #try new
            rdflib_viz(fn2) #.nt file #can work, but looks crowded now
        return read_rdf(f_nt)
    elif urn.startswith('/'):
        url=urn.replace("/","http://geocodes.ddns.net/ld/",1).replace(".jsonld",".nt",1)
        urlroot=path_leaf(url) #file w/o path
        #url += ".nt"
        cs= f'wget -a log {url}' 
        os_system(cs)
        #fn2 = urlroot + ".nt" #more specificially, what is really in it
        if viz: #can still get errors
            #rdflib_viz(fn2) #.nt file #can work, but looks crowded now
            rdflib_viz(urlroot) #.nt file #can work, but looks crowded now
        return read_rdf(f_nt)
    else:
        return f'bad-urn:{urn}'

#rdf_inited=None
def init_rdf():
    #cs='apt-get install raptor2-utils graphviz'
    cs='apt-get install raptor2-utils graphviz libmagic-dev' #can add jq yourself
    os_system(cs)  #incl rapper, can do a few rdf conversions
    rdf_inited=cs

#should just put sparql init in w/rdf _init, as not that much more work

#sparql_inited=None
def init_sparql():
    #cs='pip install sparqldataframe simplejson'
    cs='pip install sparqldataframe simplejson owlready2'
    os_system(cs)
    sparql_inited=cs
    ##get_ec("http://mbobak-ofc.ncsa.illinois.edu/ext/ec/nb/sparql-query.txt")
    #get_ec("https://raw.githubusercontent.com/MBcode/ec/master/NoteBook/sparql-query.txt")
    #return get_txtfile("sparql-query.txt")
    return get_query_txt()

#-
def dfn(fn):
    "FileName or int:for:d#.nt"
    if isinstance(fn, int):
        fnt=f'd{fn}.nt'
    else:
        fnt=fn
    return fnt
#-
def sq_file(sq,fn=1):
    fnt=dfn(fn) #maybe gen fn from int
    add2log(f'dataFN={fnt}')
    add2log(f'qry={sq}')
    if sparql_inited==None:
        si= init_sparql()  #still need to init
    #global default_world
    #from owlready2 import *
    import owlready2 as o2
    #o= o2.get_ontology("d1.nt").load()
    o= o2.get_ontology(fnt).load()
    return list(o2.default_world.sparql(sq))
#-
def pp_l2s(pp,js=None):
    "predicatePath list2str"
    if(js): #["spatialCoverage" "geo" "box" ], True  -> "spatialCoverage.geo.box"
        return "." + ".".join(pp)
    else: #["spatialCoverage" "geo" "box" ]  -> ":spatialCoverage/:geo/:box"
        return ":" + "/:".join(pp)

def rget(pp,fn=1):
    "predicate path to s/o values"
    fnt=dfn(fn)
#r=sq_file("PREFIX : <http://www.w3.org/ns/dcat#> SELECT distinct ?s ?o WHERE  { ?s :spatialCoverage/:geo/:box ?o}","d1.nt")
    #s1="PREFIX : <http://www.w3.org/ns/dcat#> SELECT distinct ?s ?o WHERE  { ?s "
    s1="PREFIX : <https://schema.org/> SELECT distinct ?s ?o WHERE  { ?s " #till fix sed
    s2=" ?o}"
    #r=sq_file(s1 + ":spatialCoverage/:geo/:box" + s2,dfn)
    pps=pp_l2s(pp)
    qs=s1 + pps + s2
    print(qs)
    #add2log(f'rget:{qs}')
    add2log(f'rget:{qs},{fnt}')
    r=sq_file(qs,fnt)
    return r
#-
def grep_po_(p,fn):
  "find predicate in nt file and returns the objects"
  #cs= f"grep '{p}' {fn}|cut -f 3"
  cs= f"grep '{p}' {fn}|cut -d' ' -f 3"
  rs= os_system_(cs)
  #ra=rs.split(" .\n")
  ra=rs.split("\n")
  ra=list(map(lambda x: x.strip(".").strip(" "), ra))[:-1]
  return ra #get rid of these

def grep_po(p,fn):
  "find predicate in nt file and returns the objects"
  cs= f"egrep '{p}' {fn}|cut -f 3"
  #cs= f"grep '{p}' {fn}|cut -d' ' -f 3"
  rs= os_system_(cs)
  ra=rs.split(" .\n")
  return ra
#could ret the Predicate,Object,(lists)and pred(s) could be the 2nd return
#unless where to call it grep_p2o or grep_pred2obj
#def grep_pred2obj(p,fn):
def grep2obj(p,fn): #=f_nt): #fn could default to (global) f_nt
  "find pattern in nt file and returns the objects, of the spo lines"
  cs= f"egrep '{p}' {fn}|cut -f 3"
  rs= os_system_(cs)
  #ra=rs.split(" .\n")
  ra=rs.split(".\n")
  if ra:
      ra=list(map(lambda x: x.strip().replace('"',''), ra))
  return ra
#get pack to using a local store, to be more robust
#def urn2accessURL(urn):
def urn2accessURL(urn,fnt=None):
    "get access/content url from urn/it's .nt file"
    if not fnt:
        fnt=urn2fnt(urn) #should be same as f_nt
    print(f'grep2obj:{fnt}')
    return grep2obj('accessURL|contentUrl',fnt)
#to iterate over this could have a getDatasetURLs &either give URNs or  ROWs&dfSPARQL
def getDatasetURLs(IDs,dfS=None):
  "return the URLs from every dataset given, by URNs or df w/rows"
  d1p= not isinstance(IDs[0], int)
  ds_urls= list(map(urn2accessURL,IDs)) if d1p else list(map(lambda row: dfRow2urls(dfS,row),IDs))  #or put in another row number to get url
  #ds_url= list(map(lambda urls: urls[0],ds_urls)) if d1p else list(map(lambda urls: urls[row][1], ds_urls)) #default to 1st of the urls
  ds_url= list(map(lambda urls: urls[0],ds_urls)) #default to 1st of the urls ;need to check in 2nd/sparql_nb w/o collection
  return ds_urls, ds_url #1st of each right now
#-might want to collect/order by file types
def sparql_f2(fq,fn,r=None): #jena needs2be installed for this, so not in NB yet;can emulate though
    "files: qry,data"
    if r: #--results= Results format (Result set: text, XML, JSON, CSV, TSV; Graph: RDF serialization)
        rs=f' --results={r} '
    else:
        rs=""
    fnt=dfn(fn) #maybe gen fn from int
    #if had txt put_txtfile; if qry.txt w/var then have2replace
    cs=f'sparql --data={fnt} --query={fq} {rs}'
    return os_system_(cs)

#-
#def nt2dn(fn,n):
def nt2dn(fn=f_nt,n=1):
    ".nt to d#.nt where n=#, w/http/s schema.org all as dcat" 
    fdn= f'd{n}.nt'
    #fnd=dfn(fn) #maybe gen fn from int
    cs=f'cat {fn}|sed "/ht*[ps]:..schema.org./s//http:\/\/www.w3.org\/ns\/dcat#/g"|cat>{fdn}'  #FIX
    os_system(cs) #this makes queries a LOT easier
    return fdn

def df2URNs(df):
  return df['g']

def dfRow2urn(df,row):
  URNs=df2URNs(df)
  return URNs[row]

def urn2rdf(urn,n=1):
    df=wget_rdf(urn)
    global f_nt
    nt2dn(f_nt,n)
    return df

def dfRow2rdf(df,row):
    urn=dfRow2urn(df,row)
    return urn2rdf(urn,row)

def dfRow2urls(df,row): 
    fnt=dfn(row) #check if dfRow2rdf already done
    from os.path import exists #can check if cached file there
    if not exists(fnt):
        dfRow2rdf(df,row)
    return rget(["contentUrl"],row)

def nt2g(fnt):
    from rdflib import ConjunctiveGraph #might just install rdflib right away
    g = ConjunctiveGraph(identifier=fnt)
    data = open(fnt, "rb") #or get_textfile -no
    g.parse(data, format="ntriples")
    return g

#def diff_nt(fn1,fn2):
def diff_nt_g(fn1,fn2):
    #import rdflib
    from rdflib.compare import to_canonical_graph, to_isomorphic, graph_diff
    g1=nt2g(fn1)
    g2=nt2g(fn2)
    iso1 = to_isomorphic(g1)
    iso2 = to_isomorphic(g2)
    if iso1 == iso2:
        return g, None, None
    else:
        in_both, in_first, in_second = graph_diff(iso1, iso2)
        #dump_nt_sorted(in_both)
        #dump_nt_sorted(in_first)
        #dump_nt_sorted(in_second)
        return in_both, in_first, in_second 

#https://github.com/RDFLib/rdflib/blob/master/rdflib/compare.py

def dump_nt_sorted(g):
    for l in sorted(g.serialize(format='nt').splitlines()):
        if l: print(l.decode('ascii'))

#fix: rdflib/plugins/serializers/nt.py:28: UserWarning: NTSerializer does not use custom encoding.
 #warnings.warn("NTSerializer does not use custom encoding.")

def diff_nt(fn1,fn2):
    in_both, in_first, in_second = diff_nt_g(fn1,fn2)
    if in_both:
        print(f'in_both:{in_both}')
        dump_nt_sorted(in_both)
    if in_first:
        print(f'in_first:{in_first}')
        dump_nt_sorted(in_first)
    if in_second:
        print(f'in_second:{in_second}')
        dump_nt_sorted(in_second)
    return in_both, in_first, in_second 


def pp2so(pp,fn): #might alter name ;basicly the start of jq via sparql on .nt files
    "SPARQL qry given a predicate-path, ret subj&obj, given nt2dn run 1st, giving fn"
    fnt=dfn(fn) #maybe gen fn from int
    #pp=":spatialCoverage/:geo/:box"
    #sq=f'PREFIX : <http://www.w3.org/ns/dcat#> \n SELECT distinct ?s ?o WHERE { ?s {pp} ?o }'
    sqpp="""PREFIX : <http://www.w3.org/ns/dcat#>
        SELECT distinct ?s ?o
        WHERE { ?s predicate-path ?o }"""
    sq=sqpp.replace("predicate-path",pp)
    add2log(f'fn={fn},sq={sq}')
    if rdf_inited==None:
        init_rdf()
    from rdflib import ConjunctiveGraph #might just install rdflib right away
    g = ConjunctiveGraph(identifier=fnt)
    data = open(fnt, "rb") #or get_textfile -no
    g.parse(data, format="ntriples")
    results = g.query(sq)
    add2log(results) #runs but still need2check output../fix
    return [str(result[0]) for result in results]

def rdfxml2nt(fnb):
    if has_ext(fnb):
        fnb=file_base(fnb)
    if rdf_inited==None:
        init_rdf()
    cs= f'rapper -i rdfxml -o ntriples {fnb}.nt|cat>{fnb}.nt'
    os_system(cs) 

def nt2svg(fnb):
    if has_ext(fnb):
        fnb=file_base(fnb)
    if rdf_inited==None:
        init_rdf()
    cs= f'rapper -i ntriples -o dot {fnb}.nt|cat>{fnb}.dot'
    os_system(cs) 
    cs= f'dot -Tsvg {fnb}.dot |cat> {fnb}.svg'
    os_system(cs)

#re/consider running sed "/https/s//http/g" on the .nt file, as an option, 
 #for cases were it's use as part of the namespace is inconsistent


#https://stackoverflow.com/questions/30334385/display-svg-in-ipython-notebook-from-a-function
def display_svg(fn):
    if rdf_inited==None:
        init_rdf()
    from IPython.display import SVG, display
    display(SVG(fn))

def append2allnt(fnb):
    cs= f'cat {fnb}.nt >> .all.nt'
    os_system(cs) 

def nt_viz(fnb=".all.nt"):
    if fnb==".all.nt" and f_nt!=None and os.path.isfile(f_nt):
        fnb=f_nt  #if have urn .nt file, &nothing run yet, can call w/o arg&will view it
    if has_ext(fnb):
        fnb=file_base(fnb)
    nt2svg(fnb) #base(before ext)of .nt file, makes .svg version&displays
    fns= fnb + ".svg"
    display_svg(fns)
    if fnb!=".all":
        append2allnt(fnb)

def rdfxml_viz(fnb): #cp&paste (rdf)xml file paths from in .zip files
    xml2nt(fnb)
    nt_viz(fnb)

#this could be generalized further to display available views of the DataFrame as well
 #so might call this viz_rdf & the other viz_df, but still have viz that can figure that out
def viz(fn=".all.nt"): #might call this rdf_viz once we get some other type of viz going
    if has_ext(fn):
        ext=file_ext(fn)
        fnb=file_base(fn) #unused, bc they should strip the ext anyway
    else:
        return "need a file extension, to know which routines to run to show it"
    if ext==".nt":
        nt_viz(fn)
    elif ext=='.xml':
        rdfxml_viz(fn)
    else:
        return "only handle .nt and .xml (rdf) right now"

#should change os version of wget to request so can more easily log the return code
 #maybe, but this is easiest way to get the file locally to have to use
  #though if we use a kglab/sublib or other that puts right to graph, could dump from that too
host = "http://141.142.218.86:3031"
#import requests

def alive():
    import requests
    r = requests.get(f'{host}/alive')
    return r

def log_msg(url): #in mknb.py logbad routed expects 'url' but can encode things
    import requests
    r = requests.get(f'{host}/logbad/?url={url}')
    return r 

#add 'rty'/error handling, which will incl sending bad-download links back to mknp.py
 #log in the except sections, below

#def check_size_(fs,df): #earlier now unused version
#    if fs:
#        if fs<300:
#            df+= "[Warn:small]"
#    else:
#        df+= "[Warn:No File]"
#    return df

def check_size(fs,df):
    "FileSize,DataFrame as ret txt"
    dfe=None
    if fs:
        if fs<300:
            dfe= "[Warn:small]"
    else:
        dfe= "[Warn:No File]"
    if dfe:
        add2log(dfe)
        log_msg(dfe) #should incl url/etc but start w/this
        df+=dfe
    return df

#considter ext2ft taking the longer-txt down to the stnd file-ext eg. .tsv ..

def nt2ft(url): #could also use rdflib, but will wait till doing other queries as well
    "path2 .nt file -> encoding~FileType"
    cs=f"grep -A4 {url} *.nt|grep encoding|cut -d' ' -f3"
    if cs:
        return os_system_(cs) 
    else:
        return None

def file_type(fn):
    from os.path import exists 
    import magic
    if exists(fn):
        add2log(magic.from_file(fn))
        mt=magic.from_file(fn, mime = True)
    else:
        mt="file not found"
    add2log(f'{fn},mime:{mt}')
    return mt
#get something that can look of header of download, before get the file, too

#def read_file(fnp, ext=nt2ft(fnp)):  $should send 'header' in
def read_file(fnp, ext=None):  #download url and ext/filetype
    "can be a url, will call pd read_.. for the ext type"
    import pandas as pd
    import re
    if rdf_inited==None: #new, going to need it
        init_rdflib()
        init_rdf()
    if(ext==None): #find filetype from .nt ecodingFormat
        ext=nt2ft(fnp)
    fn=fnp.rstrip('/') #only on right side, for trailing slash, not start of full pasted path
    fn1=path_leaf(fn) #just the file, not it's path
    fext=file_ext(fn1) #&just it's .ext
    #url = fn
    if(ext!=None):
        if ext.startswith('.'):
            ft=ext
        else:
            ft="." + ext
    else: #use ext from fn
        ft=str(fext)
        ext=ft
    df=""
    #bad_lines going away, get netcdf etc in here, even though I don't see it much
    if ext==None and len(ft)<1:
        wget(fn)
        df="no fileType info, doing:[!wget $url ],to see:[ !ls -l ] or FileExplorerPane on the left"
    elif ft=='.tsv' or re.search('tsv',ext,re.IGNORECASE) or re.search('tab-sep',ext,re.IGNORECASE):
        try:
            #df=pd.read_csv(fn, sep='\t',comment='#',warn_bad_lines=True, error_bad_lines=False)
            #df=pd.read_csv(fn, sep='\t',comment='#',warn_bad_lines=True, on_bad_lines='skip')
            df=pd.read_csv(fn, sep='\t',comment='#', on_bad_lines='skip')
            #df=pd.read_csv(fn, sep='\t',comment='#')
        except:
            df = str(sys.exc_info()[0])
            pass
    elif ft=='.csv' or re.search('csv',ext,re.IGNORECASE):
        try:
            #df=pd.read_csv(fn,comment="#",warn_bad_lines=True, error_bad_lines=False)
            df=pd.read_csv(fn,comment='#', on_bad_lines='skip')
            #df=pd.read_csv(fn,comment="#")
        except:
            df = str(sys.exc_info()[0])
            pass
    elif ft=='.txt' or re.search('text',ext,re.IGNORECASE): #want to be able to header=None here
        try:
            df=pd.read_csv(fn, sep='\n',comment='#')
        except:
            df = str(sys.exc_info()[0])
            pass
    elif ft=='.json' or re.search('js',ext,re.IGNORECASE):
        try:
            print(f'read_json({nf}')
            df=pd.read_json(fn)
        except:
            df = str(sys.exc_info()[0])
            pass
    elif ft=='.html' or re.search('htm',ext,re.IGNORECASE):
        try:
            df=pd.read_html(fn)
        except:
            df = str(sys.exc_info()[0])
            pass
    elif ft=='.zip' or re.search('zip',ext,re.IGNORECASE):
        ft='.zip'
        fs=wget_ft(fn,ft)
        #fs=os.path.getsize(fnl) #assuming it downloads w/that name
#       df=pd.read_csv(fn, sep='\t',comment='#')
        #df="can't read zip w/o knowing what is in it, doing:[!wget $url ],to see:[ !ls -l ]"
        df=f'can not read zip w/o knowing what is in it, doing:[!wget $url ],to see:[ !ls -l ]size:{fs} or FileExplorerPane on the left'
        file_type(fn1) #save2 mt and use, next
        #if fs and fs<300:
        #    df+= "[Warn:small]"
        df=check_size(fs,df)
    else:
        fs=wget_ft(fn,ft)
        #fs=os.path.getsize(fnl) #assuming it downloads w/that name
        #df="no reader, can !wget $url"
        df=f'no reader, doing:[!wget $url ],to see:[ !ls -l ]size:{fs} or FileExplorerPane on the left'
        file_type(fn1) #save2 mt and use, next
        #if fs and fs<300:
        #    df+= "[Warn:small]"
        df=check_size(fs,df)
    #look into bagit next/maybe, also log get errors, see if metadata lets us know when we need auth2get data
    #if(urn!=None): #put here for now
    #    wget_rdf(urn)
    return df

 #probably drop the [ls-l] part&just have ppl use fileBrowser, even though some CLI would still be good
#not just 404, getting small file back also worth logging
#---- sources:
def get_sources_csv(url="https://raw.githubusercontent.com/MBcode/ec/master/crawl/sources.csv"):
    return get_ec_txt(url)

def get_sources_df(url="https://raw.githubusercontent.com/MBcode/ec/master/crawl/sources.csv"):
    s= read_file(url,".csv")
    return s.loc[s['Active']] #can only crawl the active ones

#def get_sources_urls(): #could become crawl_
def crawl_sources_urls(): #work on sitemap lib to handle non-stnd ones
    import re
    s=get_sources_df()
    for url in s['URL']:
        print(f'sitemap:({url})') #dbg
        #urlb=re.sub('\/site*.xml','',url)
        urlb=re.sub('sitemap.xml','',url)
        #crawl_sitemap(urlb)
        print(f'crawl_sitemap({urlb})') #dbg
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
    if sparql_inited==None:
        si= init_sparql()  #still need to init
        #qs= iqt #or si  #need q to instantiate
    #add2log(iqt)
    global dflt_endpoint
    if not endpoint:
        endpoint=dflt_endpoint
    add2log(f'query:{iqt}')
    add2log(f'endpoint:{endpoint}')
    df = sparqldataframe.query(endpoint, iqt)
    return df

def v4qry(var,qt):
    "var + query-type 2 df"
    sqs = eval("get_" + qt + "_txt()") #get_  _txt   fncs, are above
    iqt = v2iqt(var,sqs)
    #add2log(iqt) #logged in next fnc
    return iqt2df(iqt)

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

def get_summary(g): #g not used but could make a version that gets it for only 1 graph
    "return summary version of all the graphs quads"
    return v4qry(g,"summary")


#summary_endpoint = dflt_endpoint.replace("earthcube","summary")
#def txt_query_(q,endpoint=None):
def txt_query_(q,endpoint=None):
    "or can just reset dflt_endpoint"
    global dflt_endpoint
    if not endpoint:
        df=txt_query(q)
    elif endpoint=="summary": #1st try for summary query
        save = dflt_endpoint #but do not do till can switch the qry as well
        dflt_endpoint = dflt_endpoint.replace("earthcube","summary")
        print(f'summary:txt_query,w/:{dflt_endpoint}')
        df=txt_query(q)
        dflt_endpoint = save
    else:
        save = dflt_endpoint
        dflt_endpoint = endpoint
        print(f'txt_query,w/:{dflt_endpoint}')
        df=txt_query(q)
        dflt_endpoint = save
    return df

#def get_graphs_list(endpoint=None):
def get_graphs_list(endpoint=None,dump_file=None):
    "get URNs as list, can send in alt endpoint"
    global dflt_endpoint
    if not endpoint:
        dfg=get_graphs()
    else:
        save = dflt_endpoint
        dflt_endpoint = endpoint
        dfg=get_graphs()
        dflt_endpoint = save
    if dump_file:
        dfg.to_csv(dump_file)
    return dfg['g'].tolist()

def get_graphs_cache(endpoint="http://ideational.ddns.net:9999/bigdata/namespace/nabu/sparql",dumpfile=None):
    print(f'get_graphs_cache:{endpoint}')
    l= get_graphs_list(endpoint)
    if dumpfile:
        list2txtfile(dumpfile,l)
    return l

def get_graphs_lon(repo=None,endpoint="http://ideational.ddns.net:3040/all/sparql"): 
    "for when I host a repo w/fuseki testing"
    endpnt= endpoint if repo==None else endpoint.replace("all",repo)
    print(f'get_graphs_lon:{endpnt}')
    return get_graphs_list(endpnt)

#def get_graph_per_repo(grep="milled",endpoint=None,dump_file="graphs.csv"): #try w/(None, ncsa_endpoint)
def get_graph_per_repo(grep="milled",endpoint="https://graph.geodex.org/blazegraph/namespace/earthcube/sparql",dump_file="graphs.csv"):
    "dump a file and sort|uniq -c out the repo counts"
    gl=get_graphs_list(endpoint,dump_file) #this needs full URN to get counts for the same 'repo:' s
    gn=len(gl)
    print(f'got:{gn} graphs')
    if grep != "milled":
        cs=f"cut -d':' -f2- {dump_file} |cut -d'/' -f1 | sort | uniq -c |sort -n" #this is for my ld-cache
    else:
        cs=f"cut -d':' -f3,4 {dump_file} | grep milled | sort | uniq -c |sort -n" #this is for gleaner milled..
    return os_system_(cs)

def urn_tail(urn):
    "like urn_leaf"
    return  urn if not urn else urn.split(':')[-1]

def urn_tails(URNs):
    return list(map(lambda s: s if not s else s.split(':')[-1],URNs))
    #return list(map(urn_tail,URNs))

def get_graphs_tails(endpoint):
    "just the UUIDs of the URNs in the graph"
    URNs=get_graphs_list(endpoint)
    return urn_tails(URNs)

#should get graph.geo.. from https://dev.geocodes.earthcube.org/#/config dynamically
 #incl the default path for each of those other queries, ecrr, ;rdf location as well
#=========append fnc from filtereSPARQLdataframe.ipynb
#def sq2df(qry_str):
#def txt_query(qry_str): #consider sending in qs=None =dflt lookup as now, or use what sent in
def txt_query(qry_str,sqs=None): #a generalized version would take pairs/eg. <${g}> URN ;via eq urn2graph
    "sparql to df"
    if sparql_inited==None:
        #qs=init_sparql()  #does: get_query_txt &libs
        si= init_sparql()  #still need to init
        #qs= sqs or init_sparql()  
        qs= sqs or si
    else:
        #qs=get_txtfile("sparql-query.txt")
        qs= sqs or get_txtfile("sparql-query.txt")
    import sparqldataframe, simplejson
    #endpoint = "https://graph.geodex.org/blazegraph/namespace/nabu/sparql"
    #endpoint = "https://graph.geocodes.earthcube.org/blazegraph/namespace/earthcube/sparql"
    global dflt_endpoint
    endpoint = dflt_endpoint
    add2log(qry_str)
    q=qs.replace('${q}',qry_str)
    add2log(q)
    #q=qs.replace('norway',qry_str) #just in case that is still around
    #q=qs
    #print(f'q:{q}')
    df = sparqldataframe.query(endpoint, q)
    #df.describe()
    return df

#==w/in-search-related-data: https://github.com/MBcode/ec/blob/master/qry/rec.py
#import pandas as pd
#import numpy as np
#import simplejson
#import sparqldataframe
#from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.metrics.pairwise import cosine_similarity
cosine_sim=None

def get_subj_from_index(index):
    return df[df.index == index]["subj"].values[0]

def get_index_from_subj(subj):
    return df[df.subj == subj]["index"].values[0]

def combine_features(row):
    try:
        return row['kw'] +" "+row['name']+" "+row["description"]+" "+row["pubname"]
    except:
        print("Error:", row)

def get_related(likes):
    global cosine_sim
    #movie_user_likes = "Avatar"
    #should pick one of the ones from the df randomly, or can do them all 
    #movie_user_likes = "https://www.bco-dmo.org/dataset/752737"
    ## Step 6: Get index of this movie from its subj
    dataset_index = get_index_from_subj(likes)
    similar_datasets =  list(enumerate(cosine_sim[dataset_index]))
    ## Step 7: Get a list of similar movies in descending order of similarity score
    sorted_similar_datasets = sorted(similar_datasets,key=lambda x:x[1],reverse=True)
    ## Step 8: Print subjs of first 50 movies
    i=0
    for element in sorted_similar_datasets:
        print(get_subj_from_index(element[0]))
        i=i+1
        if i>50:
            break
    return sorted_similar_datasets

def get_related_indices(like_index):
    "return a list of indices that are related to input index"
    global cosine_sim
    similar_indices =  list(enumerate(cosine_sim[like_index]))
    sorted_similar = sorted(similar_indices,key=lambda x:x[1],reverse=True)
    #return sorted_similar
    return list(map(first,sorted_similar))

def dfCombineFeaturesSimilary(df, features = ['kw','name','description','pubname']):
    "run only once per new sparql-df"
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    global cosine_sim
    df.insert(0,'index',range(0,len(df)))
    df.set_index('index')
    df["combined_features"] = df.apply(combine_features,axis=1)
    ##Step 4: Create count matrix from this new combined column
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df["combined_features"])
    terms=cv.get_feature_names() #new for topic-modeling
    tl=len(terms)
    print(f'topic-terms:{tl}')
    ##Step 5: Compute the Cosine Similarity based on the count_matrix
    cosine_sim = cosine_similarity(count_matrix) 

#=so after sparql-nb: df=txt_query(q)
#can dfCombineFeaturesSimilary(df)
#then get_related_indices(row)
#=I should also write other fnc to access rows of txt_query df returns, to get possible donwloads
def test_related(q,row=0): #eg "Norway"
    df=txt_query(q)
    dfCombineFeaturesSimilary(df)
    return get_related_indices(row)
#but sparql-nd will already have the df calculated, so just do the similarity-matrix for it once, 
 #then call get_related_indices for each dataset/row you want to look at, or can now use:
def show_related(df,row):  #after dfCombineFeaturesSimilary is run on your df 'sparql results'
    #main=df['description'][row].strip() #this should be in the related-df
    #print(f'related to row={row},{main}')
    related=get_related_indices(row)
    if len(df)<4:
        print("not many to compare with")
    for ri in related:
        des=df['description'][ri].strip()
        print(f'{ri}:{des}')

#-------------------------------------------------------------
#convert a jsonld record to a minimal crate ;started in j2c.py
crate_top = """
{ "@context": "https://w3id.org/ro/crate/1.1/context",
  "@graph": [
    {
        "@type": "CreativeWork",
        "@id": "ro-crate-metadata.json",
        "conformsTo": {"@id": "https://w3id.org/ro/crate/1.1"},
        "about": {"@id": "./"}
  },  
  {
    "@id": "./",
    "@type": [
      "Dataset"
    ],
    "hasPart":  
    """
#then all "@id": ...  ;w/, btwn
crate_middle = "},"
#then all distribution records w/"@id": ... inserted  ;w/, btwn
crate_bottom = "]}"

#now given a filename, load in the jsonld, and find the distribution
# go over that array, and make the ..url into @id's that will also go w/in the hasPart

def get_distr_dicts(fn):
    "distribution dictionary/s"
    d=get_jsfile2dict(fn)
    return d.get("distribution")

def add_id(d): #there will be other predicates to check
    "set @id as (access)url"
    u=d.get("dcat:accessURL")
    d["@id"]=u
    return d

def get_id(d):
    return d.get("@id")

def get_idd(d):
    "dict of @id value, for hasPart[]"
    id=d.get("@id")
    dr={}
    dr["@id"]=id
    return dr

#jsonld to minimal ro-crate
#started by iterativly changing the distribution, then get IDs out for hasPart
def jld2crate(fn):
    print(crate_top)
    #d=get_distribution(fn)
    dl=get_distr_dicts(fn)
    #for d in dl: #needs a comma btwn
    #    print(json.dumps(d))
    dl2=list(map(add_id,dl))
    ids=list(map(get_idd,dl))
    print(json.dumps(ids))
    print(crate_middle)
    print(json.dumps(dl2))
    print(crate_bottom)

def jld2crate_(fn):
    mkdir("roc") #for now
    fn_out="roc/" + fn
    put_txtfile(fn_out,crate_top)
    dl=get_distr_dicts(fn)
    dl2=list(map(add_id,dl))
    ids=list(map(get_idd,dl))
    put_txtfile(fn_out,json.dumps(ids))
    put_txtfile(fn_out,crate_middle)
    put_txtfile(fn_out,json.dumps(dl2))
    put_txtfile(fn_out,crate_bottom)

#so can take URN jsonld and make a crate, still need the URNs though
#tests on http://geocodes.ddns.net/ld/iedadata/324529.jsonld will take these out
def t1():
    jld2crate("324529.jsonld")

def t2(fn="324529.jsonld"):
    jld2crate_(fn)
#if we stay w/python /need to run on all
#I will have it put to files, w/more checks
#&use alt predicates for the @id if needed

#Still should add URN as another entry in crate
 #which is something gleaner generated
 #I wish we could use(a version of)the download url
 #and then we would all know what to expect w/o 
  #depending on some centeral rand#generator

#blabel: take a triple file w/every line ending in " ." and use filename to make a quad, needed for gleaner/testing
#potentially useful elsewhere; eg. if added repo: could use this in my workflow to make quads
#DF's gleaner uses the shah of the jsonld to name the .rdf files which are actually .nt files
# but then there are lots of .nq files that are actually .nt files, but should be able to get them w/this
#maybe someplace in nabu this is done, but by then I can't have the files to load them

#use filename to convert .rdf file to a .nq file
#▶<102 a09local: /milled/geocodes_demo_datasets> mo 09517b808d22d1e828221390c845b6edef7e7a40.rdf
#_:bcbhdkms5s8cef2c4s7j0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://schema.org/Dataset> .
#goes to:
#_:bcbhdkms5s8cef2c4s7j0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://schema.org/Dataset> "urn:09517b808d22d1e828221390c845b6edef7e7a40".
#fn = "09517b808d22d1e828221390c845b6edef7e7a40.rdf"

#https://stackoverflow.com/questions/3675318/how-to-replace-the-some-characters-from-the-end-of-a-string
def replace_last(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail

#def fn2nq(fn): #from 2nq.py
def nt_fn2nq(fn): #already a nt2nq
    "take a fn.* returns a fn.nq w/4th col urn:fn"
    fnb = file_base(fn)
    fn2 = fnb + ".nq"
    replace_with = f' <urn:{fnb}> .'
    with open(fn2,'w') as fd_out:
        with open(fn,'r') as fd_in:
            for line in fd_in:
                #line_out = line.replace(" .",f' "urn:{fnb}" .')
                #replace_with = f' "urn:{fnb}" .'
                ll=len(line)
                if ll>9:
                    line_out = replace_last(line, " .", replace_with)
                    fd_out.write(line_out)
    return fn2

#could do w/read_rdf then insert fn into 4th column
 #then w/recipy could generate a shah that is tracked by it's prov like system

def riot2nq(fn):
    "process .jsonld put out .nq"
    fnb = file_base(fn)
    fn2 = fnb + ".nq"
    replace_with = f' <urn:{fnb}> .'
    nts = os_system_(f'riot --stream=nt {fn}')
    fd_in = nts.split("\n") 
    lin=len(fd_in)
    print(f'got {lin} lines')
    with open(fn2,'w') as fd_out:
        for line in fd_in:
            ll=len(line)
            if ll>9:
                line_out = replace_last(line, " .", replace_with)
                fd_out.write(line_out)
                fd_out.write('\n')
    return fn2

def to_nq(fn):
    "process .jsonld put out .nq"
    fnb = file_base(fn)
    fn2 = fnb + ".nq"
    if exists(fn2):
        print(f'riot2nq:{fn2} already there')
    replace_with = f' <urn:{fnb}> .'
   #nts = os_system_(f'riot --stream=nt {fn}')
    nts=to_nt_str(fn)
    fd_in = nts.split("\n") 
    lin=len(fd_in)
    print(f'got {lin} lines')
    with open(fn2,'w') as fd_out:
        for line in fd_in:
            #ll=len(line)
            if no_error(line):
                line_out = replace_last(line, " .", replace_with)
                fd_out.write(line_out)
                fd_out.write('\n')
    return fn2

def fn2nq(fn): #if is_http wget and call self again/tranfrom input
    "output fn as .nq"
    if is_http(fn):
        fn=wget(fn)
    print(f'fn2nq on:{fn}')
    ext = file_ext(fn)
    print(f'2nq file_ext:{ext}')
    fn2="Not Found"
    if ext==".nt":
        fn2=fn2nq(fn)
    if ext==".jsonld":
        #fn2=riot2nq(fn)
        fn2=to_nq(fn)
    else: #it might still work:
        fn2=riot2nq(fn)
    print(f'gives:{fn2}')
    return fn2

#this gets minio buckets but could do get_htm_dir
 #or if run on machine w/crawl can do very quickly
 #_think I considered something over a part of get_oss_files
  #that could tell if minio or other html LD listing
#there is also the ability to just read it all into rdflib and query that
  #def xml2nt(fn,frmt="xml") takes json-ld as a format
  #also: def riot2nq(fn): "process .jsonld put out .nq"
 #that might be easier in the notebook, but this fuseki:3030 can be shared

def summoned2nq(s=None):
    "list of jsonld to one nq file"
    if not s:
        s=get_oss_files("summoned")
        sl=len(s)
        print(f'summoned:{sl} 2nq')
    fnout=f'{repo_name}.nq'
    #os_system(f'yes|gzip {fnout}') #complains if not there
    os_system(f'echo ""> {fnout}')
    nql=list(map(fn2nq,s))
    for nq in nql:
        os_system(f'cat {nq}>>{fnout}')
    return fnout

def serve_nq(fn):
    "serve file w/fuseki" #could also do w/blasegraph, for txt-test/final-run
    fnb=file_base(fn)
    cs=f'nohup fuseki-server -file={fn} /{fnb} &'
    print(f'assuming no fuseki process, check for this new one:{cs}')
    os_system(cs)

def summon2serve(s=None): #~nabu like
    "get jsonld and serve the quads"
    fnout=summoned2nq(s)
    #cs=f'nohup fuseki-server -file={fnout} /{repo_name} &'
    #os_system(cs)
    serve_nq(fnout)
    return fnout

#sitemap url to LD-cache filenames
 #in mine it is BASE_URL + file_leaf(ur)
 #gleaner needs a mapping from it's PROV:

def prov2mapping(url): #use url from p above
    "read&parse 1 PROV record"
    import json
    #print(f'prov2mapping:{url}')
    j=url2json(url)
    d=json.loads(j)
    #print(d)
    g=d.get('@graph')
    if g:
        gi=list(map(lambda g: g.get("@id"), g))
        smd=g[1] #assume 1 past the context, 1st thing being from sitemap
        sm=smd.get("@id") #gi[0]
        u=collect_pre_(gi,"urn:")
        u0=u[0]
        #print(f'{sm}=>{u0}')
        #return sm, u #if expect >1
        return sm, u[0]
    else:
        return f'no graph for:{url}'

def prov2mappings(urls): #use urls from p above
    "get sitemap<->UUID in summoned,&sitemap"
    sitemap2urn={}
    urn2sitemap={} #might need this more
    for url in urls:
        key,value=prov2mapping(url)
        sitemap2urn[key]=value
        urn2sitemap[value]=key
        value2=value.split(':')[-1]   #so can also lookup form UUID w/o urn:... before it
        urn2sitemap[value2]=key #will be in same dict, so can lookup by either
    sitemap=list(sitemap2urn.keys())
    if dbg:
        print(f'prov-sitemap:{sitemap}')
    #return sitemap2urn, urn2sitemap
    return sitemap2urn, urn2sitemap, sitemap

#some bucket/gen-urls will be json(ld)
def url2json(url):
    import requests
    r=requests.get(url)
    return r.content

#testing, where we look at gleaner's mino ld-cache via web
 #so it can be swapped out for my web LD-cache when missing
#==bucket_files.py to get (minio) files list from a bucket path
#ci_url="https://oss.geocodes-dev.earthcube.org/citesting"
#ci_url="https://oss.geocodes-dev.earthcube.org/test3"
ci_url2="https://oss.geocodes-dev.earthcube.org/citesting2"

#https://pypi.org/project/htmllistparse/ rehttpfs does a fuse mount of a html dir
#which allows for reading any of it like a file

def get_url(url): 
    "request.get url"
    import requests
    r=requests.get(url)
    return r.content
#for LD_cache_files ..;if file_ext(url)==".xml" ret xmltodict, ;could d for htm but list nicer:
#s=get_url(url) st=s.decode("utf-8"); if "<html>" in st: parse_html, w/listFD
#from stackoverflow ;so can get ~bucket_files from each dir separately
#url = 'http://mbobak.ncsa.illinois.edu/ec/minio/test3/summoned/geocodes_demo_datasets/'
#ext = 'nq' ;might start using my ld_cache too; it seems more consistent
def listFD(url, ext=''):
    from bs4 import BeautifulSoup
    import requests
    page = requests.get(url).text
    if(dbg):
        print(page)
    soup = BeautifulSoup(page, 'html.parser')
    r= [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]
    #ftd=get_file_types(r)
    #return r,ftd
    return r

def get_htm_dir(url,ext=None):
    from bs4 import BeautifulSoup
    import requests
    page = requests.get(url).text
    if(dbg):
        print(page)
    soup = BeautifulSoup(page, 'html.parser')
    if ext:
        return [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]
    else:
        return [url + '/' + node.get('href') for node in soup.find_all('a')]
#eg:
#>>> files=get_htm_dir("http://mbobak.ncsa.illinois.edu/ec/minio/test3/summoned/geocodes_demo_datasets")
#>>> get_file_ext_types(files)
#{'': 5, '.jsonld': 9, '.nq': 9, '.nt': 9}
#then can: 
#>>> fj=get_htm_dir("http://mbobak.ncsa.illinois.edu/ec/minio/test3/summoned/geocodes_demo_datasets",".jsonld")
#>>> len(fj)
#9
#>>> list(map(replace_base,fj)) #will replace the base above w/'test3' ;if not in global lambda w/{"base": "repo"}

def url_xml(url): #could just be get_url
    "given bucket url ret raw xml listing"
    import requests
    #r=requests.get(url)
    try:
        r=requests.get(url, timeout=(15, 45)) #used in check.py
    except:
        print(f'url_xml:req-execpt on:{url}')
        return None
    test_xml=r.content
    #print(test_xml) #check if 200
    status=r.status_code 
    if(status == 200):
        return test_xml
    else:
        print(f'url_xml,bad:{status},for:{url}')
        return None

def is_bytes(bs):
    return isinstance(bs, bytes)

def xmltodict_parse(test_xml):
    import xmltodict
    if not is_bytes(test_xml):
        print(f'xml_parse no str')
        return None
    try:
        d=xmltodict.parse(test_xml)
    except:
        lx=len(test_xml)
        print(f'xml_parse exception')
        d=None
    return d

def sitemap_xml2dict(test_xml): #libs don't work in diff places
    #import xmltodict
    #d=xmltodict.parse(test_xml)
    d=xmltodict_parse(test_xml)
    if(dbg):
        print(d)
    if not d:
        print(f'sitemap_xml2 not found')
        return None
    lbr=d.get("urlset")
    if lbr:
        c=lbr.get("url")
        return c
    else:
        print(f'no urlset, for:{test_xml}')
        return None

def sitemap_urls(url):
    "faster way of getting urls w/just xml lib"
    test_xml=url_xml(url)
    if not test_xml:
        return []
    c=sitemap_xml2dict(test_xml)
    if c:
        urls=list(map(lambda kd: kd.get('loc'), c))
        return urls
    else:
        print(f'no sitemap_urls xml for urls:{url}')
        #return None
        return [] #hope to still work


def bucket_xml(url):
    return url_xml(url)

def bucket_xml2dict(test_xml):
    "bucket url to list of dicts, w/file in key"
    #import xmltodict
    #d=xmltodict.parse(test_xml)
    d=xmltodict_parse(test_xml)
    #print(d)
    lbr=d.get("ListBucketResult")
    if lbr:
        c=lbr.get("Contents")
        return c
    else:
        print(f'no ListBucketResult, for:{test_xml}')
        return None

def bucket_files(url): #need to get past: <MaxKeys>1000</MaxKeys>
    "bucket_url to file listing"
    test_xml=bucket_xml(url)
    c=bucket_xml2dict(test_xml)
    if c:
        files=map(lambda kd: kd.get('Key'), c)
        dates=map(lambda kd: kd.get('LastModified'), c) #or when get prov look at file dates before the parse?
         #AttributeError: 'int' object has no attribute 'get' #had taken this out
        return list(files),list(dates)
    else:
        print(f'no bucket xml for files:{url}')
        return None, None


def endpoint_xml2dict(test_xml):
    #import xmltodict
    #d=xmltodict.parse(test_xml)
    d=xmltodict_parse(test_xml)
    if(dbg):
        print(d)
    #lbr=d.get("rdf:Description")
    #if not lbr:
    #    lbr=d.get('rdf:RDF')
    lbr=d.get('rdf:RDF')
    return lbr

def endpoint_description(url="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/citesting2/sparql"):
    "get/test if endpoint ok, description xml to see that it is healthy"
    test_xml=url_xml(url)
    ts=test_xml.decode("utf-8")
    if is_html(ts):
        return "html"
    if ts.startswith("Service"):
        return "service_description"
    c=endpoint_xml2dict(test_xml)
    lc=len(c) #2keys
    print(f'endpoint w/{lc} descriptions')
    des=c.get('rdf:Description')
    return des
#c.get('@xmlns:rdf')
#'http://www.w3.org/1999/02/22-rdf-syntax-ns#'

#once I need this for >1 bucket I will turn it into a class, and make instances
LD_cache_base=None
LD_cache_files=None
LD_cache_dates=None #Might use, or as we query the file, also want to get files metadata
LD_cache_types=None
#output: {'milled/geocodes_demo_datasets': 25, 'orgs': 1, 'prov/geocodes_demo_datasets': 31, 'results/runX': 1, 'summoned/geocodes_demo_datasets': 25}
#{'orgs': 4, 'prov/geocodes_demo_datasets': 45, 'prov/magic': 951} #so key prov/bucket_name
 #so much prov here that get _files doesn't seem to have summoned though there/fix


def get_file_ext_types(file_list):
    file_types={}
    for fn in file_list:
        base,leaf = path_base_leaf(fn)
        ext=file_ext(leaf)
        count=file_types.get(ext)
        if count:
            count += 1
        else:
            count = 1
        file_types[ext] = count
    return file_types #use w/get_htm_dir

def get_file_leaf_types(file_list): 
    "use to find duplicate files in a dir"
    file_types={}
    for fn in file_list:
        base,leaf = path_base_leaf(fn)
        #count=file_types.get(base)
        count=file_types.get(leaf)
        if count:
            count += 1
        else:
            count = 1
        #file_types[base] = count
        file_types[leaf] = count
    return file_types 

def get_file_base_types(file_list):
    file_types={}
    for fn in file_list:
        base,leaf = path_base_leaf(fn)
        count=file_types.get(base)
        if count:
            count += 1
        else:
            count = 1
        file_types[base] = count
    return file_types #can use just below/?, and w/get_htm_dir

#if folders where different, maybe layer that over for different buckets, someday
def set_bucket_files(bucket=None):
    "get+set LD_cache_ files array and types dict"
    if not bucket:
        global ci_url
        bucket=ci_url
    global LD_cache_base, LD_cache_files, LD_cache_types
    LD_cache_base=bucket
    LD_cache_files,LD_cache_dates=bucket_files(bucket)
    LD_cache_types={}
    for fn in LD_cache_files:
        base,leaf = path_base_leaf(fn)
        count=LD_cache_types.get(base)
        if count:
            count += 1
        else:
            count = 1
        LD_cache_types[base] = count
    return LD_cache_types

def get_full_key(partial_key,mydict):
    "get key that has str in it"
    #fk = next(k for k,v in LD_cache_types.items() if base_type in k) #full key
    fk = next(k for k,v in mydict.items() if partial_key in k) #full key
    return fk

#conider getting listing from repo_name/base_type ;for bucket_files

def get_bucket_files(base_type):
    "ask for base_type= summoned,milled,prov,.. get all full file paths"
    global LD_cache_base, LD_cache_files, LD_cache_types
    if not LD_cache_files:
        set_bucket_files()
    print(f'get_bucket_files:{base_type}')
  # fk = next(k for k,v in LD_cache_types.items() if base_type in k) #full key
   #ks=LD_cache_types.keys()
   #fkl=collect_pre_(ks,base_type)
   #print(f'get:{base_type} has {fk}')
    fe=collect_pre_(LD_cache_files,base_type) #end of file paths
    lfe=len(fe)
    if lfe>0:
        ff=list(map(lambda f: f'{LD_cache_base}/{f}', fe)) #full file paths
    else:
        print(f'WARN:no {base_type} in {LD_cache_base}:{fe}')
        #ff=[]
        ff=None
    return ff

#if my cache has to go into a bucket it will be extruct/repo
#also I want a put_oss_files, so get key/secret from env-vars
# S3ADDRESS  S3KEY S3SECRET get.env
S3ADDRESS=os.getenv("S3ADDRESS")
S3KEY=os.getenv("S3KEY")
S3SECRET=os.getenv("S3SECRET")

#>>> oss_ls('test3/summoned/geocodes_demo_datasets') == get_bucket_files
  #not replacing yet, bc get error, even though doesn't get drowned out
#repo_name="geocodes_demo_datasets" #for testing
#testing_bucket="test3" #or bucket_name
#def get_oss_files_(path=None, base_type=None, bucket=None, minio_endpoint_url="https://oss.geodex.org/" ,full_path=True,):
def get_oss_files_(repo=None, base_type=None, bucket="gleaner", path=None, minio_endpoint_url="https://oss.geodex.org/" ,full_path=True,): #usually do not use version ending in _
    if not bucket:
        global testing_bucket
        bucket= testing_bucket
    if not base_type:
        base_type="summonded"
    if not repo:
        global repo_name
        repo= repo_name
    if not path:
        #path=f'{testing_bucket}/{base_type}/{repo_name}'
        path=f'{bucket}/{base_type}/{repo}'
    print(f'get_oss_files_:{path}') #dbg
    #oss_ls("gleaner/summoned", True, "https://oss.geodex.org/")
    return oss_ls(path, full_path, minio_endpoint_url)
#default getting access-denied, though get xml, and from:, but was for mbci2
#oss_ls("gleaner/summoned", True, "https://oss.geodex.org/")

def get_oss_files(base_type):
    path=f'{testing_bucket}/{base_type}/{repo_name}'
    return oss_ls(path)
#>>> get_oss_files("summoned")
#['test3/summoned/geocodes_demo_datasets/257108e0760f96ef7a480e1d357bcf8720cd11e4.jsonld', 'test3/summoned/geocodes_demo_datasets/261c022db9edea9e4fc025987f1826ee7a704f06.jsonld', 'test3/summoned/geocodes_demo_datasets/7435cba44745748adfe80192c389f77d66d0e909.jsonld', 'test3/summoned/geocodes_demo_datasets/9cf121358068c7e7f997de84fafc988083b72877.jsonld', 'test3/summoned/geocodes_demo_datasets/b2fb074695be7e40d5ad5d524d92bba32325249b.jsonld', 'test3/summoned/geocodes_demo_datasets/c752617ea91a725643d337a117bd13386eae3203.jsonld', 'test3/summoned/geocodes_demo_datasets/ce020471830dc75cb1639eae403a883f9072bb60.jsonld', 'test3/summoned/geocodes_demo_datasets/fcc47ef4c3b1d0429d00f6fb4be5e506a7a3b699.jsonld', 'test3/summoned/geocodes_demo_datasets/fe3c7c4f7ca08495b8962e079920c06676d5a166.jsonld']

site_urls2UUIDs=None
urn2site_urls=None
UUIDs2site_urls={} #uuid part of urn as key
prov_sitemap=None

#def URLsUUID(url):
def urn2uuid(url):
    "pull out the UUID from w/in the URL" 
    s=urn_leaf(url)
    leaf_base = s if not s else file_base(s)
    return leaf_base

def uuid2url(uuid):
    "map from uuid alone to crawl url"
    url=UUIDs2site_urls.get(uuid)
    if not url:
        print(f'bad uuid2url:{uuid}')
        return uuid
    return url

def uuid2repo_url(uuid):
    "uuid2url w/shorter repo:leaf.json"
    url=uuid2url(uuid)
    if url:
        return replace_base(url)
    else:
        print(f'bad uuid2repo_url:{uuid}')
        return uuid
#not getting this below now
#uuid2repo_url("09517b808d22d1e828221390c845b6edef7e7a40")
#'geocodes_demo_datasets:MB_amgeo_data-01-06-2013-17-30-00.json'

def is_html(str):
    return "<html>" in str

def is_http(u):
    if not is_str(u):
        print("might need to set LD_cache") #have this where predicate called
        return None
    #might also check that the str has no spaces in it,&warn/die if it does
    return u.startswith("http")

def is_urn(u):
    if not is_str(u):
        print("might need to set LD_cache")
        return None
    return u.startswith("urn:")

def leaf(u):
    if is_http(u):
        return path_leaf(u)
    elif is_urn:
        return urn_leaf(u)
    else:
        print('no leaf:{u}')
        return u

def leaf_base(u):
    lf=leaf(u)
    if lf:
        return file_base(lf)
    else:
        print('no leaf_base:{u}')
        return lf

def to_repo_url(u):
    uuid=leaf_base(u)
    return uuid2repo_url(uuid)

def to_repo_url_(u):
    "uuid or urn to repo_url"
    if is_urn(u):
        u=urn2uuid(u)
    return uuid2repo_url(u)
#this isn't ret anything
#there are UUIDs from graph that should just go through
 #though might want get.graphs w/ urn: returns

def fill_repo_url(url,mydict,val="ok"):
    "url w/uuid ->repo:leaf as key in dict"
    key=to_repo_url(url) 
    mydict[key]=val
    print(mydict)
    return mydict
#skip these, as not by ref/rm soon
def fill_repo_urls(urls,mydict,val="ok"):
    ul=len(urls)
    print(f'frus:{ul}')
    map(lambda u: fill_repo_url(u,mydict,val), urls)
    print(mydict)
    return mydict

def urls2idict(urls,val="ok"):
    mydict={}
    if not urls:
        print(f'urls2idict:no urls')
        return mydict
    ul=len(urls) if urls else 0
    print(f'u2d:{ul}')
    for url in urls:
        key=to_repo_url(url) 
        mydict[key]=val
    if(dbg):
        print(mydict)
    return mydict
#better, but not getting the key/find/fix that

def get_vals(key,dl):
    "lookup key in a list of dicts"
    rl= list(map(lambda d: d.get(key), dl))
    rl.insert(0,key)
    return rl
#[['geocodes_demo_datasets:MB_amgeo_data-01-06-2013-17-30-00.json', 'ok', 'ok', None], ['geocodes_demo_datasets:MB_iris_syngine.json', 'ok', 'ok', None], ['geocodes_demo_datasets:MB_lipdverse_HypkanaHajkova2016.json', None, None, None], ['geocodes_demo_datasets:argo-20220707.json', 'ok', 'ok', None], ['geocodes_demo_datasets:argoSimple-v1Shapes.json', None, None, None], ['geocodes_demo_datasets:bcodmo1-20220707.json', 'ok', 'ok', None], ['geocodes_demo_datasets:bcodmo1.json', 'ok', 'ok', None], ['geocodes_demo_datasets:earthchem_1572.json', None, None, None], ['geocodes_demo_datasets:opentopo1.json', 'ok', 'ok', None]]


#use this as the key for a dict for every saved state of the workflow
 #so can put out a csv, starting w/this, as it is made from the starting sitemap-url
 #but then for summoned, and if there milled, and then quads in the graph
 #for the ones that don't get filled in, just ret a comma
#So from the processed sitemap-url's xml, get the long form, then make short if possible
 #use this as the 1st column, and iterate over the list the same way; 
  #after that states dict has been filled up as much as possilbe
#have s m, then get_graphs  for the other saved states ;can do list-diff but csv will show missing already
#def csv_dropoff(sitemap_url): #maybe add spot test output later
#this needs LD_cache full 1st, can run bucket_files3 or..
csv_out=None

#def cmp_expected_results(df=None,df2="http://mbobak.ncsa.illinois.edu/ec/test/expected_results.csv"):
def cmp_expected_results(df=None,df2="https://raw.githubusercontent.com/MBcode/ec/master/test/expected_results.csv"):
    "just show where not expected" #so bad things can still be ok
    global csv_out
    if not is_df(df) and csv_out:
        df=csv_out
    if is_http(df2):
        import pandas as pd
        df2=pd.read_csv(df2)
    print(f'df1={df},df2={df2}')
    return df_diff(df,df2)
#check/fix: ValueError: The truth value of a DataFrame is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().

#def csv_dropoff(sitemap_url="https://earthcube.github.io/GeoCODES-Metadata/metadata/Dataset/allgood/sitemap.xml",
def csv_dropoff(sitemap_url="https://raw.githubusercontent.com/MBcode/ec/master/test/sitemap.xml", #start expecte bad cases
        bucket_url=None, endpoint="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/citesting2/sparql",cmp=False):
    global csv_out
    print(f'==sitemap:{sitemap_url}')
    print(f'==graph_endpoint:{endpoint}')
    if is_df(csv_out):
        print("already have a csv_out")
        return csv_out
    if bucket_url:
        global ci_url
        if bucket_url != ci_url:
            print(f'reset from:{ci_url} to:{bucket_url}')
            ci_url = bucket_url 
    print(f'==s3_endpoint:{bucket_url}')
    #print(f'csv_dropoff,bucket:{bucket_url}')
    if not urn2site_urls:
        set_prov2site_mappings()
    sm=sitemap_list(sitemap_url) #can now use sitemap2urn to get sitemap into same ID space
    #sm_ru=list(map(to_repo_url,sm)) #acts as key for each dict #this goes2uuid but sm doens't have that
    #sm_ru=list(map(replace_base,sm)) #acts as key for each dict ;need v of replace_base w/base_url2repo, but for url
    sm_ru=list(map(replace_base,sm)) #acts as key for each dict ;need v of replace_base w/base_url2repo, but for url
    #s=get_bucket_files("summoned")
    s=get_oss_files("summoned")
    #m=get_bucket_files("milled")
    m=get_oss_files("milled")
    #p=get_bucket_files("prov")
    #g=get_graphs_tails(endpoint)
    print(f'check,endpoint:{endpoint}')
    ep_ok=endpoint_description(endpoint)
    if ep_ok:
        g=get_graphs_list(endpoint) #will strip ..urn: to uuid anyway
    else:
        print(f'cd:enpoing not ok:{endpoint}')
        g=None
    #print(f'csv_ states,sm:{sm},s:{s},m:{m},g:{g}')
    print(f'sm:{sm}')
    #print(f'sm:{sm_ru}')
    print(f's:{s}')
    print(f'm:{m}')
    print(f'g:{g}')
    sml=len(sm_ru)
    sl=len(s) if s else 0
    ml=len(m) if m else 0
    gl=len(g) if g else 0
    print(f'csv_ states,sm:{sml},s:{sl},m:{ml},g:{gl}')
    sd=urls2idict(s)
    md=urls2idict(m)
    gd=urls2idict(g)
    #these are getting set w/uuid keys, and want to_repo_url keys
     #though UUIDs2site_urls should help map them ;whatever2 uuid, to_repo_url
    print(f'sd:{sd}')
    print(f'md:{md}')
    print(f'gd:{gd}') #this needs repo:file keys instead of uuids
    dl=[sd,md,gd]
    print(f'now lookup by:{sm_ru}')
    r= list(map(lambda k: get_vals(k, dl), sm_ru))
    lr=len(r)
    print(f'{sml}={lr}')
    import pandas as pd
    df = pd.DataFrame.from_dict(r)
    #csv_out=df #so we don't rerun uncessesarily
    csv_out=df.set_axis(["repo:file_name",  "summoned", "milled", "graph"], axis=1, inplace=False)
    if cmp or dbg:
        diff=cmp_expected_results(csv_out)
        print(f'diff w/expected:{diff}')
    return csv_out
#turn this into html-table &/or dataframe
  #see what is up w/graph's comparison/fix that; bad uuid2url: 
   #so might have other crawl in graph? look for similar name/urls there
#9=9  aslo check on 3 that didn't summon
#                                                   0     1     2     3
#0  geocodes_demo_datasets:MB_amgeo_data-01-06-201...    ok    ok  None
#1        geocodes_demo_datasets:MB_iris_syngine.json    ok    ok  None
#2  geocodes_demo_datasets:MB_lipdverse_HypkanaHaj...  None  None  None
#3          geocodes_demo_datasets:argo-20220707.json    ok    ok  None
#4    geocodes_demo_datasets:argoSimple-v1Shapes.json  None  None  None
#5       geocodes_demo_datasets:bcodmo1-20220707.json    ok    ok  None
#6                geocodes_demo_datasets:bcodmo1.json    ok    ok  None
#7         geocodes_demo_datasets:earthchem_1572.json  None  None  None
#8              geocodes_demo_datasets:opentopo1.json    ok    ok  None

#def prov2site_mappings():
def set_prov2site_mappings():  #make sure it is run, to get mappings
    "use cached PROV to make mappings"
    #global LD_cache_base, LD_cache_files, LD_cache_types
    #pu=get_bucket_files("prov") #only the ones for the repo_name being run
    pu=get_bucket_files(f'prov/{repo_name}') #only the ones for the repo_name being run
    #would be great to only send the (sitemap len) newest files
    if pu:
        global site_urls2UUIDs, urn2site_urls, UUIDs2site_urls, prov_sitemap
        #return prov2mappings(pu)
        #sitemap2urn,urn2sitemap,sitemap=prov2mappings(pu)
        #site_urls2UUIDs,UUIDs2site_urls,prov_sitemap=prov2mappings(pu)
        site_urls2UUIDs,urn2site_urls,prov_sitemap=prov2mappings(pu)
       #UUIDs2site_urls from urn2site_urls ;needs is_urn
       #UUIDs2site_urls=list(map(urn2uuid,urn2site_urls));needs is_urn ;use next/or
        for k,v in urn2site_urls.items(): #=list(map(urn2uuid,urn2site_urls));needs is_urn
            k2=urn2uuid(k)
            if k2:
                UUIDs2site_urls[k2]=v
            else:
                print('bad k2 for:{k},{v}')
        l1=len(site_urls2UUIDs)
        #l2=len(UUIDs2site_urls)
        l2=len(urn2site_urls)
        l3=len(prov_sitemap)
        ss=f'set:{l1} site_urls2UUIDs,{l2} UUIDs2site_urls,{l3} prov_sitemap'
        print(ss)
        return ss
    else:
        print(f'no prov for site_mappings')
        return None #so can skip out of dependcies

#def prov2sitemap(bucket_url,pu=None):
def prov2sitemap(bucket_url=None,pu=None): #backward compat4a bit
    "return prov_sitemap, parse prov if not there"
    if not prov_sitemap:
        set_prov2site_mappings()
    return prov_sitemap

#def prov2sitemap(bucket_url):
#def prov2sitemap(bucket_url,pu=None):
def prov2sitemap_(bucket_url,pu=None): #do not use
    "parse bucket prov2get sitemap&it's mappings"
    fi=bucket_files(bucket_url)
    if not fi:
        print(f'prov2sitemap, no bucket_files:{bucket_url}')
        return None
    p=collect_pre_(fi,"prov") #only the ones for the repo_name being run
    pu=list(map(lambda fp: f'{bucket_url}/{fp}', p))
    sitemap=None
    try:
        pul=len(pu)
        #print(f'prov2mapping for:{pul}')
        print(f'prov2sitemap_mapping for:{pul}')
        sitemap2urn,urn2sitemap,sitemap=prov2mappings(pu)
        #print("got the mappings")
    except:
        #print("bad prov2mappings sitemap")
        print("bad prov2sitemap_mappings, on the:{pul}")
    return sitemap #for now

#if ret more could use in fnc/s below

#spot_ crawl_dropoff fnc below, ~being sucseeded by csv_dropoff fncs above
#want2check on: =Graph-count:9, Error count:-9, missing:[]  ;but from older way
 #I setup the old to get LD_cache info from the new; but might be better focusing on df grid a bit more now
 #so can get some more bad data through that is expected and catch it
 #s14 output mostly good, except 2not ok, not in summary../check

#will not need these other bucket_ fncs soon
 #will make spot_ crawl_dropoff something that could more easily fit
 #into a workflow check, alongside each stage, just accessing the state
 #on each side and getting the diff, for a report
 #incl. a (dbg) version aligned as a csv/spreadsheet ;algo above

def bucket_files2(url):
    "url to tuple of summoned+milled lists"
    fi=bucket_files(url)
    s=collect_pre_(fi,"summoned")
    m=collect_pre_(fi,"milled")
    return s,m

def bucket_files3(url=None): #might try using above w/this for just a bit
    if url: 
        global ci_url
        ci_url=url
    #s=get_bucket_files("summoned")
    s=get_oss_files("summoned")
    #m=get_bucket_files("milled")
    m=get_oss_files("milled")
    #p=get_bucket_files("prov")
    p=get_bucket_files(f'prov/{repo_name}') #only the ones for the repo_name being run
    #pu=list(map(lambda fp: f'{url}/{fp}', p))
    global site_urls2UUIDs, UUIDs2site_urls, prov_sitemap
    if not prov_sitemap:
        #prov_sitemap=prov2sitemap()
        prov2sitemap()
    psl=len(prov_sitemap)
    print(f'bf3,prov_sitemap:{psl}')
    sitemap2urn=site_urls2UUIDs
    urn2sitemap=UUIDs2site_urls
    if not s:
        print("bf3:no summoned")
    if not m:
        print("bf3:no milled")
    return s,m,sitemap2urn,urn2sitemap #not sending prov_sitemap yet

#going fwd, focus on being able2keep each stage in assoc, so after list_diff still know which original url started it off
 #this is in the metadata for the file, but also in the prov mappings

#def bucket_files3(url=None):
def bucket_files3_(url=None): #do not use
    "url to summoned+milled,prov lists"
    if not url:
        global ci_url
        url = ci_url
    fi=bucket_files(url)
    if not fi:
        print(f'bucket_files 3,nothings for:{url}')
        return None, None, None, None
    #s=collect_pre_(fi,"summoned") #use other ;as fix
    s=get_oss_files("summoned")
    m=collect_pre_(fi,"milled")
    p=collect_pre_(fi,"prov")
    pu=list(map(lambda fp: f'{url}/{fp}', p))
    sitemap2urn=None
    try:
        pul=len(pu)
        print(f'prov2mapping for:{pul}')
        #sitemap2urn,urn2sitemap=prov2mappings(pu)
        sitemap2urn,urn2sitemap,sitemap=prov2mappings(pu)
        #print("got the mappings")
    except:
        print("bad prov2mappings")
    if sitemap2urn: 
        return s,m,sitemap2urn,urn2sitemap
    else:
        #return s,m,p #mostly expect mappings below, &not prov
        print(f'bucket_files3 no map so send Nones, for:{url}')
        return s,m, None, None

#could also pass sitemap, in case used later from:

def bucket_files2diff(url,URNs=None):
    "list_diff_dropoff summoned milled, URNs"
    #summoned,milled=bucket_files2(url) #now have bucket_files3
    summoned,milled,sitemap2urn,urn2sitemap=bucket_files3(url) 
    if not summoned:
        print(f'bucket_files3 2diff, nones for bad:{url}') 
        return None, None, None, None, None
    su=list(map(lambda f: file_base(path_leaf(f)),summoned))
    if not milled:
        print(f'bucket_files3 2diff, no milled for bad:{url}') 
        mu=[]
    else:
        mu=list(map(lambda f: file_base(path_leaf(f)),milled))
    if dbg:
        print(f'summoned-URNs:{su}')
        print(f'milled-URNs:{mu}')
    sl=len(su)
    ml=len(mu)
    dsm=sl-ml #diff summoned&milled= datasets lost in this step
    lose_s2m=list_diff_dropoff(su,mu)
    if URNs:
        ul=len(URNs)
        dmu=ml-ul
        print(f'dmu:{dmu}=ml:{ml} - ul:{ul}') #dbg, negative if no milled
        #print(f'=Summoned-count:{sl}, Error count:{dsm}, missing:{lose_s2s}') #below
        print(f'=Milled-count:{ml}, Error count:{dmu}, missing:{lose_s2m}')
        #print(f'expected-URNs:{URNs}')
        if dbg:
            print(f'endpoint-URNs:{URNs}')
        #dropoff=f's:{sl}/m:{ml}/u:{ul} diff:{dmu}'
        dropoff=f'summoned:{sl}-{dsm}=>milled:{ml}-{dmu}=>graph:{ul}'
        if dbg:
            print(dropoff)
        lose_m2u=list_diff_dropoff(mu,URNs) 
        print(f'=Graph-count:{ul}, Error count:{dmu}, missing:{lose_m2u}')
        #return lose_s2m, lose_m2u
        #return dropoff,lose_s2m, lose_m2u
        #return dropoff,lose_s2m, lose_m2u , sitemap2urn
        return dropoff,lose_s2m, lose_m2u , sitemap2urn, su #last is summoned
    else:
        #dropoff=f's:{sl}/m:{ml} diff:{dsm}')
        dropoff=f'summoned:{sl}-{dsm}=>milled:{ml}'
        if dbg:
            print(dropoff)
        #return lose_s2m
        #return dropoff,lose_s2m
        return dropoff,lose_s2m, None, None, None

#don't need to have a diff version, bc bucket_files3 looks up PROV even w/o a sitemap
#def bucket_files3diff(sitemap,url,URNs=None):

#break out all the code in crawl_dropoff that deals w/sitemap to summoned w/mapping
#def drop1mapping(sm,sitemap2urn):
def drop1mapping(sm,sitemap2urn,su): #want to but not used yet; still in crawl_dropoff
    "break out all the code in crawl_dropoff that deals w/sitemap to summoned w/mapping"
    sml=len(sm)
    #print(f'will get:{sml} urn2urn w/:{sitemap2urn}') #dbg
    #smu=list(map(lambda s: sitemap2urn[s], sm))
    smu=list(map(lambda s: sitemap2urn.get(s), sm)) #used prov mapping to gen test sitemap
    if dbg:
        print(f'URN/UUIDs for sitemaps:{smu}')             #need to get same sitemap, &use map for cmp:
    #smu2=list(map(lambda s: s.split(':')[-1],smu))
    smu2=list(map(lambda s: s if not s else s.split(':')[-1],smu)) #=urn_tails(smu)
    if dbg:
        print(f'URN/UUIDs for sitemaps:{smu2}')             #need to get same sitemap, &use map for cmp:
    lose_s2s=list_diff_dropoff(smu2,su) 
    lsl=len(lose_s2s) #should= sml- ml from above
    print(f'lose_s2s:{lose_s2s}') #will need to map this back to the sitemap url ;if it was in prov
    ##lose_s2m=list_diff_dropoff(su,mu), from above
    #dropoff=f'sitemap:{sml} =>{dropoff2}'  #pull sl, to calc dss=sml-sl
    #dropoff=f'sitemap:{sml}-{lsl}:{lose_s2s} =>{dropoff2}'  
  # print(f'=Summoned-count:{sl}, Error count:{ls1}, missing:{lose_s2s}')
    dropoff=f'sitemap:{sml}-{lsl}:{lose_s2s} =>'  
    #dropoff=f'sitemap:{sml}-{dss}=>{dropoff2}' #can't get lose_s2s w/o PROV sitemap URLs to UUID mapping  
    #return dropoff,lose_s2m, lose_m2u
    #return dropoff,lose_s2s, lose_s2m, lose_m2u
    return dropoff,lose_s2s

def crawl_dropoff_(sitemap,bucket_url,endpoint): #do not use
    "show counts at each stage, and URN diffs when can"
    #URNs=get_graphs_list(endpoint)  #that are in the endpoint, not the expected
    URNs=get_graphs_tails(endpoint)  #that are in the endpoint, not the expected
    #dropoff2,lose_s2m, lose_m2u = bucket_files2diff(bucket_url,URNs)
    #dropoff2,lose_s2m, lose_m2u, sitemap2urn = bucket_files2diff(bucket_url,URNs)
    dropoff2,lose_s2m, lose_m2u, sitemap2urn, su = bucket_files2diff(bucket_url,URNs)
    #sml=sitemap_len(sitemap) #can now use sitemap2urn to get sitemap into same ID space
    sm=sitemap_list(sitemap) #can now use sitemap2urn to get sitemap into same ID space
    #print(f'sitemap:{sm}')
    sml=len(sm)
    if sitemap2urn:
        dropoff1,lose_s2s=drop1mapping(sm,sitemap2urn,su)
        dropoff=f'{dropoff1} =>{dropoff2}'  
        return dropoff,lose_s2s, lose_s2m, lose_m2u
    else:
        return dropoff2, lose_s2m, lose_m2u
    #print(f'will get:{sml} urn2urn w/:{sitemap2urn}') #dbg
    #smu=list(map(lambda s: sitemap2urn[s], sm))
    #rest in drop1mapping now

#should be setup w/o sitemap, to get it from PROV ;no bc won't necc have mapping for something that didn't parse

#Will want to send in sitemap(url) and compare w/that gleaned from prov, so whatever prov didn't get was is a url to be checked
def sitemap_dropoff(sitemap_url=None,bucket_url=None): #bucket to get prov's version
    "figure out which sitemap URLs that need checking"
    if sitemap_url:
        sm=sitemap_list(sitemap_url) #can now use sitemap2urn to get sitemap into same ID space
    else:
        print(f'sitemap_dropoff no sitemap_url:{sitemap_url}')
        sm=[]
    if bucket_url:
        sitemap_l=prov2sitemap(bucket_url) #this gives the list of them, which most fncs expect the sitemap_url
    else:
        print(f'sitemap_dropoff no bucket_url:{bucket_url}')
        sitemap_l=[]
    if dbg: #if sitemap is malformed can get non flat list
        print(f'sitemap_dropoff,_l:{sitemap_l},sm:{sm}') #dbg
    lose_s2s=list_diff_dropoff(sitemap_l,sm) #check_sm_urls
    sml=len(sm)
    lsl=len(lose_s2s) #should= sml- ml from above
    dropoff1=f'sitemap:{sml}-{lsl}:{lose_s2s}'  
    if dbg:
        print(f'use this dropoff1:{dropoff1}')
    return sitemap_l, sm, dropoff1

def crawl_dropoff(sitemap,bucket_url,endpoint):
    "show counts at each stage, and URN diffs when can"
    if not sitemap:
        sitemap=prov2sitemap(bucket_url) #this gives the list of them, which most fncs expect the sitemap_url
    #URNs=get_graphs_list(endpoint)  #that are in the endpoint, not the expected
    URNs=get_graphs_tails(endpoint)  #that are in the endpoint, not the expected
    print(f'crawl_dropoff:URNs:{URNs}')
    #dropoff2,lose_s2m, lose_m2u = bucket_files2diff(bucket_url,URNs)
    #dropoff2,lose_s2m, lose_m2u, sitemap2urn = bucket_files2diff(bucket_url,URNs)
    dropoff2,lose_s2m, lose_m2u, sitemap2urn, su = bucket_files2diff(bucket_url,URNs)
    #sml=sitemap_len(sitemap) #can now use sitemap2urn to get sitemap into same ID space
    #if not sitemap: #could warn here
    if not sitemap: 
        print(f'crawl_dropoff, no sitemap for:{bucket_url}')
        return None
    #elif is_str(sitemap): #could be a sep if
    if is_str(sitemap): 
        if dbg:
            print(f'=using sitemap str:{sitemap}')
        else:
            print(f'using sitemap str')
        sm=sitemap_list(sitemap) #can now use sitemap2urn to get sitemap into same ID space
    else:
        if dbg:
            print(f'using sitemap list:{sitemap}')
        else:
            smul=len(sitemap)
            print(f'using sitemap list:{smul}')
        sm=sitemap #if from prov2sitemap
    #print(f'sitemap:{sm}')
    sml=len(sm)
    if sitemap2urn: #was able to get PROV..
      # dropoff,lose_s2s=drop1mapping(sm,sitemap2urn) #only call in variant above where code below goes away
        #print(f'will get:{sml} urn2urn w/:{sitemap2urn}') #dbg
        #smu=list(map(lambda s: sitemap2urn[s], sm))
        smu=list(map(lambda s: sitemap2urn.get(s), sm)) #used prov mapping to gen test sitemap
        if dbg:
            print(f'URN/UUIDs for sitemaps:{smu}')             #need to get same sitemap, &use map for cmp:
        #smu2=list(map(lambda s: s.split(':')[-1],smu))
        smu2=list(map(lambda s: s if not s else s.split(':')[-1],smu))
        if dbg:
            print(f'URN/UUIDs for sitemaps:{smu2}')             #need to get same sitemap, &use map for cmp:
        lose_s2s=list_diff_dropoff(smu2,su) 
        lsl=len(lose_s2s) #should= sml- ml from above
        if dbg:
            print(f'lose_s2s:{lose_s2s}') #will need to map this back to the sitemap url ;if it was in prov
        ##lose_s2m=list_diff_dropoff(su,mu), from above
        #dropoff=f'sitemap:{sml} =>{dropoff2}'  #pull sl, to calc dss=sml-sl
        #print(f'=Sitemap-count:{sml}, Error count:{ls1}, missing:{loose_s2s}') #dropoff should be in the next one
        print(f'=Sitemap-count:{sml}') #dropoff should be in the next one
        sl=len(smu) #url we get from prov are once it gets run into summoned
        print(f'=Summoned-count:{sl}, Error count:{lsl}, missing:{lose_s2s}')
        dropoff=f'sitemap:{sml}-{lsl}:{lose_s2s} =>{dropoff2}'  
        #dropoff=f'sitemap:{sml}-{dss}=>{dropoff2}' #can't get lose_s2s w/o PROV sitemap URLs to UUID mapping  
        #return dropoff,lose_s2m, lose_m2u
        return dropoff,lose_s2s, lose_s2m, lose_m2u
    else:
        #return dropoff2, lose_s2m, lose_m2u
        return dropoff2, None, lose_s2m, lose_m2u

#could then take these loss lists, and map over w/ check_urn_ jsonld|rdf
 #lose_s2m would only still have summoned, so could check_urn_jsonld
 #lose_m2u would only still have milled, so could check_urn_rdf
def spot_crawl_dropoff(sitemap,bucket_url,endpoint):
    "when have spot gold stnd, can also check on that"
    print("csv_ then spot_crawl_ dropoffs")
    df=csv_dropoff(sitemap,bucket_url,endpoint)
    print(df)
    #dropoff,lose_s2m, lose_m2u = crawl_dropoff(sitemap,bucket_url,endpoint)
    dropoff,lose_s2s,lose_s2m, lose_m2u = crawl_dropoff(sitemap,bucket_url,endpoint)
    if not is_list(lose_s2m): #empty list would trip this off
        print(f'spot_ crawl_dropoff, none4lose, bad:{bucket_url}')
        return None, None, None, None, None, None
    s_check=list(map(check_urn_jsonld,lose_s2m))
    if not lose_m2u:
        print(f'scd:no milled:{lose_m2u}')
        m_check=[] #..
    else:
        m_check=list(map(check_urn_rdf,lose_m2u)) #can't do this if no milled,  can try the transformation though
    #return dropoff,lose_s2m, s_check, lose_m2u, m_check 
    #return dropoff,lose_s2s, lose_s2m, s_check, lose_m2u, m_check 
    return dropoff,lose_s2s, lose_s2m, s_check, lose_m2u, m_check, df
    #could have map interleave URN w/True=ok or diff
    #return dropoff,lose_s2m, lose_m2u

#turns out reading PROV to get sitemap<->UUID's in summoned, also gives us the sitemap run
#def tsc(sitemap=None,bucket_url=None,endpoint=None):
def tsc(sitemap=None,bucket_url=None,endpoint="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/citesting/sparql"):
    "test spot_crawl_dropoff"
    if not endpoint:
        global testing_endpoint
        endpoint = testing_endpoint
    if not bucket_url:
        global ci_url
        bucket_url = ci_url
    print(f'=s3_endpoint:{bucket_url}')
    print(f'=graph_endpoint:{endpoint}')
    sitemap_l, sm, dropoff1 = sitemap_dropoff(sitemap,bucket_url) #will still get sitemap_l if no sitemap url given
    if not sitemap: #moved into crawl_dropoff, keep here/in case
        ##sitemap2urn, urn2sitemap, sitemap=prov2mappings(..)
        #sitemap=prov2sitemap(bucket_url) #this gives the list of them, which most fncs expect the sitemap_url
        sitemap=sitemap_l
    if not sitemap:
        print("did not get sitemap from prov so go w/deflt")
        sitemap="http://geocodes.ddns.net/ec/test/sep/sitemap.xml"
    print(f'=sitemap:{sitemap}')
    return spot_crawl_dropoff(sitemap,bucket_url,endpoint)

def tsc2__(sitemap2="http://geocodes.ddns.net/ec/test/sitemap.xml",bucket_url2=None,endpoint2=None):
    "same test but send in sitemap vs get it from prov"
    tsc(sitemap=sitemap2,bucket_url=bucket_url2,endpoint=endpoint2)
#old get rid of
def tsc2_(bucket_url=None,endpoint2="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/citesting2/sparql"):
    "for mb_ci setup which uses unused citesting2 bucket&endpoint"
    if not bucket_url:
        global ci_url2
        bucket_url = ci_url2
    tsc(None,bucket_url,endpoint=endpoint2)

def tsc2(sitemap=None,bucket_url=None,endpoint="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/citesting2/sparql"):
    "as is being used in spot_test/report on geocodes-dev now" #still need to deal w/milled dissapearing in a few places
    return tsc(sitemap,bucket_url,endpoint)

#def tsc3(sitemap="http://geocodes.ddns.net/ec/test/sep/sitemap.xml",bucket_url=None,
def tsc3(sitemap="https://raw.githubusercontent.com/MBcode/ec/master/test/sitemap.xml",bucket_url=None,
        endpoint="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/citesting2/sparql"):
    "as is being used in spot_test/report on geocodes-dev now" #still need to deal w/milled dissapearing in a few places
    return tsc(sitemap,bucket_url,endpoint)

#this has the sitemap from the gSpreadsheet 'sources'
def tsc4_(sitemap="https://earthcube.github.io/GeoCODES-Metadata/metadata/Dataset/allgood/sitemap.xml",bucket_url=None,
        endpoint="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/citesting2/sparql"):
    "as is being used in spot_test/report on geocodes-dev now" #still need to deal w/milled dissapearing in a few places
    return tsc(sitemap,bucket_url,endpoint)

#this has the sitemap from the gSpreadsheet 'sources'  ;keep bucket in sync w/endpnt etc #bucket_url=ci_url2,
def tsc4(sitemap="https://earthcube.github.io/GeoCODES-Metadata/metadata/Dataset/allgood/sitemap.xml", 
        bucket_url="https://oss.geocodes-dev.earthcube.org/citesting2",
        endpoint="http://ideational.ddns.net:3030/geocodes_demo_datasets/sparql"):
       #endpoint="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/citesting2/sparql"): #nabu was not run here
    "as is being used in spot_test/report on geocodes-dev now" #still need to deal w/milled dissapearing in a few places
    return tsc(sitemap,bucket_url,endpoint)
#9=9 #this got the graph to show up, milled was skiped by gleaner, &had similar summoned
#0  geocodes_demo_datasets:MB_amgeo_data-01-06-201...    ok  None    ok
#1        geocodes_demo_datasets:MB_iris_syngine.json    ok  None    ok
#2  geocodes_demo_datasets:MB_lipdverse_HypkanaHaj...  None  None  None
#3          geocodes_demo_datasets:argo-20220707.json    ok  None    ok
#4    geocodes_demo_datasets:argoSimple-v1Shapes.json    ok  None    ok
#5       geocodes_demo_datasets:bcodmo1-20220707.json    ok  None    ok
#6                geocodes_demo_datasets:bcodmo1.json    ok  None    ok
#7         geocodes_demo_datasets:earthchem_1572.json  None  None  None
#8              geocodes_demo_datasets:opentopo1.json    ok  None    ok
#get_oss_files now gets summoned, but getting check_urn_jsonld error, that is new/but getting good urls from this fnc
#it was the test data coming from citesting vs test3 fix above/and all works
def tscg(sitemap="https://earthcube.github.io/GeoCODES-Metadata/metadata/Dataset/allgood/sitemap.xml"): #rest are global
    global bucket_url,testing_endpoint
    endpoint=testing_endpoint
    print(f'tscg:{sitemap},{bucket_url},{endpoint}')
    return tsc(sitemap,bucket_url,endpoint)

#def mb_ci2(sitemap="https://earthcube.github.io/GeoCODES-Metadata/metadata/Dataset/allgood/sitemap.xml",
#made cp of sitemap, so could add bad tests, eg. a 404
def mb_ci2(sitemap="https://raw.githubusercontent.com/MBcode/ec/master/test/sitemap.xml",
   #def mb_ci2(sitemap="http://mbobak.ncsa.illinois.edu/ec/test/sitemap.xml", #before pushing to github
          #endpoint="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/mb_ci2/sparql", #not being filled/fix
           endpoint="http://ideational.ddns.net:3030/geocodes_demo_datasets/sparql",
           bucket_url="https://oss.geocodes-dev.earthcube.org/mbci2"): 
          #bucket_url="https://oss.geocodes-dev.earthcube.org/mb_ci2"): #can't name bucket this way 
    print(f'mb_ci2:{sitemap},{bucket_url},{endpoint}')
    print(" ") #spot_crawl_dropoff has .. w/df at end, that needs a newline
    return tsc(sitemap,bucket_url,endpoint)

def test5(sitemap="https://earthcube.github.io/GeoCODES-Metadata/metadata/Dataset/allgood/sitemap.xml",
           endpoint="http://localhost:9999/blazegraph/namespace/nabu/sparql",
           bucket_url="https://oss.geocodes-dev.earthcube.org/test5"): 
    print(f'test5:{sitemap},{bucket_url},{endpoint}')
    return tsc(sitemap,bucket_url,endpoint)

#extra around summary
def rcsv(fn,d=","):
    import pandas as pd
    return pd.read_csv(fn,delimiter=d)

def tgc1_(ep=None):
    "tgc1 that can use other than dflt namespace"
    if ep:
        global dflt_endpoint
        dflt_endpoint=ep
    print(f'using:{dflt_endpoint}')
    df=get_summary("")
    ln=len(df)
    print(f'got:{ln}')
    df.to_csv("summary-gc1.csv")
    return df #assume pandas

def tgc1():
    "summarize and endpoint to csv for tsum.py to turn to tll for loading into summary namespace"
    global dflt_endpoint,gc1_endpoint
    dflt_endpoint=gc1_endpoint
    print(f'using:{dflt_endpoint}')
    df=get_summary("")
    ln=len(df)
    print(f'got:{ln}')
    df.to_csv("summary-gc1.csv")
    return df #assume pandas

#might very well put tsum.py functionality here
 #will also write a similar df row mapping as 1st quick dump of sparqldataframe df to .nt file
  #though I'm sure there will be better/more build up ways
