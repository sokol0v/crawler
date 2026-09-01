# config.py
HEADLESS = False
PROXY = None                # "http://user:pass@ip:port" или None
TIMEOUT = 60000             # таймаут загрузки страницы (мс)
WAIT_AFTER_LOAD = 3000      # задержка для рендеринга (мс)
FILTER_INTERNAL_ONLY = True # Фильтровать ли только внутренние ссылки (одного домена)
SAVE_REMOVED_LINKS = True   # Сохранять ли отдельный файл с удалёнными ссылками
ALLOW_SUBDOMAINS = True     # Разрешать ли поддомены как внутренние (например, app.scb.ru)
URLS_FILE = "urls.txt"      # Путь к файлу со списком URL (по умолчанию)
FOLDER = "href_urls"        # Папка для сохранения результатов (по умолчанию)