import sys

from main.automation.data.DataObject import DataObject
from main.automation.model.utils.FileUtils import FileUtils
from main.automation.model.utils.ArrayUtils import ArrayUtils
from main.automation.configuration import AutomationConstants
from main.automation.model.webdriver.configuration import BrowserType


class InitUtils:

    @staticmethod
    def get_argument(key: str) -> str:
        value = None

        for argument in sys.argv:
            if str(argument).startswith(key + '='):
                value = argument[str(argument).index('=') + 1:]
            elif str(argument).startswith(key):
                value = 'true'

        return value

    @staticmethod
    def get_bool_variable(key: str, data_object: DataObject = None) -> bool:
        value = InitUtils.get_argument(key)

        if value is not None and (not value or value.lower() == "true"):
            value = True
        elif value is not None and value is not '':
            value = False

        if value is None and data_object:
            value = data_object.get_var(key)

            if str(value).lower() == "true":
                value = True
            else:
                value = False

        return bool(value)

    @staticmethod
    def get_str_variable(key: str, data_object: DataObject = None) -> str:
        value = InitUtils.get_argument(key)

        if ((value is not None and not value) or value is None) and not data_object:
            value = data_object.get_var(key)

        return value

    @staticmethod
    def set_bool_variable(key: str, data_object: DataObject = None) -> bool:
        value = InitUtils.get_argument(key)

        if value is not None and (not value or value.lower() == "true"):
            value = True
        elif value is not None and value is not '':
            value = False

        if value is None:
            value = data_object.get_var(key)

            if str(value).lower() == "true":
                value = True
            else:
                value = False
        else:
            data_object.set_value(key, value)

        return bool(value)

    @staticmethod
    def set_str_variable(key: str, data_object: DataObject = None) -> str:
        value = InitUtils.get_argument(key)

        if (value is not None and not value) or value is None:
            value = data_object.get_var(key)
        else:
            data_object.set_value(key, value)

        return value

    @staticmethod
    def get_test_data_path(default_data_path):
        test_data_file = InitUtils.get_argument(AutomationConstants.TEST_DATA)

        if test_data_file:
            test_data_file = AutomationConstants.RESOURCES_FOLDER + test_data_file
        elif default_data_path:
            test_data_file = AutomationConstants.RESOURCES_FOLDER + default_data_path
        else:
            test_data_file = None

        return test_data_file

    @staticmethod
    def initialize_test_data(test_data_path, scenario_data_path, global_data_path, config_data_path):
        from main.automation.model.testing.TestDataManager import TestDataManager
        test_data: TestDataManager = TestDataManager()

        test_data.add_test_data(test_data_path)
        test_data.add_config_data(AutomationConstants.RESOURCES_FOLDER + config_data_path)
        test_data.add_scenario_data(AutomationConstants.RESOURCES_FOLDER
                                    + (AutomationConstants.SCENARIO_DATA_SET if not scenario_data_path
                                       else scenario_data_path))
        test_data.add_global_data(AutomationConstants.RESOURCES_FOLDER
                                  + (AutomationConstants.GLOBAL_DATA_SET if not global_data_path
                                     else global_data_path))

        return test_data

    @staticmethod
    def get_result_matrix_from_csv_file(file_path):
        file_path = file_path if file_path.endswith(".csv") else file_path + ".csv"

        return FileUtils.csv_file_to_matrix(file_path)

    @staticmethod
    def get_result_matrix_from_csv_string(csv_string: str):
        return FileUtils.csv_string_to_matrix(csv_string, True)

    @staticmethod
    def get_cases_matrix_from_result_matrix(result_matrix, test_case):
        test_matrix = ArrayUtils.add_index_to_matrix([[None]] * (len(result_matrix) - 1))

        cases_to_run = 0

        for i in range(1, len(result_matrix)):
            if result_matrix[i][len(result_matrix[0]) - 3] != AutomationConstants.TEST_SUCCESS:
                cases_to_run += 1

        current_case = 0
        test_matrix_aux = [[0]]

        if len(test_matrix) > 0:
            test_matrix_aux = [[(len(test_matrix[0]) - 1)]] * cases_to_run

            if len(test_matrix_aux):
                test_matrix_aux[0] = test_matrix[0]

            for i in range(1, len(test_matrix)):
                if result_matrix[i][len(result_matrix[0]) - 3] != AutomationConstants.TEST_SUCCESS:
                    test_matrix_aux[current_case] = test_matrix[i - 1]
                    current_case += 1

        return test_matrix_aux if not len(test_matrix_aux) \
            else ArrayUtils.add_column_string_to_matrix(test_matrix_aux, test_case, 0)

    @staticmethod
    def get_cases_matrix_from_test_data(test_case, size):
        test_matrix = [[]] * size

        test_matrix = ArrayUtils.add_index_to_matrix(test_matrix)
        test_matrix = ArrayUtils.add_column_string_to_matrix(test_matrix, test_case, 0)

        return test_matrix

    @staticmethod
    def get_result_matrix_from_test_data(test_data: DataObject, test_variables: []):
        contains_browser = test_data.get_row().__contains__(AutomationConstants.BROWSER)
        contains_device = test_data.get_row().__contains__(AutomationConstants.PLATFORM)
        test_variables = ArrayUtils.remove_element_from_array(test_variables, AutomationConstants.BROWSER)
        test_variables = ArrayUtils.remove_element_from_array(test_variables, AutomationConstants.DEVICE)
        test_variables = ArrayUtils.remove_element_from_array(test_variables, AutomationConstants.PLATFORM)
        result_matrix = ([[None] * (len(test_variables) + 3 + (1 if contains_browser or contains_device else 0))]
                         * (test_data.size() + 1))

        for j in range(len(test_variables)):
            result_matrix[0][j] = test_variables[j]

        if contains_device or contains_browser:
            result_matrix[0][len(result_matrix[0]) - 4] = AutomationConstants.BROWSER

        result_matrix[0][len(result_matrix[0]) - 3] = "result"
        result_matrix[0][len(result_matrix[0]) - 2] = "time"
        result_matrix[0][len(result_matrix[0]) - 1] = "exception"

        for i in range(1, len(result_matrix)):
            array_aux = [None] * (len(test_variables) + 3 + (1 if contains_browser or contains_device else 0))

            for j in range(len(test_variables)):
                array_aux[j] = test_data.get_var(test_variables[j], str(i - 1))

            if contains_browser or contains_device:
                browser = test_data.get_var(AutomationConstants.BROWSER, str(i - 1))
                browser = test_data.get_var(AutomationConstants.PLATFORM, str(i - 1)) \
                    if not contains_browser else browser

                array_aux[len(array_aux) - 4] = browser

            array_aux[len(array_aux) - 3] = AutomationConstants.TEST_UNDONE
            array_aux[len(array_aux) - 2] = "0.0"
            array_aux[len(array_aux) - 1] = "None"

            result_matrix[i] = array_aux

        return result_matrix

    @staticmethod
    def get_main_driver_from_properties():
        result = None
        browser = InitUtils.get_argument(AutomationConstants.BROWSER)
        platform = InitUtils.get_argument(AutomationConstants.PLATFORM)

        if browser and browser in BrowserType.DESKTOP_BROWSERS and platform:
            result = AutomationConstants.MOBILE_WEB
        elif ((browser is None or browser == '') or browser not in BrowserType.DESKTOP_BROWSERS) and platform:
            result = AutomationConstants.MOBILE_APP
        elif browser and (platform is None or platform == ''):
            result = AutomationConstants.WEB

        return result
