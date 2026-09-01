from urllib.parse import urlparse

class LinkProcessor:
    @staticmethod
    def is_web_link(link):
        if not link:
            return False
        excluded = ('tel:', 'mailto:', 'javascript:', '#')
        if link.startswith(excluded):
            return False
        return True

    @staticmethod
    def is_internal_link(link, base_url, allow_subdomains=True):
        if not link:
            return False
        if not link.startswith(('http://', 'https://')):
            return True
        parsed_link = urlparse(link)
        parsed_base = urlparse(base_url)
        link_domain = parsed_link.netloc.lower()
        base_domain = parsed_base.netloc.lower()
        if allow_subdomains:
            return link_domain == base_domain or link_domain.endswith('.' + base_domain)
        else:
            return link_domain == base_domain

    @staticmethod
    def filter_links(raw_links, base_url, internal_only=True, allow_subdomains=True):
        valid = []
        removed = []
        seen_valid = set()
        seen_removed = set()

        for link in raw_links:
            if not link:
                continue
            if not LinkProcessor.is_web_link(link):
                if link not in seen_removed:
                    removed.append(link)
                    seen_removed.add(link)
                continue
            if internal_only and not LinkProcessor.is_internal_link(link, base_url, allow_subdomains):
                if link not in seen_removed:
                    removed.append(link)
                    seen_removed.add(link)
                continue
            if link not in seen_valid:
                valid.append(link)
                seen_valid.add(link)

        return valid, removed

    @staticmethod
    def classify_links(links):
        absolute = []
        relative = []
        for link in links:
            if link.startswith(('http://', 'https://')):
                absolute.append(link)
            else:
                relative.append(link)
        return absolute, relative