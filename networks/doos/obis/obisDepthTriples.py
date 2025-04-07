import pandas as pd
import os

def populate_template(row):
    template = """ {{
      "@context": {{
        "@vocab": "https://schema.org/"
      }},
      "@id": "{docid}",
      "@type": "Dataset",
      "variableMeasured": [
        {{
          "@type": "PropertyValue",
          "name": "depth",
          "description": "Parsed and validated by OBIS.",
          "minValue": "{MIN}",
          "maxValue": "{MAX}",
          "propertyID": "https://obis.org/data/access/",
          "measurementTechnique": "Parsed and validated by OBIS.",
          "unitText": "m",
          "unitCode": [
            "https://qudt.org/vocab/unit/M", "https://vocab.nerc.ac.uk/collection/P06/current/ULAA/",
            "http://dbpedia.org/resource/Metre"
          ]
        }}
      ]
    }}
    """

    return template.format(MAX=row['max_depth'], MIN=row['min_depth'], docid=row['docid'])




# make sure to replace 'file.parquet' with your file path
df = pd.read_parquet('./data/idMinMaxDepth.parquet')
# df = df.head(10)

# use the values in the dataset_id to search via
# duckdb for the @id to generate the JSON-LD with.

# This section needs the OBIS JSON-LD in a directory at ./josnld/obis
# Should be able to do this against the minio S3 bucket
# this can take 5 to 10 minutes to run
# def search_duckdb(x):
#     # x = duckdb.sql(f"SELECT url FROM read_json('./jsonld/obis/*.jsonld') WHERE url like '%{x}%'").fetchall()    # directly query a JSON file
#
#     # Configure MinIO (S3-compatible)
#     duckdb.sql("SET s3_region='us-west-2'")
#     duckdb.sql("SET s3_endpoint='oss.geocodes-aws.earthcube.org:443'")
#     duckdb.sql("SET s3_access_key_id=''")
#     duckdb.sql("SET s3_secret_access_key=''")
#     duckdb.sql("SET s3_url_style='path'")  # use 'path' if MinIO is path-style
#
#     # Read from MinIO
#     query = f"""
#             SELECT url FROM read_json_auto('s3://decoder/summoned/obis/*.jsonld')
#             WHERE url LIKE '%{x}%'
#             """
#     result = duckdb.sql(query).fetchall()
#
#     xs = ", ".join(str(item[0]) for item in x)
#     return(xs)
#
# df['docid'] = df['dataset_id'].apply(lambda x: search_duckdb(x))


df_csv = pd.read_csv('bucketutil_urls.csv')
df_csv['docid'] = df_csv['url'].apply(lambda x: x.split('/')[-1])
merged_df = pd.merge(df, df_csv, left_on='dataset_id', right_on='docid', how='inner')
dfe = merged_df.explode('docid')
dfe_strict = dfe.dropna(subset=['max_depth', 'min_depth'], how='any')
dfe_strict = dfe_strict.assign(jsonld=dfe_strict.apply(populate_template, axis=1))

output_dir = './jsonld/output_strict/'
os.makedirs(output_dir, exist_ok=True)

for index, row in dfe_strict.iterrows():
    filename = str(output_dir + row['dataset_id']) + '_depth.jsonld'  # adjust file extension as per your requirement
    with open(filename, 'w') as f:
        f.write(row['jsonld'])