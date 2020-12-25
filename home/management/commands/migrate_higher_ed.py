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

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('./creds.json', scope)
gc = gspread.authorize(credentials)
raw_data = json.dumps(gc.open('Copy of epp_polling_dashboard_data_LIVE').sheet1.get_all_records())
data = json.loads(raw_data)

class Command(BaseCommand):
  def handle(self, *args, **options):
      date = datetime.datetime.today().strftime('%Y-%m-%d')
      # index = Page.objects.get(title='HigherEd Public Opinion Hub Values Index')
      scaffold()

def scaffold():
  #get EdPolicy Program
  root = Program.objects.get(title='Education Policy')
  #add Project Page
  root.add_child(instance=Project(
    title='HigherEd Public Opinion',
    slug=slugify('HigherEd Public Opinion'),
    name='HigherEd Public Opinion',
    template='survey/surveys_home_page.html',
    description='A collection of reports, insights, and analyses exploring topics within Higher Education. Created for Researchers, Journalists,  and the general public who have an interest in underatanding public opinion on Higher Education issues.',
    ))
  # get Project page and add SurveyHomePage
  project = Project.objects.get(title='HigherEd Public Opinion')
  project.add_child(instance=SurveysHomePage(title='HigherEd Public Opinion Hub'))
  # get index page
  index = SurveyValuesIndex.objects.get(title='HigherEd Public Opinion Hub Values Index')
  print(index.id, index.title)
  #add Demos, Tags, Orgs
  addDemos(index)
  addTags(index)
  addOrgs(index)

def addSurveys(home: str):
  home_page = Page.objects.get(title=home)
  date = datetime.datetime.today().strftime('%Y-%m-%d')
  surveys = getSurveys()
  for survey in surveys:
    slug = slugify(survey['Study Title'])
    is_file = re.search('^https:\/\/drive\.google\.com\/file\/',survey['download'] )
    if Page.objects.filter(slug=slug).exists():
      continue
    else:
      print('ADDING_______: ' + slug)
      home_page.add_child(instance=Survey(
        title=survey['Study Title'],
        slug=slug,
        date=date,
        year=survey['Year'],
        month=0,
        sample_number=survey['sample_number'],
        # Don't think I can add these here, but these are the keys to get them.
        # demos_key = survey['demographics_key'],
        # org = survey['Organization'],
        # tags = survey['Tags'],
        data_type = ['QUANT', 'QUAL'],
        findings = survey['Top findings directly from the report'],
        file = survey['download'] if is_file else None,
        link = survey['download'] if not is_file else None,
      ))
      child = Survey.objects.get(title=survey['Study Title'])

      # child.demos_key = getPageId(survey['demographics_key'])
      print(child)

# Add objects to the db
def addDemos(index):
  new_demos = getDemos()
  res = map(lambda d: d.title.strip(), DemographicKey.objects.all())
  known_demos = list(res)
  for demo in new_demos:
    if (demo not in known_demos):
      print('ADDING________: '+demo)
      index.add_child(instance=DemographicKey(title=demo))
      known_demos.append(demo)
    else:
      continue

def addOrgs(index):
  print(index.id)
  new_orgs = getOrgs()
  res = map(lambda o: o.title.strip(), SurveyOrganization.objects.all())
  known_orgs = list(res)
  for org in new_orgs:
    if (org not in known_orgs):
      print('ADDING________: '+org)
      index.add_child(instance=SurveyOrganization(title=org))
      known_orgs.append(org)
    else:
      continue

def addTags(index):
  new_tags = getTags()
  res = map(lambda t: t.title.strip(), SurveyTags.objects.all())
  known_tags = list(res)
  for tag in new_tags:
    if (tag not in known_tags):
      print('ADDING________: '+tag)
      index.add_child(instance=SurveyTags(title=tag))
      known_tags.append(tag)
    else:
      continue


#utility funcs
def parse_list(str, delimiter):
  li = str.split(delimiter)
  return li

def getPageId(title: str):
  item = Page.objects.get(title=title)
  return item.id



# Get data from google sheet

def getSurveys():
  surveys = []
  for survey in data:
    surveys.append(survey)
  return surveys[0:3]

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