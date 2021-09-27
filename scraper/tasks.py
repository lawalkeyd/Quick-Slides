from time import sleep
from celery import shared_task
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from .models import Details, Images, ParentInfo, ScrapedInfo
from pptx import Presentation
from django.http import HttpResponse
from QuickSlides.settings import BASE_DIR


def Check(bs, no, parent):
    tag = "tag"
    child = "child"
    text = "text"
    heads = bs.find_all('h' + str(no))
    if heads != None or (no > 6):
        for item in heads:
            parent[child] = {}
            parent[tag] = item.text
            Check(item, parent[child], no + 1)
    else:
        # image = bs.parent.find('img')
        # if image:
        #         Images.objects.create(info=parent, images=image.get_text)
        paragraph = bs.parent.find_all('p')
        if paragraph:
            parent[text] = paragraph[0].get_text
    return parent        

             

@shared_task
# some heavy stuff here
def web_scrape(url):
    print('Scraping Site ..')
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')
    # get first 5 rows
    parent = {}
    parent["title"] = bs.find('title').text
    result = Check(bs, 1, parent)


    # create objects in database
    present_dir = BASE_DIR  / 'slides_folder' 
   
    prs = Presentation(present_dir / 'Ion.pptx')

    # first_slide = prs.slides[0]
    # title = first_slide.shapes.title
    # subtitle = first_slide.placeholders[1]
    # title.text = result["title"]
    # subtitle.text = "Subtitle"

    if "child" in result:
        slide = prs.slides[0]
        title = slide.shapes.title
        title.text = result["title"]

    response = HttpResponse(content_type='application/vnd.ms-powerpoint')
    response['Content-Disposition'] = 'attachment; filename="sample.pptx"'
    prs.save(present_dir / 'Complete.pptx')
    # ppt = source_stream.getvalue()
    # source_stream.close()
    # response.write(ppt)
    return 'done'
    # sleep few seconds to avoid database block
    sleep(5)

web_scrape('https://en.wikipedia.org/wiki/Adolf_Hitler')
       

