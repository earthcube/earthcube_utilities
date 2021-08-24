#=this is also at gitlab now, but won't get autoloaded until in github or allow for gitlab_repo
 #but for cutting edge can just get the file from the test server, so can use: get_ec()

#pagemil parameterized colab/gist can get this code via:
#with httpimport.github_repo('MBcode', 'ec'):
#  import ec
import os
import sys

#more loging
#def install_recipy():
#    cs='pip install recipy'
#    os.system(cs)
#install_recipy()
#import recipy

#from qry.py
def put_txtfile(fn,s):
    with open(fn, "w") as f:
        return f.write(s)

#start adding more utils, can use to: fn=read_file.path_leaf(url) then: !head fn
def path_leaf(path):
    import ntpath
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def file_ext(fn):
    st=os.path.splitext(fn)
    return st[-1]

def file_base(fn):
    st=os.path.splitext(fn)
    return st[0]

#could think a file w/'.'s in it's name, had an .ext
 #so improve if possible; hopefully not by having a list of exts
  #but maybe that the ext is say 6char max,..
#only messed up filename when don't send in w/.ext and has dots, but ok w/.ext

def has_ext(fn):
    return (fn != file_base(fn))

def wget(fn):
    #cs= f'wget -a log {fn}' 
    cs= f'wget --tries=2 -a log {fn}' 
    os.system(cs)

def pre_rm(url):
    fnb=path_leaf(url)
    cs=f'rm {fnb}'
    os.system(cs)

def get_ec(url="http://mbobak-ofc.ncsa.illinois.edu/ext/ec/nb/ec.py"):
    pre_rm(url)
    wget(url)
    return "import ec"

def add_ext(fn,ft):
    fn1=path_leaf(fn) #just the file, not it's path
    fext=file_ext(fn1) #&just it's .ext
    r=fn1
    if fext==None or fext=='':
        fnt=fn1 + ft
        #cs= f'mv {fn1} {fnt}' 
        cs= f'sleep 2;mv {fn1} {fnt}' 
        os.system(cs)
        r=fnt
    return r

def wget_ft(fn,ft):
    wget(fn)
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
        os.system(cs)
        fnb=file_base(fnl)
        if os.path.isdir(fnb):
            cs=f'ln -s . content' #so can put . before what you paste
            os.system(cs)
    return fs

rdflib_inited=None
def init_rdflib():
    cs='pip install rdflib networkx'
    os.system(cs)
    rdflib_inited=cs

#get fnb + ".nt" and put_txtfile that str
def xml2nt(fn):
    if rdflib_inited==None:
        init_rdflib()
    fnb=file_base(fn)
    from rdflib import Graph
    g = Graph()
    g.parse(fn, format="xml")
    #s=g.serialize(format="ntriples").decode("u8") #works via cli,nb had ntserializer prob
    s=g.serialize(format="ntriples") #try w/o ;no, but works in NB w/just a warning
    fnt=fnb+".nt"
    put_txtfile(fnt,s)
    return len(s) 

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
fnt=None

def wget_rdf(urn,viz=None):
    if urn==None:
        return f'no-urn:{urn}'
    #if(urn!=None and urn.startswith('urn:')):
    elif urn.startswith('urn:'):
        url=urn.replace(":","/").replace("urn","https://oss.geodex.org",1)
        urlroot=path_leaf(url) #file w/o path
        url += ".rdf"
        cs= f'wget -a log {url}' 
        os.system(cs)
        fn1 = urlroot + ".rdf"
        fn2 = urlroot + ".nt" #more specificially, what is really in it
        cs= f'mv {fn1} {fn2}' #makes easier to load into rdflib..eg: 
        os.system(cs)
        fnt=fn2
        #from rdflib import Graph
        #g = Graph()
        #g.parse(fn2)
        if viz: #can still get errors
            rdflib_viz(fn2) #.nt file #can work, but looks crowded now
    elif urn.startswith('/'):
        url=urn.replace("/","http://mbobak-ofc.ncsa.illinois.edu/ld/",1).replace(".jsonld",".nt",1)
        urlroot=path_leaf(url) #file w/o path
        #url += ".nt"
        cs= f'wget -a log {url}' 
        os.system(cs)
        #fn2 = urlroot + ".nt" #more specificially, what is really in it
        if viz: #can still get errors
            #rdflib_viz(fn2) #.nt file #can work, but looks crowded now
            rdflib_viz(urlroot) #.nt file #can work, but looks crowded now
    else:
        return f'bad-urn:{urn}'

rdf_inited=None
def init_rdf():
    cs='apt-get install raptor2-utils graphviz'
    os.system(cs)
    rdf_inited=cs

def nt2svg(fnb):
    if has_ext(fnb):
        fnb=file_base(fnb)
    if rdf_inited==None:
        init_rdf()
    cs= f'rapper -i ntriples -o dot {fnb}.nt|cat>{fnb}.dot'
    os.system(cs) 
    cs= f'dot -Tsvg {fnb}.dot |cat> {fnb}.svg'
    os.system(cs)

#consider running sed "/https/s//http/g" on the .nt file, as an option, 
 #for cases were it's use as part of the namespace is inconsistent


#https://stackoverflow.com/questions/30334385/display-svg-in-ipython-notebook-from-a-function
def display_svg(fn):
    if rdf_inited==None:
        init_rdf()
    from IPython.display import SVG, display
    display(SVG(fn))

def append2allnt(fnb):
    cs= f'cat {fnb}.nt >> .all.nt'
    os.system(cs) 

def nt_viz(fnb=".all.nt"):
    if has_ext(fnb):
        fnb=file_base(fnb)
    nt2svg(fnb) #base(before ext)of .nt file, makes .svg version&displays
    fns= fnb + ".svg"
    display_svg(fns)
    if fnb!=".all":
        append2allnt(fnb)

def rdfxml_viz(fnb):
    xml2nt(fnb)
    nt_viz(fnb)

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

def check_size_(fs,df):
    if fs:
        if fs<300:
            df+= "[Warn:small]"
    else:
        df+= "[Warn:No File]"
    return df

def check_size(fs,df):
    "FileSize,DataFrame as ret txt"
    dfe=None
    if fs:
        if fs<300:
            dfe= "[Warn:small]"
    else:
        dfe= "[Warn:No File]"
    if dfe:
        log_msg(dfe) #should incl url/etc but start w/this
        df+=dfe
    return df

def read_file(fnp, ext=None):
    "can be a url, will call pd read_.. for the ext type"
    import pandas as pd
    import re
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
    if ext==None and len(ft)<1:
        wget(fn)
        df="no fileType info, doing:[!wget $url ],to see:[ !ls -l ] or FileExplorerPane on the left"
    elif ft=='.tsv' or re.search('tsv',ext,re.IGNORECASE) or re.search('tab-sep',ext,re.IGNORECASE):
        try:
            df=pd.read_csv(fn, sep='\t',comment='#',warn_bad_lines=True, error_bad_lines=False)
        except:
            df = str(sys.exc_info()[0])
            pass
    elif ft=='.csv' or re.search('csv',ext,re.IGNORECASE):
        try:
            df=pd.read_csv(fn,comment="#",warn_bad_lines=True, error_bad_lines=False)
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
