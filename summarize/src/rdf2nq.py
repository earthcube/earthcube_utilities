#!/usr/bin/env python3
#mike b, take a triple file w/every line ending in " ." and use filename to make a quad, needed for gleaner/testing
#potentially useful elsewhere; eg. if added repo: could use this in my workflow to make quads
import os
from os.path import exists
cwd = os.getcwd()

def path_leaf(path):
    "everything after the last /"
    import ntpath
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

#from ec.py ;below can go in utils as well, but as cli right now
def file_ext(fn):
    st=os.path.splitext(fn)
    #add2log(f'fe:st={st}')
    return st[-1]

def file_base(fn):
    st=os.path.splitext(fn)
    #add2log(f'fb:st={st}')
    return st[0]

def is_str(v):
    return type(v) is str

def is_http(u):
    if not is_str(u):
        print("might need to set LD_cache")
        return None
    return u.startswith("http")

def os_system(cs):
    "run w/o needing ret value"
    os.system(cs)
   #add2log(cs)

def os_system_(cs):
    "system call w/return value"
    s=os.popen(cs).read()
    #add2log(cs)
    return s

def path_leaf(path):
    "everything after the last /"
    import ntpath
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def wget(fn):
    #cs= f'wget -a log {fn}'  #--quiet
    cs= f'wget --tries=2 -a log {fn}' 
    os_system(cs)
    return path_leaf(fn) #new

#was xml2nt, but can call w/"json-ld" or "ntriples",but could just use fn2nq still
#def 2nt_str(fn,frmt="xml"):  #could also use rapper here, see: rdfxml2nt
def to_nt_str(fn,frmt="json-ld"):  
    "turn .xml(rdf) to .nt"
    fnb=file_base(fn)
    from rdflib import Graph
    g = Graph()
    #g.parse(fn, format="xml")
    g.parse(fn, format=frmt) #allow for "json-ld"..
    #UnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 1: invalid start byte ;fix
    #s=g.serialize(format="ntriples").decode("u8") #works via cli,nb had ntserializer prob
    s=g.serialize(format="ntriples") #try w/o ;no, but works in NB w/just a warning
   #fnt=fnb+".nt" #condsider returning this
   #put_txtfile(fnt,s)
   #add2log(f'xml2nt:{fnt},len:{s}')
    #return len(s)
   #return fnt
    return s

#DF's gleaner uses the shah of the jsonld to name the .rdf files which are actually .nt files
# but then there are lots of .nq files that are actually .nt files, but should be able to get them w/this
#maybe someplace in nabu this is done, but by then I can't have the files to load them

#use filename to convert .rdf file to a .nq file
#▶<102 a09local: /milled/geocodes_demo_datasets> mo 09517b808d22d1e828221390c845b6edef7e7a40.rdf
#_:bcbhdkms5s8cef2c4s7j0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://schema.org/Dataset> .
#goes to:
#_:bcbhdkms5s8cef2c4s7j0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://schema.org/Dataset> "urn:09517b808d22d1e828221390c845b6edef7e7a40".
#fn = "09517b808d22d1e828221390c845b6edef7e7a40.rdf"

#this should be used to check lines that have already gone through riot
def no_error(line):
    ll = len(line)
    if ll < 9:
        print(f'skipping {ll}<9: {line}')
        return False
    if "ERROR riot" in line:
        print(f'skipping: error-line:{line}')
        return False
    return True 

#also have:
#if ll>9: #to skip ~empty lines, but ..

#https://stackoverflow.com/questions/3675318/how-to-replace-the-some-characters-from-the-end-of-a-string
def replace_last(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail

def fn2nq(fn,prefix=None):
    "read in .nt put out .nq"
    fnb = file_base(fn)
    fn2 = fnb + ".nq"
    if exists(fn2):
        print(f'fn2nq:{fn2} already there')
    if prefix:
        replace_with = f' <urn:{prefix}:{fnb}> .'
    else:
        replace_with = f' <urn:{fnb}> .'
    with open(fn2,'w') as fd_out:
        with open(fn,'r') as fd_in:
            for line in fd_in:
                #line_out = line.replace(" .",f' "urn:{fnb}" .')
                #replace_with = f' "urn:{fnb}" .'
                #ll=len(line)
                if no_error(line):
                    line_out = replace_last(line, " .", replace_with)
                    fd_out.write(line_out)
    return fn2

def riot2nq(fn):
    "process .jsonld put out .nq"
    fnb = file_base(fn)
    fn2 = fnb + ".nq"
    if exists(fn2):
        print(f'riot2nq:{fn2} already there')
    replace_with = f' <urn:{fnb}> .'
    nts = os_system_(f'riot --stream=nt {fn}')
    fd_in = nts.split("\n") 
    lin=len(fd_in)
    print(f'got {lin} lines')
    with open(fn2,'w') as fd_out:
        for line in fd_in:
            #ll=len(line)
            if no_error(line):
                line_out = replace_last(line, " .", replace_with)
                fd_out.write(line_out)
                fd_out.write('\n')
    return fn2

def to_nq(fn):
    "process .jsonld put out .nq"
    fnb = file_base(fn)
    fn2 = fnb + ".nq"
    if exists(fn2):
        print(f'to_2nq:{fn2} already there')
    replace_with = f' <urn:{fnb}> .'
   #nts = os_system_(f'riot --stream=nt {fn}')
    nts=to_nt_str(fn)
    fd_in = nts.split("\n") 
    lin=len(fd_in)
    print(f'got {lin} lines')
    with open(fn2,'w') as fd_out:
        for line in fd_in:
            #ll=len(line)
            if no_error(line):
                line_out = replace_last(line, " .", replace_with)
                fd_out.write(line_out)
                fd_out.write('\n')
    return fn2

#if .nt as before, if .jsonld then riot .jsonld to .nt 1st, then dump as .nq
if __name__ == '__main__':
    import sys
    if(len(sys.argv)>1):
        fn = sys.argv[1]
        if is_http(fn):
            fn=wget(fn)
        print(f'fn2nq on:{fn}')
        ext = file_ext(fn)
        print(f'2nq file_EXT:{ext}')
        fn2="Not Found"
        if ext==".rdf": #df's idea for .nt files
            #print(f'cwd:{cwd}')
            repo=path_leaf(cwd)
            #print(f'repo:{repo}')
            prefix=f'gleaner:summoned:{repo}'
            print(f'prefix:{prefix}')
            fn2=fn2nq(fn,prefix)
        if ext==".nt":
            fn2=fn2nq(fn)
        if ext==".jsonld":
            #fn2=riot2nq(fn)
            fn2=to_nq(fn)
        print(f'gives:{fn2}')
