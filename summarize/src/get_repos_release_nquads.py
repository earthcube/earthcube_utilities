#!/usr/bin/env python3
#M Bobak, need to get gleaner output for a repo
# as issue126 comes to a close and release-graphs will be made as quads, so we can just pull them, to summarize them
#quick addition of s3path for this, and might be getting all repos at once, will find out/finish Mar2;this will get a rewrite
#as this came from get_repo almost called: get_repo_release_graph.py but will probably get them all so get_release_graphs.py
import os
import argparse
import logging as log   #can switch print's to log.info's but Readme expects it to the stdout
log.basicConfig(filename='get_repo_rg.log', encoding='utf-8', level=log.DEBUG,
                format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

##import ec
#import earthcube_utilities as ec  #make sure this is availabe
##import ../earthcube_utilities as ec  #assuming it is one level above
#for now keeping in a dir named after each repo, so next step can run2nq over it
 #where it takes the it's filename, to turn the triples into quads w/that name
#==from ec.py in case I don't want to import it:
cwd = os.getcwd()
ncsa_minio = "https://oss.geocodes.ncsa.illinois.edu/"
S3ADDRESS=os.getenv("S3ADDRESS")
S3KEY=os.getenv("S3KEY")
S3SECRET=os.getenv("S3SECRET")
dbg=False
S3PATH="gleaner/results/runX" #for old get_repo.py it was: gleaner/milled
s3path=os.getenv("S3PATH")
if s3path:
    S3APTH=s3path

def is_str(v):
    return type(v) is str

def is_http(u):
    if not is_str(u):
        log.warning("might need to set LD_cache") #have this where predicate called
        return None
    #might also check that the str has no spaces in it,&warn/die if it does
    return u.startswith("http")

def path_leaf(path):
    "everything after the last /"
    import ntpath
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

#from https://github.com/earthcube/earthcube_utilities/blob/dcm/earthcube_utilities/docs/breakdown.md#rdf-to-triples
#def s3client(config)
#def s3GetFile(s3client, file )
#def read_files(s3client, bucket, repo)
#that will probably replace just below

#def get_oss(minio_endpoint_url="https://oss.geocodes-dev.earthcube.org/",anon=True):
def get_oss(minio_endpoint_url="https://oss.geocodes.ncsa.illinois.edu/",anon=True):
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

#def oss_ls(path='test3/summoned',full_path=True,minio_endpoint_url="https://oss.geocodes-dev.earthcube.org/"):
#def oss_ls(path='gleaner/milled',full_path=True,minio_endpoint_url="https://oss.geocodes.ncsa.illinois.edu/"):
def oss_ls(path=S3PATH,full_path=True,minio_endpoint_url="https://oss.geocodes.ncsa.illinois.edu/"):
    oss=get_oss(minio_endpoint_url) #global oss
    import s3fs
    epl= oss.ls(path)
    if full_path:
        return list(map(lambda ep: f'{minio_endpoint_url}{ep}', epl))
    else:
        return epl

def os_system(cs):
    "run w/o needing ret value"
    os.system(cs)
    #add2log(cs)

def wget_(fn):
    #cs= f'wget -a log {fn}'  #--quiet
    cs= f'wget --tries=2 -a log {fn}'
    os_system(cs)
    return path_leaf(fn) #new

def wget(url):
    import requests
    fn=path_leaf(url)
    response = requests.get(url)
    open(fn, "wb").write(response.content)
    return fn

def list2txtfile(fn,l,wa="w"):
    with open(fn, "a") as f:
        for elt in l:
            f.write(f'{elt}\n')
    return len(l)

#def wget_oss_repo(repo=None,path="gleaner/milled",bucket=ncsa_minio):
#def wget_oss_repo(repo=None,path="gleaner/milled",s3address=ncsa_minio):
def wget_oss_repo(repo=None,path=S3PATH,s3address=ncsa_minio):
    "download all the rdf from a gleaner bucket"
    if not repo:
        global cwd  #I like having it go from the dirname, so files don't get mixed up
        repo=path_leaf(cwd)
        print(f'using, repo:{repo}=path_leaf({cwd})') #as 2nq.py will use cwd for repo, if it runs .rdf files
    files=oss_ls(f'{path}/{repo}',True,s3address)
    #print(f'will wget:{files}')
    for f in files:
        fl=path_leaf(f)
        from os.path import exists #can check if cached file there
        if not exists(fl):
            #print(f'will wget:{f}')
            print(f'will request:{f}')
            wget(f)
        else:
            print(f'have:{fl} already')
    if dbg: #might dump this all time, or by arg
        list2txtfile("l1h",files)
    return files

#=end utils

#def get_repo(repo):
def get_repo(repo, default_s3address= "https://oss.geocodes.ncsa.illinois.edu/"):
    #I think it uses cwd for repo, but want to override that
    if not repo:  
        #was cwd=ec.cwd, which are the same
        cwd=os.getcwd()
        #repo = ec.path_leaf(cwd)
        repo = path_leaf(cwd)
        print(f'using: cwd={cwd} to get the repo={repo} to downloads files into')
    else:
        print(f'will get files for {repo} in a dir named after it')
        exists=os.path.exists(repo)
        if not exists:
            print(f'will create the {repo} dir') 
            os.makedirs(repo)
        os.chdir(repo)
        cwd=os.getcwd()
        print(f'cd to: cwd={cwd} to get the repo={repo} to downloads files into')
    #ec.wget_oss_repo(repo) #defaults to bucket=ncsa_minio =https://oss.geocodes.ncsa.illinois.edu/
    #ec.wget_oss_repo(repo=repo,path="gleaner/milled",bucket=default_bucket)
    #wget_oss_repo(repo=repo,path="gleaner/milled",s3address=default_s3address)
    wget_oss_repo(repo=repo,path=S3PATH,s3address=default_s3address)

#def read_files(s3client, bucket, path) #path v repo ;path could incl the bucket
#def get_repos(path, default_s3address= "https://oss.geocodes.ncsa.illinois.edu/"):
def read_files(path=S3PATH, default_s3address= "https://oss.geocodes.ncsa.illinois.edu/"): #not s3_ bc still use urls
    "get all files/repos from path"
    if not path:
        log.warning("read_files:need a path")
        return None
    runXdir = path_leaf(path) #so can keep repo.nq files together on this machine, not necessary
    wget_oss_repo(None,path,s3address=default_s3address) #could still pull a repo at a time from the 'path'

def read_file(file, path=S3PATH, default_s3address= "https://oss.geocodes.ncsa.illinois.edu/"): #not s3_ bc still use urls
    "get one file=repo from path"
    if not path:
        log.warning("read_file:need a path")
        return None
    runXdir = path_leaf(path) #so can keep repo.nq files together on this machine, not necessary
    wget_oss_repo(file,path,s3address=default_s3address) #could still pull a repo at a time from the 'path'

def url_w_end_slash(url):
    if len(url)-1 != "/":
        return url + "/"
    else:
        return url

#later can import click, have 2nd arg be named eg.-bucket, and incl a -help
if __name__ == '__main__':
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument("repo",  help='repository name')
    parser.add_argument("--s3address",  help='s3address s3/minio url')
    parser.add_argument("--s3path",  help='s3path e.g. gleaner/results/runX')
    print(f'argv={sys.argv}')
    s3=""
    if(len(sys.argv)==1):
        #get_release_graphs.py assume just the path now soon, will change repo setting below&iteraction above
        #print("you need to enter the name of a repo to summarize")
        print("you need to enter the path of all the repo quad files to summarize")
    else:
        args = parser.parse_args() #would fail here, if no arg w/o printing help
        cli_s3=args.s3address
        s3=os.getenv("ECU_S3ADDRESS") 
        if cli_s3:  
            s3=cli_s3
            print(f'--s3address [{cli_s3}]  overrides ECU_S3ADDRESS [{s3}]')

    default_s3address= "https://oss.geocodes.ncsa.illinois.edu/"
    #s3=os.getenv("S3ADDRESS") 
    #if ec.is_str(s3):
    if is_str(s3):
        #if not ec.is_http(s3):
        if not is_http(s3):
            s3="https://" + url_w_end_slash(s3)
        #print(f'set default_bucket to S3ADDRESS={s3}')
        #print(f'set default_s3address to ECU_S3ADDRESS={s3}')
        print(f'set default_s3address to {s3}')
        default_s3address=s3
  # if(len(sys.argv)>2): #using argparse for this now
  #     default_s3address = url_w_end_slash(sys.argv[2])
  #     print(f'reset default_s3address to 2nd cli arg:{default_s3address}')
    #decide if want all repos at once so could just give path, or give each; solve by only having add_args
     #could do it, if 1 arg, then still a repo, and just get that file, otherwise get them all
    if(len(sys.argv)>1):
        repo = sys.argv[1]
        print(f'will run over:{repo}')
        #get_repo(repo)
     #  get_repo(repo,default_s3address)
        read_file(repo,s3path,default_s3address)
        #run2nq(repo) #done in next step
    else:
        print("use cwd=repo")
    #   get_repo(None)
        read_files(s3path,default_s3address)
