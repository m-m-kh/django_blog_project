from django.contrib import admin

from blog.models import BlogPost, PostComment


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'datetime_created', 'datetime_modified', 'author')


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'datetime_created')
