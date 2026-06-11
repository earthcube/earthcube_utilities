# DataDistribution SPARQL Queries - Descriptions

This document provides a one-line explanation for each query created for Issue #92.

## Count Queries (All Graph)

### `all_count_datasets_with_distribution_urls.sparql`
Counts how many datasets have at least one distribution with a URL (either landing page or direct access).

### `all_count_distribution_types.sparql`
Counts distribution @type values to see what types exist besides DataDownload (e.g., Dataset, WebSite, WebAPI).

### `all_count_total_distributions.sparql`
Counts the total number of distributions across all datasets in the graph.

### `all_count_distributions_with_url.sparql`
Counts distributions that have a landing page URL (schema:url) - these require visiting a page to access data.

### `all_count_distributions_with_contenturl.sparql`
Counts distributions that have a direct access URL (schema:contentUrl) - these allow direct download without visiting a landing page.

### `all_count_distributions_with_both_urls.sparql`
Counts distributions that have both a landing page URL and a direct access URL.

### `all_count_distribution_access_types.sparql`
Provides a breakdown count of distributions by access type: landing pages, direct access, both, and total.

### `all_count_service_endpoints.sparql`
Counts datasets that have service endpoints defined via potentialAction (for API-based data access).

## Property Analysis Queries (All Graph)

### `all_distribution_properties_by_provider.sparql`
Shows which properties distributions have, grouped by provider/graph (based on assay-data README example).

### `all_distribution_properties_by_popularity.sparql`
Counts which distribution properties are most commonly used across all providers (based on assay-data README example).

## Detailed Analysis Queries (All Graph)

### `all_distribution_analysis.sparql`
Returns detailed information for all distributions: type, name, encoding format, landing page URL, and direct access URL for FAIR evaluation.

### `all_distribution_encoding_format_and_name.sparql`
Returns encoding format and name information for all distributions to analyze data format availability.

### `all_service_endpoints.sparql`
Returns detailed information about service endpoints (potentialAction) including action type, name, target URL, and result format.

## Repo-Specific Count Queries

### `repo_count_datasets_with_distribution_urls.sparql`
Counts datasets with distribution URLs for a specific repository (requires ${repo} parameter).

### `repo_count_distribution_types.sparql`
Counts distribution types for a specific repository (requires ${repo} parameter).

### `repo_count_distribution_access_types.sparql`
Provides breakdown of distribution access types (landing page vs direct access) for a specific repository (requires ${repo} parameter).

## Repo-Specific Analysis Queries

### `repo_distribution_analysis.sparql`
Returns detailed distribution analysis for a specific repository (requires ${repo} parameter).

### `repo_service_endpoints.sparql`
Returns service endpoint details for a specific repository (requires ${repo} parameter).

### `repo_distribution_properties_by_provider.sparql`
Shows distribution properties grouped by provider for a specific repository (requires ${repo} parameter).

## Summary

**Total: 18 queries**
- 8 count queries (all graph)
- 2 property analysis queries (all graph)
- 3 detailed analysis queries (all graph)
- 3 repo-specific count queries
- 3 repo-specific analysis queries

All queries follow the existing naming convention:
- `all_*` = queries for entire graph (no parameters)
- `repo_*` = queries for specific repository (require `${repo}` parameter)


