from django.shortcuts import render

from django.views.generic import CreateView
from django.http import JsonResponse
from .models import Post
from .form import PostForm

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post.html'
