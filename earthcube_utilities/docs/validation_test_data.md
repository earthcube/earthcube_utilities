# Validate using test data


This need to be [Approval testing](https://approvaltests.com/), 
if a result differs, then alert and ask if this is ok.
If there is no change, then test passes.

To do this we need some approval tests.

## Approval Tests:
### Has the config file changed
except for the secrets, has the config file changed

### does the counts match
run count, capture to approval test. Should only fail when a file is added.

### Does JSONLD == JSONLD
does the JSONLD uploaded to s3 equal the last approval test result. 
There may be changes over time as we refine the conversion... but that it what approval tests are for


### Does the Graph == graph
Does the uploaded and downloaded triples match

### Has the SHACL Validation result changed
Capture SHACL Validation, and see if it has changed.

