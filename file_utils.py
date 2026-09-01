import os
import re
import sys
import subprocess
from urllib.parse import urlparse

def build_filename(url):
    parsed = urlparse(url)
    path = parsed.path.strip('/')
    if not path:
        return "index.txt"
    safe_name = re.sub(r'[\\/*?:"<>|]', '_', path)
    safe_name = re.sub(r'_+', '_', safe_name)
    return safe_name + ".txt"

def clean_folder(folder):
    if os.path.exists(folder):
        for item in os.listdir(folder):
            item_path = os.path.join(folder, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
        print(f"🧹 Папка '{folder}' очищена (все файлы удалены).")
    else:
        os.makedirs(folder, exist_ok=True)
        print(f"📁 Папка '{folder}' создана.")

def ask_cleanup(folder):
    """
    Проверяет наличие файлов в папке. Если есть – запрашивает подтверждение очистки.
    Если пользователь не вводит 'y' – завершает программу.
    """
    if os.path.exists(folder):
        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        if files:
            print(f"⚠️ В папке '{folder}' есть {len(files)} старых файлов.")
            answer = input("Очистить папку перед запуском? (y/n): ").strip().lower()
            if answer != 'y':
                print("❌ Очистка отменена. Выход.")
                sys.exit(0)
            else:
                clean_folder(folder)
        else:
            # Папка существует, но пуста – ничего не делаем
            pass
    else:
        # Папки нет – создаём
        os.makedirs(folder, exist_ok=True)
        print(f"📁 Папка '{folder}' создана.")

def read_urls(filepath="urls.txt"):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ Файл {filepath} не найден.")
        return None

def open_folder(folder):
    if not os.path.exists(folder):
        print(f"⚠️ Папка '{folder}' не существует.")
        return
    try:
        if sys.platform == 'win32':
            subprocess.Popen(['explorer', '/n,', os.path.abspath(folder)])
        elif sys.platform == 'darwin':
            subprocess.run(['open', '-a', 'Finder', folder])
        else:
            subprocess.Popen(['xdg-open', folder])
        print(f"📂 Папка '{folder}' открыта (окно активировано).")
    except Exception as e:
        print(f"⚠️ Не удалось открыть папку: {e}")