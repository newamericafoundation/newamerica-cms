from .newamerica_api_client import NAClient

def load_posts():
    for post in NAClient().get_posts():
        print(post['programs'])
