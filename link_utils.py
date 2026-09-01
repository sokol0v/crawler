from urllib.parse import urlparse

def is_valid_http_link(link):
    if not link:
        return False
    return link.startswith(('http://', 'https://'))

def is_internal_link(link, base_url, allow_subdomains=True):
    """
    Проверяет, принадлежит ли ссылка тому же домену, что и base_url.
    Если allow_subdomains=True, то поддомены тоже считаются внутренними.
    """
    if not link:
        return False
    # Относительные ссылки всегда внутренние
    if not link.startswith(('http://', 'https://')):
        return True

    parsed_link = urlparse(link)
    parsed_base = urlparse(base_url)
    link_domain = parsed_link.netloc.lower()
    base_domain = parsed_base.netloc.lower()

    if allow_subdomains:
        # Проверяем, что link_domain заканчивается на base_domain или равен ему
        return link_domain == base_domain or link_domain.endswith('.' + base_domain)
    else:
        return link_domain == base_domain

def filter_links(raw_links, base_url, internal_only=True, allow_subdomains=True):
    valid = []
    removed = []
    seen_valid = set()
    seen_removed = set()

    for link in raw_links:
        if not link:
            continue

        if not is_valid_http_link(link):
            if link not in seen_removed:
                removed.append(link)
                seen_removed.add(link)
            continue

        if internal_only and not is_internal_link(link, base_url, allow_subdomains):
            if link not in seen_removed:
                removed.append(link)
                seen_removed.add(link)
            continue

        if link not in seen_valid:
            valid.append(link)
            seen_valid.add(link)

    return valid, removed