from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=100, blank=False)
    text = models.TextField()
    slug = models.SlugField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='logo/', blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts')
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    # def save(self, *args, **kwargs):
    #     self.slug = slug

class PostComment(models.Model):
    RATE = (
        ('very good', 'very good'),
        ('good', 'good'),
        ('bad', 'bad')
    )
    text = models.TextField(blank=False, null=False)
    rate = models.CharField(max_length=10, choices=RATE, default='good', blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'{self.author}:{self.post}:{self.pk}:{self.replies}'


class CommentReply(models.Model):
    text = models.TextField(blank=False, null=False)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    to_comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, related_name='replies')
