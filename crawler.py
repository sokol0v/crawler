import os
import argparse
from config import (
    HEADLESS, PROXY, TIMEOUT, WAIT_AFTER_LOAD,
    FILTER_INTERNAL_ONLY, SAVE_REMOVED_LINKS, ALLOW_SUBDOMAINS,
    URLS_FILE, FOLDER
)
from file_utils import ask_cleanup, build_filename, read_urls, open_folder
from browser_utils import init_browser
from link_utils import filter_links

def parse_args():
    parser = argparse.ArgumentParser(description="Краулер ссылок с обходом антибот-защиты.")
    parser.add_argument('--input', '-i', default=URLS_FILE,
                        help=f'Путь к файлу с URL-адресами (по умолчанию: {URLS_FILE})')
    parser.add_argument('--output', '-o', default=FOLDER,
                        help=f'Папка для сохранения результатов (по умолчанию: {FOLDER})')
    return parser.parse_args()

def crawl(input_file, output_folder):
    ask_cleanup(output_folder)

    urls = read_urls(input_file)
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
        full_path = os.path.join(output_folder, filename)
        removed_filename = filename.replace('.txt', '_removed.txt')
        removed_full_path = os.path.join(output_folder, removed_filename)

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

            with open(full_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(valid_links))

            if SAVE_REMOVED_LINKS:
                with open(removed_full_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(removed_links))
                print(f"   ✅ Валидных: {len(valid_links)}, удалённых: {len(removed_links)}")
            else:
                print(f"   ✅ Валидных: {len(valid_links)}")

        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(f"Ошибка: {e}")

    browser.close()
    playwright.stop()

    print(f"\n🎉 Готово! Все файлы сохранены в папке '{output_folder}'.")
    open_folder(output_folder)

if __name__ == '__main__':
    args = parse_args()
    crawl(args.input, args.output)