from django.urls import path
from .views import PostCreateView
from django.urls import reverse

# https://stackoverflow.com/questions/6266415/django-class-based-generic-view-no-url-to-redirect-to/9218749
urlpatterns = [
    path('create', PostCreateView.as_view(), name='post'),
]
