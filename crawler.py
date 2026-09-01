import os
from urllib.parse import urljoin
from config import (
    HEADLESS, PROXY, FOLDER, TIMEOUT, WAIT_AFTER_LOAD,
    FILTER_INTERNAL_ONLY, SAVE_REMOVED_LINKS, ALLOW_SUBDOMAINS
)
from file_utils import ask_cleanup, build_filename, read_urls, open_folder
from browser_utils import init_browser
from link_utils import filter_links

def classify_by_type(links):
    absolute = []
    relative = []
    for link in links:
        if link.startswith(('http://', 'https://')):
            absolute.append(link)
        else:
            relative.append(link)
    return absolute, relative

def resolve_relative_links(links, base_url):
    resolved = []
    for link in links:
        if link.startswith(('http://', 'https://')):
            resolved.append(link)
        else:
            absolute = urljoin(base_url, link)
            resolved.append(f"{absolute} (ОТНОСИТЕЛЬНАЯ ССЫЛКА)")
    return resolved

def crawl():
    # Запрашиваем очистку только для основной папки
    ask_cleanup(FOLDER)

    urls = read_urls()
    if urls is None or not urls:
        print("❌ Нет URL для обработки.")
        return

    browser, playwright = init_browser(HEADLESS, PROXY)
    context = browser.new_context()
    page = context.new_page()

    total = len(urls)
    for idx, url in enumerate(urls, 1):
        print(f"🔄 {idx}/{total}: {url}")

        filename = build_filename(url)
        full_path = os.path.join(FOLDER, filename)
        removed_filename = filename.replace('.txt', '_removed.txt')
        removed_full_path = os.path.join(FOLDER, removed_filename)

        try:
            page.goto(url, wait_until='domcontentloaded', timeout=TIMEOUT)
            page.wait_for_timeout(WAIT_AFTER_LOAD)

            elements = page.query_selector_all('a[href]')
            raw_links = [el.get_attribute('href') for el in elements if el.get_attribute('href')]

            valid_links, removed_links = filter_links(
                raw_links,
                base_url=url,
                internal_only=FILTER_INTERNAL_ONLY,
                allow_subdomains=ALLOW_SUBDOMAINS
            )

            absolute_links, relative_links = classify_by_type(valid_links)
            resolved_valid = resolve_relative_links(valid_links, url)

            with open(full_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(resolved_valid))

            if SAVE_REMOVED_LINKS:
                with open(removed_full_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(removed_links))
                print(f"   ✅ Валидных: {len(valid_links)} (абс: {len(absolute_links)}, отн: {len(relative_links)}), удалённых: {len(removed_links)}")
            else:
                print(f"   ✅ Валидных: {len(valid_links)} (абс: {len(absolute_links)}, отн: {len(relative_links)})")

        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(f"Ошибка: {e}")

    browser.close()
    playwright.stop()

    print(f"\n🎉 Готово! Все файлы сохранены в папке '{FOLDER}'.")
    open_folder(FOLDER)

if __name__ == '__main__':
    crawl()