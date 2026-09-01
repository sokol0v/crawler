import os
import re
import sys
import subprocess
import webbrowser
from urllib.parse import urlparse

class FileManager:
    def __init__(self, folder):
        self.folder = folder

    def build_filename(self, url):
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        if not path:
            return "index.txt"
        safe_name = re.sub(r'[\\/*?:"<>|]', '_', path)
        safe_name = re.sub(r'_+', '_', safe_name)
        return safe_name + ".txt"

    def clean_folder(self):
        if os.path.exists(self.folder):
            for item in os.listdir(self.folder):
                item_path = os.path.join(self.folder, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
            print(f"🧹 Папка '{self.folder}' очищена.")
        else:
            os.makedirs(self.folder, exist_ok=True)
            print(f"📁 Папка '{self.folder}' создана.")

    def ask_cleanup(self):
        if os.path.exists(self.folder):
            files = [f for f in os.listdir(self.folder) if os.path.isfile(os.path.join(self.folder, f))]
            if files:
                print(f"⚠️ В папке '{self.folder}' есть {len(files)} старых файлов.")
                answer = input("Очистить папку перед запуском? (y/n): ").strip().lower()
                if answer != 'y':
                    print("❌ Очистка отменена. Выход.")
                    sys.exit(0)
                self.clean_folder()
        else:
            os.makedirs(self.folder, exist_ok=True)
            print(f"📁 Папка '{self.folder}' создана.")

    def read_urls(self, filepath="urls.txt"):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"❌ Файл {filepath} не найден.")
            return None

    def save_valid_links(self, url, links):
        filename = self.build_filename(url)
        full_path = os.path.join(self.folder, filename)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(links))
        return full_path

    def save_removed_links(self, url, links):
        filename = self.build_filename(url)
        removed_filename = filename.replace('.txt', '_removed.txt')
        full_path = os.path.join(self.folder, removed_filename)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(links))
        return full_path

    def save_html_report(self, html_content, filename="report.html"):
        full_path = os.path.join(self.folder, filename)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"📄 HTML-отчёт сохранён: {full_path}")
        return full_path

    def open_html_report(self, filename="report.html"):
        path = os.path.join(self.folder, filename)
        if os.path.exists(path):
            webbrowser.open(path)
            print(f"🌐 HTML-отчёт открыт в браузере: {path}")
        else:
            print(f"⚠️ Файл отчёта не найден: {path}")

    def open_folder(self):
        if not os.path.exists(self.folder):
            print(f"⚠️ Папка '{self.folder}' не существует.")
            return
        try:
            if sys.platform == 'win32':
                subprocess.Popen(['explorer', '/n,', os.path.abspath(self.folder)])
            elif sys.platform == 'darwin':
                subprocess.run(['open', '-a', 'Finder', self.folder])
            else:
                subprocess.Popen(['xdg-open', self.folder])
            print(f"📂 Папка '{self.folder}' открыта.")
        except Exception as e:
            print(f"⚠️ Не удалось открыть папку: {e}")