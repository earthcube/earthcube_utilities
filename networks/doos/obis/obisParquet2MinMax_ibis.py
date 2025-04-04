import duckdb
import pandas as pd

# Connect to duckdb
ddb_con = duckdb.connect()
print("Connected to duckdb using duckdb.connect()")

# Path to the parquet file
data = "/home/fils/scratch/data/obis_20240625.parquet"  # very big....  put somewhere local
print(f"Reading parquet file: {data}")

sql_query = f"""
    SELECT 
        dataset_id,
        MIN(minimumDepthInMeters) as min_depth,
        MAX(maximumDepthInMeters) as max_depth
    FROM read_parquet('{data}')
    GROUP BY dataset_id
"""

# Execute the query and write directly to a parquet file
result_file = "./data/idMinMaxDepth.parquet"
ddb_con.execute(f"COPY ({sql_query}) TO '{result_file}' (FORMAT PARQUET)")
print(f"Successfully wrote result to parquet file: {result_file}")
