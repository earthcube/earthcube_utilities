#!/bin/bash
#to resolve https://github.com/gleanerio/gleaner/issues/126 till gleaner can dump quads in runX
./get_repo.py $1 
./run2nq.py $1 
#once gleaner can dump quads, we will just pull (v fix) them&run: summarize_repo.sh next 
