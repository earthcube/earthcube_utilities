#!/bin/bash
#to show that now it has to get into ./repo dir to fix the quads &cp up to ./repo.nq
fix_runX.sh $1
#takes repo.nq loads to fuseki /repo namespace, and runs: 'tsum.py repo' to make a repo.ttl file
summarize_repo.sh $1
#later could have a ttl2blaze.sh to put that in the store
