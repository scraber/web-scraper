from app import celery
from models.image import PageImage, Image
from models.text import PageText
from tools.scrape import get_all_images_data, get_all_text_data


@celery.task(name="celery_scrape_text")
def scrape_text(url: str):
    """
    Scrape webpage for text and create PageText object

    Args:
        url (str): URL of page to be scrapped
    """
    text = get_all_text_data(url)
    page = PageText(url=url, text=text)
    page.save_to_db()


@celery.task(name="celery_scrape_images")
def scrape_images(url: str):
    """
    Scrape webpage for images and create multiple PageImage objects

    Args:
        url (str): URL of page to be scrapped
    """
    images_tuple = get_all_images_data(url)
    page = PageImage(url=url)
    page.save_to_db()
    for image_url, img_data in images_tuple:
        img = Image(img_url=image_url, page_id=page.id, data=img_data)
        img.save_to_db()
