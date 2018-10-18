from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from django.core.cache import cache
from dateutil.relativedelta import relativedelta
import datetime

import os
import json

from programs.models import Program
from home.models import Post
from newamericadotorg.api.post.serializers import PostSerializer

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE = {
  "type": "service_account",
  "project_id": "post-location-1500647458160",
  "private_key_id": os.getenv('GOOGLE_SERVICE_PRIVATE_KEY_ID'),
  "private_key":  bytes(os.environ['GOOGLE_SERVICE_PRIVATE_KEY'], 'utf-8').decode("unicode_escape"),
  "client_email": "trending-posts@post-location-1500647458160.iam.gserviceaccount.com",
  "client_id": "108457953544433140358",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/trending-posts%40post-location-1500647458160.iam.gserviceaccount.com"
}

VIEW_ID = '91076142'


def init_analytics_service():
  credentials = ServiceAccountCredentials.from_json_keyfile_dict(
      KEY_FILE, SCOPES)

  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics


def get_top_posts(analytics, program_slug):
  dimensions = [
      { 'name': 'ga:pagePathLevel1' },
      { 'name': 'ga:pagePathLevel2' },
      { 'name': 'ga:pagePathLevel3' }
    ]

  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'pageSize': 10,
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:pageViews'}],
          "orderBys":[
            {"fieldName": "ga:pageViews", "sortOrder": "DESCENDING"}
          ],
          'dimensions': dimensions,
          "dimensionFilterClauses": [
            {
              "operator": "AND",
              "filters": [
                {
                  "dimensionName": "ga:pagePathLevel1",
                  "operator": "EXACT",
                  "expressions": "/%s/" % program_slug
                },
                {
                    "dimensionName": "ga:hostname",
                    "operator": "EXACT",
                    "expressions": "www.newamerica.org"
                }
              ]
            }]
        }]
      }
  ).execute()



def parse_report(report):
    slugs = []

    try:
        data = report['reports'][0]['data']['rows']
    except KeyError:
        return False

    for d in data:
        result = d['dimensions']
        slug = result[2].replace('/', '')
        if slug == '': continue
        slugs.append(slug)

    if len(slugs) == 0: return False
    return slugs



def get_program_posts():
    programs = Program.objects.all()
    analytics = init_analytics_service()

    for p in programs:
        report = get_top_posts(analytics, p.slug)
        slugs = parse_report(report)
        if not slugs: continue

        year_ago = datetime.datetime.now() - relativedelta(years=1)
        posts = Post.objects.filter(slug__in=slugs)
        d = PostSerializer(posts, many=True).data

        key = 'TRENDING_%s' % p.slug
        cache.set(key, d, 60 * 60 * 25)

        print('cached trending %s posts' % key)
