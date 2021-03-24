from app import celery
from models.image import PageImage
from models.text import PageText
from tools.scrape import get_all_text_data, get_all_images_data
import logging


@celery.task(name='celery_scrape_text')
def scrape_text(url:str):
    text = get_all_text_data(url)
    page = PageText(url=url, text=text)
    page.save_to_db()

@celery.task(name='celery_scrape_images')
def scrape_images(url:str):
    images_list = get_all_images_data(url)
    for image in images_list:
        page = PageImage(url=url, image=image)
        page.save_to_db()

