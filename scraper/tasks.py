from time import sleep
from celery import shared_task
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from .models import ScrapedInfo

@shared_task
# some heavy stuff here
def web_scrape(url):
    print('Scraping Site ..')
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')
    # get first 5 rows
    title = bs.find('title').text
    doc = ScrapedInfo.objects.create(title = title, url=url)
    h1 = bs.find('h1').text
    images = bs.find_all('img').text
    print(title)


    # create objects in database
   
        
    # sleep few seconds to avoid database block
    sleep(5)

web_scrape('https://theconcordschool.org/')

def Check(bs, title):
    h1 = bs.find_all('h1')