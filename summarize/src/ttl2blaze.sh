#!/bin/bash
# A wrapper script for loading RDF into Jena 
# usage:  load2Blaze.sh directory endpoint
# example:  load2Blaze.sh mydata.ttl https://example.org/blazegraph/namespace/kb/sparql
# example:  ttl2Blaze.sh https://example.org/blazegraph/namespace/kb/sparql
# example:  ttl2Blaze.sh http://localhost:9999/blazegraph/namespace/kb/sparql
pushd $1

files=$( ls -1  *.ttl )
counter=0
for i in $files ; do
      echo "-------------start-------------"
      echo Next: $i
      # rapper -e -c -i turtle $i 
      #curl -X POST -H 'Content-Type:text/x-turtle' --data-binary @$i $2
      curl -X POST -H 'Content-Type:text/x-turtle' --data-binary @$i $1
      echo "-------------done--------------"
done

popd

