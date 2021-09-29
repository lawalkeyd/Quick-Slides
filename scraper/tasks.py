from time import sleep
from celery import shared_task
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from .models import Details, Images, ParentInfo, ScrapedInfo
from pptx import Presentation
from django.http import HttpResponse
from QuickSlides.settings import BASE_DIR


class Scrape_Site:
    filename  = slide = site_url = None
    parent = {}
    booktitle = ''

    def __init__(self, request):
        self.site_url = request.data.get('site_url')
        print('Scraping Site ..')
        req = Request(self.site_url, headers=request.headers.__dict__)
        html = urlopen(req).read()
        bs = BeautifulSoup(html, 'html.parser')
        self.booktitle = bs.find('title').text
        self.create_powerpoint()
        self.find_info(bs, 1, self.parent)

    def create_powerpoint(self):
        present_dir = BASE_DIR  / 'slides_folder' 
        prs = Presentation(present_dir / 'Ion.pptx')
        self.slide = prs

    def find_info(bs, no):
        tag = "tag"
        child = "child"
        text = "text"
        heads = bs.find_all('h' + str(no))
        for head in heads:
            heading_headers = head.parent.find_all('h' + str(no+1))
            if heading_headers != None and (no <= 6):
                    self.create_section(head.text)
                    self.find_info(head.parent, no + 1)
            else:
                paragraph = head.parent.find_all('p')
                if paragraph:
                    self.create_slide(head.text, paragraph[0].get_text)
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
    parent["title"] = BookTitle = bs.find('title').text
    result = Find_Info(bs, 1, parent)


    # create objects in database
    present_dir = BASE_DIR  / 'slides_folder' 
    prs = Presentation(present_dir / 'Ion.pptx')


    if "child" in result:
        slide = prs.slides[0]
        title = slide.shapes.title
        title.text = result["title"]

    response = HttpResponse(content_type='application/vnd.ms-powerpoint')
    response['Content-Disposition'] = 'attachment; filename="sample.pptx"'
    prs.save(present_dir / '{}.pptx'.format(BookTitle))
    # ppt = source_stream.getvalue()
    # source_stream.close()
    # response.write(ppt)
    return 'done'
    # sleep few seconds to avoid database block
    sleep(5)

web_scrape('https://en.wikipedia.org/wiki/Adolf_Hitler')
       

