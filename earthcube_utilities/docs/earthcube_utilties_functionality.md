# Functionality of the Earthcube Utilities

## Earthcube Utilities Functionality Docments:
* [Functionality Breakdown ](./breakdown.md)
  * [Mini-base](./mini-base.md)
  * [Query Graphstore](./ec_query.md)
  * [RDF to Quads](/.rdf2triples.md)
  * [Validation](./validation_overall.md)
    * [Validating Sitemaps](./validation_sitemap.md)
    * [Validating JSONLD](./validation_jsonld.md)
    * [Validating Graph Loading](./validation_graph.md)
    * [Check Distribution Links](./validate_distribution_links.md)
  * [Implementation Testing](./validation_test_data.md)
  * [Repository Reporting](./repository_reporting.md)]
  * [RoCrate, aka collection](./ro_crate.md)
  * [JSONLD Utils](./sos_jsonld_utils.md)
  * Notebooks
    * [Visualization](./viz.md)


## Goal 
We want earthcube_utilities to be a pypi package... 

The present codebase needs to reimplemented, and **documented** so that it can be a package, and can be used by others.

The present earthcube_utilities.py  [in the top level directory](https://github.com/earthcube/earthcube_utilities/blob/main/earthcube_utilities.py)
is large (3700 lines of code) and contains a lot of dead code that makes it difficult to 
comprehend. It needs to be **redone**. 

Note, this directory contains an older version, and so it can be deleted when developement of 
the revised code begins.

Reimplementation will need to be done with **planning**, and a clean room approach to modularization.
Ideally, code should be reimplemented, cleanly with logical function names, and not just copied.
The implementation should include unit testing, if appropriate. Especially, if such
tests help demonstrate functionality.

### Steps

* **Plan:** Document what functionality that you think needs to exist in the package.
  * functionality, basically, what are the 'modules'
  * Document, what methods that you expect users to call to get access to the functionality of the modules.
  * What are the base modules that need to be implemented first.
* **Implementation** Implement functionality in modular chunks.
  * Pick a 'feature'/functionality,
  * Write  tests, and code.  
  * Revise documentation, or just incorporate documentation into the code, and generate automatically

Know that by utilizing  unit tests, you  demonstrate how some of the functionality is utilized, and
reduce cruft in the actual code.

You can test **pandas dataframes** by reading in data dumped for pandas dataframes.

For _dataframe_ testing, you  load data from a csv using load pandas.read_csv...

To get data for testing, I suggest using pycharm, you can [dump a dataframe using the export](https://www.jetbrains.com/help/pycharm/matplotlib-support.html#data) when viewing in debuging...
**Caveat: name with a .csv extension**.... and trim testing data it down to a row or two.  

