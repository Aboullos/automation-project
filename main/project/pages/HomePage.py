from selenium.webdriver.common.keys import Keys
from main.automation.model.testing.objects.PageObject import PageObject
from main.automation.model.webdriver.DriverHelper import DriverHelper


class HomePage(PageObject):

    __search_input = "input[title]"

    def search_text(self, text):
        self.debug_begin()
        self._web_driver.append_text(self.__search_input, text + Keys.ENTER)
        self.debug_end()

        return self
