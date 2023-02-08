#!/usr/bin/env python3
#M Bobak, need to get gleaner output for a repo
# for now have to pull all files to turn to quads here ;till issue126 
import os
#import ec
import earthcube_utilities as ec  #make sure this is availabe
#for now keeping in a dir named after each repo, so next step can run2nq over it
 #where it takes the it's filename, to turn the triples into quads w/that name

#def get_repo(repo):
def get_repo(repo, default_bucket= "https://oss.geocodes.ncsa.illinois.edu/"):
    #I think it uses cwd for repo, but want to override that
    if not repo:  
        #was cwd=ec.cwd, which are the same
        cwd=os.getcwd()
        repo = ec.path_leaf(cwd)
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
    ec.wget_oss_repo(repo=repo,path="gleaner/milled",bucket=default_bucket)

def url_w_end_slash(url):
    if len(url)-1 != "/":
        return url + "/"
    else:
        return url


if __name__ == '__main__':
    import sys
    print(f'argv={sys.argv}')
    default_bucket= "https://oss.geocodes.ncsa.illinois.edu/"
    s3=os.getenv("S3ADDRESS") 
    if ec.is_str(s3):
        if not ec.is_http(s3):
            s3="https://" + url_w_end_slash(s3)
        print(f'set default_bucket to S3ADDRESS={s3}')
        default_bucket=s3
    if(len(sys.argv)>2):
        default_bucket = sys.argv[1]
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
