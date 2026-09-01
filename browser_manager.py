from playwright.sync_api import sync_playwright
from cloakbrowser.download import ensure_binary
from cloakbrowser.config import get_default_stealth_args

class BrowserManager:
    def __init__(self, headless=True, proxy=None):
        self.headless = headless
        self.proxy = proxy

    def init(self):
        binary_path = ensure_binary()
        stealth_args = get_default_stealth_args()
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(
            executable_path=binary_path,
            headless=self.headless,
            args=stealth_args,
            proxy=self.proxy
        )
        return browser, playwright