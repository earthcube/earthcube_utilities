import csv
from io import StringIO
from urllib import request

from ec.sitemap.sitemap import Sitemap
import argparse

from ec.logger import config_app

log = config_app()


# Example of CSV URL: 'https://docs.google.com/spreadsheets/d/1pqZpMWqQFwUrleHXPbvXqXX59Xcj1Yrtqt2nJTh1reM/pub?output=csv'
def readSourceCSV(gsheet_csv_url):
    response = request.urlopen(gsheet_csv_url)
    csv_reader = csv.DictReader(response.read().decode('utf-8').splitlines())
    data_list = list(csv_reader)
    return data_list


def convert_gsheet_csv_to_sitemap(gsheet_csv_url):
    sources = readSourceCSV(gsheet_csv_url)
    return sources

def start():
    """
        Run the sitemap_checker program.
        Sitemap checker. Default option  checks if url is sitemap exist.
        Arguments:
            args: Arguments passed from the command line.
        Returns:
            result of check as csv.

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help='URL of the source CSV file', default=True)
    args = parser.parse_args()

    result = convert_gsheet_csv_to_sitemap(args.url)
    print(result)

if __name__ == '__main__':

    result = start()

