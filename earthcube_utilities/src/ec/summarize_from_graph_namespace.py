#!/usr/bin/env python3

import argparse
import logging
import os
import errno
from ec.graph.manageGraph import ManageBlazegraph as mg
from ec.summarize import summaryDF2ttl, get_summary4graph,get_summary4repoSubset
from ec.gleanerio.gleaner import endpointUpdateNamespace,getNabu, reviseNabuConfGraph, runNabu
from urllib.parse import urlparse


def dumpToFile(repo,summaryttl ):
    if repo is None or repo == '':
        repo = 'pass_repo_flag'
    filename = os.path.join("output", f"{repo}.ttl")
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(filename, 'w') as f:
        f.write(summaryttl)
    return
def isValidURL(toValidate):
    o = urlparse(toValidate)
    if o.scheme and o.netloc:
        return True
    else:
        return False


def summarizeGraphOnly():
    """ Summarize directly from a namespace, upload to provided summarize namespace

    Description:
        * query for repository graphs using defined repo parameter,

        * build summary triples

        * loading to a summarized namespace

    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--repo", dest='repo', help='repo name used in the  urn')

    parser.add_argument('--graphendpoint', dest='graphendpoint',
                        help='graph endpoint with namespace',
                        default="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/sparql"
                        , required=True)

    parser.add_argument('--nographsummary', action='store_true', dest='nographsummary',
                        help='send triples to file', default=False)
    parser.add_argument('--summary_namespace', dest='summary_namespace',
                        help='summary_namespace  just the namspace. defaults to "repo_summary"',
                        )
    args = parser.parse_args()
    repo = args.repo

    if args.summary_namespace:
        if isValidURL(args.summary_namespace):
            msg = 'For summary_namespace, Please enter the namespace only.'
            print(msg)
            logging.error(msg)
            return 1
        summary = args.summary_namespace
    else:
        summary = f"{repo}_summary"

    endpoint= args.graphendpoint
    graphendpoint = mg.graphFromEndpoint(endpoint)

    try:

        sumnsgraph = mg(graphendpoint, summary)

        summaryendpoint =endpointUpdateNamespace(endpoint,summary)

        if repo is not None:
            summarydf = get_summary4repoSubset(endpoint, repo)
        else:
            # this really needs to be paged ;)
            summarydf = get_summary4graph(endpoint)
            repo = ""

        nt,g = summaryDF2ttl(summarydf,repo) # let's try the new generator

        summaryttl = g.serialize(format='longturtle')
        # write to s3  in future
        # with open(os.path.join("output",f"{repo}.ttl"), 'w') as f:
        #      f.write(summaryttl)
        if not args.nographsummary:
            inserted = sumnsgraph.insert(bytes(summaryttl, 'utf-8'),content_type="application/x-turtle" )
            if inserted:
                logging.info(f"Inserted into graph store{sumnsgraph.namespace}" )
            else:
                logging.error(f" dumping file {repo}.ttl  Repo {repo} not inserted into {sumnsgraph.namespace}")
                dumpToFile(repo, summaryttl)
                return 1
        else:
            logging.info(f" dumping file {repo}.ttl  nographsummary: {args.nographsummary} ")

            dumpToFile(repo, summaryttl)
    except Exception as ex:
        logging.error(f"error {ex}")
        print(f"Error: {ex}")
        return 1

if __name__ == '__main__':

    exitcode= summarizeGraphOnly()
    exit(exitcode)
