import requests
import json

# from PIL import Image
# from io import BytesIO

from django.conf import settings

headers = {
  'Accept': '*/*',
  'Authorization': f'Bearer {settings.DATAWRAPPER_KEY}',
}


# def publish_chart(id):
#   requests.post(f'https://api.datawrapper.de/v3/charts/{id}/publish', headers=headers)
#   print(f'Published {id}')

def get_embed(id):
  response = requests.get(f'https://api.datawrapper.de/v3/charts/{id}', headers=headers)
  chart_info = json.loads(response.text)['metadata']['publish']
  code = chart_info['embed-codes']['embed-method-responsive']
  width = chart_info['embed-width']
  return code, width

# def export_image(id):
#   url = f'https://api.datawrapper.de/v3/charts/{id}/export/png?height=auto'
#   headers = {
#     'Accept': 'image/png',
#     'Authorization': f'Bearer {settings.DATAWRAPPER_KEY}',
#   }
#   response = requests.get(url, headers=headers)
#   image = Image.open(BytesIO(response.content))
#   chart_title_string = '_'.join(chart['title'].split()[:2])
#   chart_title_string = chart_title_string.replace('/','_').replace(',','').replace('.','')
#   file_path = f'{folder_name}/{chart_title_string}_{id}.png'
#   image.save(file_path)
#   print(f'Exported {id} to {file_path}')

