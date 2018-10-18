## Creating Related Content on posts

at the bottom posts (blogs, podcasts etc.) Related content that the author chooses or that we somehow automatically figure out posts


1. Created `related table` called RelatedPosts that links a Post to many posts
2. Add RelatedPosts as a field to the Post Model
3. Add RelatedPosts as a field option in Wagtail Admin
4. Make a migration for Home app
5. Migrate

6. Add related posts components to the base Post.html template in Django
OR
6. Create an API View (aka a Controller)
7. Create a PostRelatedContent Serializer (turns a Django Model into JSON)
8. Create a RelatedContent Endpoint
9. Create a React Component that retrieves data from that endpoint
