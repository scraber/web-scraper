from io import BytesIO
from zipfile import ZipFile


def fix_url_http(url: str) -> str:
    """
    Checks given URL.
    Adds http prefix if it's missing one,
    If URL starts with 'www.' removes it and adds http prefix


    Args:
        url (str):URL to fix

    Returns:
        str: Fixed URL starting with 'http' prefix
    """
    if url.startswith("www."):
        return "http://" + url[4:]
    elif not url.startswith("http"):
        return "http://" + url
    return url


def get_resource_full_url(base_url: str, resource_url: str) -> str:
    """
    Auxiliary function.
    Some pages have relative URL.
    This method checks and returns full path for resource

    Args:
        base_url (str): URL of resource's host
        resource_url (str): URL of resource
    Returns:
        str: Full resource path
    """
    if resource_url.startswith("http"):
        return resource_url
    elif resource_url.startswith("/") and base_url.endswith("/"):
        return base_url + resource_url[1:]
    elif not resource_url.startswith("/") and not base_url.endswith("/"):
        return base_url + "/" + resource_url
    return base_url + resource_url


def archive_bytes_stream(bytes_data):
    """
    Auxiliary function, archives given bytes data into single file

    Args:
        bytes_data (List): List of Bytes Data

    Returns:
        bytes: Compressed zip bytes data
    """

    buffer = BytesIO()

    with ZipFile(buffer, "w") as zip_file:
        for count, data in enumerate(bytes_data):
            zip_file.writestr(count, data)

    return buffer.getvalue()
