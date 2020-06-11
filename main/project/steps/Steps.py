import time
from selenium.webdriver.common.keys import Keys

from main.automation.data.DataObject import DataObject
from main.automation.model.testing.UserStory import UserStory
from main.automation.model.testing.objects.InteractionObject import InteractionObject
from main.automation.model.webdriver.DriverHelper import DriverHelper
from main.project.pages.HomePage import HomePage
from main.project.pages.LoginPage import LoginPage


class Steps(InteractionObject):

    host = 'http://127.0.0.1:8081'

    def log_in(self):
        self.go_to_path("/auth/realms/master/account/#/app/personal-info")
        LoginPage(self._user_s).log_in("admin", "admin")

    def go_to_path(self, path):
        self.debug_info("Going to: " + self.host + path)
        self._user_s.get_web_driver().go(self.host + path)

    def run_performance(self):
        self.debug_begin()
        load = 0
        finish_time = 0
        dom_content_load = 0
        first_paint = 0
        size = 0
        requests = 0
        repeat = int(self._user_s.get_test_var("repeat"))
        download_throughput = float(self._user_s.get_test_var("download_throughput"))
        upload_throughput = float(self._user_s.get_test_var("upload_throughput"))
        latency = float(self._user_s.get_test_var("latency"))

        url = self._user_s.get_test_var("performance_url")

        cookies = self._user_s.get_web_driver().get_cookies()

        for i in range(repeat):
            self._user_s.get_web_driver().quit()

            self._user_s.get_web_driver().go(self.host + "/auth/admin/master/console/#/realms/master")
            self._user_s.get_web_driver().add_cookies(cookies)
            self._user_s.get_web_driver().set_timeouts(280)
            self._user_s.get_web_driver().set_network_conditions(
                offline=False,
                latency=latency,
                download_throughput=download_throughput * 1024,
                upload_throughput=upload_throughput * 1024)

            initial_time = time.time()
            self.go_to_path(url)
            self._user_s.get_web_driver().wait_for_load_to_complete()

            last_request_n = 0
            request_n = 1

            while last_request_n != request_n:
                last_request_n = request_n
                request_n = int(str(self._user_s.get_web_driver().execute_javascript(
                    'return window.performance.getEntries().length')))

                self._user_s.get_web_driver().wait(6)

            dom_content_load_aux = float(str(self._user_s.get_web_driver().execute_javascript(
                'return window.performance.getEntries()[0].domInteractive')))
            load_aux = float(str(self._user_s.get_web_driver().execute_javascript(
                'return window.performance.getEntries()[0].duration')))
            finish_time_aux = float(str(self._user_s.get_web_driver().execute_javascript(
                'resources = performance.getEntriesByType("resource"); max = 0;'
                'for(x in resources) { if(resources[x].responseEnd > max) max = resources[x].responseEnd;}'
                'return max')))
            first_paint_aux = float(str(self._user_s.get_web_driver().execute_javascript(
                'return performance.getEntriesByType("paint")[0].startTime')))
            size_aux = float(str(self._user_s.get_web_driver().execute_javascript(
                'resources = window.performance.getEntriesByType("resource"); size = 0; '
                'for(resource in resources) { size += resources[resource].encodedBodySize} return size')))
            requests_aux = float(str(self._user_s.get_web_driver().execute_javascript(
                'return performance.getEntriesByType("resource").length')))

            print("Iteration", i, ": domContentLoad:", int(dom_content_load_aux), ", load:", int(load_aux),
                  ", finish:", int(finish_time_aux), ", first paint:", int(first_paint_aux), ", size:", int(size_aux),
                  ", reqests:", requests_aux)

            dom_content_load += dom_content_load_aux
            load += load_aux
            finish_time += finish_time_aux
            first_paint += first_paint_aux
            size += size_aux
            requests += requests_aux

        self._set_test_var("requests", str(int(requests / repeat)))
        self._set_test_var("size", str(int(size / repeat)))
        self._set_test_var("dom_content_load", str(int(size / repeat)))
        self._set_test_var("load_time", str(int(load / repeat)))
        self._set_test_var("finish_time", str(int(finish_time / repeat)))
        self._set_test_var("first_paint", str(int(first_paint / repeat)))

        print("Final: domContentLoad:", int(dom_content_load / repeat), ", load:", int(load / repeat),
              ", finish:", int(finish_time / repeat), ", first paint:", int(first_paint / repeat),
              ", size:", int(size / repeat))

        """script_to_execute = "var performance = window.performance || window.mozPerformance " \
                            "|| window.msPerformance || window.webkitPerformance || {}; " \
                            "var network = performance.getEntries() || {}; return network;"

        print(self._user_s.get_web_driver().execute_javascript(script_to_execute))"""
        self.debug_end()
