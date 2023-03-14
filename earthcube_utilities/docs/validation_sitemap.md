# Validating sitemaps

There is a tool in development for validating sitemaps with a github action.

[workflow](https://github.com/iodepo/odis-arch/tree/master/workflows)

[example action](https://github.com/iodepo/odis-arch/blob/master/.github/workflows/sitemapcheck.yml)

## research
are there other more complete libraries that might be integrated?
There is a [sitemap assay notebook](https://github.com/gleanerio/notebooks/blob/master/notebooks/sitemap_assay.ipynb). Is this useful?

## Steps that will be needed:
* extract code from oih to a gleanerio repository
    * fork into earthcube
* test
* write first documentation

* Add:
  * are the url's unique
  * implement full ping on all urls, multithead if it's allowed in an action.
  * Implement ability to trigger an email to a repository holder or at least a EC developer when 
    * sitemap no longer exists (404)
    * count of JSONLD extracted, or 404 errors changes significantly.
  * [command line like](https://github.com/iodepo/odis-arch/blob/master/workflows/actions/sitemapcheck/check_sitemap_loop.py)

## Functionality:

* does sitemap exist (daily)
* send email (do we want this, can it be a github user name?)
* multithreaded check of url in sitemap (weekly or monthly?)