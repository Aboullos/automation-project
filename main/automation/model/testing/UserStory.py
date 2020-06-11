import os
import time
from array import array
from multiprocessing.sharedctypes import synchronized
from typing import Callable

from main.automation.configuration import AutomationConstants
from main.automation.data.DataObject import DataObject
from main.automation.model.httprequest.RequestHelper import RequestHelper
from main.automation.model.testing import SuiteManager, TestDataManager

from main.automation.model.utils.FileUtils import FileUtils
from main.automation.model.utils.InitUtils import InitUtils
from main.automation.model.utils.objects.DebugLogger import DebugLogger
from main.automation.model.webdriver.DriverHelper import DriverHelper
from main.automation.model.webdriver.configuration import BrowserType


class UserStory:

    def __init__(self, test_case: str, thread_id: str = '0', suite_m: SuiteManager = None):
        self.__suite_m = suite_m
        self.__test_id = thread_id
        self.__scenario = test_case
        self.__test_case = test_case
        self.__test_data_manager = None

        self.__tries: int = 0
        self.__duration: int = 0
        self.__result: str = AutomationConstants.TEST_UNDONE
        self.__browser: str = None
        self.__last_exception: str = ''
        self.__test_result: bool = False

        self.__on_fail_list: list = list()
        self.__on_success_list: list = list()
        self.__on_end_list: list = list()
        self.__after_last_list: list = list()

        self.__exception: Exception = None
        self.__error: IOError = None

        self.__web_driver: DriverHelper = None
        self.__request: RequestHelper = None
        self.__logger: DebugLogger = None

        self.__action_steps: list = list()
        self.__stepper = None
        self.__method_name = None
        self.__parameters = None
        self.__step_category = "given"

        self.__logger = DebugLogger(thread_id)

    def add_data(self, data_object: DataObject, key: str):
        self.get_test_data_manager().add_data(data_object, key)

        return self

    def add_dm_data(self, file_name: str, key: str):
        self.get_test_data_manager().add_dm_data(file_name, key)

        return self

    def add_md_data(self, file_name: str, key: str):
        self.get_test_data_manager().add_md_data(file_name, key)

        return self

    # region Getters
    def get_test_id(self) -> str:
        return self.__test_id

    def get_scenario(self) -> str:
        return self.__scenario

    def get_result(self) -> str:
        return self.__result

    def __assign_browser(self):
        if self.__suite_m.get_main_driver() == AutomationConstants.WEB:
            self.__browser = self.__assign_if_null(self.__browser, self.get_test_var(AutomationConstants.BROWSER))
            self.__browser = self.__assign_if_null(self.__browser, self.get_config_var(AutomationConstants.BROWSER))
            self.__browser = self.__assign_if_null(self.__browser, BrowserType.CHROME)
        elif self.__suite_m.get_main_driver() == AutomationConstants.MOBILE_APP \
                or self.__suite_m.get_main_driver() == AutomationConstants.MOBILE_WEB:
            self.__browser = self.__assign_if_null(self.__browser, InitUtils.get_argument(AutomationConstants.DEVICE))
            self.__browser = self.__assign_if_null(self.__browser, self.get_test_var(AutomationConstants.DEVICE))
            self.__browser = self.__assign_if_null(self.__browser, self.get_config_var(AutomationConstants.DEVICE))

    def get_browser(self) -> str:
        if self.__browser is None:
            self.__assign_browser()

        return self.__browser

    def get_last_exception(self) -> str:
        return self.__last_exception

    def get_tries(self) -> int:
        return self.__tries

    def get_max_tries(self) -> int:
        return self.__suite_m.get_max_tries()

    def get_duration(self) -> int:
        return self.__duration

    def __get_result_matrix(self) -> [[]]:
        return self.__suite_m.get_result_matrix(self.__test_case)

    def get_web_driver(self) -> DriverHelper:
        if self.__web_driver is None:
            self.__assign_browser()
            self.__add_driver_configuration()

        return self.__web_driver

    def get_request(self) -> RequestHelper:
        if self.__request is None:
            self.__request = RequestHelper

        return self.__request

    def get_test_data_manager(self) -> TestDataManager:
        return self.__suite_m.get_test_data_manager(self.__test_case)

    def get_data(self, key: str) -> DataObject:
        result_data: DataObject = self.__suite_m.get_suite_data(key)

        if result_data is None:
            result_data = self.get_test_data_manager().get_data(key)

        return result_data

    def get_config_data(self) -> DataObject:
        return self.get_test_data_manager().get_config_data()

    def get_suite_var(self, key: str) -> str:
        return self.__suite_m.get_suite_var(key)

    def get_global_var(self, key: str) -> str:
        return self.get_test_data_manager().get_global_var(key)

    def get_scenario_var(self, key: str) -> str:
        return self.get_test_data_manager().get_scenario_var(self.__scenario, key)

    def get_test_var(self, key: str) -> str:
        return self.get_test_data_manager().get_test_var(self.__test_id, key)

    def get_config_var(self, key: str) -> str:
        return self.get_test_data_manager().get_config_var(key)

    def get_var(self, key: str, row_key: str=None) -> str:
        result_var: str = self.get_test_data_manager().get_var(key, row_key)

        if result_var is None:
            result_var = self.__suite_m.get_suite_var(key, row_key)

        return result_var

    def get_report_path(self) -> str:
        return self.get_test_data_manager().get_report_path()

    def get_timestamp(self) -> str:
        return self.get_test_data_manager().get_timestamp()
    # endregion

    # region Setters
    def set_suite_var(self, key: str, value: str):
        self.__suite_m.set_suite_var(key, value)

    def set_global_var(self, key: str, value: str):
        self.get_test_data_manager().set_global_var(key, value)

    def set_scenario_var(self, key: str, value: str):
        self.get_test_data_manager().set_scenario_var(self.__scenario, key, value)

    def set_test_var(self, key: str, value: str):
        self.get_test_data_manager().set_test_var(self.__test_id, key, value)

    def set_config_var(self, key: str, value: str):
        self.get_test_data_manager().set_config_var(key, value)

    def set_report_path(self, report_path: str):
        self.get_test_data_manager().set_report_path(report_path)

    def set_scenario(self, __scenario: str):
        self.__scenario += 1
        return self

    @staticmethod
    def __assign_if_null(variable: str, assign: str) -> str:
        return assign if variable is None else variable
    # endregion

    # region Add methods
    def given(self, method: classmethod, *args):
        self.__step_category = self.given.__name__

        self.__process_step(method, *args)

        return self

    def when(self, method: classmethod, *args):
        self.__step_category = self.when.__name__

        self.__process_step(method, *args)

        return self

    def then(self, method: classmethod, *args):
        self.__step_category = self.then.__name__

        self.__process_step(method, *args)

        return self

    def and_(self, method: classmethod, *args):
        self.__process_step(method, *args)

        return self

    def on_success(self, method: classmethod, *args):
        self.__step_category = self.on_success.__name__

        self.__process_step(method, *args)

        return self

    def on_fail(self, method: classmethod, *args):
        self.__step_category = self.on_fail.__name__

        self.__process_step(method, *args)

        return self

    def on_end(self, method: classmethod, *args):
        self.__step_category = self.on_end.__name__

        self.__process_step(method, *args)

        return self

    def on_last_iteration(self, method: classmethod, *args):
        self.__step_category = self.on_last_iteration.__name__

        self.__process_step(method, *args)

        return self

    def __process_step(self, method: classmethod, *args):
        import_ = "from " + method.__module__ + " import " + method.__module__.split(".")[-1]
        evaluation = method.__module__.split(".")[-1] + "(self)"

        # Add method dependent variables
        if self.__step_category not in ["given", "when", "then"]:
            eval("self.__" + self.__step_category + "_list")\
                .append((self.__step_category, import_, evaluation, method.__name__, args))
        else:
            self.__action_steps.append((self.__step_category, import_, evaluation, method.__name__, args))

        return self
    # endregion

    # region Run methods
    def __run_fail_actions(self):
        if self.__on_fail_list:
            error_str: str = self.get_test_data_manager().case_variables_to_string(self.__test_id)
            if error_str:
                error_str += ", "

            error_str += "" if self.__browser is None else AutomationConstants.BROWSER + ": " + self.__browser + ", "

            self.__logger.error(error_str + "lastException: " + self.__last_exception)

            try:
                self.__logger.begin()

                for step in self.__on_fail_list:
                    # Initialize StepObject
                    exec(step[1])

                    # Run step
                    getattr(eval(step[2]), step[3])(*step[4])

                self.__logger.end()
            except Exception as e:
                print(e, 'On FAIL actions')

    def __run_success_actions(self):
        if self.__on_success_list:
            try:
                self.__logger.begin()

                for step in self.__on_success_list:
                    # Initialize StepObject
                    exec(step[1])

                    # Run step
                    getattr(eval(step[2]), step[3])(*step[4])

                self.__logger.end()
            except Exception as e:
                print(e, 'On SUCCESS actions')

    def __run_end_actions(self):
        if self.__on_end_list:
            try:
                self.__logger.begin()

                for step in self.__on_end_list:
                    # Initialize StepObject
                    exec(step[1])

                    # Run step
                    getattr(eval(step[2]), step[3])(*step[4])

                self.__logger.end()
            except Exception as e:
                print(e, 'On END actions')

    def run__after_last_iteration_actions(self):
        if self.__after_last_list:
            try:
                self.__logger.begin()

                for step in self.__after_last_list:
                    # Initialize StepObject
                    exec(step[1])

                    # Run step
                    getattr(eval(step[2]), step[3])(*step[4])

                self.__logger.end()
            except Exception as e:
                print(e, 'After LAST iteration actions')

    def __handle_test_end(self, test_result: bool, exception: Exception, error: IOError):
        if not test_result:
            self.__result = AutomationConstants.TEST_FAILURE

            self.__run_fail_actions()
            self.__run_end_actions()

            self.__save_exception_into_file(str(exception.__traceback__) if exception
                                            else str(error.__traceback__) if error else None, self.__test_id)

            failure: str = ''

            if exception is not None and exception.__cause__ is not None:
                failure = exception.__cause__
            elif error is not None and error.__cause__ is not None:
                failure = error.__cause__

            self.__logger.info('Test execution ended with failure' + (': ' + failure if failure else ''))

            self.__update_result_matrix()

            import sys
            # TODO add layer to handle raises
            if exception:
                raise exception
            elif error:
                raise error
            else:
                print("Unkown error")

        else:
            self.__result = AutomationConstants.TEST_SUCCESS

            self.__run_success_actions()
            self.__run_end_actions()

            self.__update_result_matrix()

    def run(self):
        self.__test_result = False

        self.__logger.begin()
        start_time = int(round(time.time() * 1000))

        try:
            info_string: str = self.get_test_data_manager().case_variables_to_string(self.__test_id)

            if info_string:
                self.__logger.info('Variables: ' + info_string)

            for step in self.__action_steps:
                # Initialize StepObject
                exec(step[1])

                # Run step
                getattr(eval(step[2]), step[3])(*step[4])

            self.__logger.info('Test execution ended successfully')
            self.__test_result = True
        except Exception as e:
            self.__logger.error(
                "EXCEPTION ON TEST ACTIONS:" + self.get_test_data_manager().case_variables_to_string(self.__test_id))
            self.__exception = e

            self.__take_error_screen_shot()
        except IOError as er:
            self.__logger.error(
                "ERROR ON TEST ACTIONS:" + self.get_test_data_manager().case_variables_to_string(self.__test_id))
            self.__exception = er

            self.__take_error_screen_shot()

        if self.__web_driver:
            self.__web_driver.quit()

        if (self.__suite_m.get_tests_finished(self.__test_case) + 1 is self.__suite_m.get_test_to_run(
                self.__test_case) and self.__after_last_list):
            self.run__after_last_iteration_actions()

        if not self.__test_result and self.__check_tries(self.__exception, self.__error):
            self.__run_fail_actions()
            self.__logger.end()

            return self.run()
        else:
            self.__duration = int((round(time.time() * 1000) - start_time) / 1000)
            self.__handle_test_end(self.__test_result, self.__exception, self.__error)

            return self.__test_result
    # endregion

    def __add_driver_configuration(self):
        self.__logger.begin()

        self.__web_driver = DriverHelper(self.__browser, self.get_config_data())
        self.__web_driver.set_id(self.__test_id)

        main_driver_value: str = ''

        if self.__suite_m.get_main_driver() == AutomationConstants.WEB \
                or self.__suite_m.get_main_driver() == AutomationConstants.MOBILE_WEB:
            main_driver_value = AutomationConstants.BROWSER
        elif self.__suite_m.get_main_driver() == AutomationConstants.MOBILE_APP:
            main_driver_value = AutomationConstants.DEVICE

        self.get_test_data_manager().set_test_var(self.__test_id, main_driver_value, self.__browser)
        self.__logger.info(main_driver_value + ': ' + self.__browser + ', ip: ' + self.get_config_data().get_var(
            AutomationConstants.IP)
                           + ', port: ' + self.get_config_data().get_var(
            AutomationConstants.PORT) + ', remote: ' + self.get_config_data().get_var(
            AutomationConstants.REMOTE_MODE))

        self.__logger.end()

        return self

    def __take_error_screen_shot(self):
        try:
            if self.get_timestamp() is not None and self.__web_driver is not None:
                self.__logger.begin()
                self.__file_name = '[ERROR] - ' + self.get_timestamp() + '.i' + self.__test_id + '.png'

                self.__logger.info('Taking screenshot: ' + self.__file_name)
                os.makedirs(os.path.join(self.get_report_path(), AutomationConstants.IMAGES_FOLDER), exist_ok=True)

                self.__suite_m.send_img_to_database(
                    self.__suite_m.get_timestamp_driver(self.get_test_data_manager()),
                    self.get_timestamp() + '.i' + self.__test_id,
                    self.__web_driver.take_screenshot(
                        self.__file_name, self.get_report_path() + '/' + AutomationConstants.IMAGES_FOLDER))
                self.__logger.end()
        except IOError:
            pass

        return self

    def __check_tries(self, exception: Exception, error: IOError) -> bool:
        self.__result_aux: bool = False

        failure: str = exception is not None if str(exception.__class__).split('.')[-1] \
            else str(error.__class__).split('.')[-1]

        self.__logger.info('Checking retry on fail: ' + str(self.__suite_m.get_retry_on_fail())
                           + (', max tries: ' + self.__suite_m.get_max_tries() + ', current tries: ' + (self.__tries + 1)
                              if self.__suite_m.get_retry_on_fail() else '')
                           + (", stopping execution because of same error"
                              if self.__last_exception is not None and self.__last_exception == failure else ''))

        if ((self.__suite_m.get_retry_on_fail() and self.__last_exception is not None
             and self.__last_exception != failure) and self.__tries < self.__suite_m.get_max_tries()):
            self.__tries += 1
            self.__logger.info('Trying again')

            self.__result_aux = True
        elif self.__suite_m.get_retry_on_fail():
            self.__logger.info('Last try, finishing with error')

        self.__last_exception = failure

        return self.__result_aux

    def __save_exception_into_file(self, exception: str, __id: str):
        self.__logger.begin()

        try:
            os.makedirs(self.get_report_path() + '/' + AutomationConstants.EXCEPTIONS_FOLDER, exist_ok=True)

            FileUtils.write_file(self.get_report_path() + '/' + AutomationConstants.EXCEPTIONS_FOLDER
                                 + self.get_timestamp() + '.e' + __id + '.txt', exception)
        except IOError:
            self.__logger.error('Saving Exception into file')

        self.__logger.end()

    def __get_execution_result_array(self, add_browser_to_matrix: bool) -> list:
        self.__result_array = [str()] * (len(self.get_test_data_manager().get_case_variables())
                                         + 3 + (1 if add_browser_to_matrix else 0))

        for i in range(len(self.get_test_data_manager().get_case_variables())):
            self.__result_array[i] = self.get_test_var(self.get_test_data_manager().get_case_variables()[i])

        if add_browser_to_matrix:
            self.__result_array[len(self.__result_array) - 4] = self.get_browser()

        self.__result_array[len(self.__result_array) - 3] = self.__result
        self.__result_array[len(self.__result_array) - 2] = str(self.__duration)
        self.__result_array[len(self.__result_array) - 1] = \
            self.__last_exception if self.__result != AutomationConstants.TEST_SUCCESS else ''

        return self.__result_array

    def __update_result_matrix(self):
        if self.__get_result_matrix() is not None:
            try:
                self.__logger.begin()

                info_string: str = self.get_test_data_manager().case_variables_to_string(self.__test_id)
                if info_string is not None:
                    info_string += ', '

                add_browser_to_matrix: bool = AutomationConstants.BROWSER in self.__get_result_matrix()[0]

                browser_string = ("browser: " + self.__browser + ", "
                                  if self.__browser and add_browser_to_matrix else '')

                self.__logger.info(info_string + browser_string + "time: " + str(self.__duration)
                                   + (", report: " + str(self.__last_exception)
                                      if self.__last_exception and not self.__result == AutomationConstants.TEST_SUCCESS
                                      else ''))

                self.__get_result_matrix()[int(self.__test_id) + 1] = \
                    self.__get_execution_result_array(add_browser_to_matrix)

                print(self.__get_result_matrix())

                self.__logger.info('Saving result as ' + self.get_test_data_manager().get_timestamp() + '.csv')
                os.makedirs(self.get_report_path(), exist_ok=True)
                FileUtils.write_matrix_to_csv_file(
                    self.get_report_path() + self.get_test_data_manager().get_timestamp() + '.csv',
                    self.__get_result_matrix())

                self.__suite_m.update_test_finished(self.__test_case)

                self.__logger.end()

            except IOError as e:
                self.__logger.print_stack_trace(e)
                self.__logger.end()
                raise IOError
    # endregion
