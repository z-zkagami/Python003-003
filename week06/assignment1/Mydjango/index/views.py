from django.shortcuts import render
from .models import Ratings
from django.http import HttpResponse
# Create your views here.

def index(request):
    ratings = Ratings.objects.all()
    return render(request, 'index.html', locals())