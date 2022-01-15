from django.shortcuts import render

from django.views.generic import CreateView
from django.http import JsonResponse
from .models import Post
from .form import PostForm
from radio.models import Radio

from django_filters.views import FilterView
from .filters import PostFilter



class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post.html'

class PostFilterView(FilterView):
    filterset_class = PostFilter
    template_name = 'tasklist_filter.html'

def post_list_view(request):
    context = {}
    context["object_list"] = Post.objects.all()
    context["radios"] = Radio.objects.all()

    return render(request, "tasklist_list.html", context)

def post_detail_view(request, id):
    context = {}
    context["post"] = Post.objects.get(id=id)

    return render(request, "tasklist_detail.html", context)