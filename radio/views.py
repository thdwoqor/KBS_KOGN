from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import DetailView
from django.core import serializers
import json
from radio.models import Radio

# Create your views here.
class RadioDetailView(DetailView):
    model = Radio

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = serializers.serialize('json', [self.object])
        # https://stackoverflow.com/questions/2391002/django-serializer-for-one-object
        return HttpResponse(data[1:-1], content_type='application/json')