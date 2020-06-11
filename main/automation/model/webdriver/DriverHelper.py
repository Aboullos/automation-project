import time
import os
import platform
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.driver import ChromeDriver
from webdriver_manager.driver import GeckoDriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from main.automation.configuration import AutomationConstants
from main.automation.data.DataObject import DataObject
from main.automation.model.utils.InitUtils import InitUtils
from main.automation.model.utils.objects.DebugLogger import DebugLogger
from main.automation.model.webdriver.configuration import BrowserType
from main.automation.model.webdriver.configuration.ChromeConfiguration import ChromeConfiguration
from main.automation.model.webdriver.configuration.FirefoxConfiguration import FirefoxConfiguration
from main.automation.model.webdriver.configuration.IEConfiguration import IEConfiguration


class DriverHelper:

    def __init__(self, browser, config_data=DataObject()):
        self.__browser = browser
        self.__id = '0'
        self.__report_path = None
        self.__ip = "localhost"
        self.__port = "4444"
        self.__browser_type = None
        self.__emulation_browser = None
        self.__driver_type = "WEB"
        self.__device_name = None
        self.__device_platform = None
        self.__remote = False
        self.__desktop = True
        self.__driver: webdriver.Remote = None
        self.__driver_path = None
        self.__maximize = True
        self.__wait_for_page = True
        self.__wait_for_angular = True
        self.__wait_for_jquery = False
        self.__short_wait = 3
        self.__implicit_timeout = 50
        self.__script_timeout = 50
        self.__page_load_timeout = 50
        self.__small_window_limit = 1025
        self.__default_window_height = 768
        self.__default_window_width = 1366
        self.__download_drivers = True
        self.__plugin_files = []
        self.__headless = False
        self.__language = None
        self.__use_proxy = False
        self.__driver_type = AutomationConstants.WEB
        self.__config_data = config_data
        self.__logger: DebugLogger = DebugLogger()

        self.__initialize_base_variables(browser)

    # region Driver methods
    def set_maximize(self, value):
        self.__maximize = value

    def set_small_window_limit(self, limit):
        self.__small_window_limit = limit

    def set_window_size(self, height, width):
        self.__default_window_height = height
        self.__default_window_width = width

    def __set_window_variables(self):
        if self.__config_data.get_var(AutomationConstants.SMALL_WINDOW_LIMIT) is not None:
            self.set_small_window_limit(int(self.__config_data.get_var(AutomationConstants.SMALL_WINDOW_LIMIT)))

        self.set_maximize(InitUtils.set_bool_variable(AutomationConstants.MAXIMIZE_ON_START, self.__config_data))

        if (self.__config_data.get_var(AutomationConstants.WINDOW_HEIGHT) is not None
                and self.__config_data.get_var(AutomationConstants.WINDOW_WIDTH) is not None):
            self.set_window_size(self.__config_data.get_var(AutomationConstants.WINDOW_HEIGHT),
                                 self.__config_data.get_var(AutomationConstants.WINDOW_WIDTH))
        elif self.__config_data.get_var(AutomationConstants.WINDOW_HEIGHT)is not None:
            self.set_window_size(self.__default_window_width,
                                 self.__config_data.get_var(AutomationConstants.WINDOW_HEIGHT))
        elif self.__config_data.get_var(AutomationConstants.WINDOW_WIDTH)is not None:
            self.set_window_size(self.__config_data.get_var(AutomationConstants.WINDOW_WIDTH),
                                 self.__default_window_height)

    def __set_driver_waits(self):
        if (not self.__config_data.get_var(AutomationConstants.WAIT_FOR_PAGE)
                or (InitUtils.get_argument(AutomationConstants.WAIT_FOR_PAGE) is None
                    and InitUtils.get_argument(AutomationConstants.WAIT_FOR_PAGE is not ''))):
            self.set_wait_for_page(InitUtils.set_bool_variable(AutomationConstants.WAIT_FOR_PAGE, self.__config_data))

        self.set_wait_for_angular(InitUtils.set_bool_variable(AutomationConstants.WAIT_FOR_ANGULAR, self.__config_data))
        self.set_wait_for_angular(InitUtils.set_bool_variable(AutomationConstants.WAIT_FOR_JQUERY, self.__config_data))

        timeout = InitUtils.get_argument(AutomationConstants.TIMEOUT)

        if timeout is not None and timeout is not '':
            self.__config_data.set_value(AutomationConstants.TIMEOUT, timeout)

        if self.__config_data.get_var(AutomationConstants.TIMEOUT) is not None:
            self.set_implicit_wait(int(self.__config_data.get_var(AutomationConstants.TIMEOUT)))
            self.set_script_wait(int(self.__config_data.get_var(AutomationConstants.TIMEOUT)))
            self.set_page_load_wait(int(self.__config_data.get_var(AutomationConstants.TIMEOUT)))
        else:
            if self.__config_data.get_var(AutomationConstants.IMPLICIT_WAIT):
                self.set_implicit_wait(int(self.__config_data.get_var(AutomationConstants.IMPLICIT_WAIT)))

            if self.__config_data.get_var(AutomationConstants.SCRIPT_WAIT):
                self.set_script_wait(int(self.__config_data.get_var(AutomationConstants.SCRIPT_WAIT)))

            if self.__config_data.get_var(AutomationConstants.PAGE_LOAD_WAIT):
                self.set_page_load_wait(int(self.__config_data.get_var(AutomationConstants.PAGE_LOAD_WAIT)))

    def __set_config_data_variables(self):
        self.set_report_path(self.__config_data.get_var(AutomationConstants.REPORT_PATH))

        self.__set_driver_waits()

        self.set_language(InitUtils.set_str_variable(AutomationConstants.DRIVER_LANGUAGE, self.__config_data))

        self.set_download_drivers(InitUtils.set_bool_variable(AutomationConstants.DRIVER_DOWNLOAD, self.__config_data))

        aux_port = InitUtils.get_str_variable(AutomationConstants.PORT, self.__config_data)

        if (not aux_port and (self.__driver_type == AutomationConstants.MOBILE_APP
                              or self.__driver_type == AutomationConstants.MOBILE_WEB)):
            aux_port = InitUtils.set_str_variable(AutomationConstants.MOBILE_PORT, self.__config_data)
        elif not aux_port:
            aux_port = InitUtils.set_str_variable(AutomationConstants.PORT, self.__config_data)

        self.__config_data.set_value(AutomationConstants.PORT, aux_port)

        self.set_hub(InitUtils.set_str_variable(AutomationConstants.IP, self.__config_data), aux_port)
        self.set_remote(InitUtils.set_bool_variable(AutomationConstants.REMOTE_MODE, self.__config_data))

        self.__set_window_variables()

    def __initialize_base_variables(self, browser):
        self.__headless = browser.__contains__("_headless")

        if (browser.replace("_headless", "") in BrowserType.DEVICE_EMULATION_BROWSERS
                or browser.replace("_headless", "") in BrowserType.DESKTOP_BROWSERS):
            self.__browser_type = browser.replace("_headless", "")
            self.__driver_type = AutomationConstants.WEB

            if (self.__browser_type == BrowserType.SAFARI_IPHONE
                    or self.__browser_type == BrowserType.SAFARI_IPAD):
                self.__emulation_browser = BrowserType.SAFARI
        elif BrowserType.IPHONE == browser:
            self.__browser_type = browser
            self.__driver_type = AutomationConstants.MOBILE_APP
            self.__desktop = False
        else:
            self.__device_name = browser
            self.__driver_type = AutomationConstants.MOBILE_APP
            self.__desktop = False

        self.__set_config_data_variables()

    def initialize_driver(self):
        if not self.__remote:
            if self.__download_drivers:
                self.__driver.path = self.__download_driver()
            else:
                self.__set_property_driver_path()

            options = self.__create_browser_configuration()

            self.__driver = self.__create_local_web_driver(options)
        else:
            hub = "http://" + self.__ip + ":" + self.__port + "/wd/hub"

            if self.__browser == BrowserType.CHROME:
                self.__driver = webdriver.Remote(hub, webdriver.DesiredCapabilities.CHROME)
            elif self.__browser == BrowserType.FIREFOX:
                self.__driver = webdriver.Remote(hub, webdriver.DesiredCapabilities.FIREFOX)
            elif self.__browser == BrowserType.INTERNET_EXPLORER:
                self.__driver = webdriver.Remote(hub, webdriver.DesiredCapabilities.INTERNETEXPLORER)

        self.set_timeouts()

    def __download_driver(self):
        path = None

        if not self.__remote:
            if self.__browser == BrowserType.CHROME:
                path = ChromeConfiguration.download_driver()
            elif self.__browser == BrowserType.FIREFOX:
                path = FirefoxConfiguration.download_driver()
            elif self.__browser == BrowserType.INTERNET_EXPLORER:
                path = IEConfiguration.download_driver()
        else:
            # TODO
            pass

        return path

    def __set_property_driver_path(self):
        if platform.system().__contains__("Windows"):
            self.__driver_path = os.getenv('USERPROFILE') + '/.wdm/drivers/'
        else:
            self.__driver_path = os.getenv('HOME') + '/.wdm/drivers/'

        if self.__browser_type == BrowserType.CHROME:
            self.__driver_path += 'chromedriver/'
        elif self.__browser_type == BrowserType.FIREFOX:
            self.__driver_path += 'geckdriver/'

        self.__driver_path += os.listdir(self.__driver_path)[-1]

        self.__driver_path += "/" + ("win32/" if platform.system() == "Windows" else "linux64/")\
                              + "chromedriver" + (".exe" if platform.system() == "Windows" else "")

    def __create_browser_configuration(self):
        options = None

        if self.__browser == BrowserType.CHROME:
            options = ChromeConfiguration()
        elif self.__browser == BrowserType.FIREFOX:
            options = FirefoxConfiguration()
        elif self.__browser == BrowserType.INTERNET_EXPLORER:
            options = IEConfiguration()

        if self.__browser != BrowserType.INTERNET_EXPLORER:
            options.set_plugin_file(self.__plugin_files)

            options.set_headless(self.__headless)
            options.set_language(self.__language)

        return options

    def __create_local_web_driver(self, options):
        aux_driver = None

        if self.__browser == BrowserType.CHROME:
            aux_driver = webdriver.Chrome(
                executable_path=self.__driver_path,
                chrome_options=options.create_options())
            #aux_driver = webdriver.Chrome(ChromeDriverManager().install(),
            #                              chrome_options=options.create_options())
        elif self.__browser == BrowserType.FIREFOX:
            aux_driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),
                                           firefox_options=options.create_options())
        elif self.__browser == BrowserType.INTERNET_EXPLORER:
            aux_driver = webdriver.Ie(executable_path=os.getenv('USERPROFILE') + "/.wdm/drivers/IEDriverServer"
                                                                                 "/x64/IEDriverServer.exe",
                                      ie_options=options.create_options())

        return aux_driver

    # Getters
    def get_driver(self):
        return self.__driver

    def get_driver_type(self):
        return self.__driver_type

    def get_title(self):
        return self.__driver.title

    def get_url(self):
        return self.__driver.current_url

    def get_window_size(self):
        return self.__driver.get_window_size()

    def get_wait_for_angular(self):
        return self.__wait_for_angular

    def get_wait_for_jquery(self):
        return self.__wait_for_jquery

    def get_report_path(self):
        return self.__report_path

    def is_remote(self):
        return self.__remote

    # Setters
    def set_language(self, language):
        self.__language = language

    def set_id(self, id_):
        self.__id = id_

    def set_wait_for_angular(self, value):
        self.__wait_for_angular = value

    def set_wait_for_jquery(self, value):
        self.__wait_for_jquery = value

    def set_report_path(self, path):
        self.__report_path = path

    def set_download_drivers(self, value):
        self.__download_drivers = value

    def set_remote(self, value):
        self.__remote = value

    def set_hub(self, ip, port):
        self.__ip = ip
        self.__port = port

    def set_implicit_wait(self, wait_time):
        try:
            if self.__driver:
                self.__implicit_timeout = wait_time
                self.__driver.implicitly_wait(wait_time)
        except Exception as e:
            self.__logger.debug_error("Error setting implicit timeout")

    def set_script_wait(self, wait_time):
        try:
            if self.__driver:
                self.__script_timeout = wait_time
                self.__driver.set_script_timeout(wait_time)
        except Exception as e:
            self.__logger.debug_error("Error setting script timeout")

    def set_page_load_wait(self, wait_time):
        try:
            if self.__driver:
                self.__page_load_timeout = wait_time
                self.__driver.set_page_load_timeout(wait_time)
        except Exception as e:
            self.__logger.debug_error("Error setting page load timeout")

    def set_timeouts(self, wait_time=None):
        try:
            if self.__driver:
                self.__driver.implicitly_wait(wait_time if wait_time is not None else self.__implicit_timeout)
        except Exception as e:
            self.__logger.debug_error("Error setting implicit timeout")

        try:
            if self.__driver:
                self.__driver.set_script_timeout(wait_time if wait_time is not None else self.__script_timeout)
        except Exception as e:
            self.__logger.debug_error("Error setting script timeout")

        try:
            if self.__driver:
                self.__driver.set_page_load_timeout(wait_time if wait_time is not None else self.__page_load_timeout)
        except Exception as e:
            self.__logger.debug_error("Error setting page load timeout")

    def set_wait_for_page(self, value):
        self.__wait_for_page = value

    def __get_by(self, locator, by=None):
        if not by and not isinstance(locator, By):
            by = By.CSS_SELECTOR

            if len(locator) > 0 and ("/" == locator[0] or "*" == locator[0]):
                by = By.XPATH
        elif not by and isinstance(locator, By):
            by = locator

        return by
    # endregion

    # region Selenium methods
    # Getters
    def get_element(self, element, by=None):
        if not by:
            by = self.__get_by(element)

        return self.__driver.find_element(by, element)

    def get_elements(self, element, by=None):
        if not by:
            by = self.__get_by(element)

        return self.__driver.find_elements(by, element)

    def get_current_title(self):
        return self.__driver.title

    def get_current_url(self):
        return self.__driver.current_url

    def get_source(self):
        return self.__driver.page_source

    def get_attribute(self, element, attribute):
        return self.get_element(element).get_attribute(attribute)

    def get_element_location(self, element, by=None):
        return self.get_element(element, by).location

    def get_element_size(self, element, by=None):
        return self.get_element(element, by).size

    # Setters
    def set_attribute(self, element, attribute, value):
        self.__driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2])",
                                     self.get_element(element), attribute, value)

    def remove_attribute(self, element, attribute):
        self.__driver.execute_script("arguments[0].removeAttribute(arguments[1])",
                                     self.get_element(element), attribute)

    def remove_element(self, element):
        self.__driver.execute_script("arguments[0].remove()",
                                     self.get_element(element))

    def set_window_position(self, x, y):
        return self.__driver.set_window_position(x, y)

    def maximize_window(self):
        return self.__driver.maximize_window()

    def resize_window(self, width, height):
        return self.__driver.set_window_size(width, height)

    def execute_javascript(self, script, *args):
        return self.__driver.execute_script(script, *args)

    def execute_async_javascript(self, script, *args):
        return self.__driver.execute_async_script(script, *args)

    def go(self, url):
        if self.__driver is None:
            self.initialize_driver()

        self.__driver.get(url)
        self.wait_for_load_to_complete()

    def refresh(self):
        self.__driver.refresh()
        self.wait_for_load_to_complete()

    def forward(self):
        self.__driver.forward()
        self.wait_for_load_to_complete()

    def back(self):
        self.__driver.back()
        self.wait_for_load_to_complete()

    def quit(self):
        try:
            self.__driver.close()
            self.__driver.quit()
            self.__driver = None
        except:
            pass

    # Click methods
    def click(self, element, by=None):
        self.wait_for_element_to_be_clickable(element, by).click()
        self.wait_for_load_to_complete()

    def click_in_frame(self, element, frame, by_element=None, by_frame=None):
        self.switch_to_frame(frame, by_frame)
        self.click(element, by_element)
        self.exit_frame()

    def click_over(self, element, by=None):
        self.__driver.execute_script("document.elementFromPoint("
                                     "arguments[0].getBoundingClientRect().x, "
                                     "arguments[0].getBoundingClientRect().y).click()",
                                     self.get_element(element, by))
        self.wait_for_load_to_complete()

    def click_over_in_frame(self, element, frame, by_element=None, by_frame=None):
        self.switch_to_frame(frame, by_frame)
        self.click_over(element, by_element)
        self.exit_frame()

    # Text methods
    def get_text(self, element, by=None):
        return self.get_element(element, by).text

    def get_text_in_frame(self, element, frame, by_element=None, by_frame=None):
        self.switch_to_frame(frame, by_frame)
        result = self.get_text(element, by_element)
        self.exit_frame()

        return result

    def append_text(self, element, text, by=None):
        self.get_element(element, by).send_keys(text)
        self.wait_for_load_to_complete()

    def append_text_in_frame(self, element, text, frame, by_element=None, by_frame=None):
        self.switch_to_frame(frame, by_frame)
        self.append_text(element, text, by_element)
        self.exit_frame()

    def set_text(self, element, text, by=None):
        self.clear_text(element, by)
        self.append_text(element, text, by)

    def set_text_in_frame(self, element, text, frame, by_element=None, by_frame=None):
        self.switch_to_frame(frame, by_frame)
        self.set_text(element, text, by_element)
        self.exit_frame()

    def clear_text(self, element, by=None):
        self.get_element(element, by).clear()

    def clear_text_in_frame(self, element, frame, by_element=None, by_frame=None):
        self.switch_to_frame(frame, by_frame)
        self.clear_text(element, by_element)
        self.exit_frame()

    # Frame methods
    def switch_to_frame(self, element, by=None):
        if not by:
            by = self.__get_by(element)

        self.__driver.switch_to.frame(self.get_element(element, by))

    def exit_frame(self):
        self.__driver.switch_to.default_content()

    # JavaScript methods
    def dispatch_event(self, element, event):
        self.__driver.execute_script("arguments[0].dispatchEvent(new Event('" + event + "', {bubbles:true}))",
                                     self.get_element(element))

    def trigger_angular_event(self, element, event):
        self.__driver.execute_script("angular.element(arguments[0]).triggerHandler('" + event + "')",
                                     self.get_element(element))

    # Scroll methods
    def scroll_to_top(self):
        self.__driver.execute_script("window.scrollTo(window.pageXOffset, 0)")

    def scroll_to_bottom(self):
        self.__driver.execute_script("window.scrollTo(window.pageXOffset, document.body.scrollHeight)")

    def scroll_page_down(self):
        self.__driver.execute_script("window.scrollTo("
                                     "window.pageXOffset, window.pageYOffset + (window.innerHeight * 0.8))")

    # Element state methods
    def is_displayed(self, element, by=None):
        return self.get_element(element, by).is_displayed()

    def is_enabled(self, element, by=None):
        return self.get_element(element, by).is_enabled()

    def is_selected(self, element, by=None):
        return self.get_element(element, by).is_selected()

    # Waits
    def wait_for_load_to_complete(self):
        if self.__desktop and self.__driver_type != AutomationConstants.MOBILE_APP:
            if self.__wait_for_page:
                self.wait_for_page_to_load()

            if self.__wait_for_angular:
                self.wait_for_angular()

            if self.__wait_for_page:
                self.wait_for_jquery()

    def wait_for_page_to_load(self):
        try:
            (WebDriverWait(self.__driver, self.__implicit_timeout, poll_frequency=0.5)
             .until("true" == self.execute_javascript(
                'return !!document && document.readyState == "complete"')))
        except:
            self.__logger.error("Exception waiting for page to load")

    def wait_for_angular(self):
        if self.__driver_type != AutomationConstants.MOBILE_APP:
            try:
                (WebDriverWait(self.__driver, self.__implicit_timeout, poll_frequency=0.5)
                 .until("true" == str(self.execute_javascript(
                    "return !window.angular  || (!!window.angular && !!angular.element(document).injector()"
                    "&& angular.element(document).injector().get('$http').pendingRequests.length === 0);"))))
            except:
                self.__logger.error("Exception wait for Angular")

    def wait_for_jquery(self):
        if self.__driver_type != AutomationConstants.MOBILE_APP:
            try:
                (WebDriverWait(self.__driver, self.__implicit_timeout, poll_frequency=0.5)
                 .until("true" == str(self.execute_javascript(
                    "return jQuery.active == 0  && jQuery.isReady;"))))
            except:
                self.__logger.error("Exception waiting for jQuery")

    def wait_for_element_to_be_present(self, wait_element, by=None):
        if not by:
            by = self.__get_by(wait_element)

        (WebDriverWait(self.__driver, self.__implicit_timeout, poll_frequency=0.5,
                       ignored_exceptions=WebDriverException)
         .until(expected_conditions.presence_of_element_located((by, wait_element))))

        return self.get_element(wait_element, by)

    def wait_for_element_not_to_be_present(self, wait_element, by=None):
        if not by:
            by = self.__get_by(wait_element)

        (WebDriverWait(self.__driver, self.__implicit_timeout, poll_frequency=0.5,
                       ignored_exceptions=WebDriverException)
         .until_not(expected_conditions.presence_of_element_located((by, wait_element))))

    def wait_for_element_to_be_visible(self, wait_element, by=None):
        if not by:
            by = self.__get_by(wait_element)

        (WebDriverWait(self.__driver, self.__implicit_timeout, poll_frequency=0.5,
                       ignored_exceptions=WebDriverException)
         .until(expected_conditions.visibility_of_element_located((by, wait_element))))

        return self.get_element(wait_element, by)

    def wait_for_element_not_to_be_visible(self, wait_element, by=None):
        if not by:
            by = self.__get_by(wait_element)

        (WebDriverWait(self.__driver, self.__implicit_timeout, poll_frequency=0.5,
                       ignored_exceptions=WebDriverException)
         .until_not(expected_conditions.visibility_of_element_located((by, wait_element))))

    def wait_for_element_to_be_clickable(self, wait_element, by=None):
        if not by:
            by = self.__get_by(wait_element)

        (WebDriverWait(self.__driver, self.__implicit_timeout, poll_frequency=0.5,
                       ignored_exceptions=WebDriverException)
         .until(expected_conditions.element_to_be_clickable((by, wait_element))))

        return self.get_element(wait_element, by)

    def wait_for_element_not_to_be_clickable(self, wait_element, by=None):
        if not by:
            by = self.__get_by(wait_element)

        (WebDriverWait(self.__driver, self.__implicit_timeout, poll_frequency=0.5,
                       ignored_exceptions=WebDriverException)
         .until_not(expected_conditions.element_to_be_clickable((by, wait_element))))

    def wait_for_alert_to_be_present(self):
        (WebDriverWait(self.__driver, self.__implicit_timeout, poll_frequency=0.5,
                       ignored_exceptions=WebDriverException)
         .until(expected_conditions.alert_is_present()))

    def wait(self, seconds):
        time.sleep(seconds)

    # Alert methods
    def alert_is_present(self):
        result = False

        try:
            self.get_alert_text()
            result = True
        except:
            pass

        return result

    def get_alert_text(self):
        result = self.__driver.switch_to.alert.text
        self.exit_frame()

        return result

    def accept_alert(self):
        self.__driver.switch_to.alert.accept()
        self.exit_frame()

    def dismiss_alert(self):
        self.__driver.switch_to.alert.dismiss()
        self.exit_frame()

    # Cookies methods
    def get_cookie(self, cookie):
        return self.__driver.get_cookie(cookie)

    def get_cookies(self):
        return self.__driver.get_cookies()

    def add_cookie(self, cookie):
        self.__driver.add_cookie(cookie)

    def add_cookies(self, cookies):
        for cookie in cookies:
            self.add_cookie(cookie)

    def delete_cookie(self, cookie):
        self.__driver.delete_cookie(cookie)

    def delete_all_cookies(self):
        self.__driver.delete_all_cookies()

    # Cache
    def get_keys_in_cache(self):
        return list(self.execute_async_javascript("var callback = arguments[0];"
                                                  "caches.keys().then(function(keys) { callback(keys);})"))

    def get_cache_resources(self, cache):
        return list(self.execute_async_javascript("var callback = arguments[0];"
                                                  "caches.open('" + cache + "').then(function(cache) { "
                                                                            "cache.keys().then((keys) => {"
                                                                            "var result = new Array(); "
                                                                            "for(var i = 0; i < keys.length; i++) { "
                                                                            "result.push(keys[i].url);};"
                                                                            "callback(result);})})"))

    def get_resource_in_cache(self, cache, resource):
        return list(self.execute_async_javascript("var callback = arguments[0];"
                                                  "caches.open('" + cache + "').then(function(cache) { "
                                                                            "cache.keys().then((keys) => {"
                                                                            "var result = new Array(); "
                                                                            "for(var i = 0; i < keys.length; i++) { "
                                                                            "result.push(keys[i].url);};"
                                                                            "callback(result);})})"))

    def delete_cache(self, cache):
        return self.execute_javascript("caches.delete('" + cache + "')")

    def clear_cache(self):
        return self.execute_async_javascript("var callback = arguments[0];"
                                             "caches.keys().then(function(keys) {"
                                             "keys.forEach(function(key) {"
                                             "caches.delete(key);}); callback();})")

    def clear_local_storage(self):
        return self.execute_javascript("window.localStorage.clear();")

    def clear_session_storage(self):
        return self.execute_javascript("window.sessionStorage.clear();")

    def refresh_without_cache(self):
        return self.execute_javascript("window.location.reload(true);")

    # Window
    def close_tab(self):
        self.__driver.close()

    def get_current_window(self):
        return self.__driver.current_window_handle

    def get_window_handles(self):
        return self.__driver.window_handles

    def switch_to_window(self, window):
        self.__driver.switch_to().window(window)

    def switch_to_next_window(self):
        next_window_handle = self.__driver.current_window_handle

        for i in range(len(self.__driver.window_handles)):
            if self.__driver.window_handles[i] == self.__driver.current_window_handle:
                if i + 1 != len(self.__driver.window_handles):
                    next_window_handle = self.__driver.window_handles[i + 1]
                else:
                    next_window_handle = self.__driver.window_handles[0]

                break

        self.__driver.switch_to().window(next_window_handle)

    def switch_to_previous_window(self):
        previous_window_handle = self.__driver.current_window_handle

        for i in range(len(self.__driver.window_handles)):
            if self.__driver.window_handles[i] == self.__driver.current_window_handle:
                previous_window_handle = self.__driver.window_handles[i - 1]

                break

        self.__driver.switch_to().window(previous_window_handle)

    # Network
    def set_network_conditions(self, **network_conditions):
        if self.__browser == BrowserType.CHROME:
            self.__driver.execute("setNetworkConditions", {'network_conditions': network_conditions})
        elif self.__browser == BrowserType.FIREFOX:
            self.__driver.execute("setNetworkCondition", {'network_name': 'Regular 4G'})

    def get_network_conditions(self):
        return self.__driver.execute("getNetworkConditions")['value']

    # Take screenshots
    def take_screenshot(self, file_name, file_path):
        image = None

        try:
            image = self.__driver.save_screenshot(file_path + file_name)
        except:
            print("Exception trying to save screenshot")

        return image
    # endregion