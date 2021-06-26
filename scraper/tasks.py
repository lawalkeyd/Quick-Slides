from time import sleep
from celery import shared_task
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from .models import ScrapedInfo

@shared_task
# some heavy stuff here
def web_scrape(url):
    print('Creating forex data ..')
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')
    # get first 5 rows
    title = bs.find('title').text
    text = bs.find('div').text
    images = bs.find_all('img')
    print(title)


    # create objects in database
    ScrapedInfo.objects.create(title = title, text = text)
        
    # sleep few seconds to avoid database block
    sleep(5)

web_scrape('https://theconcordschool.org/')