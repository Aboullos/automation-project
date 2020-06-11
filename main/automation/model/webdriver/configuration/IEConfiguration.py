import os

from main.automation.model.webdriver.configuration.BrowserConfiguration import BrowserConfiguration
from webdriver_manager.microsoft import IEDriverManager
from selenium.webdriver import IeOptions
from selenium.webdriver import DesiredCapabilities


class IEConfiguration(BrowserConfiguration):

    def __init__(self):
        super().__init__()

    @staticmethod
    def download_driver():
        return IEDriverManager().install()

    def create_options(self):
        options = IeOptions()

        options.add_argument("--disable-popup-blocking")
        options.add_argument("--start-fullscreen")

        if super()._use_proxy:
            pass

        return options

