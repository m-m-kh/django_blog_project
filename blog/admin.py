from django.contrib import admin

from blog.models import BlogPost, PostComment, CommentReply


class CommentReplyInlineAdmin(admin.TabularInline):
    model = CommentReply
    extra = 0

class CommentInlineAdmin(admin.TabularInline):
    model = PostComment
    extra = 0

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'datetime_created', 'datetime_modified', 'author')
    prepopulated_fields = {'slug': ('title',)
                           }
    inlines = [CommentInlineAdmin]

@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'datetime_created')
    inlines = [CommentReplyInlineAdmin]
@admin.register(CommentReply)
class ReplyCommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'to_comment')
