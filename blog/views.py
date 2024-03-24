import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from . import models, forms
from django.shortcuts import reverse, redirect
from django.core.paginator import Paginator
from .models import BlogPost
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Create your views here.


class Home(generic.ListView):
    model = models.BlogPost
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    ordering = ['-datetime_created']
    paginate_by = 5


class PostDetail(LoginRequiredMixin, generic.DetailView, generic.CreateView):
    model = models.BlogPost
    form_class = forms.PostCommentForm
    template_name = 'blog/detail_view.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        print(self.request.GET)
        context = super().get_context_data()
        post = self.model.objects.get(slug = self.kwargs['slug'])
        context['form'] = self.get_form()
        context['post'] = post
        paginator = Paginator(post.comments.all().order_by('datetime_created'),2)
        page = self.request.GET.get('cp')
        context['comments'] = paginator.get_page(1 if not page else int(page))
        context['paginator'] = paginator
        context['pp'] = models.CommentReply.objects.filter(to_comment=1)

        return context

    def form_valid(self, form):
        if comment_pk:=self.request.GET.get('reply_to'):
            form = forms.ReplyCommentForm(self.request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.author = self.request.user
                form.to_comment = get_object_or_404(models.PostComment, pk=int(comment_pk))
                form.save()
        else:
            if form.is_valid():
                form = form.save(commit=False)
                form.author = self.request.user
                form.post = self.get_object()
                form.save()
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.GET.get('reply_to'):
            r = self.request.GET.copy()
            r.pop('reply_to')
            return reverse('post_detail', args=[self.get_object().slug],)+"?"+r.urlencode()
        return reverse('post_detail', args=[self.get_object().slug],)+"?"+self.request.GET.urlencode()

class PostEditView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    template_name = 'blog/post_edit.html'
    model = models.BlogPost
    form_class = forms.BlogPostForm
    context_object_name = 'post'
    def get_success_url(self):
        return reverse('post_edit', kwargs={'slug': self.get_object().slug})

    def test_func(self):
        return self.get_object().author == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = models.BlogPost
    template_name = 'blog/post_delete.html'
    context_object_name = 'post'
    def get_success_url(self):
        return reverse('home')
    def test_func(self):
        return self.get_object().author == self.request.user
# class SendComment(generic.CreateView):
#     form_class = forms.PostCommentForm
#
#     def post(self, request, *args, **kwargs):
#
#         form = self.form_class(request.POST)
#         post = get_object_or_404(BlogPost, pk=self.kwargs['pk'])
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.author = self.request.user
#             comment.post = post.pk
#             comment.save()
#             return redirect('post_detail', pk=self.kwargs['pk'])
#         return render(request, 'blog/detail_view.html', {'form': form, 'post': post})
