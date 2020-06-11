import datetime
import os
from distutils.util import strtobool

from main.automation.configuration import AutomationConstants
from main.automation.data.DataObject import DataObject
from main.automation.data.DataObjectManager import DataObjectManager
from main.automation.model.httprequest.RequestHelper import RequestHelper
from main.automation.model.testing.TestDataManager import TestDataManager
from main.automation.model.testing.UserStory import UserStory
from main.automation.model.utils.CsvToHtml import CsvToHtml
from main.automation.model.utils.ArrayUtils import ArrayUtils
from main.automation.model.utils.FileUtils import FileUtils
from main.automation.model.utils.InitUtils import InitUtils
from main.automation.model.utils.StringUtils import StringUtils
from main.automation.model.utils.objects.DebugLogger import DebugLogger
from main.automation.model.webdriver.configuration import BrowserType


class SuiteManager:

    __FILE_SENT_SUCCESS_MESSAGE: str = "File sent correctly"
    __FILE_SENT_FAILURE_MESSAGE: str = "Error sending file"

    def __init__(self, suite_name: str):
        self.__suite_name = suite_name
        self.__initial_timestamp: str = datetime.datetime.now().strftime('%Y.%m.%d %H.%M.%S')

        self.__max_tries: int = 0
        self.__api_url: str = None
        self.__project_id: str = None
        self.__report_path: str = None
        self.__special_case: str = None
        self.__main_driver: str = None

        self.__test_data_path: str = None
        self.__scenario_data_path: str = None
        self.__global_data_path: str = None

        self.__retry_on_fail = False
        self.__test_data_path_set = False
        self.__scenario_data_path_set = False
        self.__global_data_path_set = False

        self.__logger: DebugLogger = DebugLogger('')
        self.__suite_data: DataObjectManager = DataObjectManager()

        self.__console_logs: dict
        self.__test_cases: list = list()
        self.__test_suite_object: dict = dict()

    def set_test_data_path(self, path: str):
        self.__test_data_path_set = True
        self.__test_data_path = path

    def set_scenario_data_path(self, path: str):
        self.__scenario_data_path_set = True
        self.__scenario_data_path = path

    def set_global_data_path(self, path: str):
        self.__global_data_path_set = True
        self.__global_data_path = path

    def get_name(self) -> str:
        return self.__suite_name

    def get_daily_case(self) -> str:
        return self.__special_case

    def get_main_driver(self) -> str:
        return self.__main_driver

    def get_max_tries(self) -> int:
        return self.__max_tries

    def get_retry_on_fail(self) -> bool:
        return self.__retry_on_fail

    def get_suite_data_keys(self):
        return self.__suite_data.get_key_set()

    def get_suite_var_key(self, row_key: str, key: str) -> str:
        for data_key in self.__suite_data.get_key_set():
            result_var = self.get_suite_var_suite(data_key, self.__suite_data.get_data(data_key).get_key(), key)

            if result_var is not None:
                return result_var

    def get_suite_var_row(self, row_key: str, key: str) -> str:
        for data_key in self.__suite_data.get_key_set():
            result_var = self.get_suite_var_suite(data_key, row_key, key)

            if result_var is not None:
                return result_var

    def get_suite_var_suite(self, suite_key: str, row_key: str, key: str) -> str:
        if self.__suite_data.get_data(suite_key).get_row(row_key) is not None and key in self.__suite_data.get_data(
                suite_key).get_row(row_key).keys():
            return self.__suite_data.get_data(suite_key).get_var(key)

    def set_suite_var(self, key: str, value: str):
        if self.get_suite_data(AutomationConstants.SUITE_DATA) is None:
            self.add_suite_data(DataObject().add_row('row'), AutomationConstants.SUITE_DATA)

        self.get_suite_data(AutomationConstants.SUITE_DATA).set_value(value_key=key, value=value)

    def set_suite_var_row(self, row_key: str, key: str, value: str):
        value_set: bool = False

        for data_key in self.__suite_data.get_key_set():
            if self.__suite_data.get_data(data_key).get_row(row_key) is not None:
                self.set_suite_var_suite(data_key, row_key, key, value)
                value_set = True
                break

        if not value_set:
            if self.get_suite_data(AutomationConstants.SUITE_DATA) is None:
                self.add_suite_data(DataObject().add_row('row').add_row(row_key).set_key(row_key),
                                    AutomationConstants.SUITE_DATA)
            self.get_suite_data(AutomationConstants.SUITE_DATA).set_value(row_key, key, value)

    def set_suite_var_suite(self, suite_key: str, row_key: str, key: str, value: str):
        self.__suite_data.get_data(suite_key).set_value(row_key, key, value)

    def get_suite_data(self, data_key: str):
        return self.__suite_data.get_data(data_key)

    def add_suite_data(self, data_object: DataObject, data_key: str):
        if self.__suite_data.contains_key(data_key):
            self.__suite_data.replace_data(data_key, data_object)
        else:
            self.__suite_data.add_data(data_key, data_object)

    def add_suite_data_file(self, file_path: str, data_key: str):
        if file_path is not None and not os.path.isabs(file_path):
            file_path = AutomationConstants.RESOURCES_FOLDER + file_path

        data_object: DataObject = DataObject(FileUtils.file_to_dm_data(file_path))
        self.add_suite_data(data_object, data_key)

    def add_console_log(self, test_case: str, id_: str, logs: list):
        self.__console_logs.get(test_case)[id_] = logs

    def set_test_order(self, test_list: list):
        test_cases_aux: list = list()
        for test_case in test_list:
            for test_case_dict in self.__test_cases:
                if test_case in test_case_dict.keys():
                    test_cases_aux.append(test_case_dict)
                    break

        self.__test_cases = test_cases_aux

    def create_modified_html_report(self, report_class: CsvToHtml, translation_file: str = None):
        report_class.set_report_path(self.__report_path)
        report_class.create_joint_report(self.get_timestamp(self.get_test_cases()[0]), self.get_report_path(),
                                         self.get_test_cases(), self.get_relevant_columns(), translation_file)

    def create_html_report(self, translation_file: str = None):
        html_report = CsvToHtml()
        html_report.set_report_path(self.__report_path)
        html_report.create_joint_report(self.get_timestamp(self.get_test_cases()[0]), self.get_name(),
                                        self.get_test_cases(), self.get_relevant_columns(), translation_file)

    def create_modified_pdf_report(self, report_class: CsvToHtml, translation_file: str = None):
        report_class.set_report_path(self.__report_path)
        report_class.create_joint_report(self.get_timestamp(self.get_test_cases()[0]), self.get_name(),
                                         self.get_test_cases(), self.get_relevant_columns(), translation_file)

    def create_pdf_report(self, translation_file: str = None):
        html_report = CsvToHtml()
        html_report.set_report_path(self.__report_path)
        html_report.create_joint_report(self.get_timestamp(self.get_test_cases()[0]), self.get_name(),
                                        self.get_test_cases(), self.get_relevant_columns(), translation_file)

    def get_logs_from_all_threads(self, test_case_info: dict):
        result: str = str()
        total_threads: int = len(self.get_result_matrix(list(test_case_info.keys())[0])) - 1

        for i in range(total_threads):
            if i is 0:
                result += '[' + list(test_case_info.keys())[0] + ']\n'

            if self.__console_logs.get(list(test_case_info.keys())[0]).get(str(i)) is not None:
                for log in self.__console_logs.get(list(test_case_info.keys())[0]).get(str(i)):
                    result += 'Thread(' + str(i) + ') - ' + log + '\n'

                result += '\n'

        return result

    def create_log_report(self):
        result: str = str()
        path: str = self.__report_path + '/' + self.__suite_name + 'ConsoleLogReport.txt'

        if os.path.exists(self.__report_path + '/' + self.__suite_name + 'ConsoleLogReport.txt'):
            file_text = FileUtils.read_file(path)
            result += '' if file_text is None else file_text

        for test_case_info in self.__test_cases:
            result += self.get_logs_from_all_threads(test_case_info)

        if result:
            FileUtils.write_file(path, result)

    def get_initial_stamp(self):
        return self.__initial_timestamp

    def get_timestamp(self, test_case: str = None) -> str:
        if test_case is None:
            timestamp_aux: str = self.__test_suite_object[self.__test_cases[0][0]][0].get_timestamp()
            timestamp_aux = timestamp_aux.replace(self.__test_cases[0][0], self.get_name())
        else:
            timestamp_aux = self.__test_suite_object[test_case][0].get_timestamp()

        return timestamp_aux

    def get_test_data_manager(self, test_case) -> TestDataManager:
        test_data_m: TestDataManager = None

        if self.__test_suite_object[test_case] is not None:
            test_data_m = self.__test_suite_object[test_case][0]

        return test_data_m

    def get_result_matrix(self, test_case: str):
        result_matrix = None

        if self.__test_suite_object[test_case] is not None:
            result_matrix = self.__test_suite_object[test_case][1]

        return result_matrix

    def get_test_cases(self):
        result = [[] * len(self.__test_cases)]

        for i in range(len(self.__test_cases)):
            result[i] = self.__test_cases[i][0]

        return result

    def get_relevant_columns(self, test_case: str = None):
        if test_case is None:

            result = [[] * len(self.__test_cases)]

            for i in range(len(self.__test_cases)):
                result[i] = self.__test_cases[0][1][2]
        else:
            result: int = -1

            for i in range(len(self.__test_cases)):
                if test_case is self.__test_cases[i][0]:
                    result = self.__test_cases[i][0][2]

        return result

    def get_report_path(self):
        return self.__report_path

    def set_report_path(self, report_path: str):
        self.__report_path = report_path

    def set_relevant_column(self, test_case: str, relevant_column: str):
        for i in range(len(self.__test_cases)):
            if test_case is self.__test_cases[i][0]:
                self.__test_cases[i][1][2] = relevant_column

    def update_test_finished(self, test_case: str):
        for i in range(len(self.__test_cases)):
            if test_case is self.__test_cases[i][0]:
                self.__test_cases[i][1][1] = self.__test_cases[i][1][1] + 1

        if self.get_tests_finished(test_case) is self.get_test_to_run(test_case):
            self.__logger.info('Last test execution from ' + str(self.get_test_to_run(test_case)))

            if InitUtils.get_bool_variable(AutomationConstants.SEND_CSV,
                                           self.get_test_data_manager(test_case).get_config_data()):
                self.send_all_csv_report()
        else:
            self.__logger.info(
                'Remaining executions ' + str(self.get_test_to_run(test_case) - self.get_tests_finished(
                    test_case)) + ' from ' + str(self.get_test_to_run(test_case)))

    def get_test_to_run(self, test_case: str):
        result: int = -1

        for i in range(len(self.__test_cases)):
            if test_case is self.__test_cases[i][0]:
                result = self.__test_cases[i][1][0]

        return result

    def get_tests_finished(self, test_case: str):
        result: int = -1

        for i in range(len(self.__test_cases)):
            if test_case is self.__test_cases[i][0]:
                result = self.__test_cases[i][1][1]

        return result

    def get_project_id(self):
        return self.__project_id

    def set_project_id(self, config: DataObject):
        if self.__project_id is None:
            self.__project_id = InitUtils.get_str_variable(AutomationConstants.PROJECT_ID, config)

    # START TODO: Check send and get methods
    def send_img_to_database(self, main_driver: str, file_name: str, image):

        send_img = InitUtils.get_argument(AutomationConstants.SEND_IMG)

        if image is not None and send_img is not None and send_img and strtobool(send_img):
            try:
                build_id = self.__project_id + self.__suite_name + (
                    '' if not main_driver else '.' + main_driver) + self.__initial_timestamp
                request = RequestHelper(
                    self.__api_url + '/' + self.__project_id + '/images/upload' + build_id + '/' + file_name + '.png')\
                    .add_param('Encoding', 'base64').set_send_file(name='imagefile', file_name=file_name + '.png',
                                                                   file_type='image/png', encode=True)
                if request.post().status_code is 201:
                    self.__logger.info('Image send correctly: ' + file_name)
                else:
                    self.__logger.info('Error sending image: ' + file_name)
            except Exception as e:
                self.__logger.error('Error sending image: ' + file_name)
                # self.logger.print_stack_trace(e)

    def send_html_to_database(self, file_name: str, text: str):
        request = RequestHelper(self.__api_url + '/' + self.__project_id + '/html/' + file_name).set_send_file(
            file_name=file_name, file_type='text/html; charset=utf-8', encode=True)

        if request.post().status_code is 201:
            self.__logger.info(self.__FILE_SENT_SUCCESS_MESSAGE + file_name)
        else:
            self.__logger.info(self.__FILE_SENT_FAILURE_MESSAGE + file_name + (
                ' (' + request.get_status_code() + ' - ' + request.get_response_message() + ')'
                if request.get_response_message() is not None else ''))
            if request.get_response_as_string() is not None:
                self.__logger.info(request.get_response_as_string())

    def get_csv_file(self, file_name: str):
        result: list = None
        file_name = file_name if file_name.endswith('.csv') else file_name + '.csv'
        request = RequestHelper(self.__api_url + '/' + self.__project_id + '/csvfile/' + file_name)

        if request.get().status_code is 200:
            self.__logger.info('File was received correctly' + file_name)
            result = InitUtils.get_result_matrix_from_csv_string(
                request.get_response_as_string().replace('\r\n', '\n'))
        else:
            self.__logger.error("File wasn't received")

        return result

    def send_csv_file(self, file_name: str, text: str):
        try:
            file_name = file_name if file_name.endswith('.csv') else file_name + '.csv'
            request = RequestHelper(self.__api_url + '/' + self.__project_id + '/csvfile/' + file_name).set_send_file(
                file_name=file_name, file_type='text/csv', encode=False)

            if request.post().status_code is 201:
                self.__logger.info(self.__FILE_SENT_SUCCESS_MESSAGE + file_name)
            else:
                self.__logger.info(self.__FILE_SENT_FAILURE_MESSAGE + file_name + (
                    '(' + request.get_status_code() + ' - ' + request.get_response_message() + ')' if request.get_response_message() is not None else ''))
                if request.get_response_as_string() is not None:
                    self.__logger.info(request.get_response_as_string())
        except Exception as e:
            self.__logger.print_stack_trace(e)

    def get_csv_report(self, timestamp: str) -> list:
        result: list = None
        request = RequestHelper(self.__api_url + '/' + self.__project_id + '/csv/' + timestamp + '.csv')

        if request.get().status_code is 200:
            self.__logger.info('File was received correctly: ' + timestamp + '.csv')
            result = InitUtils.get_result_matrix_from_csv_string(
                request.get_response_as_string().replace('\r\n', '\n'))
        else:
            self.__logger.error("File wasn't received: " + timestamp + '.csv')

        return result

    def send_csv_report(self, file_name: str, text: str, driver: str):
        file_name = file_name if file_name.endswith('.csv') else file_name + '.csv'
        build_id: str = self.__project_id + self.__suite_name + ('' if not driver else '.' + driver)

        request = RequestHelper(
            self.__api_url + '/' + self.__project_id + '/post/' + self.__suite_name + '/' + build_id)

        request.set_send_file(file_name=file_name, file_type='text/csv', encode=True).post()

        if request.get_status_code() is 201:
            self.__logger.info(self.__FILE_SENT_SUCCESS_MESSAGE + file_name)
        else:
            self.__logger.info(self.__FILE_SENT_FAILURE_MESSAGE + file_name + (
                ' (' + request.get_status_code() + ' - ' + request.get_response_message() + ')'
                if request.get_response_message() is not None else ''))
            if request.get_response_as_string() is not None:
                self.__logger.info(request.get_response_as_string())
    # END TODO

    @staticmethod
    def get_result_string_with_relevant_column(result_matrix: list, relevant_columns: int):
        result: list = list()

        for i in range(len(result_matrix)):
            for j in range(len(result_matrix[i])):
                result[i][j] = result_matrix[i][j]

                if i is 0 and j is relevant_columns:
                    result[i][j] = '*' + result[i][j]

        return ArrayUtils.matrix_to_string(result, '\n', ';')

    def send_all_csv_report(self):
        if self.__project_id is None:
            self.__logger.error('File not sent: client id not declared')
        elif self.__api_url is None:
            self.__logger.error('File not sent: api_url is null')
        else:
            for i in range(len(self.__test_cases)):
                test_case = list(self.__test_cases[i].keys())[0]
                driver = self.get_timestamp_driver(self.get_test_data_manager(test_case))
                file_name = self.get_test_data_manager(test_case).get_timestamp() + '.csv'

                self.send_csv_report(file_name,
                                     self.get_result_string_with_relevant_column(self.get_result_matrix(test_case),
                                                                                 self.get_relevant_columns(test_case)),
                                     driver)

    def remove_device_emulation_cases(self, test_case: str, cases_matrix: list):
        result: list = None
        result_matrix: list = self.get_result_matrix(test_case)

        if cases_matrix is not None:
            result_matrix = ArrayUtils.remove_rows_containing(result_matrix,
                                                              BrowserType.DEVICE_EMULATION_BROWSERS, 2)
            result = InitUtils.get_cases_matrix_from_result_matrix(result_matrix, test_case)
            result = self.apply_execution_filter(result_matrix, result)

            if len(cases_matrix) is 0:
                for i in range(len(self.__test_cases)):
                    if test_case is list(self.__test_cases[i].keys())[0]:
                        self.__test_cases.remove(i)
                        break
                self.__test_suite_object.pop(test_case)
            else:
                self.__test_suite_object[test_case] = {
                    list(self.__test_suite_object.get(test_case).keys())[0]: result_matrix}

        return result

    def remove_mobile_emulation_cases(self, test_case: str, cases_matrix: list):
        result: list = None
        result_matrix: list = self.get_result_matrix(test_case)

        if cases_matrix is not None:
            result_matrix = ArrayUtils.remove_rows_containing(result_matrix,
                                                              BrowserType.MOBILE_EMULATION_BROWERS, 2)
            result = InitUtils.get_cases_matrix_from_result_matrix(result_matrix, test_case)
            result = self.apply_execution_filter(result_matrix, result)

            if len(cases_matrix) is 0:
                for i in range(len(self.__test_cases)):
                    if test_case is list(self.__test_cases[i].keys())[0]:
                        self.__test_cases.remove(i)
                        break
                self.__test_suite_object.pop(test_case)
            else:
                self.__test_suite_object[test_case] = {
                    list(self.__test_suite_object.get(test_case).keys())[0]: result_matrix}

        return result

    def remove_tablet_emulation_cases(self, test_case: str, cases_matrix: list):
        result: list = None
        result_matrix: list = self.get_result_matrix(test_case)

        if cases_matrix is not None:
            result_matrix = ArrayUtils.remove_rows_containing(result_matrix,
                                                              BrowserType.TABLET_EMULATION_BROWERS, 2)
            result = InitUtils.get_cases_matrix_from_result_matrix(result_matrix, test_case)
            result = self.apply_execution_filter(result_matrix, result)

            if len(cases_matrix) is 0:
                for i in range(len(self.__test_cases)):
                    if test_case is list(self.__test_cases[i].keys())[0]:
                        self.__test_cases.remove(i)
                        break

                self.__test_suite_object.pop(test_case)
            else:
                self.__test_suite_object[test_case] = {
                    list(self.__test_suite_object.get(test_case).keys())[0]: result_matrix}

        return result

    def add_test_objects(self, test_case: str, test_data_m: TestDataManager, result_matrix: list, tests_to_run: int):
        self.__test_suite_object[test_case] = (test_data_m, result_matrix)
        self.__test_cases.append((test_case, [tests_to_run, 0, -1]))

    def __get_browser_argument(self, test_data_m: TestDataManager):
        browser_argument = InitUtils.get_argument(AutomationConstants.BROWSER)

        if browser_argument is None or not browser_argument and self.__main_driver \
                and (self.__main_driver == AutomationConstants.WEB
                     or self.__main_driver == AutomationConstants.MOBILE_WEB):
            browser_argument = test_data_m.get_config_var(AutomationConstants.BROWSER)

        return browser_argument

    def __get_device_argument(self, test_data_m: TestDataManager):
        device_argument = InitUtils.get_argument(AutomationConstants.DEVICE)

        if device_argument is None or not device_argument and self.__main_driver\
                and (self.__main_driver == AutomationConstants.MOBILE_APP
                     or self.__main_driver == AutomationConstants.MOBILE_WEB):
            device_argument = test_data_m.get_config_var(AutomationConstants.DEVICE)

        return device_argument

    def __get_platform_argument(self, test_data_m: TestDataManager):
        platform_argument = InitUtils.get_argument(AutomationConstants.PLATFORM)

        if platform_argument is None or not platform_argument and self.__main_driver \
                and (self.__main_driver == AutomationConstants.MOBILE_APP
                     or self.__main_driver == AutomationConstants.MOBILE_WEB):
            platform_argument = test_data_m.get_config_var(AutomationConstants.PLATFORM)

        return platform_argument

    def add_browser_to_test_data(self, test_data_m: TestDataManager):
        browser_argument = self.__get_browser_argument(test_data_m)
        device_argument = self.__get_device_argument(test_data_m)

        if self.__main_driver == AutomationConstants.WEB or self.__main_driver == AutomationConstants.MOBILE_WEB \
                and test_data_m.get_test_data() is not None \
                and test_data_m.get_test_data().get_row() is not None \
                and AutomationConstants.BROWSER not in test_data_m.get_test_data().get_row().keys() \
                and browser_argument is not None and browser_argument:
            for i in range(test_data_m.get_test_data().size()):
                test_data_m.set_test_var(str(i), AutomationConstants.BROWSER, browser_argument)

        if self.__main_driver == AutomationConstants.MOBILE_APP or self.__main_driver == AutomationConstants.MOBILE_WEB \
                and test_data_m.get_test_data() is not None \
                and test_data_m.get_test_data().get_row() is not None \
                and AutomationConstants.PLATFORM not in test_data_m.get_test_data().get_row() \
                and device_argument is not None and device_argument:
            for i in range(test_data_m.get_test_data().size()):
                test_data_m.set_test_var(str(i), AutomationConstants.PLATFORM, device_argument)
                test_data_m.set_test_var(str(i), AutomationConstants.DEVICE, device_argument)

    def set_main_driver(self, config_data: DataObject):
        if self.__main_driver is None:
            self.__main_driver = InitUtils.get_main_driver_from_properties()

            if (self.__main_driver is None or not self.__main_driver) and config_data is not None \
                    and config_data.get_var(AutomationConstants.MAIN_DRIVER) is not None \
                    and config_data.get_var(AutomationConstants.MAIN_DRIVER):
                self.__main_driver = config_data.get_var(AutomationConstants.MAIN_DRIVER)

            if self.__main_driver is None or not self.__main_driver:
                self.__main_driver = 'api'

    def set_case_variables(self, test_data_path: str, test_data_m: TestDataManager):
        if test_data_path is not None:
            test_data_m.set_case_variables(FileUtils.csv_file_to_matrix(test_data_path, True)[0])
        else:
            test_data_m.set_case_variables(['id'])

    def set_max_tries(self, config_data: DataObject):
        if StringUtils.is_number(InitUtils.set_str_variable(AutomationConstants.MAX_TRIES, config_data)):
            self.__max_tries = config_data.get_var(AutomationConstants.MAX_TRIES)
        else:
            config_data.set_value(AutomationConstants.MAX_TRIES, str(self.__max_tries))

    def set_api_url(self, config_data: DataObject):
        if self.__api_url is None:
            __server_url = os.environ.get(AutomationConstants.API_URL)

            if __server_url is not None and __server_url:
                self.__api_url = __server_url
                config_data.set_value(AutomationConstants.API_URL, self.__api_url)
            else:
                self.__api_url = config_data.get_var(AutomationConstants.API_URL)
        else:
            config_data.set_value(AutomationConstants.API_URL, self.__api_url)

    def get_result_matrix_from_api(self, test_data_m: TestDataManager):
        __result_matrix: list = None
        __get_csv: bool = InitUtils.get_bool_variable(AutomationConstants.GET_CSV, test_data_m.get_config_data())

        if __get_csv and self.__project_id is not None and self.__api_url is not None:
            __result_matrix = self.get_csv_report(test_data_m.get_timestamp())

        if __get_csv and self.__project_id is None:
            self.__logger.info('Project ID not declared')
        if __get_csv and self.__project_id is None:
            self.__logger.info('API URL not declared')

        return __result_matrix

    def apply_execution_filter(self, result_matrix: list, cases_matrix: list):
        execution_filter = InitUtils.get_argument(AutomationConstants.EXECUTION_FILTER)

        if execution_filter is not None and execution_filter:
            self.__logger.info('Applying execution filter (' + execution_filter + ')')
            remove_indexes = ArrayUtils.get_filters_indexes(execution_filter, result_matrix)

            for i in range(len(remove_indexes)):
                new_index = remove_indexes[i] - 1
                remove_indexes.pop(i)
                remove_indexes.insert(i, new_index)

            cases_matrix = ArrayUtils.remove_rows_containing(cases_matrix,
                                                             ArrayUtils.integer_array_to_string_array(remove_indexes),
                                                             1)
        return cases_matrix

    def handle_no_cases_to_run_with_api(self, file_from_api: bool, test_data_m: TestDataManager, result_matrix: list,
                                        cases_matrix: list):
        if not file_from_api and len(cases_matrix) is 0 and InitUtils.get_bool_variable(
                AutomationConstants.SEND_CSV, test_data_m.get_config_data()):
            self.send_all_csv_report()
        elif file_from_api and len(cases_matrix) is 0:
            os.makedirs(test_data_m.get_report_path(), exist_ok=True)
            FileUtils.write_matrix_to_csv_file(test_data_m.get_report_path() + test_data_m.get_timestamp() + '.cvs',
                                               result_matrix)

    def get_timestamp_driver(self, test_data_m: TestDataManager):
        timestamp_driver = ''

        if self.__main_driver == AutomationConstants.WEB or self.__main_driver == AutomationConstants.MOBILE_WEB:
            timestamp_driver = self.__get_browser_argument(test_data_m)

        if self.__main_driver == AutomationConstants.MOBILE_APP or self.__main_driver == AutomationConstants.MOBILE_WEB:
            device = InitUtils.get_str_variable(AutomationConstants.DEVICE, test_data_m.get_config_data())
            timestamp_driver = device if timestamp_driver is not None and timestamp_driver \
                else device + '.' + timestamp_driver

        if timestamp_driver is None or not timestamp_driver:
            timestamp_driver = 'api'

        return timestamp_driver

    def initialize_test_objects(self, test_case: str, scenario_data_path: str=None, test_data_path: str=None,
                                global_data_path: str=None):
        self.__logger.info('Case: ' + test_case)
        cases_matrix = None
        result_matrix = None

        test_data_path = InitUtils.get_test_data_path(test_data_path)

        test_data_m: TestDataManager = InitUtils.initialize_test_data(test_data_path, scenario_data_path,
                                                                      global_data_path,
                                                                      AutomationConstants.CONFIGURATION_DATA)

        self.set_main_driver(test_data_m.get_config_data())
        self.add_browser_to_test_data(test_data_m)

        test_data_m.generate_timestamp(test_case, self.get_timestamp_driver(test_data_m))

        self.__report_path = test_data_m.get_report_path()
        test_data_m.set_config_var(AutomationConstants.REPORT_PATH, self.__report_path)

        self.set_case_variables(test_data_path, test_data_m)
        self.set_project_id(test_data_m.get_config_data())
        self.set_max_tries(test_data_m.get_config_data())
        self.set_api_url(test_data_m.get_config_data())

        self.__retry_on_fail = InitUtils.set_bool_variable(AutomationConstants.RETRY_ON_FAIL,
                                                           test_data_m.get_config_data())

        file_from_api: bool = False

        self.__special_case = test_data_m.get_daily_case()

        if 'continue' in test_data_m.get_daily_case():
            self.__logger.info('Continue daily')

            result_matrix = self.get_result_matrix_from_api(test_data_m)

            if result_matrix is not None:
                file_from_api = True

            if result_matrix is None and os.path.exists(
                    test_data_m.get_report_path() + test_data_m.get_timestamp() + '.csv'):
                self.__logger.info("Getting test data from report file '" + test_data_m.get_timestamp() + ".csv'")
                result_matrix = InitUtils.get_result_matrix_from_csv_file(
                    test_data_m.get_report_path() + test_data_m.get_timestamp() + '.csv')

            if result_matrix is not None:
                cases_matrix = InitUtils.get_cases_matrix_from_result_matrix(result_matrix, test_case)

        if cases_matrix is None:
            self.__logger.info('Creating ' + (
                'base test data' if test_data_path is None else "test data from '" + test_data_path + "'"))
            cases_matrix = InitUtils.get_cases_matrix_from_test_data(test_case, test_data_m.get_test_data().size())
            result_matrix = InitUtils.get_result_matrix_from_test_data(test_data_m.get_test_data(),
                                                                       test_data_m.get_case_variables())

        cases_matrix = self.apply_execution_filter(result_matrix, cases_matrix)

        self.add_test_objects(test_case, test_data_m, result_matrix, len(cases_matrix))

        self.__logger.info('Cases to run on this execution: ' + str(len(cases_matrix)) + (
            ' from ' + str(len(result_matrix) - 1) if len(cases_matrix) is not len(result_matrix) - 1 else ''))

        self.handle_no_cases_to_run_with_api(file_from_api, test_data_m, result_matrix, cases_matrix)

        return cases_matrix

    def create_user_story(self, test_case: str, id_: str = "0"):
        return UserStory(test_case, id_, self)
