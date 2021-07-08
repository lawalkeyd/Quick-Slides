from time import sleep
from celery import shared_task
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from .models import Details, Images, ParentInfo, ScrapedInfo

def Check(bs, title, no):
    parent = ParentInfo.objects.create(title= title) 
    head = bs.find_all('h' + str(no))
    if head or no > 6:
        for item in head:
            Check(item, item.text, no + 1)
    else:
        image = bs.parent.find('img')
        if image:
                Images.objects.create(info=parent, images=image.text)
        paragraph = bs.parent.find('p')
        if paragraph:
            Details.objects.create(info=parent, text=paragraph.text)

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
    #images = bs.find('img').text
    print(title)
    Check(bs, title, 1)


    # create objects in database
   
        
    # sleep few seconds to avoid database block
    sleep(5)

web_scrape('https://en.wikipedia.org/wiki/Adolf_Hitler')
       

