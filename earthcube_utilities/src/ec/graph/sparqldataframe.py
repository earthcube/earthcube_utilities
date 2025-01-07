import pandas as pd
from simplejson import JSONDecodeError
import requests
import logging as log

def dbpedia_query(sparql_query):
    url = 'http://dbpedia.org/sparql'
    return query(url, sparql_query)


def wikidata_query(sparql_query):
    url = 'https://query.wikidata.org/sparql'
    return query(url, sparql_query)


def query(url, sparql_query):
    try:
        headers = {'accept': 'application/sparql-results+json'}
        r = requests.get(url,headers=headers, params={'format': 'json', 'query': sparql_query})
        if r.status_code == 200:
            data = r.json()
        else:
            raise Exception(f'sparqldataframe status {r.status_code} bad endpoint? {url} reason {r.reason}')
    except JSONDecodeError as e:
        #print(r.content)
        log.error(f'sparqldataframe: query to {url}  response:  "{r.content}"  ')
        raise Exception(f'Invalid query or bad decoding {e}')

    if ('results' in data) and ('bindings' in data['results']):
        columns = data['head']['vars']
        rows = [[binding[col]['value'] if col in binding else None
                for col in columns]
                for binding in data['results']['bindings']]
    else:
        raise Exception('No results')

    return pd.DataFrame(rows, columns=columns)
