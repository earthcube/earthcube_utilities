# Validate using test data

**Test Level 1 and level 2, WORKING**
This is incorporated in the
https://github.com/earthcube/GeoCODES-Metadata


They utilize [Approval testing](https://approvaltests.com/), 
if a result differs, then alert and ask if this is ok.
If there is no change, then test passes.

If a **test fails** look in integration_testing/approved_files
for a file with a .received.txt extenstion
look at it, rename it to approved if it looks good.

Since the JSON testing is only line counts for now, you may need to debug to see
the output.




## Approval Tests:
Coding
* need to have an s3 client to pull the data from minio.

Logic, after files are approved, they should not change, so testing can be automated.
using approvals tests approach

## NOTE
I am going to suggest that this be done in the GeocodesMetadata reop, rather than earthcube utilities
closer to the metadata is a good thing.

Also, that would mean that a small portion of the EC utilities is packaged and documented.
* graph (graph directory from  to  ec_utils)
* s3 just use the minio client or boto... 

### Test 1: basic loading
* pre-setup
  * create a config file, sans secrets. store.
  * pass glcon env variables for secrets. (put in github, also)
* Test setup
  * test  code creates a temp bucket 
  * test  code create a temp graph  (summary does this)
  * Test code executes glcon command to run gleaner, and nabu using the 
* testing
  * Approvals Summon:
    * count in {bucket}/summoned/{repo}
  * Approvals JSONLD:
    * for each file in bucket, 
       * is file valid json,
       * Approval of JSON LD loaded to s3
  * Approvals Graph
    * for each file {bucket}/milled/{repo}
       * is file non-zero length
       * Approval. Does is look like the loaded triples match the JSONLD
  * Approvals Nabu
    * does the count of triples equal the last time run
    * for each urn (aka file in bucket) 
       * does the triples count for the graph match the count in the {bucket}/milled/{repo}
         * do we realy need to test to see they match if the counts are equal?

### Testing 2, test for duplicate loads, and pruning.
This might be just added as a test with an additional load
* Test setup
  * test  code creates a temp bucket 
  * test  code create a temp graph  (summary does this)
  * Test code executes glcon command to run gleaner, and nabu using the 
  * test code loads to nabu a SECOND time
* testing
  * Approvals Nabu
    * Did the count of triples increase from the original load. 
       *  If so, fail. just use an approval to do this. run count if it changed, bad.
    * for each urn (aka file in bucket) 
       * does the triples count for the graph match the count in the {bucket}/milled/{repo}
         * do we realy need to test to see they match if the counts are equal?

### Has the config file changed
except for the secrets, has the config file changed. This is just heads up warning


### does the counts match
run count, capture to approval test. Should only fail when a file is added.

### Does JSONLD == JSONLD
does the JSONLD uploaded to s3 equal the last approval test result. 
There may be changes over time as we refine the conversion... but that it what approval tests are for


### Does the Graph == graph
Does the uploaded and downloaded triples match

### Has the SHACL Validation result changed (future)
Capture SHACL Validation, and see if it has changed.

