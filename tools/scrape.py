from typing import List

import requests
from bs4 import BeautifulSoup

from tools.utils import fix_url_http, get_resource_full_url


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


def get_all_text_data(url: str):
    url = fix_url_http(url)

    page_content = _get_page_text(url)

    soup = BeautifulSoup(page_content, "lxml")

    all_text_data = [line.strip() for line in soup.get_text().splitlines()]

    text_data = ''.join(entry for entry in list(filter(None,all_text_data)))

    return text_data

def get_all_images_data(url: str) -> List:
    url = fix_url_http(url)

    page_content = _get_page_bytes(url)

    soup = BeautifulSoup(page_content, "lxml")

    image_urls = [
        get_resource_full_url(url, image.get("src")) for image in soup.find_all("img")
    ]

    image_data = [_get_page_bytes(entry) for entry in image_urls]

    return image_data
