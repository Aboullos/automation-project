from selenium.webdriver.common.keys import Keys
from main.automation.model.testing.objects.PageObject import PageObject
from main.automation.model.webdriver.DriverHelper import DriverHelper


class LoginPage(PageObject):

    __username_input = "#username"
    __password_input = "#password"
    __login_btn = "#kc-login"

    def log_in(self, username, password):
        self.debug_begin()

        self._web_driver.append_text(self.__username_input, username)
        self._web_driver.append_text(self.__password_input, password)

        self._web_driver.click(self.__login_btn)

        self.debug_end()

        return self
