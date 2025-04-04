import pandas as pd
import duckdb

# make sure to replace 'file.parquet' with your file path
df = pd.read_parquet('./data/idMinMaxDepth.parquet')
# df = df.head(10)

# use the values in the dataset_id to search via
# duckdb for the @id to generate the JSON-LD with.

# This section needs the OBIS JSON-LD in a directory at ./josnld/obis
# Should be able to do this against the minio S3 bucket
def search_duckdb(x):
    x = duckdb.sql(f"SELECT url FROM read_json('./jsonld/obis/*.jsonld') WHERE url like '%{x}%'").fetchall()    # directly query a JSON file
    xs = ", ".join(str(item[0]) for item in x)
    return(xs)

df['docid'] = df['dataset_id'].apply(lambda x: search_duckdb(x))

df = df.explode('docid')

# ------------   the rest is still in the notebook version


print(df.head)