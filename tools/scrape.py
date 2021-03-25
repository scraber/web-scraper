from typing import List

import requests
from bs4 import BeautifulSoup

from tools.utils import fix_url_http, get_resource_full_url


def _get_page_text(url: str) -> str:
    """
    Sends GET request for given URL and returns text
    If response code was not 20xx, throws HTTP error

    Args:
        url (str): URL of webpage

    Returns:
        str: Non-formatted site text
    """
    response = requests.get(url)
    # throw an exception if status was unsuccessful
    response.raise_for_status()

    return response.text


def _get_page_bytes(url: str) -> bytes:
    """
    Sends GET request for given URL and returns byte content
    If response code was not 20xx, throws HTTP error

    Args:
        url (str): URL of webpage

    Returns:
        str: Non-formatted site byte content
    """
    response = requests.get(url)
    # throw an exception if status was unsuccessful
    response.raise_for_status()

    return response.content


def get_all_text_data(url: str) -> str:
    """
    Using bs4 this function gathers all available text
    removing all unnecessary tags

    Args:
        url (str): URL of webpage

    Returns:
        str: text from webpage
    """
    url = fix_url_http(url)

    page_content = _get_page_text(url)

    soup = BeautifulSoup(page_content, "lxml")

    all_text_data = [line.strip() for line in soup.get_text().splitlines()]

    text_data = "".join(entry for entry in list(filter(None, all_text_data)))

    return text_data


def get_all_images_data(url: str) -> List:
    """
    Using bs4 this function gathers urls for all available images
    and gets theirs byte data

    Args:
        url (str): URL of webpage

    Returns:
        List: of tuples (img_url, images bytes data)
    """
    url = fix_url_http(url)

    page_content = _get_page_bytes(url)

    soup = BeautifulSoup(page_content, "lxml")

    image_urls = [
        get_resource_full_url(url, image.get("src", image.get("data-src")))
        for image in soup.find_all("img")
    ]

    image_data = [(entry, _get_page_bytes(entry)) for entry in image_urls]

    return image_data
