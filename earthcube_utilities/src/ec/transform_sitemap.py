import csv
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

    data_list = [
        row for row in csv_reader
        if row.get('Type') == 'Dataset'
    ]
    return data_list


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

def generate_sitemap(gsheet_csv_url):
    data_list = read_community_items_CSV(gsheet_csv_url)

    sitemap_entries = []
    for data in data_list:
        url = data['Dataset Webpage URL']

        if check_url_for_jsonld(url):
            entry = f"""
    <url>
        <loc>{url}</loc>
    </url>"""
            sitemap_entries.append(entry)
        else:
            print(f"No JSON-LD data found for {url}.")

    sitemap_xml = f"""<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{''.join(sitemap_entries)}
</urlset>"""

    return sitemap_xml

@click.command()
@click.option('--url_items', help='URL for Community Items of the source CSV file', required=True)
@click.option('--s3server', help='s3 server address')
@click.option('--s3bucket', help='s3 bucket')
def convert_gsheet_csv_to_sitemap(url_items, s3server, s3bucket):
    s3Minio = s3.MinioDatastore(s3server, None)
    sitemap = generate_sitemap(url_items)
    # upload the generated sitemap to s3 bucket
    s3Minio.putSitemapFile(s3bucket, "geochemistry_sitemap.xml", sitemap)
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

