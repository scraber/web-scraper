from zipfile import ZipFile
from io import BytesIO

def fix_url_http(url: str) -> str:
    if not url.startswith("http"):
        return "http://" + url
    return url


def get_resource_full_url(base_url: str, resource_url: str) -> str:
    if resource_url.startswith("http"):
        return resource_url
    if resource_url.startswith("/") and base_url.endswith("/"):
        return base_url + resource_url[1:]
    return base_url + resource_url

def archive_bytes_stream(bytes_data):
    buffer = BytesIO()

    with ZipFile(buffer, 'w') as zip_file:
        for count, data in enumerate(bytes_data):
            zip_file.writestr(count, data)

    return buffer.getvalue()
