import os
import re
import sys
import subprocess
from urllib.parse import urlparse

def build_filename(url):
    """
    Формирует имя файла из пути URL (без домена).
    Все слеши заменяются на подчёркивания.
    Пример: /apply/credit/kredit-nalichnymi/ -> apply_credit_kredit-nalichnymi.txt
    """
    parsed = urlparse(url)
    path = parsed.path.strip('/')
    if not path:
        return "index.txt"
    # Заменяем недопустимые символы на подчёркивания
    safe_name = re.sub(r'[\\/*?:"<>|]', '_', path)
    # Убираем множественные подчёркивания
    safe_name = re.sub(r'_+', '_', safe_name)
    return safe_name + ".txt"

def clean_folder(folder):
    """Удаляет все файлы внутри папки, но саму папку оставляет."""
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
    """Спрашивает, нужно ли очистить папку, если в ней есть файлы."""
    if os.path.exists(folder):
        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        if files:
            answer = input(f"⚠️ В папке '{folder}' есть {len(files)} старых файлов. Очистить перед запуском? (y/n): ").strip().lower()
            if answer == 'y':
                clean_folder(folder)
                return True
            else:
                print("💾 Старые файлы сохранены. Новые будут добавлены.")
                return False
        else:
            return True
    else:
        os.makedirs(folder, exist_ok=True)
        print(f"📁 Папка '{folder}' создана.")
        return True

def read_urls(filepath="urls.txt"):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ Файл {filepath} не найден.")
        return None

def open_folder(folder):
    """Открывает папку в файловом менеджере и активирует окно."""
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