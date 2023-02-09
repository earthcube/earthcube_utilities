#!/usr/bin/env python3
#M Bobak, need to get gleaner output for a repo
# for now have to pull all files to turn to quads here ;till issue126 
import os
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

def is_str(v):
    return type(v) is str

def is_http(u):
    if not is_str(u):
        print("might need to set LD_cache") #have this where predicate called
        return None
    #might also check that the str has no spaces in it,&warn/die if it does
    return u.startswith("http")

def path_leaf(path):
    "everything after the last /"
    import ntpath
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

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
def oss_ls(path='gleaner/milled',full_path=True,minio_endpoint_url="https://oss.geocodes.ncsa.illinois.edu/"):
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

def wget(fn):
    #cs= f'wget -a log {fn}'  #--quiet
    cs= f'wget --tries=2 -a log {fn}'
    os_system(cs)
    return path_leaf(fn) #new

def wget_oss_repo(repo=None,path="gleaner/milled",bucket=ncsa_minio):
    "download all the rdf from a gleaner bucket"
    if not repo:
        global cwd  #I like having it go from the dirname, so files don't get mixed up
        repo=path_leaf(cwd)
        print(f'using, repo:{repo}=path_leaf({cwd})') #as 2nq.py will use cwd for repo, if it runs .rdf files
    files=oss_ls(f'{path}/{repo}',True,bucket)
    #print(f'will wget:{files}')
    for f in files:
        fl=path_leaf(f)
        from os.path import exists #can check if cached file there
        if not exists(fl):
            print(f'will wget:{f}')
            wget(f)
        else:
            print(f'have:{fl} already')
    if dbg: #might dump this all time, or by arg
        list2txtfile("l1h",files)
    return files

#=end utils

#def get_repo(repo):
def get_repo(repo, default_bucket= "https://oss.geocodes.ncsa.illinois.edu/"):
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
    wget_oss_repo(repo=repo,path="gleaner/milled",bucket=default_bucket)

def url_w_end_slash(url):
    if len(url)-1 != "/":
        return url + "/"
    else:
        return url

#later can import click, have 2nd arg be named eg.-bucket, and incl a -help
if __name__ == '__main__':
    import sys
    print(f'argv={sys.argv}')
    default_bucket= "https://oss.geocodes.ncsa.illinois.edu/"
    #s3=os.getenv("S3ADDRESS") 
    s3=os.getenv("ECU_S3ADDRESS") 
    #if ec.is_str(s3):
    if is_str(s3):
        #if not ec.is_http(s3):
        if not is_http(s3):
            s3="https://" + url_w_end_slash(s3)
        #print(f'set default_bucket to S3ADDRESS={s3}')
        print(f'set default_bucket to ECU_S3ADDRESS={s3}')
        default_bucket=s3
    if(len(sys.argv)>2):
        default_bucket = url_w_end_slash(sys.argv[2])
        print(f'reset default_bucket to 2nd cli arg:{default_bucket}')
    if(len(sys.argv)>1):
        repo = sys.argv[1]
        print(f'will run over:{repo}')
        #get_repo(repo)
        get_repo(repo,default_bucket)
        #run2nq(repo) #done in next step
    else:
        print("use cwd=repo")
        get_repo(None)
