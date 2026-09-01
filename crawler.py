import os
from config import (
    HEADLESS, PROXY, FOLDER, TIMEOUT, WAIT_AFTER_LOAD,
    FILTER_INTERNAL_ONLY, SAVE_REMOVED_LINKS, ALLOW_SUBDOMAINS
)
from file_manager import FileManager
from link_processor import LinkProcessor
from browser_manager import BrowserManager

class Crawler:
    def __init__(self):
        self.fm = FileManager(FOLDER)
        self.processor = LinkProcessor()
        self.browser_manager = BrowserManager(HEADLESS, PROXY)

    def _process_page(self, url, page):
        try:
            page.goto(url, wait_until='domcontentloaded', timeout=TIMEOUT)
            page.wait_for_timeout(WAIT_AFTER_LOAD)

            raw_links = [el.get_attribute('href') for el in page.query_selector_all('a[href]') if el.get_attribute('href')]

            valid_links, removed_links = self.processor.filter_links(
                raw_links,
                base_url=url,
                internal_only=FILTER_INTERNAL_ONLY,
                allow_subdomains=ALLOW_SUBDOMAINS
            )

            absolute_links, relative_links = self.processor.classify_links(valid_links)
            resolved_valid = self.processor.resolve_relative_links(valid_links, url)

            self.fm.save_valid_links(url, resolved_valid)
            if SAVE_REMOVED_LINKS:
                self.fm.save_removed_links(url, removed_links)

            return {
                'valid': len(valid_links),
                'absolute': len(absolute_links),
                'relative': len(relative_links),
                'removed': len(removed_links) if SAVE_REMOVED_LINKS else 0
            }

        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
            filename = self.fm.build_filename(url)
            full_path = os.path.join(FOLDER, filename)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(f"Ошибка: {e}")
            return None

    def run(self):
        self.fm.ask_cleanup()
        urls = self.fm.read_urls()
        if not urls:
            print("❌ Нет URL для обработки.")
            return

        browser, playwright = self.browser_manager.init()
        context = browser.new_context()
        page = context.new_page()

        total = len(urls)
        for idx, url in enumerate(urls, 1):
            print(f"🔄 {idx}/{total}: {url}")
            stats = self._process_page(url, page)
            if stats:
                if SAVE_REMOVED_LINKS:
                    print(f"   ✅ Валидных: {stats['valid']} (абс: {stats['absolute']}, отн: {stats['relative']}), удалённых: {stats['removed']}")
                else:
                    print(f"   ✅ Валидных: {stats['valid']} (абс: {stats['absolute']}, отн: {stats['relative']})")

        browser.close()
        playwright.stop()

        print(f"\n🎉 Готово! Все файлы сохранены в папке '{FOLDER}'.")
        self.fm.open_folder()

if __name__ == '__main__':
    crawler = Crawler()
    crawler.run()