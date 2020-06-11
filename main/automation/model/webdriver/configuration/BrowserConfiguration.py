import socket
from abc import ABC, abstractmethod
from selenium.webdriver.common.proxy import Proxy, ProxyType


class BrowserConfiguration(ABC):
    _language = None
    _use_proxy = False
    _headless = False
    _selenium_proxy = None

    def __init__(self):
        pass

    @abstractmethod
    def create_options(self):
        pass

    def set_language(self, language):
        self._language = language

    def set_headless(self, headless):
        self._headless = headless

    def set_use_proxy(self, user_proxy):
        self._use_proxy = user_proxy

    def create_proxy(self):
        pass

    def debug_begin(self):
        pass

    def debug_end(self):
        pass

    def debug_info(self):
        pass
