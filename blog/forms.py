from django.forms import ModelForm, forms,TypedChoiceField
from .models import PostComment, CommentReply, BlogPost
# TypedChoiceField(.bound_data())

class PostCommentForm(ModelForm):
    class Meta:
        model = PostComment
        fields = ['text', 'rate']

class ReplyCommentForm(ModelForm):
    class Meta:
        model = CommentReply
        fields = ['text']

class BlogPostForm(ModelForm):
    class Meta:
        model = BlogPost()
        fields = ('title','text','logo')

