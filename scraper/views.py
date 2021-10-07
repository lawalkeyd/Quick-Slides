from django.shortcuts import render
from .tasks import Scrape_Site
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@csrf_exempt
def create_slide(request):
    site_url = 'https://en.wikipedia.org/wiki/Adolf_Hitler'
    Scrape_Site(request, site_url)
