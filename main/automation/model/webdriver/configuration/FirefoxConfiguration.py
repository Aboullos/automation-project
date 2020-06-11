import os

from selenium.webdriver import FirefoxOptions
from selenium.webdriver import FirefoxProfile

from webdriver_manager.firefox import GeckoDriverManager

from main.automation.model.webdriver.configuration.BrowserConfiguration import BrowserConfiguration


class FirefoxConfiguration(BrowserConfiguration):
    __plugin_files = []

    def __init__(self):
        super().__init__()

    def set_plugin_file(self, plugin_file):
        self.__plugin_files = plugin_file

    @staticmethod
    def download_driver():
        return GeckoDriverManager().install()

    def create_options(self):
        super().debug_begin()

        options = FirefoxOptions()

        options.add_argument("--start-maximized")

        if super()._language is not None:
            options.add_argument("--lang=" + super()._language)

        if super()._headless:
            options.add_argument("-headless")
            options.add_argument("--disable-gpu")

        profile = FirefoxProfile()
        profile.accept_untrusted_certs = True

        for file_name in self.__plugin_files:
            if '\\.' not in file_name:
                file_name += '.xpi'
            profile.add_extension(os.getcwd() + '/' + file_name)

        options.profile = profile

        if super()._use_proxy:
            # options.add_argument('--ignore-certificate-errors')
            pass

        super().debug_end()

        return options
