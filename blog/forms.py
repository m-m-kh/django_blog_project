from django.forms import ModelForm, forms,TypedChoiceField
from .models import PostComment
# TypedChoiceField(.bound_data())

class PostCommentForm(ModelForm):
    class Meta:
        model = PostComment
        fields = ['text', 'rate']
