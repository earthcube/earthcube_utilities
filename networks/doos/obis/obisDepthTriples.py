import os
import json
import pandas as pd
from ec.datastore import s3
import xml.etree.ElementTree as ET

def make_depth_property(row):
    return {
        "@type": "PropertyValue",
        "name": "depth",
        "description": "Parsed and validated by OBIS.",
        "minValue": row["min_depth"],
        "maxValue": row["max_depth"],
        "propertyID": "https://obis.org/data/access/",
        "measurementTechnique": "Parsed and validated by OBIS.",
        "unitText": "m",
        "unitCode": [
            "https://qudt.org/vocab/unit/M",
            "https://vocab.nerc.ac.uk/collection/P06/current/ULAA/",
            "http://dbpedia.org/resource/Metre"
        ]
    }

# 1) Load depth DataFrame
df = pd.read_parquet("./data/idMinMaxDepth.parquet")

# 2) Load CSV of URLs + SHAs; extract docid
df_csv = pd.read_csv("bucketutil_urls.csv", dtype=str)
df_csv["docid"] = df_csv["url"].apply(lambda u: u.rstrip("/").split("/")[-1])

# 3) Merge on dataset_id ↔ docid
merged = pd.merge(df,
                  df_csv,
                  left_on="dataset_id",
                  right_on="docid",
                  how="inner") \
           .dropna(subset=["min_depth", "max_depth"], how="any")

# 4) Prepare MinIO client
#s3_client = s3.MinioDatastore("oss.geocodes-aws.earthcube.org", None)
s3_client = s3.MinioDatastore("oss.geocodes.ncsa.illinois.edu", None)

# 5) Prepare output dirs
jsonld_out = "./jsonld/output_strict/"
os.makedirs(jsonld_out, exist_ok=True)

# 6) Hold the URLs we upload for sitemap
uploaded_urls = []

for _, row in merged.iterrows():
    sha  = row["sha"]
    dsid = row["dataset_id"]

    # fetch existing JSON‑LD
    try:
        s3ObjectInfo = {"bucket_name": "decoder", "object_name": f"summoned/obis/{sha}"}
        existing_str = s3_client.getFileFromStore(s3ObjectInfo)
        data = json.loads(existing_str)
    except Exception as e:
        print(f"⚠️  could not fetch {sha}: {e}")
        continue

    # append depth property
    depth_prop = make_depth_property(row)
    vm = data.get("variableMeasured")
    if isinstance(vm, list):
        vm.append(depth_prop)
    else:
        data["variableMeasured"] = [depth_prop]

    # write locally
    local_path = os.path.join(jsonld_out, f"{dsid}_depth.jsonld")
    with open(local_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅  wrote {local_path}")

    # upload to decoder/community_resources/deepoceans/obis_depth
    object_name = f"{dsid}_depth.jsonld"
    s3_client.putCommunityResourceFile(
        "decoder",
        "deepoceans/obis_depth",
        object_name,
        json.dumps(data)
    )
    #url = f"https://oss.geocodes-aws.earthcube.org/decoder/community_resources/deepoceans/obis_depth/{object_name}"
    url = f"https://oss.geocodes.ncsa.illinois.edu/decoder/community_resources/deepoceans/obis_depth/{object_name}"
    uploaded_urls.append(url)
    print(f"✅  uploaded {object_name}")

# 7) Generate sitemap XML
urlset = ET.Element(
    "urlset",
    xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
)
for loc_url in uploaded_urls:
    url_el = ET.SubElement(urlset, "url")
    loc_el = ET.SubElement(url_el, "loc")
    loc_el.text = loc_url

sitemap_str = ET.tostring(
    urlset,
    encoding="utf-8",
    xml_declaration=True
).decode()

# write sitemap locally
sitemap_local = "./jsonld/obis_depth_sitemap.xml"
with open(sitemap_local, "w") as f:
    f.write(sitemap_str)
print(f"✅  wrote sitemap to {sitemap_local}")

# upload sitemap to decoder/sitemaps/obis_depth_sitemap.xml
s3_client.putSitemapFile(
    "decoder",
    "obis_depth_sitemap.xml",
    sitemap_str
)
print("✅  uploaded sitemap to decoder/sitemaps/obis_depth_sitemap.xml")
