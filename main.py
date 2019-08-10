"""Find Popular pages from Google Analytics."""

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import yaml
import json
import os
import logging
from dotenv import load_dotenv

# Configure Logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)-15s: %(name)s - %(levelname)s - %(message)s')

# Loading environment variables
load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = os.getenv('KEY_FILE_LOCATION')
VIEW_ID = os.getenv('VIEW_ID')
OUTPUT_FILE_LOCATION = os.getenv('OUTPUT_FILE_LOCATION')
OUTPUT_FORMAT = os.getenv('OUTPUT_FORMAT') # Supported formats: json, yaml
MAX_SIZE = int(os.getenv('MAX_SIZE'))

def initialize_analyticsreporting():
  """Initializes an Analytics Reporting API V4 service object.

  Returns:
    An authorized Analytics Reporting API V4 service object.
  """
  logging.info("Initializing Analytics API...")

  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)

  # Build the service object.
  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics


def get_report(analytics):
  """Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """
  logging.info("Fetching reports from google analytics")

  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:pageviews'}, {'expression': 'ga:uniquePageviews'}, {'expression': 'ga:timeOnPage'}, {'expression': 'ga:bounces'}, {'expression': 'ga:entrances'}, {'expression': 'ga:exits'}],
          'dimensions': [{'name': 'ga:pagePath'}],
          'orderBys': [{'fieldName': 'ga:pageviews', 'sortOrder': 'DESCENDING'}],
          'pageSize': MAX_SIZE
        }]
      }
  ).execute()


def write_response(response):
  """Parses and writes the Analytics Reporting API V4 response.

  Args:
    response: An Analytics Reporting API V4 response.
  """
  logging.info("Parsing analytics response...")

  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

    pages = {'popular': []}

    for row in report.get('data', {}).get('rows', []):
      dimensions = row.get('dimensions', [])
      metrics = row.get('metrics', [])
      metricValues = []
      if metrics:
        metricValues = metrics[0]['values']

      for header, dimension in list(zip(dimensionHeaders, dimensions)):
        if dimension == '/' or dimension.startswith('/categories') or dimension.startswith('/series') or dimension.startswith('/about'):
          continue
        all_metrics = zip(metricHeaders, metricValues) 
        page_views_metric = next((metricValue for metricHeader, metricValue in all_metrics if metricHeader['name'] == 'ga:pageviews'), None)
        
        pages['popular'].append({
          'path': dimension,
          'views': int(page_views_metric)
        })

    logging.info("Writing response...")
    if OUTPUT_FORMAT == 'json':
      write_json_response(pages)
    elif OUTPUT_FORMAT == 'yaml' or OUTPUT_FORMAT == 'yml':
      write_yaml_response(pages)
    else:
      print(pages)     

def write_yaml_response(data):
  with open(OUTPUT_FILE_LOCATION, 'w') as yaml_file:
    yaml.dump(data, yaml_file, default_flow_style=False)

def write_json_response(data):
  with open(OUTPUT_FILE_LOCATION, 'w') as json_file:
    json.dump(data, json_file, indent=3)

def main():
  analytics = initialize_analyticsreporting()
  response = get_report(analytics)
  write_response(response)

if __name__ == '__main__':
  main()
