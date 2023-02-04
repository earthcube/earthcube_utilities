#!/usr/bin/env python3
#mbobak, run 2nq.py over a repo/dir
#easier w/py than bash, and could put in 2nq.py
 #as a way to run itself over the repo/dirs
import os
from os.path import exists
import rdf2nq

def os_system(cs):
    "run w/o needing ret value"
    os.system(cs)
    #add2log(cs)

def os_system_(cs):
    "system call w/return value"
    s=os.popen(cs).read()
    #add2log(cs)
    return s

def is_str(v):
    return type(v) is str

def is_list(v):
    return type(v) is list

def file_ext(fn):
    "the ._part of the filename"
    st=os.path.splitext(fn)
    #add2log(f'fe:st={st}')
    return st[-1]

def collect_ext_(l,ext):
  return list(filter(lambda x: file_ext(x)==ext,l))

#=
def run2nq(repo):
    rl=os.listdir(repo)
    if not rl:
        print("nothing there")
        return None
    else:
        lrl=len(rl)
        print(f'found:{lrl} files')
        print(rl)
        rdfl=collect_ext_(rl,".rdf")
        lrl=len(rdfl)
        print(f'found:{lrl} rdf files')
        #2nq.py skips output file if it already exists
        for f in rdfl:
            infn=f'{repo}/{f}'
            rdf2nqo=rdf2nq.fn2nq(infn)
            print(f'2nq,gives:{rdf2nqo}')
            #cs=f'2nq.py {repo}/{f}'
            #os_system(cs)
        # repo/*.nq > repo.nq
        outfn=f'{repo}.nq'
        print(f'out-filename={outfn}')
        if exists(outfn):
            print("allready exits, so won't copy up")
        else:
            os_system(f'cat {repo}/*.nq > {outfn}')
            print("created")

if __name__ == '__main__':
    import sys
    if(len(sys.argv)>1):
        repo = sys.argv[1]
        print(f'will run over:{repo}')
        run2nq(repo)
