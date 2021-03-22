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
