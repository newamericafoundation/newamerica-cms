from .newamerica_api_client import NAClient

from article.models import Article

from django.utils.text import slugify

import json

def get_programs(program_id):
	str(program_id)
	
	old_programs = {
		'15': 'Asset Building',
		'7': 'Better Life Lab',
		'19': 'Cybersecurity Initiative',
		'13': 'Economic Growth',
		'5': 'Education Policy',
		'20': 'Family Centered Social Policy',
		'1': 'Future of War',
		'9': 'Fellows',
		'2': 'Future Tense',
		'22': 'Global Cybersecurity Norms',
		'10': 'International Security',
		'8': 'New America',
		'24': 'New America CA',
		'17': 'New America Live',
		'18': 'New America NYC',
		'16': 'Open Markets',
		'3': 'Open Technology Institute',
		'6': 'Political Reform',
		'14': 'Post Secondary National Policy Institute',
		'21': 'Profits & Purpose',
		'23': 'Resilient Communities',
		'25': 'Resource Security',
		'12': 'The Weekly Wonk',
		'4': 'Youthsave',
	}

def get_post_date(original_date):
	old_date_split = original_date.split("T")
	new_date = old_date_split[0]
	return new_date

def load_posts():
    for post in NAClient().get_posts():
        if post['type'] == "Article":
        	article_slug = slugify(post['title'])
        	new_article = Article.objects.filter(slug=article_slug).first()
        	if not new_article:
	        	new_article = Article(
	        		search_description='',
	        		seo_title='',
	        		show_in_menus=False,
	        		slug=article_slug,
	        		title=post['title'],
	        		date=get_post_date(post['publish_at']),



	        	)

def education_posts():
	for content in NAClient().education_content():
		with open("education_content.json", "a") as f:
			json.dump(content, f)

