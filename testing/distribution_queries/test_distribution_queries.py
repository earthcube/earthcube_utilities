#!/usr/bin/env python3
"""
Test script for DataDistribution SPARQL queries (Issue #92)
Tests all new distribution queries and saves results to test_results.txt
"""
import sys
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "earthcube_utilities" / "src"))

from ec.graph.sparql_query import queryWithSparql

ENDPOINT = "https://graph.geocodes.ncsa.illinois.edu/blazegraph/namespace/decoder/sparql"
TEST_REPO = "opentopography"
RESULTS_FILE = Path(__file__).parent / "test_results.txt"

def format_time(seconds):
    """Format time in a readable way"""
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    else:
        mins = int(seconds // 60)
        secs = seconds % 60
        return f"{mins}m {secs:.2f}s"

def format_result(df, max_rows=3):
    """Format DataFrame result for display"""
    if df is None or len(df) == 0:
        return "  (No results)"
    result_str = f"  Rows: {len(df)}, Columns: {list(df.columns)}\n"
    display_df = df.head(max_rows)
    result_str += "  Sample data:\n"
    for idx, row in display_df.iterrows():
        result_str += f"    {dict(row)}\n"
    if len(df) > max_rows:
        result_str += f"    ... ({len(df) - max_rows} more rows)\n"
    return result_str

def test_query(query_name, description, params=None):
    """Test a single query and save to file"""
    print(f"\n{'='*70}")
    print(f"Testing: {query_name}")
    print(f"Description: {description}")
    if params:
        print(f"Parameters: {params}")
    print(f"{'='*70}")
    
    # Write to results file
    with open(str(RESULTS_FILE), 'a', encoding='utf-8') as f:
        f.write(f"\n{'='*70}\n")
        f.write(f"Query: {query_name}\n")
        f.write(f"Description: {description}\n")
        if params:
            f.write(f"Parameters: {params}\n")
        f.write(f"{'='*70}\n")
    
    start = time.time()
    try:
        print("  Running query...")
        if params:
            result = queryWithSparql(query_name, ENDPOINT, parameters=params)
        else:
            result = queryWithSparql(query_name, ENDPOINT)
        elapsed = time.time() - start
        
        print(f"✓ Success! Time: {format_time(elapsed)}")
        result_text = format_result(result)
        print(result_text)
        
        # Save to file
        with open(str(RESULTS_FILE), 'a', encoding='utf-8') as f:
            f.write(f"✓ Success! Time: {format_time(elapsed)}\n")
            f.write(result_text)
            f.write("\n")
        
        return {"status": "success", "time": elapsed, "rows": len(result) if result is not None else 0}
    except Exception as e:
        elapsed = time.time() - start
        error_msg = f"✗ Error after {format_time(elapsed)}: {e}"
        print(error_msg)
        
        # Save error to file
        with open(str(RESULTS_FILE), 'a', encoding='utf-8') as f:
            f.write(error_msg + "\n")
            f.write("\n")
        
        return {"status": "error", "time": elapsed, "error": str(e)}

# Initialize results file
print("="*70)
print("Testing DataDistribution SPARQL Queries (Issue #92)")
print("="*70)
print(f"Results will be saved to: {RESULTS_FILE}")
print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*70)

# Backup existing file if it exists
if RESULTS_FILE.exists():
    backup_file = f"test_results_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    print(f"\nBacking up existing {RESULTS_FILE} to {backup_file}")
    Path(RESULTS_FILE).rename(backup_file)

# Initialize new results file
with open(str(RESULTS_FILE), 'w', encoding='utf-8') as f:
    f.write("="*70 + "\n")
    f.write("Testing DataDistribution SPARQL Queries (Issue #92)\n")
    f.write("="*70 + "\n")
    f.write(f"Endpoint: {ENDPOINT}\n")
    f.write(f"Test Repo: {TEST_REPO}\n")
    f.write(f"Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("="*70 + "\n")

# All new distribution queries
queries = [
    # Count queries
    ("all_count_datasets_with_distribution_urls", None, "Count datasets with distribution URLs"),
    ("all_count_distribution_types", None, "Count distribution @type values"),
    ("all_count_total_distributions", None, "Count total distributions"),
    ("all_count_distributions_with_url", None, "Count distributions with landing page URL"),
    ("all_count_distributions_with_contenturl", None, "Count distributions with direct access URL"),
    ("all_count_distributions_with_both_urls", None, "Count distributions with both URLs"),
    ("all_count_distribution_access_types", None, "Distribution access types breakdown"),
    ("all_count_service_endpoints", None, "Count datasets with service endpoints"),
    
    # Property analysis queries (based on assay-data README)
    ("all_distribution_properties_by_provider", None, "Distribution properties by provider"),
    ("all_distribution_properties_by_popularity", None, "Distribution properties by popularity"),
    
    # Detailed analysis queries (may take 1-2 minutes each - return 600k+ rows)
    ("all_distribution_analysis", None, "Detailed distribution analysis"),
    ("all_distribution_encoding_format_and_name", None, "Encoding format and name analysis"),
    ("all_service_endpoints", None, "Service endpoints details"),
    
    # Repo-specific queries
    ("repo_count_datasets_with_distribution_urls", {"repo": TEST_REPO}, "Count datasets with distribution URLs for repo"),
    ("repo_count_distribution_types", {"repo": TEST_REPO}, "Count distribution types for repo"),
    ("repo_count_distribution_access_types", {"repo": TEST_REPO}, "Distribution access types breakdown for repo"),
    ("repo_distribution_analysis", {"repo": TEST_REPO}, "Detailed distribution analysis for repo"),
    ("repo_service_endpoints", {"repo": TEST_REPO}, "Service endpoints details for repo"),
    ("repo_distribution_properties_by_provider", {"repo": TEST_REPO}, "Distribution properties by provider for repo"),
]

print(f"\nTotal queries to test: {len(queries)}")
print("Starting tests...\n")

results = []
start_time = time.time()

# Test each query
for i, (query_name, params, description) in enumerate(queries, 1):
    print(f"[{i}/{len(queries)}] {query_name}")
    result = test_query(query_name, description, params)
    result["name"] = query_name
    results.append(result)
    print(f"  → Saved to {RESULTS_FILE}")

total_time = time.time() - start_time

# Final summary
print("\n" + "="*70)
print("SUMMARY")
print("="*70)

successful = [r for r in results if r["status"] == "success"]
failed = [r for r in results if r["status"] == "error"]

summary_text = f"""
Total queries tested: {len(results)}
Successful: {len(successful)}
Failed: {len(failed)}
Total execution time: {format_time(total_time)}
"""

print(summary_text)

if successful:
    times = [r["time"] for r in successful]
    print(f"""
Timing Statistics:
  Total query time: {format_time(sum(times))}
  Average time per query: {format_time(sum(times)/len(times))}
  Fastest: {format_time(min(times))}
  Slowest: {format_time(max(times))}
""")

if failed:
    print("\nFailed Queries:")
    for r in failed:
        print(f"  ✗ {r['name']}: {r.get('error', 'Unknown error')}")

# Save summary to file
with open(str(RESULTS_FILE), 'a', encoding='utf-8') as f:
    f.write("\n" + "="*70 + "\n")
    f.write("SUMMARY\n")
    f.write("="*70 + "\n")
    f.write(f"\nTotal queries tested: {len(results)}\n")
    f.write(f"Successful: {len(successful)}\n")
    f.write(f"Failed: {len(failed)}\n")
    f.write(f"Total execution time: {format_time(total_time)}\n")
    
    if successful:
        times = [r["time"] for r in successful]
        f.write(f"""
Timing Statistics:
  Total query time: {format_time(sum(times))}
  Average time per query: {format_time(sum(times)/len(times))}
  Fastest: {format_time(min(times))}
  Slowest: {format_time(max(times))}
""")
    
    if failed:
        f.write("\nFailed Queries:\n")
        for r in failed:
            f.write(f"  ✗ {r['name']}: {r.get('error', 'Unknown error')}\n")
    
    f.write("\n" + "="*70 + "\n")
    f.write("Testing complete!\n")
    f.write("="*70 + "\n")

print(f"\n{'='*70}")
print("✓ Testing complete!")
print(f"Results saved to: {RESULTS_FILE}")
print("="*70)
