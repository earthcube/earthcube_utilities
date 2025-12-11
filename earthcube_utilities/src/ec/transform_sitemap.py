import csv
import json
import re
from urllib import request
import click
import requests
from ec.logger import config_app
from ec.datastore import s3

log = config_app()

# Example of CSV URL: 'https://docs.google.com/spreadsheets/d/1pqZpMWqQFwUrleHXPbvXqXX59Xcj1Yrtqt2nJTh1reM/pub?output=csv'
def read_community_items_CSV(gsheet_csv_url):
    response = request.urlopen(gsheet_csv_url)
    csv_reader = csv.DictReader(response.read().decode('utf-8').splitlines())
    return csv_reader


def check_url_for_jsonld(url):
    try:
        # Fetch the content of the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        # Search for <script> tags with type="application/ld+json" using a regular expression
        pattern = r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>'
        matches = re.findall(pattern, response.text, re.DOTALL)

        if matches:
            # Return True if JSON-LD data is found
            return True
        else:
            # Return False if no JSON-LD data is found
            return False
    except requests.RequestException as e:
        print(f"An error occurred while trying to fetch the URL: {e}")
        return False

def generate_sitemap(gsheet_csv_url, file_paths):
    data_list = read_community_items_CSV(gsheet_csv_url)

    sitemap_entries = []
    for data in data_list:
        if not data.get("Type") == "Dataset":
            continue

        url = data['Dataset Webpage URL']

        if check_url_for_jsonld(url):
            entry = f"""
    <url>
        <loc>{url}</loc>
    </url>"""
            sitemap_entries.append(entry)
        else:
            print(f"No JSON-LD data found for {url}.")

    for file_path in file_paths:
        entry = f"""
    <url>
        <loc>{file_path}</loc>
    </url>"""
        sitemap_entries.append(entry)

    sitemap_xml = f"""<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{''.join(sitemap_entries)}
</urlset>"""

    return sitemap_xml

def generate_webpages(s3Minio, s3bucket, gsheet_csv_url):
    data_list = read_community_items_CSV(gsheet_csv_url)

    file_paths = []
    for data in data_list:
        if data.get("Type") == "Webpage":
            file_path = generate_upload_webpage(s3Minio, s3bucket, data)
            file_paths.append(file_path)

    return file_paths

def generate_upload_webpage(s3Minio, s3bucket, data):
    url = data.get('Dataset Webpage URL')
    name = data.get('Dataset Name')
    description = data.get('Description')
    group = data.get('Group')
    creator = data.get('Creator')
    provider = data.get('Provider')
    publisher = data.get('Publisher')
    box_lon_min = data.get('box_lon_min')
    box_lon_max = data.get('box_lon_max')
    box_lat_min = data.get('box_lat_min')
    box_lat_max = data.get('box_lat_max')

    # Safely handle missing keywords
    raw_keywords = data.get('Keywords') or ""
    # split on semicolons, trim whitespace, and drop empty fragments
    keywords_list = [kw.strip() for kw in raw_keywords.split(';') if kw.strip()]

    # add group to keywords if present
    if group:
        keywords_list.append(group.strip())

    # optional: de-duplicate while preserving order
    keywords_list = list(dict.fromkeys(keywords_list))

    file_name = re.sub(r'[^A-Za-z0-9]+', '-', name.strip()).strip('-').lower()
    file_path = f"https://{s3Minio.endpoint}/{s3bucket}/community_resources/earthsurface/{file_name}.jsonld"

    jsonld = {
        "@context": {
            "@vocab": "https://schema.org/",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "schema": "https://schema.org/",
            "xsd": "http://www.w3.org/2001/XMLSchema#"
        },
        "@type": "Dataset",
        "additionalType": "WebPage",
        "isAccessibleForFree": True,
        "creator": {
            "@type": "Organization",
            "name": creator
        },
        "description": description,
        "url": url,
        "datePublished": "2010-01-01",
        "keywords": keywords_list,
        "name": name,
        "provider": {
            "@type": "Organization",
            "name": provider
        },
        "publisher": {
            "@type": "Organization",
            "name": publisher
        },
        "spatialCoverage": {
            "@type":
                "Place",
            "geo":
                {
                    "@type":
                        "GeoShape",
                    "box":
                        f"{box_lat_min} {box_lon_min} {box_lat_max} {box_lon_max}"
                }
        },
        "version": 1
    }

    s3Minio.putCommunityResourceFile(s3bucket, "earthsurface", f"{file_name}.jsonld", json.dumps(jsonld, indent=4))

    return file_path



@click.command()
@click.option('--url_items', help='URL for Community Items of the source CSV file', required=True)
@click.option('--s3server', help='s3 server address')
@click.option('--s3bucket', help='s3 bucket')
def convert_gsheet_csv_to_sitemap(url_items, s3server, s3bucket):
    s3Minio = s3.MinioDatastore(s3server, None)
    file_paths = generate_webpages(s3Minio, s3bucket, url_items)
    sitemap = generate_sitemap(url_items, file_paths)
    # upload the generated sitemap to s3 bucket
    s3Minio.putSitemapFile(s3bucket, "earthsurface_sitemap.xml", sitemap)
    return sitemap

def start():
    """
        Read datasets from the google sheet and convert them to a sitemap
        Arguments:
            args: Arguments passed from the command line.
        Returns:
            a sitemap

    """
    result = convert_gsheet_csv_to_sitemap()

if __name__ == '__main__':

    result = start()

