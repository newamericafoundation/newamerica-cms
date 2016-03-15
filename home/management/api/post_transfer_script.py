from .newamerica_api_client import NAClient

from article.models import Article, ProgramArticlesPage

from django.utils.text import slugify

from home.models import PostProgramRelationship

from programs.models import Program

mapped_programs = {
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
		'8': 'New America DC',
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
		'12': 'New America Weekly',
		'4': 'Asset Building',
	}


def get_program(programs, post):

	for old_program in programs:
		old_program = str(old_program)
		new_program = Program.objects.get_or_create(title=mapped_programs['old_program'],description=mapped_programs['old_program'], depth=3)
		relationship = PostProgramRelationship(program=new_program, post=post)
		relationship.save()


def get_post_date(original_date):
	old_date_split = original_date.split("T")
	new_date = old_date_split[0]
	
	return new_date


def download_image(url, image_filename):
    if url:
        image_location = os.path.join(
            'home/management/api/images',
            image_filename
        )
        urllib.urlretrieve(url, image_location)
        image = Image(
            title=image_filename,
            file=ImageFile(open(image_location), name=image_filename)
        )
        image.save()
        return image


def load_articles():
    for post, program_id in NAClient().get_articles():
    	program_id = str(program_id)
    	post_parent_program = Program.objects.get_or_create(title=mapped_programs[program_id])

    	parent_program_articles_homepage = first_parent_program.add_child(instance=)


    	article_slug = slugify(post['title'])
    	new_article = Article.objects.filter(slug=article_slug).first()
    	
    	if not new_article:
        	new_article = Article(
        		search_description='',
        		seo_title='',
        		depth=4,
        		show_in_menus=False,
        		slug=article_slug,
        		title=post['title'],
        		date=get_post_date(post['publish_at']),
        		body=json.dumps([{'type':'paragraph', 'value':post['content']}]),
        		story_exerpt=post['summary'],
        		story_image=download_image(post['cover_image_url'], post['title'] = "_image.jpeg")
        	)

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
	        		date='2016-03-15',


	        	)