#=Mbobak mainstay-basic utils, that are starting to get copied in a few places
# need to modularize ;not bad now, but could get that way, so pulling them out now
#earthcube_utilities> grep def dc.py >mb.py
#=so can see where they were in the original for a bit

#Note: there are doctests in this, that can be part of the git workflow
 #e.g. python3 -m doctest mb.py   #will return nothing if still ok

#as in issue21 qry.py and rdf2nq.py already broken out
 #[and now the commented def's they hold are noted below]
# so w/this&those and next sections broken out
#  will assemble in a branch that is a more modular
#  version of earthcube_utiliites.py ;in the end

#-
#def laptop(): #could call: in_binder
#def local():

import os
import sys
import json

import logging as log  
log.basicConfig(filename='mb.log', encoding='utf-8', level=log.DEBUG,
                format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

#=new
#-from tsum:
def file_size(fn):
    size= os.path.getsize(fn)
    log.info(f'size:{size}')
    return size

#-from get_repo:
def url_w_end_slash(url):
    """make sure url has slash at the end
    >>> url_w_end_slash("https://graph.geocodes.ncsa.illinois.edu/blazegraph/namespace")
    'https://graph.geocodes.ncsa.illinois.edu/blazegraph/namespace/'
    >>> """
    if len(url)-1 != "/":
        return url + "/"
    else:
        return url
#-

def now():
    from datetime import datetime
    now = datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
    return dt_string

def head(l, n=5):
    """>>> l=[1,2,3,4,5,6]
    >>> head(l)
    [1, 2, 3, 4, 5]
    """
    return l[:n]

def tail(l, n=5):
    """>>> l=[1,2,3,4,5,6]
    >>> tail(l)
    [2, 3, 4, 5, 6]"""
    return l[-n:]

def is_str(v):
    """
    >>> is_str("")
    True
    >>> is_str(5)
    False
    """
    return type(v) is str

def is_list(v):
    """
    >>> l_,l0,l1=1,[],[1]
    >>> is_list(l_)
    False
    >>> is_list(l0)
    True
    >>> is_list(l1)
    True
    """
    return type(v) is list


def falsep(val):
    """predicate to see if false = not
    >>> falsep(True)
    False
    >>> falsep(False)
    True
    """
    return val == False

#def ndtq_(name=None,datasets=None,queries=None,tools=None):
#def ndtq(name=None,datasets=None,queries=None,tools=None):
##def install_recipy():

def first(l):
    """get the first in an iterable ;check_on l1 case
    >>> l_,l0,l1=1,[],[1]
    >>> first(l_)
    1
    >>> first(l1)
    1
    """
    from collections.abc import Iterable
    if isinstance(l,list):
        return l[0]
    elif isinstance(l,Iterable):
        return list(l)[0]
    else:
        return l

def flatten(xss): #stackoverflow
    """make list of lists into 1 flat list ;check_on 1st level non-list case
    >>> ld=[[1], [2,3], [4]]
    >>> flatten(ld)
    [1, 2, 3, 4]
    """
    return [x for xs in xss for x in xs]

#from old qry.py
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


#not needed as logging set up w/the date on every line now
#def date2log(): #could use now to put on same line, but this breaks it apart
#    cs="date>>log"
#    os.system(cs)

def add2log(s):
    "logging" #will use lib
    log.info(s)
   #date2log()
   #fs=f'[{s}]\n'
   #put_txtfile("log",fs,"a")

def print2log(s): #I think there is a logging setting that will do both
    print(s)
    add2log(s)

def os_system(cs):
    "run w/o needing ret value"
    os.system(cs)
    add2log(cs)

def os_system_(cs):
    """system call w/return value
    os_system_('ls -1|grep -v ~|grep dc.py')
    'dc.py\ndc.py~\n'
    """
    s=os.popen(cs).read()
    add2log(cs)
    return s

def curl_url(url):
    cs=f'curl {url}'
    return os_system_(cs)

def whoami():
    return os_system_("whoami")

def urn_leaf(s): #like urn_tail
    """last part of : sep string
    >>> urn_leaf("protocol://one.two.three/repo:last_bit.txt")
    'last_bit.txt'
    """
    leaf = s if not s else s.split(':')[-1]
    return leaf

#start adding more utils, can use to: fn=read_file.path_leaf(url) then: !head fn
def path_leaf(path):
    """everything after the last /
    >>> path_leaf("protocol://one.two.three/repo:last_bit.txt")
    'repo:last_bit.txt'
    """
    import ntpath
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def path_base_leaf(path):
    """like path_leaf but gives base 1st
    >>> path_base_leaf("protocol://one.two.three/repo:last_bit.txt")
    ('protocol://one.two.three', 'repo:last_bit.txt')
    """
    import ntpath
    head, tail = ntpath.split(path)
    if not tail:
        tail = ntpath.basename(head)
    return head, tail

#def replace_base(path,mydict=base_url2repo,sep=":"): #for context like: repo:filename

def file_ext(fn):
    """the ._part of the filename
    >>> file_ext("filename.txt")
    '.txt'
    """
    st=os.path.splitext(fn)
    add2log(f'fe:st={st}')
    return st[-1]

def file_base(fn):
    """the base part of base.txt
    >>> file_base("filename.txt")
    'filename'
    """
    st=os.path.splitext(fn)
    add2log(f'fb:st={st}')
    return st[0]

def file_leaf_base(path):
    """base of the leaf file
    >>> file_leaf_base("a/b/c/filename.txt")
    'filename'
    """
    pl=path_leaf(path)
    return file_base(pl)

#sparql.ipynb:    "ds_url=ec.collect_ext(ds_urls,ext)\n",
 #want to switch so _ are the flatten versions
def collect_ext(l,ext):
  return list(filter(lambda x: file_ext(x)==ext,flatten(l)))

def collect_ext_(l,ext):
    """filter list for extensions of interest
    >>> collect_ext_(['f1.zip', 'f2.txt', 'f3.nt', 'f4.txt'], '.txt')
    ['f2.txt', 'f4.txt']
    """
    return list(filter(lambda x: file_ext(x)==ext,l))

def collect_pre(l,pre):
  return list(filter(lambda x: x.startswith(pre),flatten(l)))

def collect_pre_(l,pre):
    """take from list things starting w/a prefix
    >>> collect_pre_(['http://f1.zip', 'https://f2.txt', 'urn://f3.nt', 'urn://f4.txt'], 'http')
    ['http://f1.zip', 'https://f2.txt']
    """
    return list(filter(lambda x: x.startswith(pre),l))

def collect_str(l,s):
  return list(filter(lambda x: s in x ,flatten(l)))

def collect_str_(l,s):
    """ret lists that have particular str in them
    >>> collect_str_([[1, 2, 'str'], [3, 4], ['str', 5]],'str')
    [[1, 2, 'str'], ['str', 5]]
    """
    return list(filter(lambda x: s in x ,l))

#could think a file w/'.'s in it's name, had an .ext
 #so improve if possible; hopefully not by having a list of exts
  #but maybe that the ext is say 6char max,..
#only messed up filename when don't send in w/.ext and has dots, but ok w/.ext

def has_ext(fn):
    """does filename have an extension
    >>> has_ext('zipfile_wo_ext')
    False
    """
    return (fn != file_base(fn))

def wget_(fn): #start using requests version below instead, though this is hardier now
    #cs= f'wget -a log {fn}'  #--quiet
    cs= f'wget --tries=2 -a log {fn}' 
    os_system(cs)
    return path_leaf(fn) #new below from get_repo.py

#def wget(url):
def request(url):
    import requests
    fn=path_leaf(url)
    response = requests.get(url)
    open(fn, "wb").write(response.content)
    return fn

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
    #wget(url)
    request(url)
    return "import ec"

    #often want to get newest ec.py if debugging
    # but don't need to get qry-txt each time, but if fails will use latest download anyway

def get_ec_txt(url):
    fnb= pre_rm(url)
    #wget(url)
    request(url)
    return get_txtfile(fnb)

#def blabel_l(fn): 
#def read_sd_(fn):
#def read_sd(fn):

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

#def post_untar(url,uncompress="tar -zxvf "): #could be "unzip -qq "
#def install_url(url): #use type for uncompress later
#def install_java():
#def install_jena(url="https://dlcdn.apache.org/jena/binaries/apache-jena-4.5.0.tar.gz"):
#def install_fuseki(url="https://dlcdn.apache.org/jena/binaries/apache-jena-fuseki-4.5.0.tar.gz"):
#def install_any23(url="https://dlcdn.apache.org/any23/2.7/apache-any23-cli-2.7.tar.gz"):
#def setup_blabel(url="http://geocodes.ddns.net/ld/bn/blabel.jar"):
#def setup_j(jf=None):
#-----------------------------qry.py has
##def get_relateddatafilename_txt(url="https://raw.githubusercontent.com/earthcube/facetsearch/toolMatchNotebookQuery/client/src/sparql_blaze/sparql_relateddatafilename.txt"):
#def get_relateddatafilename_txt(url="https://raw.githubusercontent.com/MBcode/ec/master/NoteBook/sparql_relateddatafilename.txt"):
#def get_webservice_txt(url="https://raw.githubusercontent.com/earthcube/facetsearch/master/client/src/sparql_blaze/sparql_gettools_webservice.txt"):
#def get_download_txt(url="https://raw.githubusercontent.com/earthcube/facetsearch/master/client/src/sparql_blaze/sparql_gettools_download.txt"):
#def get_notebook_txt(url="https://raw.githubusercontent.com/MBcode/ec/master/NoteBook/sparql_gettools_notebook.txt"):
##def get_query_txt(url="https://raw.githubusercontent.com/earthcube/facetsearch/master/client/src/sparql_blaze/sparql_query.txt"):
#def get_query_txt(url="https://raw.githubusercontent.com/MBcode/ec/master/NoteBook/sparql-query.txt"):
##def get_summary_query_txt(url="https://raw.githubusercontent.com/earthcube/facetsearch/master/client/src/sparql_blaze/sparql_query.txt"): #had limit at end
#def get_summary_query_txt(url="http://mbobak.ncsa.illinois.edu/ec/nb/sparql_blaze.txt"):
#def get_subj2urn_txt(url="http://geocodes.ddns.net/ec/nb/sparql_subj2urn.txt"):
#def get_graphs_txt(url="http://geocodes.ddns.net/ec/nb/sparql_graphs.txt"):
#def get_graph_txt(url="http://geocodes.ddns.net/ec/nb/get_graph.txt"):
#def get_summary_txt(url="http://geocodes.ddns.net/ec/nb/get_summary.txt"):
#-----

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
    #wget(fn)
    request(fn)
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

#def init_rdflib(): #maybe combine w/init_sparql
##def crawl_LD(url) ;could get other than jsonld, &fuse
#def url2jsonLD(url):
#def url2jsonLD_fn(url,fn):
#def url2jsonLD_file(url):
#---------------------rdf2nq.py
##def fn2jsonld(fn, base_url=None):
#def fn2jsonld(fn, base_url=None):
#def getjsonLD(url):
##def 2nt  from any rdf frmt to a .nt file, bc easiest to concat
#def xml2nt(fn,frmt="xml"):  #could also use rapper here, see: rdfxml2nt
#def to_nt_str(fn,frmt="json-ld"):  
#---
#def jsonld2nt(fn,frmt="json-ld"):
#def url2nt(url):
#def append2everyline(fn,aptxt,fn2=None):
#def url2nq(url):

def ls(dir): #there are other py commands to do this
    cs=f'ls {dir}'
    return os_system_(cs)

def ls_(path):
    lstr=ls(path)
    return lstr.split("\n")

##def nt2nq(fn,dir="nt"): #default ~hardcode, bc not sent in loop
#def nt2nq(fn,dir=""): #use this dflt in ec.py in case no ./nt
#def all_nt2nq(dir):
#def rdflib_viz(url,ft=None): #or have it default to ntriples ;'turtle'
#def read_rdf(fn,ext=".tsv"):  #too bad no tabs though../fix?
##def urn2uri_(urn):  #looking for a more stable indicator
#def urn2uri(urn): 
#def get_gID(): #could have arg that defaults to gName
#def get_collectionID(collectionName):
#def set_collectionName(collectionName):
##def set_collection_rows(collection,rows): #needs collection generated from set_collectionName right now
#def set_collection_rows(collectionName,rows):
#def rows2collection_(rows,collectionName):
##def rows2collection_nt(rows,collectionName): #could reuse above in parts & transform
#def rows2collection(rows,collectionName): #redo above 1st
##def urn2uri(urn): #from wget_rdf, replace w/this call soon
#def urn2urls(urn): #from wget_rdf, replace w/this call soon
#def urn2fnt(urn):
#def rdf2nt(urlroot_):
#def is_node(url): #not yet
##def is_tn(url):
#def tn2bn(url):
#def cap_http(url):
#def cap_doi(url):
#def fix_url3(url):
##def fix_url_(url,obj=True): #should only get a chance to quote if the obj of the triple
#def fix_url(url):
#def df2nt(df,fn=None):
#def get_rdf(urn,viz=None): #get graph 
#def get_rdf2nt_str(urn): #get graph 
#def get_rdf2jld_str(urn):
#def compact_jld_str(jld_str):
#def get_rdf2nt(urn):
#def nt2jld(fn):
#def nt2ttl(fn):
#def get_rdf2jld(urn):
#def get_rdf2ttl(urn):
#def wget_rdf(urn,viz=None):
#def wget_rdf_(urn,viz=None):
#def init_rdf():
#def init_sparql(): #maybe combine w/init_rdflib
#def dfn(fn):
#def sq_file(sq,fn=1):
#    #global default_world
#    return list(o2.default_world.sparql(sq))
#def pp_l2s(pp,js=None):
#def rget(pp,fn=1):
#def grep_po_(p,fn):
#def grep_po(p,fn):
##def grep_pred2obj(p,fn):
#def grep2obj(p,fn): #=f_nt): #fn could default to (global) f_nt
##def urn2accessURL(urn):
#def urn2accessURL(urn,fnt=None):
#def getDatasetURLs(IDs,dfS=None):
#  #ds_url= list(map(lambda urls: urls[0],ds_urls)) if d1p else list(map(lambda urls: urls[row][1], ds_urls)) #default to 1st of the urls
#  ds_url= list(map(lambda urls: urls[0],ds_urls)) #default to 1st of the urls ;need to check in 2nd/sparql_nb w/o collection
#def sparql_f2(fq,fn,r=None): #jena needs2be installed for this, so not in NB yet;can emulate though
##def nt2dn(fn,n):
#def nt2dn(fn=f_nt,n=1):
#def df2URNs(df):
#def dfRow2urn(df,row):
#def urn2rdf(urn,n=1):
#def dfRow2rdf(df,row):
#def dfRow2urls(df,row): 
#def nt2g(fnt):
#def nt_str2g(nt_str): 
##def diff_nt(fn1,fn2):
#def diff_nt_g(fn1,fn2):
#def dump_nt_sorted(g):
#def diff_nt(fn1,fn2):
#def pp2so(pp,fn): #might alter name ;basicly the start of jq via sparql on .nt files
##def gdf(qry,g):
#def gdf(qry,fn):
#def query_fn(qry,fn_): 
#def kg_query_fn(qry,fn): #needs fix/testing 
#def rdfxml2nt(fnb):
#def nt2svg(fnb):
#def display_svg(fn):
##def append2allnt(fnb): #in_colab no .all.nt to start w/
#def append2allnt(fnb=None):
#    "append to default viz file"
#def nt_viz(fnb=".all.nt"):
#def rdfxml_viz(fnb): #cp&paste (rdf)xml file paths from in .zip files
#def viz(fn=".all.nt"): #might call this rdf_viz once we get some other type of viz going
#def alive():
#def log_msg(url): #in mknb.py logbad routed expects 'url' but can encode things
##def check_size_(fs,df): #earlier now unused version
#def check_size(fs,df):
#def nt2ft(url): #could also use rdflib, but will wait till doing other queries as well
#def file_type(fn): #w/unzip it can be a dir; so fix
##def read_file(fnp, ext=nt2ft(fnp)):  $should send 'header' in
#def read_file(fnp, ext=None):  #download url and ext/filetype
#def get_sources_csv(url="https://raw.githubusercontent.com/MBcode/ec/master/crawl/sources.csv"):
#def get_sources_df(url="https://raw.githubusercontent.com/MBcode/ec/master/crawl/sources.csv"):
##def get_sources_urls(): #could become crawl_
#def crawl_sources_urls(): #work on sitemap lib to handle non-stnd ones
#-------------qry.py has:
#def qs2graph(q,sqs):
#def urn2graph(urn,sqs):
##def sti(sqs, matchVar, replaceValue): #assume only1(replacement)right now,in the SPARQL-Qry(file)String(txt)
#def v2iqt(var,sqs):  #does the above fncs
##def iqt2df(iqt,endpoint="https://graph.geodex.org/blazegraph/namespace/nabu/sparql"):
##def iqt2df(iqt,endpoint="https://graph.geocodes.earthcube.org/blazegraph/namespace/earthcube/sparql"):
##def iqt2df(iqt,endpoint=dflt_endpoint):
#def iqt2df(iqt,endpoint=None):
#def v4qry(var,qt):
#def search_query(q): #same as txt_query below
#def search_relateddatafilename(q):
#def search_download(urn):
#def search_webservice(urn):
#def search_notebook(urn):
#def subj2urn(doi):
#def get_graphs():
#def get_graph(g):
#def get_summary(g=""): #g not used but could make a version that gets it for only 1 graph
##def get_summary_query(g=""): #g not used but could make a version that gets it for only 1 graph
#def summary_query(g=""): #this is finally used in: txt_query_summary
#----------
 #-qry.py doesn't incl these just below, but could _ also want to get a kglab query a file, that is better than what we have in
##def txt_query_(q,endpoint=None):
#def txt_query_(q,endpoint=None):
#def txt_query_summary(q): #might need to switch qry as well, to gs.txt
##def get_graphs_list(endpoint=None):
#def get_graphs_list(endpoint=None,dump_file=None):
#def get_graphs_cache(endpoint="http://ideational.ddns.net:9999/bigdata/namespace/nabu/sparql",dumpfile=None):
#def get_graphs_lon(repo=None,endpoint="http://ideational.ddns.net:3040/all/sparql"): 
##def get_graph_per_repo(grep="milled",endpoint=None,dump_file="graphs.csv"): #try w/(None, ncsa_endpoint)
#def get_graph_per_repo(grep="milled",endpoint="https://graph.geodex.org/blazegraph/namespace/earthcube/sparql",dump_file="graphs.csv"):

def urn_tail(urn):
    "like urn_leaf"
    return  urn if not urn else urn.split(':')[-1]

def urn_tails(URNs):
    return list(map(lambda s: s if not s else s.split(':')[-1],URNs))
    #return list(map(urn_tail,URNs))

#def get_graphs_tails(endpoint):
# #incl the default path for each of those other queries, ecrr, ;rdf location as well
##def sq2df(qry_str):
##def txt_query(qry_str): #consider sending in qs=None =dflt lookup as now, or use what sent in
#def txt_query(qry_str,sqs=None): #a generalized version would take pairs/eg. <${g}> URN ;via eq urn2graph
#def get_subj_from_index(index):
#def get_index_from_subj(subj):
#def combine_features(row):
#def get_related(likes):
#def get_related_indices(like_index):
#def dfCombineFeaturesSimilary(df, features = ['kw','name','description','pubname']):
#def test_related(q,row=0): #eg "Norway"
#def show_related(df,row):  #after dfCombineFeaturesSimilary is run on your df 'sparql results'
#def get_distr_dicts(fn):
#def add_id(d): #there will be other predicates to check
#def get_id(d):
#def get_idd(d):
#def jld2crate(fn):
#def jld2crate_(fn):
#def t1():
#def t2(fn="324529.jsonld"):
##▶<102 a09local: /milled/geocodes_demo_datasets> mo 09517b808d22d1e828221390c845b6edef7e7a40.rdf
##_:bcbhdkms5s8cef2c4s7j0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://schema.org/Dataset> "urn:09517b808d22d1e828221390c845b6edef7e7a40".
##fn = "09517b808d22d1e828221390c845b6edef7e7a40.rdf"

def replace_last(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail

#---------------------rdf2nq.py
##def fn2nq(fn): #from 2nq.py
#def nt_fn2nq(fn): #already a nt2nq
#def riot2nq(fn):
#def to_nq(fn,prefix=None):
#def fn2nq(fn): #if is_http wget and call self again/tranfrom input
#--------------
#  #def xml2nt(fn,frmt="xml") takes json-ld as a format
#  #also: def riot2nq(fn): "process .jsonld put out .nq"
#def summoned2nq(s=None):
#def serve_nq(fn):
#def summon2serve(s=None): #~nabu like
#def prov2mapping(url): #use url from p above
#def prov2mappings(urls): #use urls from p above

#some bucket/gen-urls will be json(ld)
def url2json(url):
    import requests
    r=requests.get(url)
    return r.content

def get_url(url): #also in testing 
    "request.get url"
    import requests
    r=requests.get(url)
    return r.content

def is_bytes(bs):
    return isinstance(bs, bytes)

#_testing was@2672
#_testing end

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

#def rcsv(fn,d=","):
#=these should have gone in dct testing
#def tgc1_(ep=None):
#def tgc1():
#=============will have more notes on a breakdown, but will sketch in notes v here for a bit
#there are also sections that make use of certain libs that should be broken out separately, eg. anything that uses java
