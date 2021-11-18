from time import sleep
from celery import shared_task
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from .models import Details, Images, ParentInfo, ScrapedInfo
from pptx import Presentation
from django.http import HttpResponse
from QuickSlides.settings import BASE_DIR

import os


class Scrape_Site:
    filename  = slide = site_url = None
    parent = {}
    booktitle = ''
    master_slide = 0
    title_layout = 0
    title_content_layout = 1

    def __init__(self, request, site_url):

        self.site_url = site_url
        filename = 'slide.log'
        self.log = open(os.path.join(os.path.dirname(__file__),filename),'w')        
        self.log.write(self.site_url)
        self.log.write('Scraping Site ..')
        req = Request(self.site_url)
        html = urlopen(req).read()
        bs = BeautifulSoup(html, 'html.parser')
        self.booktitle = bs.find('title').text
        self.create_powerpoint()
        self.find_info(bs, 1)
        self.slide.save(BASE_DIR  / 'slides_folder' / '{}.pptx'.format(self.booktitle))
        self.log.close


    def create_powerpoint(self):
        present_dir = BASE_DIR  / 'slides_folder' 
        prs = Presentation(present_dir / 'Template1.pptx')
        self.slide = prs

    def add_section(self, text):
        self.log.write('starting section adding')
        prs = self.slide
        
        slide_layout = prs.slide_masters[self.master_slide].slide_layouts[self.title_layout]
        slide = prs.slides.add_slide(slide_layout)

        title = slide.placeholders[0]
        title.text = text

    def add_slide(self, title, text):
        self.log.write('starting slide adding')
        prs = self.slide
        slide_layout = prs.slide_masters[self.master_slide].slide_layouts[self.title_content_layout]    
        slide = prs.slides.add_slide(slide_layout)

        for shape in slide.placeholders:
            self.log.write('Index: %d Name: %s Type: %s\n' % (shape.placeholder_format.idx, shape.name, shape.placeholder_format.type))

        title_placeholder = slide.placeholders[0]
        title_placeholder.text = title

        paragraph = slide.placeholders[1]
        self.log.write(text + ' testing text')
        paragraph.text = text



    def find_info(self, bs, no):
        tag = "tag"
        child = "child"
        text = "text"
        heads = bs.find_all('h' + str(no))
        self.log.write('there are {} headings\n'.format([i.text[0:] for i in heads]))
        for head in heads:
            self.log.write('heading {} found\n'.format(no))
            heading_headers = head.parent.find_all('h' + str(no))
            if heading_headers != None and (no <= 5):
                no += 1
                self.log.write('adding section {}\n'.format(head.text))
                self.add_section(head.text)
                self.find_info(head.parent, no)
            elif no <= 5:
                no += 1
                self.log.write('going through this again\n')
                self.find_info(head.parent, no)        

            elif head.parent == bs:
                self.log.write('Writing paragraphs \n')
                paragraph = head.next_element.find_all('p')
                if paragraph:
                    self.log.write('Slide is added')
                    self.add_slide(head.text, paragraph[0].get_text)
            else:
                paragraph = head.parent.find_all('p')
                self.log.write('Paragraph is added')
                if paragraph:
                    self.add_slide(head.text, paragraph[0].get_text())        
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

       

