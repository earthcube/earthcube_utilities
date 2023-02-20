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
import logging as log  #have some dgb prints, that will go to logs soon/but I find it slow to have to cat the small logs everytime 
log.basicConfig(filename='ecu.log', encoding='utf-8', level=log.DEBUG,
                format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
#def install_recipy():
#    cs='pip install recipy'
#    os.system(cs)
#install_recipy()
#import recipy

#from qry.py

#https://github.com/MBcode/dc/blob/main/dcm.py ----
#=starting a version of dc.py   
#that has mb.py and these 2 other files taken out, where it recomposes them
#in this staging ground, I'll call it: dcm.py, For: DeCoder-Module version
#-
#in a way, this is an example of how any file might just include what is necessary
# the summarize files, that use the last 2 imports, could then import mb
# as they do in this collection of files, and they should work the same way
#-
#as more a clean-room way of doing it, it could just start with
#import mb
from mb import *  #do this too, if you want this to approach be a replacement for: earthcube_utillities, that I can put in a new branch
#presently the files below have some fncs from the one above
  #was called qry.py in summarize
#import query 
#import rdf2nq 
#could try this, to avoid longer prefix, but will probably just import the parts you want and call directly
from query import * 
from rdf2nq import *
#so now to remove them, from those files, and make refs to mb ;done
#once again, this might just be an example, but could let you load all the utils
#-----


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
    cs=f'cat {fn}|sed "/ht*[ps]:..schema.org./s//http:\/\/www.w3.org\/ns\/dcat#/g"|cat>{fdn}'
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
#----this that was below is in query
##reminder, this was just an old version of the file
##the utils file above was updated more, as it is what is loaded from: httpimport.github_repo
##this is the begging of a packaged version of most of that, w/better organization
##I only left some of what was not already in the 1st sub-modules that became needed for summarization
