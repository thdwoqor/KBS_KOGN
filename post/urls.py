from django.urls import path
from .views import PostCreateView, PostFilterView, post_list_view ,post_detail_view
from django.urls import reverse

# https://stackoverflow.com/questions/6266415/django-class-based-generic-view-no-url-to-redirect-to/9218749
urlpatterns = [
    path('create/', PostCreateView.as_view(), name='post'),
    path("filter/", PostFilterView.as_view(), name="post-filter"),
    path("<id>/", post_detail_view, name="post-detail"),
    path("", post_list_view, name="post-list"),
    
]
