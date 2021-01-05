from django.core.management.base import BaseCommand
from wagtail.core.models import Page
from django.core.validators import slug_re
from programs.models import Program, Subprogram, AbstractContentPage, Project
from survey.models import DemographicKey, SurveyOrganization, SurveyTags, Survey, SurveysHomePage, SurveyValuesIndex
from django.utils.text import slugify
import datetime
import json
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from apiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('./creds.json', scope)
gc = gspread.authorize(credentials)
raw_data = json.dumps(gc.open('Copy of epp_polling_dashboard_data_LIVE').sheet1.get_all_records())
data = json.loads(raw_data)

class Command(BaseCommand):
  def handle(self, *args, **options):
    scaffold()

def scaffold():
  # Get EdPolicy Program Page.
  root = Program.objects.get(title='Education Policy')
  # Add Project Page.
  root.add_child(instance=Project(
    title='HigherEd Public Opinion Hub',
    slug=slugify('HigherEd Public Opinion Hub'),
    name='HigherEd Public Opinion Hub',
    template='survey/surveys_home_page.html',
    description='A collection of reports, insights, and analyses exploring topics within Higher Education. Created for Researchers, Journalists,  and the general public who have an interest in underatanding public opinion on Higher Education issues.',
    ))
  # Get Project page and add SurveyHomePage.
  project = Project.objects.get(title='HigherEd Public Opinion Hub')
  project.add_child(instance=SurveysHomePage(title='Reports & Insights'))
  # Get SurveyHomePage.
  home = SurveysHomePage.objects.get(title='Reports & Insights')
  # Get index page.
  index = SurveyValuesIndex.objects.get(title='Reports & Insights Values Index')
  print(index.id, index.title)
  # Add Demos, Tags, Orgs and Surveys.
  addDemos(index)
  addTags(index)
  addOrgs(index)
  addSurveys(home)

def addSurveys(home: SurveysHomePage):
  date = datetime.datetime.today().strftime('%Y-%m-%d')
  surveys = getSurveys()
  for survey in surveys:
    slug = slugify(survey['Study Title'])
    is_file = re.search('^https:\/\/drive\.google\.com\/file\/',survey['download'] )
    if Page.objects.filter(slug=slug).exists():
      continue
    else:
      print('ADDING SURVEY_______: ' + slug)
      new_survey = Survey(
        title=survey['Study Title'],
        slug=slug,
        date=date,
        year=survey['Year'],
        month=None,
        sample_number=survey['sample_number'],
        data_type = ['QUANT', 'QUAL'],
        findings = survey['Top findings directly from the report'],
        link = survey['download'] if not is_file else None
      )

      home.add_child(instance=new_survey)

      # Load the survey object.
      child = Survey.objects.get(title=survey['Study Title'])

      addSurveyFile(child, survey, is_file)
      addSurveyTags(child, survey)
      addSurveyOrgs(child, survey)
      addSurveyDemos(child, survey)

      child.save()

def addDemos(index):
  new_demos = getDemos()
  res = map(lambda d: d.title.strip(), DemographicKey.objects.all())
  known_demos = list(res)
  for demo in new_demos:
    if (demo not in known_demos):
      print('ADDING DEMO KEY________: '+demo)
      index.add_child(instance=DemographicKey(title=demo))
      known_demos.append(demo)
    else:
      continue

def addOrgs(index):
  new_orgs = getOrgs()
  res = map(lambda o: o.title.strip(), SurveyOrganization.objects.all())
  known_orgs = list(res)
  for org in new_orgs:
    if (org not in known_orgs):
      print('ADDING ORG________: '+org)
      index.add_child(instance=SurveyOrganization(title=org))
      known_orgs.append(org)
    else:
      print('Skipped org:%s' % org)
      continue

def addTags(index):
  new_tags = getTags()
  res = map(lambda t: t.title.strip(), SurveyTags.objects.all())
  known_tags = list(res)
  for tag in new_tags:
    if (tag not in known_tags):
      print('ADDING TAG________: '+tag)
      index.add_child(instance=SurveyTags(title=tag))
      known_tags.append(tag)
    else:
      continue

def addSurveyDemos(survey, survey_data):
  demos = parse_list(survey_data['demographics_key'], ',')
  for demo in demos:
    survey_demo = DemographicKey.objects.get(title=demo.strip())
    survey.demos_key.add(survey_demo)

def addSurveyOrgs(survey, survey_data):
  org = survey_data['Organization']
  survey_org = SurveyOrganization.objects.get(title=org.strip())
  survey.org.add(survey_org)

def addSurveyTags(survey, survey_data):
  tags = parse_list(survey_data['Tags'], ',')
  for tag in tags:
    survey_tag = SurveyTags.objects.get(title=tag.strip())
    survey.tags.add(survey_tag)

def addSurveyFile(survey, data, is_file):
  if is_file:
    # Create Google Drive API service.
    service = build('drive', 'v3', credentials=credentials)
    # Get file id.
    file_id = getFileId(data['download'])
    # Get filename from API.
    meta = service.files().get(fileId=file_id).execute()
    filename = meta['name']
    # Download file to temp location.
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO('/tmp/%s' % filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
      status, done = downloader.next_chunk()
      print("Download %d%%." % int(status.progress() * 100))
    # Open the file.
    f = open('/tmp/%s' % filename, 'rb')
    # Save file to model.
    survey.file.save(filename, File(f))
  else:
    survey.file = None

# Utility methods.
def parse_list(str, delimiter):
  li = str.split(delimiter)
  return li

def getPageId(title: str):
  item = Page.objects.get(title=title)
  return item.id

def getFileId(url: str):
  regex = "([\w-]){33}|([\w-]){19}"
  return re.search(regex,url).group()

# Get data from google sheet.
def getSurveys():
  surveys = []
  for survey in data:
    surveys.append(survey)
  return surveys

def getTags():
  tags = []
  for survey in data:
    my_tags = parse_list(survey['Tags'], ',')
    for tag in my_tags:
      if tag not in tags:
        tags.append(tag.strip())
  return tags

def getDemos():
  demos = []
  for survey in data:
    demo = survey['demographics_key']
    if demo not in demos:
      demos.append(demo.strip())
  return demos

def getOrgs():
  orgs = []
  for survey in data:
    org = survey['Organization']
    if org not in orgs:
      orgs.append(org.strip())
  return orgs
