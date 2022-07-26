#M Bobak, for ncsa.uiuc NSF EarthCube effort, GeoCODES search&resource use w/in NoteBooks
# some on (new)direction(s) at: https://mbcode.github.io/ec
#=this is also at gitlab now, but won't get autoloaded until in github or allow for gitlab_repo
 #but for cutting edge can just get the file from the test server, so can use: get_ec()
rdf_inited,rdflib_inited,sparql_inited=None,None,None
def laptop(): #could call: in_binder
    "already have libs installed"
    global rdf_inited,rdflib_inited,sparql_inited
    rdf_inited,rdflib_inited,sparql_inited=True,True,True
    return "rdf_inited,rdflib_inited,sparql_inited=True,True,True"

def local():
    "do in binder till can autoset if not in colab"
    #put in a binder version of sparql_nb template, for now
    laptop()

#pagemil parameterized colab/gist can get this code via:
#with httpimport.github_repo('MBcode', 'ec'):   
#  import ec
#version in template used the earthcube utils
import os
import sys
import json
IN_COLAB = 'google.colab' in sys.modules
if not IN_COLAB:
    local()

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
    from collections.abc import Iterable
    if isinstance(l,list):
        return l[0]
    elif isinstance(l,Iterable):
        return list(l)[0]
    else:
        return l

def flatten(xss): #stackoverflow
    return [x for xs in xss for x in xs]

#from qry.py
def get_txtfile(fn):
    with open(fn, "r") as f:
        return f.read()

def get_jsfile2dict(fn):
    #s=get_txtfile(fn)
    #return json.loads(s)
    with open(fn, "r") as f:
        return json.load(f)

def put_txtfile(fn,s,wa="w"):
    #with open(fn, "w") as f:
    with open(fn, "a") as f:
        return f.write(s)

def date2log():
    cs="date>>log"
    os.system(cs)

def add2log(s):
    date2log()
    fs=f'[{s}]\n'
    put_txtfile("log",fs,"a")

def os_system(cs):
    os.system(cs)
    add2log(cs)

def os_system_(cs):
    "system call w/return value"
    s=os.popen(cs).read()
    add2log(cs)
    return s

#start adding more utils, can use to: fn=read_file.path_leaf(url) then: !head fn
def path_leaf(path):
    import ntpath
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def file_ext(fn):
    st=os.path.splitext(fn)
    add2log(f'fe:st={st}')
    return st[-1]

def file_base(fn):
    st=os.path.splitext(fn)
    add2log(f'fb:st={st}')
    return st[0]

def file_leaf_base(path):
    pl=path_leaf(path)
    return file_base(pl)

def collect_ext(l,ext):
  return list(filter(lambda x: file_ext(x)==ext,flatten(l)))

def collect_str(l,s):
  return list(filter(lambda x: s in x ,flatten(l)))

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
    install_url(url)

def install_fuseki(url="https://dlcdn.apache.org/jena/binaries/apache-jena-fuseki-4.5.0.tar.gz"):
    install_url(url)

def install_any23(url="https://dlcdn.apache.org/any23/2.7/apache-any23-cli-2.7.tar.gz"):
    install_url(url)

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
    return addpath

#get_  _txt   fncs:
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

rdflib_inited=None
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
    cs='pip install s3fs' #assume done rarely, once/session 
    os_system(cs)

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

def sitemap_len(url):
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

minio_prod= "https://oss.geodex.org" #minio
minio_dev= "https://oss.geocodes.earthcube.org"
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

#take urn2uri out of this, but have to return a few vars
def wget_rdf(urn,viz=None):
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

rdf_inited=None
def init_rdf():
    #cs='apt-get install raptor2-utils graphviz'
    cs='apt-get install raptor2-utils graphviz libmagic-dev' #can add jq yourself
    os_system(cs)  #incl rapper, can do a few rdf conversions
    rdf_inited=cs

#should just put sparql init in w/rdf _init, as not that much more work

sparql_inited=None
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
import requests

def alive():
    r = requests.get(f'{host}/alive')
    return r

def log_msg(url): #in mknb.py logbad routed expects 'url' but can encode things
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

#def read_file(fnp, ext=nt2ft(fnp)):
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
    elif ft=='.txt' or re.search('text',ext,re.IGNORECASE):
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
def iqt2df(iqt,endpoint="https://graph.geocodes.earthcube.org/blazegraph/namespace/earthcube/sparql"):
    "instantiated-query-template/txt to df"
    if not iqt:
        return "need isntantiated query text"
    import sparqldataframe, simplejson
    if sparql_inited==None:
        si= init_sparql()  #still need to init
        #qs= iqt #or si  #need q to instantiate
    add2log(iqt)
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

def subj2urn(doi):
    return v4qry(doi,"subj2urn")

def get_graphs():
    return v4qry("","graphs")

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
    endpoint = "https://graph.geocodes.earthcube.org/blazegraph/namespace/earthcube/sparql"
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
