# Режим без окон
HEADLESS = False

# Прокси (если нужен) – строка вида "http://user:pass@ip:port"
PROXY = None

# Папка для сохранения результатов
FOLDER = "href_urls"

# Таймаут загрузки страницы (мс)
TIMEOUT = 60000

# Задержка после загрузки для рендеринга (мс)
WAIT_AFTER_LOAD = 3000

# Фильтровать только внутренние ссылки (одного домена)
FILTER_INTERNAL_ONLY = True

# Разрешать поддомены как внутренние (например, app.scb.ru)
ALLOW_SUBDOMAINS = True

# Сохранять отдельный файл с удалёнными ссылками (суффикс _removed)
SAVE_REMOVED_LINKS = True