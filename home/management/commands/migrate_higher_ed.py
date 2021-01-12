from django.core.management.base import BaseCommand
from wagtail.core.models import Page
from django.core.validators import slug_re
from programs.models import Program, Subprogram, AbstractContentPage, Project
from survey.models import DemographicKey, SurveyOrganization, SurveyTags, Survey, SurveysHomePage, SurveyValuesIndex, PageAuthorRelationship
from survey.blocks import CtaBlock
from person.models import Person
from django.utils.text import slugify
import datetime
import json
import re
import uuid
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from apiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
# Credentials for HigherEd google sheet migration. Burn after migrating. See https://www.youtube.com/watch?v=T1vqS1NL89E for details.

credentials = ServiceAccountCredentials.from_json_keyfile_name('./google_sheet_creds.json', scope)
gc = gspread.authorize(credentials)

raw_data = json.dumps(gc.open('Copy of epp_polling_dashboard_data_LIVE').sheet1.get_all_records())
data = json.loads(raw_data)




class Command(BaseCommand):
  def handle(self, *args, **options):
    scaffold()

def scaffold():
  # Survey Homepage preset attribs
  name = "HigherEd Public Opinion Hub"
  about = "<p>The HigherEd Public Opinion Hub comprises public opinion surveys on higher education that have been conducted in the U.S. since 2010. Surveys in the dashboard explore the general public’s opinion on issues pertaining to higher education such as funding, diversity, and value. Some focus on opinion of first-year college students, college and university presidents, and faculty. The Hub is a helpful source for researchers, journalists, and the general public who are interested in understanding public opinion on higher education issues. It is, however, by no means an exhaustive source of public opinion surveys about higher education.</p>"
  methodology = "<p>Surveys in the Hub were collected by searching “higher education public opinion survey” in Google News. To be added, the survey needed to address the general public or other groups&#x27; opinion on at least one issue in higher education, be transparent about the methodology, and add the margins of error included where possible. Most of the surveys in the Hub are nationally representative, but some surveys that look into a specific population such as students, faculty, or administrators, may only capture the responses of those surveyed. To capture relatively recent data, we chose 2010 as the first year in which to include surveys; those before 2010 were excluded.</p>"
  subheading = "A collection of reports, insights, and analyses exploring topics within Higher Education. Created for Researchers, Journalists, and the general public who have an interest in understanding public opinion on Higher Education issues."
  subscribe_id= uuid.uuid4()
  submisssions_id = uuid.uuid4()
  subscribe =  "[{\"type\": \"cta_block\", \"value\": {\"title\": \"Love all this insight?\", \"description\": \"Subscribe to our newsletter to receive updates on what\\u2019s new in Education Policy.\", \"link_text\": \"Subscribe\", \"link_url\": \"https://www.newamerica.org/education-policy/higher-education/subscribe/\"}, \"id\": %d}]" %subscribe_id
  submissions = "[{\"type\": \"cta_block\", \"value\": {\"title\": \"Call for Submissions\", \"description\": \"Know of a survey report that should be added to our list?\", \"link_text\": \"Send us an email today.\", \"link_url\": \"nguyens@newamerica.org\"}, \"id\": %d}]" %submisssions_id
  about_submission = "<p>If you know of a survey that could be added to the site, please email the survey to <a href=\"mailto:nguyens@newamerica.org\">nguyens@newamerica.org.</a></p>"
  authors_ids = [18400, 21696]

  # Get EdPolicy Program Page.
  root = Program.objects.get(title='Education Policy')
  
  # Add SurveysHomePage.
  root.add_child(instance=SurveysHomePage(
    title = name,
    subheading = subheading,
    about = about,
    methodology=methodology,
    subscribe = subscribe,
    submissions = submissions,
    about_submission = about_submission,
    ))
  # Get SurveysHomePage, add authors and save.
  home = SurveysHomePage.objects.get(title=name)
  addAuthor(home, authors_ids)
  home.save()
  # Get index page.
  index = SurveyValuesIndex.objects.get(title=name+' Values Index')
  # Add Demos, Tags, Orgs and Surveys.
  addDemos(index)
  addTags(index)
  addOrgs(index)
  addSurveys(home)

def addSurveys(home: SurveysHomePage):
  date = datetime.datetime.today().strftime('%Y-%m-%d')
  surveys = getSurveys()
  for survey in surveys:
    slugified = slugify(survey['Study Title'] + '-' + str(survey['Year']))
    is_file = re.search('^https:\/\/drive\.google\.com\/file\/', survey['download'])
    title = setTitle(survey)
    print('ADDING SURVEY_______: ' + title)
    new_survey = Survey(
      title=title,
      slug=slugified,
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
    child = Survey.objects.get(title=title)

    addSurveyFile(child, survey, is_file)
    addSurveyTags(child, survey)
    addSurveyOrgs(child, survey)
    addSurveyDemos(child, survey)

    child.save()

def addDemos(index):
  new_demos = getProp('demographics_key')
  res = map(lambda d: d.title.strip(), DemographicKey.objects.all())
  known_demos = list(res)
  for demo in new_demos:
    if (demo not in known_demos):
      print('ADDING DEMO KEY________: '+demo)
      index.add_child(instance=DemographicKey(title=demo))
      known_demos.append(demo)
    else:
      print('Skipped demo:%s' % demo)
      continue

def addOrgs(index):
  new_orgs = getProp('Organization')
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
  new_tags = getProp('Tags')
  res = map(lambda t: t.title.strip(), SurveyTags.objects.all())
  known_tags = list(res)
  for tag in new_tags:
    if (tag not in known_tags):
      print('ADDING TAG________: '+tag)
      index.add_child(instance=SurveyTags(title=tag))
      known_tags.append(tag)
    else:
      print('Skipped tag:%s' % tag)
      continue

def addAuthor(page, author_ids):
  for auth_id in author_ids:
    author = Person.objects.get(id=auth_id)
    print('ADDING AUTHOR________: ' + str(author))
    rel = PageAuthorRelationship(author = author, page = page)
    rel.save()

def addSurveyDemos(survey, survey_data):
  demos = parse_list(survey_data['demographics_key'], ',')
  for demo in demos:
    survey_demo = DemographicKey.objects.get(title=demo.strip())
    survey.demos_key.add(survey_demo)

def addSurveyOrgs(survey, survey_data):
  orgs = parse_list(survey_data['Organization'], ',')
  for org in orgs:
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

def setTitle(survey: object):
  study_title = survey['Study Title']
  alt_title = survey['Study Title'] + '(' + str(survey['Year']) + ')'
  title_extant = Page.objects.filter(title=study_title).exists()
  if title_extant:
    return alt_title
  else:
    return study_title


# Get data from google sheet.
def getSurveys():
  surveys = []
  for survey in data:
    surveys.append(survey)
  return surveys

def getProp(prop:str):
  items = []
  for survey in data:
    my_items = parse_list(survey[prop], ',')
    for item in my_items:
      if item not in items:
        items.append(item.strip())
  return items
