import django_filters
from django import forms
from django.db import models
from django.db.models.query import QuerySet

from .models import Post

class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Post
        fields = ["title","radio"]
    # https://wayhome25.github.io/django/2017/04/01/django-ep9-crud/



