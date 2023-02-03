#!/usr/bin/env python3
#M Bobak, need to get gleaner output for a repo
# for now have to pull all files to turn to quads here ;till issue126 
import os
#for now keeping in a dir named after each repo, so next step can run2nq over it
 #where it takes the it's filename, to turn the triples into quads w/that name

def get_repo(repo):
    import ec
    #I think it uses cwd for repo, but want to override that
    if not repo:
        #print(f'cwd={ec.cwd} used to be the dir you would download the repo-s files into')
        repo = ec.path_leaf(ec.cwd)
        print(f'using: cwd={ec.cwd} to get the repo={repo} to downloads files into')
    else:
        print(f'will get files for {repo} in a dir named after it')
        exists=os.path.exists(repo)
        if not exists:
            print(f'will create the {repo} dir') 
            os.makedirs(repo)
        os.chdir(repo)
        cwd=os.getcwd()
        print(f'cd to: cwd={cwd} to get the repo={repo} to downloads files into')
    ec.wget_oss_repo(repo) #defaults to bucket=ncsa_minio =https://oss.geocodes.ncsa.illinois.edu/


if __name__ == '__main__':
    import sys
    if(len(sys.argv)>1):
        repo = sys.argv[1]
        print(f'will run over:{repo}')
        get_repo(repo)
        #run2nq(repo) #done in next step
    else:
        print("use cwd=repo")
        get_repo(None)
