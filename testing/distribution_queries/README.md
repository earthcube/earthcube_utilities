# DataDistribution SPARQL Queries Testing

This folder contains test scripts and documentation for the DataDistribution SPARQL queries created for [Issue #92](https://github.com/earthcube/earthcube_utilities/issues/92).

## Files

- **`test_distribution_queries.py`** - Main test script that runs all distribution queries
- **`test_results.txt`** - Test results (generated when script runs)
- **`QUERY_DESCRIPTIONS.md`** - One-line descriptions for each query

## Quick Start

Activate your virtual environment and run:
```cmd
python test_distribution_queries.py
```

Results will be saved to `test_results.txt` in this directory.

## What the Script Does

### `test_distribution_queries.py`
- Tests all 18 new distribution queries
- Saves results to `test_results.txt`
- Count queries: Fast (1-5 seconds each)
- Property analysis queries: Fast (1-30 seconds each)
- Detailed queries: Slower (1-2 minutes each, return 600k+ rows)
- Total time: ~5-10 minutes for all queries

## Expected Output

You'll see:
```
======================================================================
Testing: all_count_datasets_with_distribution_urls
Description: Count datasets with distribution URLs
======================================================================
  Running query...
✓ Success! Time: 4.61s
  Rows: 1, Columns: ['datasetcount']
  Sample data:
    {'datasetcount': '139881'}
  → Saved to test_results.txt
```

## If It Seems Slow

The detailed queries (`all_distribution_analysis`, `all_distribution_encoding_format_and_name`) return 661,633 rows and take 1-2 minutes each. They're **not stuck**, just processing a large dataset. 

**Note:** The script saves results after each query, so you can check `test_results.txt` even if you need to cancel.

## Viewing Results

Results are saved to `test_results.txt`. You can:
- Open it in any text editor
- View in Command Prompt: `type test_results.txt`
- View in PowerShell: `Get-Content test_results.txt`

## Queries Tested

The script tests 18 new SPARQL queries:
- 8 count queries (fast, 1-5 seconds each)
- 2 property analysis queries (fast, 1-30 seconds each)
- 3 detailed analysis queries (slower, 1-2 minutes each, return 600k+ rows)
- 5 repo-specific queries (fast, 1-5 seconds each)

All queries are located in: `earthcube_utilities/src/ec/graph/sparql_files/`

See `QUERY_DESCRIPTIONS.md` for detailed descriptions of each query.
