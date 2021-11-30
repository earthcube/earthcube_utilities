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

#pagemil parameterized colab/gist can get this code via:
#with httpimport.github_repo('MBcode', 'ec'):   
#  import ec
#version in template used the earthcube utils
import os
import sys
import json

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

#from qry.py
def get_txtfile(fn):
    with open(fn, "r") as f:
        return f.read()

def get_jsfile2dict(fn):
    s=get_textfile(fn)
    return json.loads(s)

def put_txtfile(fn,s,wa="w"):
    #with open(fn, "w") as f:
    with open(fn, wa) as f:
        return f.write(s)

def add2log(s):
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

#could think a file w/'.'s in it's name, had an .ext
 #so improve if possible; hopefully not by having a list of exts
  #but maybe that the ext is say 6char max,..
#only messed up filename when don't send in w/.ext and has dots, but ok w/.ext

def has_ext(fn):
    return (fn != file_base(fn))

def wget(fn):
    #cs= f'wget -a log {fn}' 
    cs= f'wget --tries=2 -a log {fn}' 
    os_system(cs)

def pre_rm(url):
    fnb=path_leaf(url)
    cs=f'rm {fnb}'
    os_system(cs)
    return fnb

def get_ec(url="http://mbobak-ofc.ncsa.illinois.edu/ext/ec/nb/ec.py"):
    pre_rm(url)
    wget(url)
    return "import ec"

    #often want to get newest ec.py if debugging
    # but don't need to get qry-txt each time, but if fails will use latest download anyway

def get_ec_txt(url):
    fnb= pre_rm(url)
    wget(url)
    return get_txtfile(fnb)

def get_webservice_txt(url="https://raw.githubusercontent.com/earthcube/facetsearch/master/client/src/sparql_blaze/sparql_gettools_webservice.txt"):
    return get_ec_txt(url)

def get_download_txt(url="https://raw.githubusercontent.com/earthcube/facetsearch/master/client/src/sparql_blaze/sparql_gettools_download.txt"):
    return get_ec_txt(url)

def get_notebook_txt(url="https://raw.githubusercontent.com/MBcode/ec/master/NoteBook/sparql_gettools_notebook.txt"):
    return get_ec_txt(url)

def get_query_txt(url="https://raw.githubusercontent.com/MBcode/ec/master/NoteBook/sparql-query.txt"):
    return get_ec_txt(url)

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
    cs='pip install rdflib rdflib-jsonld networkx extruct' 
    os_system(cs)
    rdflib_inited=cs

#-from crawlLD.py
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

def wget_rdf(urn,viz=None):
    if urn==None:
        return f'no-urn:{urn}'
    #if(urn!=None and urn.startswith('urn:')):
    elif urn.startswith('urn:'):
        global f_nt
        url=urn.replace(":","/").replace("urn","https://oss.geodex.org",1)
        urlroot=path_leaf(url) #file w/o path
        urlj= url + ".jsonld" #get this as well so can get_jsfile2dict the file
        urlj.replace("milled","summoned")
        url += ".rdf"
        cs= f'wget -a log {url}' 
        os_system(cs)
        cs= f'wget -a log {urlj}' 
        os_system(cs)
        fn1 = urlroot + ".rdf"
        fn2 = urlroot + ".nt" #more specificially, what is really in it
        #cs= f'mv {fn1} {fn2}' #makes easier to load into rdflib..eg: #&2 read into df
        cs= f'cat {fn1}|sed "/> /s//>\t/g"|sed "/ </s//\t</g"|sed "/doi:/s//DOI:/g"|cat>{fn2}'
        os_system(cs)   #fix .nt so .dot is better ;eg. w/doi
        f_nt=fn2
        #from rdflib import Graph
        #g = Graph()
        #g.parse(fn2)
        if viz: #can still get errors
            rdflib_viz(fn2) #.nt file #can work, but looks crowded now
        return read_rdf(f_nt)
    elif urn.startswith('/'):
        url=urn.replace("/","http://mbobak-ofc.ncsa.illinois.edu/ld/",1).replace(".jsonld",".nt",1)
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
    cs='apt-get install raptor2-utils graphviz'
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
    "FileName ore d#"
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
    dfn=dfn(fn)
#r=ec.sq_file("PREFIX : <http://www.w3.org/ns/dcat#> SELECT distinct ?s ?o WHERE  { ?s :spatialCoverage/:geo/:box ?o}","d1.nt")
    #s1="PREFIX : <http://www.w3.org/ns/dcat#> SELECT distinct ?s ?o WHERE  { ?s "
    s1="PREFIX : <https://schema.org/> SELECT distinct ?s ?o WHERE  { ?s " #till fix sed
    s2=" ?o}"
    #r=ec.sq_file(s1 + ":spatialCoverage/:geo/:box" + s2,dfn)
    pps=pp_l2s(pp)
    qs=s1 + pps + s2
    print(qs)
    add2log(f'rget:{qs}')
    r=sq_file(qs,dfn)
    return r
#-
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
def nt2dn(fn,n):
    ".nt to d#.nt where n=#, w/http/s schema.org all as dcat" 
    fdn= f'd{n}.nt'
    #fnd=dfn(fn) #maybe gen fn from int
    cs=f'cat {fn}|sed "/ht*[ps]:..schema.org./s//http:\/\/www.w3.org\/ns\/dcat#/g"|cat>{fdn}'  #FIX
    os_system(cs) #this makes queries a LOT easier
    return fdn

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

def read_file(fnp, ext=None):  #download url and ext/filetype
#def read_file(fnp, ext=nt2ft(fnp)):
    "can be a url, will call pd read_.. for the ext type"
    import pandas as pd
    import re
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
            df=pd.read_csv(fn, sep='\t',comment='#',warn_bad_lines=True, error_bad_lines=False)
            #df=pd.read_csv(fn, sep='\t',comment='#')
        except:
            df = str(sys.exc_info()[0])
            pass
    elif ft=='.csv' or re.search('csv',ext,re.IGNORECASE):
        try:
            df=pd.read_csv(fn,comment="#",warn_bad_lines=True, error_bad_lines=False)
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
        #if fs and fs<300:
        #    df+= "[Warn:small]"
        df=check_size(fs,df)
    else:
        fs=wget_ft(fn,ft)
        #fs=os.path.getsize(fnl) #assuming it downloads w/that name
        #df="no reader, can !wget $url"
        df=f'no reader, doing:[!wget $url ],to see:[ !ls -l ]size:{fs} or FileExplorerPane on the left'
        #if fs and fs<300:
        #    df+= "[Warn:small]"
        df=check_size(fs,df)
    #look into bagit next/maybe, also log get errors, see if metadata lets us know when we need auth2get data
    #if(urn!=None): #put here for now
    #    wget_rdf(urn)
    return df

 #probably drop the [ls-l] part&just have ppl use fileBrowser, even though some CLI would still be good
#not just 404, getting small file back also worth logging
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

def iqt2df(iqt,endpoint="https://graph.geodex.org/blazegraph/namespace/nabu/sparql"):
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
    sqs = eval("get_" + qt + "_txt()")
    iqt = v2iqt(var,sqs)
    return iqt2df(iqt)

def search_query(q): #same as txt_query below
    return v4qry(q,"query")

def search_download(urn):
    return v4qry(urn,"download")

def search_webservice(urn):
    return v4qry(urn,"webservice")

def search_notebook(urn):
    return v4qry(urn,"notebook")

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
    endpoint = "https://graph.geodex.org/blazegraph/namespace/nabu/sparql"
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

#=so after sparql-nb: df=ec.txt_query(q)
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
    main=df['description'][row]
    print(f'related to row={row},{main}')
    related=get_related_indices(row)
    for ri in related:
        des=df['description'][ri]
        print(f'{ri}:{des}')
