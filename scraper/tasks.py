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
    master_slide = 0
    title_layout = 0
    title_content_layout = 1

    def __init__(self, request, site_url):

        self.site_url = site_url
        print(self.site_url)
        print('Scraping Site ..')
        req = Request(self.site_url)
        html = urlopen(req).read()
        bs = BeautifulSoup(html, 'html.parser')
        self.booktitle = bs.find('title').text
        self.create_powerpoint()
        self.find_info(bs, 1)
        self.slide.save(BASE_DIR  / 'slides_folder' / '{}.pptx'.format('finished_titlr.pptx'))


    def create_powerpoint(self):
        present_dir = BASE_DIR  / 'slides_folder' 
        prs = Presentation(present_dir / 'Template1.pptx')
        self.slide = prs

    def add_section(self, text):
        prs = self.slide
        
        slide_layout = prs.slide_masters[self.master_slide].slide_layouts[self.title_layout]
        slide = prs.slides.add_slide(slide_layout)

        title = slide.placeholders[0]
        title.text = text

    def add_slide(self, title, text):
        prs = self.slide
        slide_layout = prs.slide_masters[self.master_slide].slide_layouts[self.title_content_layout]    
        slide = prs.add_slide(slide_layout)

        for shape in slide.placeholders:
            print('Index: %d Name: %s Type: %s' % (shape.placeholder_format.idx, shape.name, shape.placeholder_format.type))

        title = slide.placeholders[1]
        title.text = title

        paragraph = slide.placeholders[2]
        paragraph.text = text



    def find_info(self, bs, no):
        tag = "tag"
        child = "child"
        text = "text"
        heads = bs.find_all('h' + str(no))
        no += 1
        for head in heads:
            heading_headers = head.parent.find_all('h' + str(no))
            if heading_headers != None and (no <= 6):
                    self.add_section(head.text)
                    self.find_info(head.parent, no + 1)
            elif head.parent == bs:
                paragraph = head.next_element.find_all('p')
                if paragraph:
                    self.add_slide(head.text, paragraph[0].get_text)
            else:
                paragraph = head.parent.find_all('p')
                if paragraph:
                    self.add_slide(head.text, paragraph[0].get_text)        
        return        

             

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

       

