from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from . import models, forms
from django.shortcuts import reverse, redirect

from .models import BlogPost


# Create your views here.


class Home(generic.ListView):
    model = models.BlogPost
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    ordering = ['-datetime_created']
    paginate_by = 5


class PostDetail(generic.DetailView, generic.CreateView):
    model = models.BlogPost
    form_class = forms.PostCommentForm
    template_name = 'blog/detail_view.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = self.get_form()
        context['post'] = self.model.objects.get(pk =self.kwargs['pk'])
        return context

    def form_valid(self, form):
        print(form.errors)
        form = form.save(commit=False)
        form.author = self.request.user
        form.post = self.get_object()
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', args=[self.get_object().pk])


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
