import json
import logging
from datetime import date, datetime
import time
from typing import Any

import pandas
import pydash

import ec.sitemap
from ec.graph.release_graph import ReleaseGraph
from ec.graph.sparql_query import queryWithSparql

from ec.datastore.s3 import bucketDatastore
from ec.sitemap import Sitemap

import csv
from urllib import request


"""
reports

simplifying the thinking.
These go into a reports store in the datastore

we can calculate in multiple ways
eg for items that were not summoned due to no jsonld, calculate from s3 compare to sitemap, and pull for gleaner logs 

Let's start with ones we can do easily.

Reports
* PROCESSING REPORT: (processing.json) 
**  general report with the basics. counts, good, bad, etc.
*** sitemap count
*** summoned count ec.datastore.s3.countJsonld
*** milled count ec.datastore.s3.countMilled
*** graph count repo_count_graphs.sparql ec.graph.sparql_query.queryWithSparql("repo_count_graphs", release_file, parameters={"repo": repo})
*** when processing details is working, then add counts of  was summoned but did not make it into the graph

* PROCESSING REPORT DETAILS:
** thought... how to handle what got lost... need to know, or perhaps files with lists of what got lost along the way
*** SITEMAP Details and issues
**** (sitemap_badurls.csv)list of bad urls
**** (sitemap_summon_issues.csv) list of urls for items that had no JSONLD. 
*****  Grab list of metadater-Url from Datastore, ec.datastore.s3.listSummonedUrls
*****  compare to sitemap url list
*****  remove bad urls. if it cannot be retrieved, we don't need to chase it down
*** PROCESSING Detials and issues
**** (summon_graph_missing.csv; summon_milled_missing.csv;) what made and did not make it. Parameters
**** summoned ids: ec.datastore.s3.listJsonld
# will need to do a list(map(lambda , collection) to get a list of urls.
o_list = list(map(lambda f: ec.datastore.s3.urnFroms3Path(f.object_name), objs))
**** milled ids: ec.datastore.s3.listMilledRdf
**** graph ids:  ec.graph.sparql_query.queryWithSparql("repo_select_graphs", release_file, parameters={"repo": repo})

***** suggest compare using pydash, or use pandas...
then look up the urls' using: ec.datastore.s3.getJsonLDMetadata

* GRAPHSTORE REPORTS: sparql.json
This runs a list of sparql queries
** What is in the overall graph, 
** Data Loading reports by  Repo 


Probably run the all repo report monthly, or after a large data load
Run the repo report have a repo is reloaded.

FUTURE:
Use issues from repo reports as data for a tool that can evaluate the failures

"""
def get_url_from_sha_list(shas: list,  bucket, repo, datastore: bucketDatastore):
    """if a repo has issues with milling or loading to a graph, then get the summoned file"""

    pass

def missingReport(valid_sitemap_url :str , bucket, repo, datastore: bucketDatastore, graphendpoint, milled=True, summon=False):
    today = date.today().strftime("%Y-%m-%d")
    response = {"source":repo,"graph":graphendpoint,"sitemap":valid_sitemap_url,
                "date": today, "bucket": bucket, "s3store": datastore.endpoint }
    t = time.time()
    sitemap = ec.sitemap.Sitemap(valid_sitemap_url)
    if not sitemap.validUrl():
        raise ValueError(valid_sitemap_url)
    sitemap_urls = sitemap.uniqueUrls()
    response["sitemap_geturls_time"] = time.time() - t
    sitemap_count = pydash.collections.size(sitemap_urls)
    t = time.time()
    summoned_list = datastore.listSummonedUrls(bucket, repo)
    response["s3_geturls_time"] = time.time() - t
    summoned_count = pydash.collections.size(summoned_list)
    summoned_urls = list(map(lambda s: s.get("url"), summoned_list))
    dif_sm_summon = pydash.arrays.difference(sitemap_urls, summoned_urls)
    dif_summon_sm = pydash.arrays.difference( summoned_urls, sitemap_urls)
    response["sitemap_count"] = sitemap_count
    response["summoned_count"] = summoned_count
    response["missing_sitemap_summon_count"] = len(dif_sm_summon)
    response["missing_sitemap_summon"] = dif_sm_summon
    response["extra_in_summon_count"] = len(dif_summon_sm)
    response["extra_in_summon"] = dif_summon_sm
    if summon:
        return response
    ##### summmon to graph
    t = time.time()
    summoned_sha_list = datastore.listSummonedSha(bucket, repo)
    response["summon_list_s3_sha_time"] = time.time() - t
    t = time.time()
    graph_urns = ec.graph.sparql_query.queryWithSparql("repo_select_graphs", graphendpoint, {"repo": repo})
    graph_shas = list(map(lambda u: pydash.strings.substr_right_end(u, ":"), graph_urns['g']))
    response["graph_sha_urn_time"] = time.time() - t
    dif_summon_graph = pydash.arrays.difference(summoned_sha_list, graph_shas)
    response["graph_urn_count"] = pydash.collections.size(graph_shas)
    response["missing_summon_graph_count"] = len(dif_summon_graph)
    response["missing_summon_graph"] = dif_summon_graph
    if milled:
        t = time.time()
        milled_list = datastore.listMilledSha(bucket, repo)
        response["milled_sha_time"] = time.time() - t
        dif_summon_milled = pydash.arrays.difference(summoned_sha_list, milled_list)
        response["milled_count"] = pydash.collections.size(milled_list)
        response["missing_summon_milled"] = len(dif_summon_milled)
        response["missing_summon_milled"] = dif_summon_milled
    return response

def compareSitemap2Summoned(valid_sitemap_url :str , bucket, repo, datastore: bucketDatastore):
    #Grab list of metadater-Url from Datastore, ec.datastore.s3.listSummonedUrls
    sitemap = ec.sitemap.Sitemap(valid_sitemap_url)
    sitemap_urls = sitemap.uniqueUrls()
    sitemap_count= pydash.collections.size(sitemap_urls)
    summoned_list = datastore.listSummonedUrls(bucket,repo)
    summoned_count = pydash.collections.size(summoned_list)
    summoned_urls=list(map(lambda s: s.get("url"),summoned_list ))
    difference = pydash.arrays.difference( sitemap_urls, summoned_urls)
    return {
        "sitemap_count": sitemap_count,
        "summoned_count": summoned_count,
            "missing": difference
            }


def compareSummoned2Milled(bucket, repo, datastore: bucketDatastore):
    """ return list of missing urns/urls
    Generating milled will be good to catch such errors"""
    # compare using s3, listJsonld(bucket, repo) to  listMilledRdf(bucket, repo)
    summoned_list = datastore.listSummonedSha(bucket, repo)
    milled_list = datastore.listMilledSha(bucket, repo)
    difference = pydash.arrays.difference(summoned_list, milled_list)
    return {
        "summoned_count": pydash.collections.size(summoned_list),
        "milled_count": pydash.collections.size(milled_list),
            "missing": difference
            }
def compareSummoned2Graph(bucket, repo, datastore: bucketDatastore, graphendpoint):
    """ return list of missing .
    we do not alway generate a milled.
    """
    # compare using s3, listJsonld(bucket, repo) to queryWithSparql("repo_select_graphs", release_file)
    summoned_list = datastore.listSummonedSha(bucket, repo)
    graph_urns = ec.graph.sparql_query.queryWithSparql("repo_select_graphs",graphendpoint,{"repo":repo})
    graph_shas = list(map(lambda u: pydash.strings.substr_right_end(u, ":"), graph_urns['g']))
    difference = pydash.arrays.difference(summoned_list, graph_shas)
    return {
        "summoned_count": pydash.collections.size(summoned_list),
        "milled_count": pydash.collections.size(graph_shas),
            "missing": difference
            }


##################################
#  REPORT GENERATION USING SPARQL QUERIES
#   this uses defined spaql queries to return counts for reports
###################################
reportTypes = {
    "all": [
        {"code": "triple_count", "name": "all_count_triples"},
            {"code": "graph_count_by_repo", "name": "all_repo_count_graphs"},
        {"code": "dataset_count", "name": "all_count_datasets"},
        {"code": "dataset_count_by_repo", "name": "all_repo_count_datasets"},
        {"code": "types_count", "name": "all_count_types"},
        {"code": "types_count_by_repo", "name": "all_repo_count_types"},
        {"code": "mutilple_version_count", "name": "all_count_multiple_versioned_datasets"},
        {"code": "mutilple_version_count_by_repo", "name": "all_repo_count_versioned_datasets"},
        {"code": "repos_with_keywords", "name": "all_repo_with_keywords"},
    ],
    # add the triple count by graph, and graph sizes
    # this will need to be added, managed in the generate_graph
    # add a basic by default, detailed if requested with a flag
    "all_detailed": [
        {"code": "triple_count", "name": "all_count_triples"},
        {"code": "graph_count_by_repo", "name": "all_repo_count_graphs"},
        {"code": "dataset_count", "name": "all_count_datasets"},
        {"code": "dataset_count_by_repo", "name": "all_repo_count_datasets"},
        {"code": "types_count", "name": "all_count_types"},
        {"code": "types_count_by_repo", "name": "all_repo_count_types"},
        {"code": "mutilple_version_count", "name": "all_count_multiple_versioned_datasets"},
        {"code": "mutilple_version_count_by_repo", "name": "all_repo_count_versioned_datasets"},
        {"code": "keywords_counts_by_repo", "name": "all_repo_count_keywords"},
        {"code": "keywords_count", "name": "all_count_keywords"},
        {"code": "variablename_count", "name": "all_count_variablename"},
        {"code": "graph_sizes", "name": "all_graph_sizes"},

    ],
    "repo": [
        {"code": "triple_count", "name": "repo_count_triples"},
        {"code": "dataset_count", "name": "repo_count_datasets"},
        {"code": "type_count", "name": "repo_count_types"},
        {"code": "kw_count", "name": "repo_count_keywords"},
        {"code": "variablename_count", "name": "repo_count_variablename"},
        {"code": "version_count", "name": "repo_count_multi_versioned_datasets"},
        {"code": "graph_sizes_count", "name": "repo_graph_sizes"},
    ],
    # add the triple count by graph, and graph sizes
    # this will need to be added, managed in the generate_graph
    # add a basic by default, detailed if requested with a flag
    "repo_detailed": [
        {"code": "triple_count", "name": "repo_count_triples"},
        {"code": "kw_count", "name": "repo_count_keywords"},
        {"code": "dataset_count", "name": "repo_count_datasets"},
        {"code": "triple_count", "name": "repo_count_triples"},
        {"code": "type_count", "name": "repo_count_types"},
        {"code": "version_count", "name": "repo_count_multi_versioned_datasets"},
        {"code": "variablename_count", "name": "repo_count_variablename"},
        {"code": "graph_sizes_count", "name": "repo_graph_sizes"},
        {"code": "triple_count_by_graph", "name": "repo_count_triples_by_graph"},
    ]
}

def _get_report_type(reports, code) -> str:
    report = pydash.find(reports, lambda r: r["code"] == code)
    return report["name"]

# this is a sinlge repo...
# was reportTypes["all"]
# really don't even need to do the filers, but
# repo works best for now
def generateGraphReportsRelease(repo,  release_file, reportList=reportTypes["repo"]) -> Any:
    #queryWithSparql("repo_count_types", release_file)
    parameters = {"repo": repo}
    current_dateTime = datetime.now().strftime("%Y-%m-%d")
    rg = ReleaseGraph()
    rg.load_release(release_file)
    reports= []
    for report in reportList:
        try:
            t = time.time()
            result =  rg.query_release(template_name=report["name"],parameters=parameters)
            elapsed_time = time.time() - t
            data = result.dropna()
            data = data.to_dict('records')
            reports.append(  {"report": report["code"],
                     "processing_time": elapsed_time,
                     "length": len(data),
             "data": data
             })
        except Exception as ex:
            logging.error(f"query with sparql against release failed: report:{report['code']}  repo:{repo}   {ex}")
            elapsed_time = time.time() - t
            reports.append( {"report": report["code"],
                    "errpr": f"{ex}",
                     "processing_time": elapsed_time,
             "data": []
             })
    return json.dumps({"version": 0, "repo": repo, "date": current_dateTime, "reports": reports }, indent=4)

##  for the 'object reports, we should have a set.these could probably be make a set of methos with (ObjectType[triples,keywords, types, authors, etc], repo, endpoint/datastore)
def generateGraphReportsRepo(repo, graphendpoint, reportList=reportTypes["all"]) -> str:
    current_dateTime = datetime.now().strftime("%Y-%m-%d")
    reports = map (lambda r:    generateAGraphReportsRepo(repo, r,
                                 graphendpoint, reportList)
                                      ,
                                reportList)

    reports = list(reports)
    return json.dumps({"version": 0, "repo": repo, "date": current_dateTime, "reports": reports }, indent=4)


def generateAGraphReportsRepo(repo, r, graphendpoint, reportList) -> Any:
    #queryWithSparql("repo_count_types", release_file)
    parameters = {"repo": repo}
    try:
        t = time.time()
        report =   queryWithSparql(_get_report_type(reportList, r['code']), graphendpoint, parameters=parameters)
        elapsed_time = time.time() - t
        data = report.dropna()
        data = data.to_dict('records')

        return  {"report": r["code"],
                 "processing_time": elapsed_time,
                 "length": len(data),
         "data": data
         }
    except Exception as ex:
        logging.error(f"query with sparql failed: report:{r['code']}  repo:{repo}   {ex}")
        elapsed_time = time.time() - t
        return {"report": r["code"],
                "errpr": f"{ex}",
                 "processing_time": elapsed_time,
         "data": []
         }

def getGraphReportsLatestRepoReports(repo,  datastore: bucketDatastore):
    """get the latest for a dashboard"""
    date="latest"
    path = f"{datastore.paths['reports']}/{repo}/{date}/sparql.json"
    filelist = datastore.getReportFile(datastore.default_bucket, repo, path)

def listGraphReportDates4Repo(repo,  datastore: bucketDatastore):
    """get the latest for a dashboard"""
    path = f"{datastore.paths['reports']}/{repo}/"
    filelist = datastore.listPath(path)
    return filelist

def generateIdentifierRepo(repo, bucket, datastore: bucketDatastore):
    jsonlds = datastore.listJsonld(bucket, repo, include_user_meta=True)
    objs = map(lambda f: datastore.s3client.stat_object(f.bucket_name, f.object_name), jsonlds)
    o_list = list(map(lambda f: {'Source': repo,
                                 'Identifiertype': f.metadata.get('X-Amz-Meta-Identifiertype'),
                                 'Matchedpath': f.metadata.get('X-Amz-Meta-Matchedpath'),
                                 'Uniqueid': f.metadata.get('X-Amz-Meta-Uniqueid'),
                                 'Example': f.metadata.get('X-Amz-Meta-Uniqueid')
                                 }, objs))
    df = pandas.DataFrame(o_list)
    identifier_stats = df.groupby(['Source', 'Identifiertype', 'Matchedpath'], group_keys=True, dropna=False) \
        .agg({'Uniqueid': 'count', 'Example': lambda x: x.iloc[0:5].tolist()}).reset_index()
    return identifier_stats

# Example of CSV URL: 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTt_45dYd5LMFK9Qm_lCg6P7YxG-ae0GZEtrHMZmNbI-y5tVDd
# 8ZLqnEeIAa-SVTSztejfZeN6xmRZF/pub?gid=1340502269&single=true&output=csv'
def readSourceCSV(csv_url):
    response = request.urlopen(csv_url)
    csv_reader = csv.DictReader(response.read().decode('utf-8').splitlines())
    data_list = list(csv_reader)
    return data_list

def generateReportStats(url, bucket, datastore: bucketDatastore, graphendpoint, community):
    sources = readSourceCSV(url)
    #sources = list(filter(lambda source: source.get('Active') == "TRUE", sources))
    if community != "all":
        sources = list(filter(lambda source: source.get('Community') == community, sources))

    report = []
    for i in sources:
        source_url = i.get('URL')
        source_landing_page = i.get('Domain')
        source_name = i.get('Name')
        source_proper_name = i.get('ProperName')
        source_community = i.get('Community')
        source_des = i.get('Description')

        try:
            sm = Sitemap(source_url)
            if not sm.validUrl():
                logging.error(f"Invalid or unreachable URL: {source_url} ")

            parameters = {"repo": source_name}
            df = queryWithSparql("repo_count_graphs", graphendpoint, parameters)
            source_records = 0
            if df.empty:
                logging.info(f"Repo is empty in graph: {source_name} ")
            else:
                source_records = df.at[0, "graphs"]

            dict = {
                "source": source_name,
                "title": source_proper_name,
                "website": source_landing_page,
                "sitemap": source_url,
                "image": f"{source_name}.png",
                "community": source_community,
                "description": source_des,
                "records": source_records
            }

            report.append(dict)

        except Exception as e:
            logging.error(
                f"could not write report stats for {source_name} {bucket} error:{str(e)}")

    report_json = json.dumps(report, indent=4)

    return report_json




