from django.urls.conf import path
from .views import RadioDetailView


urlpatterns = [
    path('radio/<pk>', RadioDetailView.as_view(), name='radio'),
]