### Earthcube Query

Implemented in ec/graph

 manageGraph/ManageBlazegraph


<ins>**query.py** </ins> is can do all the SPARQL queries the UI can do.

Query returns a pandas dataframe using the sparqldataframe library. A set of queries based
on the the [facetserch UI sparql queries](https://github.com/earthcube/facetsearch/tree/master/client/src/sparql_blaze)
and other queries utilized for data exploration and data validation are included.

LIST QUERIES: This is the detailed functionality

(I am going to suggest that a list of queries, and functionality, and some details be incorporated into an assets
list. The list should probably be a file in YAML or JSON format in the resources directory.)

|  short_name | file | detailed description |
|-------------| ---- | ------ | 
| summary     | ./resources/sparql/summary.txt | takes query term, `q`, and returns a summary of the matched resoruces |
| sbj2urn     | ./resources/sparql/sbj2urn.txt  | returns the urn of the graph  for a given graph `g`   |

_This is the proposed implementation stratedgy..._ 
it is setup to add one get_{qry_name}\_txt  function to get the txt of the query, usually from raw git 
then a function: {qry_name} that calls one fuction with {qry_name} as the arg, and maybe a variable
it will get the txt from the 1st function, and replace the var w/in the template txt, run the query and return a DF

(**above  reads  like a possible security hole** I am going to run a method with a dynamically defined name.
Implementation seems overly complex, 

Suggest that queries be embedded in resources. which would make things clearer than many courtesy methods.
something simpler, like:

```
def QUERY(endpoint)
# validate that endpoint exists.
def listQueries() 
# return list of queries
def query(self, short_name=summary, options)
# where options would be an object containing passed parameters {"q":"steens"}
def queryFromURL(self, url="https://raw.githubusercontent.com/MBcode/ec/master/NoteBook/sparql-query.txt", options)
```

```python
q = QUERY("http:example.com")
dataframe = q.query("sub2urn",options={"g":"somegraph"} )
dataframe2 = q.queryFromURL( url="https://raw.githubusercontent.com/MBcode/ec/master/NoteBook/sparql-query.txt", options={"q":"steens"})

```

#### Usages:
many. 
* It can be used to get information to validated informaiton from the graph,
* it can be used in notebooks to run queries.

Also, suggest jinja2, or the [standard python3 templates](https://docs.python.org/3.4/library/string.html#template-strings) for replacing parameters in templates.
