#!/usr/bin/env python3

import argparse
import logging
import os
from ec.graph.manageGraph import ManageBlazegraph as mg
from ec.graph.release_graph import ReleaseGraph
from ec.graph.sparql_query import _getSparqlFileFromResources
from ec.summarize.summarize_materializedview import summaryDF2ttl, get_summary4graph,get_summary4repoSubset
from ec.gleanerio.gleaner import endpointUpdateNamespace,getNabu, reviseNabuConfGraph, runNabu
from rdflib import Dataset
from urllib.parse import urlparse


def isValidURL(toValidate):
    o = urlparse(toValidate)
    if o.scheme and o.netloc:
        return True
    else:
        return False

def summarizeReleaseOnly():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", dest='url', help='url of file',
                        default="https://oss.geocodes-dev.earthcube.org/gleaner-wf/graphs/latest/summonediris_2023-03-13-11-02-47_release.nq"

                        )

    parser.add_argument("--repo", dest='repo', help='repo name used in the  urn', default="dummy")
    parser.add_argument('--s3base', dest='s3base',
                        help='basurl of',
                        default="https://oss.geocodes-dev.earthcube.org/"
                        )
    parser.add_argument('--s3bucket', dest='s3bucket',
                        help='basurl of',
                        default="gleaner-wf"

                        )
    parser.add_argument('--graphendpoint', dest='graphendpoint',
                        help='graph endpoint with namespace',
                        default="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/sparql"
                        )
    parser.add_argument('--nographsummary', action='store_true', dest='nographsummary',
                        help='send triples to file', default=False)
    args = parser.parse_args()


    endpoint= args.graphendpoint
    graphendpoint = mg.graphFromEndpoint(endpoint)
    rg = ReleaseGraph()




## this returns no rows.
    # WE CAN USE BLAZEGRAPH, so no use going direct


    try:  # temp has been created
        # created = tempnsgraph.createNamespace()
        rg.load_release(args.url)
        summarydf = rg.summarize()
        nt, g = summaryDF2ttl(summarydf, args.repo)  # let's try the new generator
        summaryttl = g.serialize(format='longturtle')

        with open(os.path.join("output", f"{args.repo}.ttl"), 'w') as f:
            f.write(summaryttl)
    except Exception as ex:
        logging.error(f"error {ex}")
        print(f"Error: {ex}")
        return 1
    # finally:
    #     # need to figure out is this is run after return, I think it is.
    #     logging.debug(f"Deleting Temp namespace {tempnsgraph.namespace}")
    #     deleted = tempnsgraph.deleteNamespace()


if __name__ == '__main__':
    """ Summarize a from a gleaner 'release' set of n-quads file

    Description:
       untested
    """
    # these need to be better
    # url
    # OR
    # s3base, s3bucket
    #   if not repo, read all nq files in graphs/latest
    #
    # graph endpoint,


    exitcode= summarizeReleaseOnly()
    exit(exitcode)
