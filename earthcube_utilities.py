#pagemil parameterized colab/gist can get this code via:
#with httpimport.github_repo('MBcode', 'ec'):
#  import ec
import os
import sys

#start adding more utils, can use to: fn=read_file.path_leaf(url) then: !head fn
def path_leaf(path):
    import ntpath
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def file_ext(fn):
    st=os.path.splitext(fn)
    return st[-1]

def wget(fn):
    cs= f'wget -a log {fn}' 
    os.system(cs)

def add_ext(fn,ft):
    fn1=path_leaf(fn) #just the file, not it's path
    fext=file_ext(fn1) #&just it's .ext
    if fext==None or fext=='':
        fnt=fn1 + ft
        cs= f'mv {fn1} {fnt}' 
        os.system(cs)

def wget_ft(fn,ft):
    wget(fn)
    add_ext(fn,ft)

def wget_rdf(urn):
    if(urn!=None and urn.startswith('urn:')):
        url=urn.replace(":","/").replace("urn","https://oss.geodex.org",1)
        urlroot=path_leaf(url) #root before ext added
        url += ".rdf"
        cs= f'wget -a log {url}' 
        os.system(cs)
        fn1 = urlroot + ".rdf"
        fn2 = urlroot + ".nt" #more specificially, what is really in it
        cs= f'mv {fn1} {fn2}' #makes easier to load into rdflib..eg: 
        os.system(cs)
        #from rdflib import Graph
        #g = Graph()
        #g.parse(fn2)
    else:
        return f'bad-urn:{urn}'

#should change os version of wget to request so can more easily log the return code
 #maybe, but this is easiest way to get the file locally to have to use
  #though if we use a kglab/sublib or other that puts right to graph, could dump from that too

#add 'rty'/error handling, which will incl sending bad-download links back to mknp.py
 #log in the except sections, below

def read_file(fnp, ext=None):
    "can be a url, will call pd read_.. for the ext type"
    import pandas as pd
    import re
    fn=fnp.strip('/')
    fn1=path_leaf(fn) #just the file, not it's path
    fext=file_ext(fn1) #&just it's .ext
    #url = fn
    if(ext!=None):
        ft="." + ext
    else: #use ext from fn
        ft=str(fext)
    df=""
    if ext==None and len(ft)<1:
        wget(fn)
        df="no fileType info, doing:[!wget $url ],to see:[ !ls -l ]"
    elif ft=='.tsv' or re.search('tsv',ext,re.IGNORECASE) or re.search('tab-sep',ext,re.IGNORECASE):
        try:
            df=pd.read_csv(fn, sep='\t',comment='#')
        except:
            df = str(sys.exc_info()[0])
            pass
    elif ft=='.csv' or re.search('csv',ext,re.IGNORECASE):
        try:
            df=pd.read_csv(fn)
        except:
            df = str(sys.exc_info()[0])
            pass
    elif ft=='.txt' or re.search('text',ext,re.IGNORECASE):
        try:
            df=pd.read_csv(fn, sep='\n',comment='#')
        except:
            df = str(sys.exc_info()[0])
            pass
    elif ft=='.zip' or re.search('zip',ext,re.IGNORECASE):
        ft='.zip'
        wget_ft(fn,ft)
#       df=pd.read_csv(fn, sep='\t',comment='#')
        df="can't read zip w/o knowing what is in it, doing:[!wget $url ],to see:[ !ls -l ]"
    else:
        wget_ft(fn,ft)
        #df="no reader, can !wget $url"
        df="no reader, doing:[!wget $url ],to see:[ !ls -l ]"
    #look into bagit next/maybe, also log get errors, see if metadata lets us know when we need auth2get data
    #if(urn!=None): #put here for now
    #    wget_rdf(urn)
    return df
