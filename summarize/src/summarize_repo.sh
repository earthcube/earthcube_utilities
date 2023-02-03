#!/bin/bash
fnq.py $1
echo wait_for_fuseki_to_come_up ; sleep 20
tsum.py $1 |egrep -v "not IN_COLAB|rdf_inited|try:http"|cat>$1.ttl
