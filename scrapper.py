import requests
from bs4 import BeautifulSoup
from utils import fix_url_http, fix_url_base_relative


def _get_page_text(url: str) -> str:
    response = requests.get(url)
    # throw an exception if status was unsuccessful
    response.raise_for_status()

    return response.text


def _get_page_bytes(url: str) -> bytes:
    response = requests.get(url)
    # throw an exception if status was unsuccessful
    response.raise_for_status()

    return response.content


def get_all_images_data(url: str):
    url = fix_url_http(url)

    page_content = _get_page_bytes(url)

    soup = BeautifulSoup(page_content, "lxml")

    image_urls = [fix_url_base_relative(url, image.get("src")) for image in soup.find_all("img")]

    image_data = [_get_page_bytes(entry) for entry in image_urls]

    return image_data
