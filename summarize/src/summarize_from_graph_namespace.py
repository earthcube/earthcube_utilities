#!/usr/bin/env python3

import argparse

import logging


import os
from ec.graph.manageGraph import ManageBlazegraph as mg
from ec.summarize.summarize_materializedview import summaryDF2ttl, get_summary4graph,get_summary4repoSubset
from ec.gleanerio.gleaner import endpointUpdateNamespace,getNabu, reviseNabuConfGraph, runNabu

# def endpointUpdateNamespace( fullendpoint, namepsace='temp'):
#     paths = fullendpoint.split('/')
#     paths[len(paths)-2] = namepsace
#     newurl= '/'.join(paths)
#     return newurl
#
# def getNabu( cfgfile):
#     cfg = yaml.safe_load(cfgfile)
#     endpoint = cfg['sparql']['endpoint']
#     return endpoint, cfg
#
# def reviseNabuConf(cfg, endpoint):
#     newcfg = copy.deepcopy(cfg)
#     newcfg['sparql']['endpoint'] = endpoint
#     return newcfg
#
# def runNabu(cfg, repo,glcon="~/indexing/glcon"):
#     if shutil.which(glcon) is not None:
#         filename = f"nabu_{repo}" # avoid possible naming conflicts
#         with open(filename, 'w') as f:
#             yaml.dump(cfg, f)
#         executeNabu = f"{glcon} nabu prefix --cfg {filename} --prefix summoned/{repo}"
#         try:
#             result = os.system(executeNabu)
#             if result != 0:
#                 raise Exception(f"running glcon failed {result}")
#         except Exception as ex:
#             raise Exception(f"running glcon failed {ex}")
#         # delete config file here
#         return True
#     else:
#         raise Exception(f"glcon not found at {glcon}. Pass path to glcon with --glcon")

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

    parser.add_argument('--graphsummary', dest='graphsummary',
                        help='upload triples to graphsummary', default=True)
    parser.add_argument('--summary_namespace', dest='summary_namespace',
                        help='summary_namespace defaults to {repo_summary}',
                        )
    args = parser.parse_args()
    repo = args.repo
    if args.summary_namespace:
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
        if args.graphsummary:
            inserted = sumnsgraph.insert(bytes(summaryttl, 'utf-8'),content_type="application/x-turtle" )
            if inserted:
                logging.info(f"Inserted into graph store{sumnsgraph.namespace}" )
            else:
                logging.error(f" dumping file {repo}.ttl  Repo {repo} not inserted into {sumnsgraph.namespace}")

                with open(os.path.join("output",f"{repo}.ttl"), 'w') as f:
                     f.write(summaryttl)
                return 1
        else:
            logging.info(f" dumping file {repo}.ttl  graphsummary: {args.graphsummary} ")

            with open(os.path.join("output", f"{repo}.ttl"), 'w') as f:
                f.write(summaryttl)
    except Exception as ex:
        logging.error(f"error {ex}")
        print(f"Error: {ex}")
        return 1



if __name__ == '__main__':

    exitcode= summarizeGraphOnly()
    exit(exitcode)