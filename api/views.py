from django.shortcuts import render
from django.http import JsonResponse


def api_home(reques, *args, **kwargs):
    return JsonResponse({'message': 'Hello we are testing this shit'})
# Create your views here.
