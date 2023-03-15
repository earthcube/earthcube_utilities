#!/usr/bin/env python3

import argparse
import copy
import logging
import yaml
import shutil


import os
from graph.manageGraph import ManageBlazegraph as mg
from summarize_materializedview import summaryDF2ttl, get_summary4graph,get_summary4repoSubset
from rdflib import Dataset

def endpointUpdateNamespace( fullendpoint, namepsace='temp'):
    paths = fullendpoint.split('/')
    paths[len(paths)-2] = namepsace
    newurl= '/'.join(paths)
    return newurl

def getNabu( cfgfile):
    cfg = yaml.safe_load(cfgfile)
    endpoint = cfg['sparql']['endpoint']
    return endpoint, cfg

def reviseNabuConf(cfg, endpoint):
    newcfg = copy.deepcopy(cfg)
    newcfg['sparql']['endpoint'] = endpoint
    return newcfg

def runNabu(cfg, repo,glcon="~/indexing/glcon"):
    if shutil.which(glcon) is not None:
        filename = f"nabu_{repo}" # avoid possible naming conflicts
        with open(filename, 'w') as f:
            yaml.dump(cfg, f)
        executeNabu = f"{glcon} nabu prefix --cfg {filename} --prefix summoned/{repo}"
        try:
            result = os.system(executeNabu)
            if result != 0:
                raise Exception(f"running glcon failed {result}")
        except Exception as ex:
            raise Exception(f"running glcon failed {ex}")
        # delete config file here
        return True
    else:
        raise Exception(f"glcon not found at {glcon}. Pass path to glcon with --glcon")

def summarizeReleaseOnly(args):
    repo = args.repo
    if args.summary_namespace:
        summary = args.summary_namespace
    else:
        summary = f"{repo}_summary"
    endpoint= args.graphendpoint
    graphendpoint = mg.graphFromEndpoint(endpoint)

    g = Dataset()
    g.parse(args.url, format='nquads')
    ## HOW TO SUMMARIZE from RDF QUadss?
    # this will need to be modularlized, ad reqworked.

    file = '../resources/sparql/all_summary_query.sparql'
    with open(file, 'r') as f:
        lines = f.read()
    sumresults = g.query(lines)
## this returns no rows.
    # WE CAN USE BLAZEGRAPH, so no use going direct


    try:  # temp has been created
        # created = tempnsgraph.createNamespace()
        # if ( created=='Failed'):
        #     logging.fatal("coould not create namespace")
        sumnsgraph = mg(graphendpoint, summary)
        # created = sumnsgraph.createNamespace()
        # if ( created=='Failed'):
        #     logging.fatal("coould not create summary namespace")
        # endpoints for file
        # tempendpoint =endpointUpdateNamespace(endpoint,f"{repo}_temp")

        summaryendpoint =endpointUpdateNamespace(endpoint,summary)

        # newNabucfg = reviseNabuConf(cfg,tempendpoint )
        # runNabu(newNabucfg,repo, args.glcon )

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
        return 1
    # finally:
    #     # need to figure out is this is run after return, I think it is.
    #     logging.debug(f"Deleting Temp namespace {tempnsgraph.namespace}")
    #     deleted = tempnsgraph.deleteNamespace()


if __name__ == '__main__':

    # these need to be better
    # url
    # OR
    # s3base, s3bucket
    #   if not repo, read all nq files in graphs/latest
    #
    # graph endpoint,
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", dest='url', help='url of file',
    default = "https://oss.geocodes-dev.earthcube.org/gleaner-wf/graphs/latest/summonediris_2023-03-13-11-02-47_release.nq"

    )

    parser.add_argument("--repo", dest='repo', help='repo name used in the  urn')

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
    parser.add_argument('--graphsummary', dest='graphsummary',
                        help='upload triples to graphsummary', default=True)
    parser.add_argument('--summary_namespace', dest='summary_namespace',
                        help='summary_namespace defaults to {repo_summary}',
                        )
    args = parser.parse_args()

    exitcode= summarizeReleaseOnly(args)
    exit(exitcode)