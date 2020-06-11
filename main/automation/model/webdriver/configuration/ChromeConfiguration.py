import os

from main.automation.model.webdriver.configuration.BrowserConfiguration import BrowserConfiguration

from selenium.webdriver import ChromeOptions

from webdriver_manager.chrome import ChromeDriverManager


class ChromeConfiguration(BrowserConfiguration):
    __plugin_files = []

    def __init__(self):
        super().__init__()

    def set_plugin_file(self, plugin_file: list):
        self.__plugin_files = plugin_file

    @staticmethod
    def download_driver():
        return ChromeDriverManager().install()

    def create_options(self):
        super().debug_begin()

        options = ChromeOptions()

        for file_name in self.__plugin_files:
            if '\\.' not in file_name:
                file_name += '.crx'
            options.add_extension(os.getcwd() + '/' + file_name)

        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--enable-strict-powerful-feature-restrictions")
        options.add_argument("--disable-geolocation")

        if super()._language is not None:
            options.add_argument("--lang=" + super()._language)

        if super()._headless:
            options.add_argument("-headless")
            options.add_argument("--disable-gpu")

        if super()._use_proxy:
            # options.add_argument('--ignore-certificate-errors')
            pass

        super().debug_end()

        return options
