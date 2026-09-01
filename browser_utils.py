# browser_utils.py
from playwright.sync_api import sync_playwright
from cloakbrowser.download import ensure_binary
from cloakbrowser.config import get_default_stealth_args

def init_browser(headless, proxy=None):
    """
    Запускает защищённый браузер CloakBrowser.
    Возвращает объект browser, который нужно закрыть после работы.
    """
    binary_path = ensure_binary()
    stealth_args = get_default_stealth_args()

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(
        executable_path=binary_path,
        headless=headless,
        args=stealth_args,
        proxy=proxy
    )
    return browser, playwright