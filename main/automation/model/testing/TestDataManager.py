import os
import datetime

from main.automation.configuration import AutomationConstants
from main.automation.data.DataObject import DataObject
from main.automation.data.DataObjectManager import DataObjectManager
from main.automation.model.utils.ArrayUtils import ArrayUtils
from main.automation.model.utils.FileUtils import FileUtils
from main.automation.model.utils.InitUtils import InitUtils
from main.automation.model.utils.objects.DebugLogger import DebugLogger


class TestDataManager:

    __test_case: str
    __daily_case: str = ''
    __timestamp: str
    __report_path: str
    __case_variables: list = list()
    __data: DataObjectManager
    __logger: DebugLogger = DebugLogger()

    def __init__(self, data=None):
        if data is None or not isinstance(data, DataObjectManager):
            self.__data = DataObjectManager()
        elif isinstance(data, DataObjectManager):
            self.__data = data

        if isinstance(data, DataObject):
            self.__data.add_data(AutomationConstants.TEST_DATA, data)

    def generate_timestamp(self, test_case: str, timestamp_driver: str):
        self.__test_case = test_case
        self.__daily_case = '' if InitUtils.get_argument(AutomationConstants.EXECUTION_CASE) is None \
            else InitUtils.get_argument(AutomationConstants.EXECUTION_CASE)

        self.__timestamp = datetime.datetime.now().strftime(
            "%Y.%m.%d{}".format(".%H.%M.%S" if not self.__daily_case else ""))

        self.__logger.info('Execution ID: ' + self.__timestamp)

        self.__report_path: str = os.path.join(AutomationConstants.ROOT_PATH,
                                               AutomationConstants.REPORTS_FOLDER,
                                               'T' + self.__timestamp.replace(".", "")) + "/"

        build_group = InitUtils.get_argument(AutomationConstants.BUILD_GROUP)
        build_group = '' if build_group is None or not build_group else '.' + build_group

        self.__timestamp += '.' + test_case + '.' + timestamp_driver + build_group

    # region Getters
    def get_test_case(self) -> str:
        return self.__test_case

    def get_daily_case(self) -> str:
        return self.__daily_case

    def get_report_path(self) -> str:
        return self.__report_path

    def get_timestamp(self) -> str:
        return self.__timestamp

    def get_case_variables(self) -> list:
        return self.__case_variables

    def case_variables_to_string(self, test_id: str) -> str:
        text_info: str = str()

        for index, case_variable in enumerate(self.__case_variables):

            if self.get_test_var(test_id, case_variable):
                text_info += (' ' + case_variable + ': ' + self.get_test_var(test_id, case_variable))
                if index < len(self.__case_variables) - 1:
                    text_info += ','

        return text_info

    def get_data_manager(self) -> DataObjectManager:
        return self.__data

    def get_data(self, data_key: str) -> DataObject:
        return self.__data.get_data(data_key)

    def get_test_data(self) -> DataObject:
        return self.__data.get_data(AutomationConstants.TEST_DATA)

    def get_config_data(self) -> DataObject:
        return self.__data.get_data(AutomationConstants.CONFIGURATION_DATA)

    def get_global_var(self, key: str) -> str:
        return self.__data.get_data(AutomationConstants.GLOBAL_DATA).get_var(value_key=key)

    def get_scenario_var(self, scenario: str, key: str) -> str:
        return self.__data.get_data(AutomationConstants.SCENARIO_DATA).get_var(row_key=scenario, value_key=key)

    def get_test_var(self, test_id: str, key: str) -> str:
        return self.__data.get_data(AutomationConstants.TEST_DATA).get_var(row_key=test_id, value_key=key)

    def get_config_var(self, key: str):
        return self.__data.get_data(AutomationConstants.CONFIGURATION_DATA).get_var(value_key=key)
    # endregion

    # region Setters
    def set_test_data(self, test_data: DataObject):
        self.__data.replace_data(AutomationConstants.TEST_DATA, test_data)

    def set_report_path(self, path: str):
        self.__report_path = path

    def set_timestamp(self, timestamp: str):
        self.__timestamp = timestamp

    def set_case_variables(self, case_variables: list):
        if AutomationConstants.BROWSER in case_variables:
            case_variables.remove(AutomationConstants.BROWSER)

        self.__case_variables = case_variables

    def set_global_var(self, key: str, value: str):
        self.__data.get_data(AutomationConstants.GLOBAL_DATA).set_value(value_key=key, value=value)

    def set_scenario_var(self, scenario: str, key: str, value: str):
        self.__data.get_data(AutomationConstants.SCENARIO_DATA).set_value(row_key=scenario, value_key=key, value=value)

    def set_test_var(self, test_id: str, key: str, value: str):
        self.__data.get_data(AutomationConstants.TEST_DATA).set_value(row_key=test_id, value_key=key, value=value)

    def set_config_var(self, key: str, value: str):
        self.__data.get_data(AutomationConstants.CONFIGURATION_DATA).set_value(value_key=key, value=value)
    # endregion

    # region Data Access
    def get_var(self, variable_key: str, row_key: str=None) -> str:
        result: str = None

        if self.__data.get_data(AutomationConstants.GLOBAL_DATA) \
                and self.__data.get_data(AutomationConstants.GLOBAL_DATA).get_var(variable_key) is not None:
            result = self.__data.get_data(AutomationConstants.GLOBAL_DATA).get_var(variable_key)
        elif (self.__data.get_data(AutomationConstants.SCENARIO_DATA)
              and self.__data.get_data(AutomationConstants.SCENARIO_DATA).get_row(row_key) is not None
              and self.__data.get_data(AutomationConstants.SCENARIO_DATA)
                      .get_var(variable_key, row_key) is not None):
            if row_key is None:
                row_key = self.__data.get_data(AutomationConstants.SCENARIO_DATA).get_key()

            result = self.__data.get_data(AutomationConstants.SCENARIO_DATA)\
                .get_var(variable_key, row_key)
        elif (self.__data.get_data(AutomationConstants.TEST_DATA)
              and self.__data.get_data(AutomationConstants.TEST_DATA).get_row(row_key) is not None
              and self.__data.get_data(AutomationConstants.TEST_DATA)
                      .get_var(variable_key, row_key) is not None):
            if row_key is None:
                row_key = self.__data.get_data(AutomationConstants.TEST_DATA).get_key()

            result = self.__data.get_data(AutomationConstants.TEST_DATA)\
                .get_var(variable_key, row_key)
        else:
            data = [AutomationConstants.GLOBAL_DATA, AutomationConstants.SCENARIO_DATA, AutomationConstants.TEST_DATA,
                    AutomationConstants.CONFIGURATION_DATA]

            for data_key in self.__data.get_key_set():
                if data_key not in data and self.__data.get_data(data_key).get_row(row_key) is not None \
                        and self.get_data(data_key).get_var(variable_key, row_key) is not None:
                    if row_key is None:
                        row_key = self.__data.get_data(data_key).get_key()

                    result = self.__data.get_data(data_key).get_var(variable_key, row_key)
                    break

        return result

    def generate_test_row(self, row_key: str):
        if self.__data.contains_key(AutomationConstants.TEST_DATA):
            self.__data.get_data(AutomationConstants.TEST_DATA).add_row(row_key)
        else:
            row = DataObject()
            self.__data.add_data(AutomationConstants.TEST_DATA, row.add_row(row_key))
    # endregion

    # region Data Setters
    def __print_data_access_error(self, data_type: str, file_path: str, e: Exception):
        if not os.path.exists(FileUtils.get_file_path_from_relative(file_path)):
            self.__logger.error('No ' + data_type + ' data file found')
        else:
            self.__logger.error('Error reading the ' + data_type + 'data'
                                + ': ' + str(e) if e else '')

    def add_global_data(self, test_data: DataObject):
        if self.__data.contains_key(AutomationConstants.GLOBAL_DATA):
            self.__data.replace_data(AutomationConstants.GLOBAL_DATA, test_data)
        else:
            self.__data.add_data(AutomationConstants.GLOBAL_DATA, test_data)

    def add_global_data_from_file(self, file_path: str):
        global_data: DataObject = None

        if file_path:
            try:
                global_data = DataObject(FileUtils.file_to_m_data(file_path))
                self.__data.set_key(AutomationConstants.GLOBAL_DATA)
            except Exception as e:
                self.__print_data_access_error('global', file_path, e)

        if global_data and self.__data.contains_key(AutomationConstants.GLOBAL_DATA):
            self.__data.replace_data(AutomationConstants.GLOBAL_DATA, global_data)
        elif global_data:
            self.__data.add_data(AutomationConstants.GLOBAL_DATA, global_data)
        else:
            self.__data.add_data(AutomationConstants.GLOBAL_DATA, DataObject().add_row('row'))

    def add_scenario_data(self, test_data: DataObject):
        if self.__data.contains_key(AutomationConstants.SCENARIO_DATA):
            self.__data.replace_data(AutomationConstants.SCENARIO_DATA, test_data)
        else:
            self.__data.add_data(AutomationConstants.SCENARIO_DATA, test_data)

    def add_scenario_data_from_file(self, file_path: str):
        scenario_data: DataObject = None

        if file_path:
            try:
                scenario_data = DataObject(FileUtils.file_to_dm_data(file_path))
                self.__data.set_key(AutomationConstants.SCENARIO_DATA)
            except Exception as e:
                self.__print_data_access_error('scenario', file_path, e)

        if scenario_data and self.__data.contains_key(AutomationConstants.SCENARIO_DATA):
            self.__data.replace_data(AutomationConstants.SCENARIO_DATA, scenario_data)
        elif scenario_data:
            self.__data.add_data(AutomationConstants.SCENARIO_DATA, scenario_data)

    def add_config_data(self, file_path: str):
        conf: DataObject = None

        try:
            conf = DataObject(FileUtils.file_to_m_data(file_path))
        except Exception as e:
            self.__print_data_access_error('configuration', file_path, e)

        if conf and self.__data.contains_key(AutomationConstants.CONFIGURATION_DATA):
            self.__data.replace_data(AutomationConstants.CONFIGURATION_DATA, conf)
        elif conf:
            self.__data.add_data(AutomationConstants.CONFIGURATION_DATA, conf)
        else:
            self.__data.add_data(AutomationConstants.CONFIGURATION_DATA, DataObject().add_row('row'))

    def add_test_data_from_file(self, file_path: str):
        test_data: DataObject = None

        if file_path:
            try:
                test_filter = os.environ.get(AutomationConstants.TEST_FILTER)
                csv_matrix = FileUtils.csv_file_to_matrix(file_path, True)

                if test_filter:
                    remove_indexes = ArrayUtils.get_filters_indexes(test_filter, csv_matrix)
                    csv_matrix = ArrayUtils.remove_rows_from_matrix(remove_indexes, csv_matrix, True)

                test_data = DataObject(
                    FileUtils.csv_string_to_m_data(ArrayUtils.matrix_to_string(csv_matrix, '\n', ';')))
                self.__data.set_key(AutomationConstants.TEST_DATA)

            except Exception as e:
                self.__logger.print_stack_trace(e)
                self.__print_data_access_error('test', file_path, e)
        else:
            test_data = DataObject().add_row('0')
            test_data.set_value('id', '0')

        if test_data and self.__data.contains_key(AutomationConstants.TEST_DATA):
            self.__data.replace_data(AutomationConstants.TEST_DATA, test_data)
        elif test_data:
            self.__data.add_data(AutomationConstants.TEST_DATA, test_data)

    def add_test_data(self, test_data):
        if isinstance(test_data, DataObject):
            if self.__data.contains_key(AutomationConstants.TEST_DATA):
                self.__data.replace_data(AutomationConstants.TEST_DATA, test_data)
            else:
                self.__data.add_data(AutomationConstants.TEST_DATA, test_data)

        elif isinstance(test_data, str):
            data_object: DataObject = None
            file_path = test_data

            if file_path:
                try:
                    test_filter = InitUtils.get_argument(AutomationConstants.TEST_FILTER)
                    csv_matrix = FileUtils.csv_file_to_matrix(file_path, True)

                    if test_filter:
                        remove_indexes = ArrayUtils.get_filters_indexes(test_filter, csv_matrix)

                        # TODO check method
                        csv_matrix = ArrayUtils.remove_rows_from_matrix(remove_indexes, csv_matrix, True)

                    data_object = DataObject(FileUtils.csv_string_to_m_data(
                        ArrayUtils.matrix_to_string(csv_matrix, "\n", ";")))
                    self.__data.set_key(AutomationConstants.TEST_DATA)
                except Exception as e:
                    self.__logger.print_stack_trace(e)
                    self.__print_data_access_error("test", file_path, e)
            else:
                data_object = DataObject().add_row("0")
                data_object.set_value("id", "0")

            if data_object:
                self.__data.add_data(AutomationConstants.TEST_DATA, data_object)

    def add_data(self, data_object: DataObject, data_key: str):
        if self.__data.contains_key(data_key):
            self.__data.replace_data(data_key, data_object)
        else:
            self.__data.add_data(data_key, data_object)

    def add_dm_data(self, file_path: str, data_key: str):
        if os.path.isabs(file_path):
            file_path = os.path.join(AutomationConstants.RESOURCES_FOLDER, file_path)

        data_object: DataObject = DataObject(FileUtils.file_to_dm_data(file_path))

        if self.__data.contains_key(data_key):
            self.__data.replace_data(data_key, data_object)
        else:
            self.__data.add_data(data_key, data_object)

    def add_m_data(self, file_name: str, data_key: str):
        if os.path.isabs(file_name):
            file_name = os.path.join(AutomationConstants.RESOURCES_FOLDER, file_name)
        data_object: DataObject = DataObject(FileUtils.file_to_m_data(file_name))

        if self.__data.contains_key(data_key):
            self.__data.replace_data(data_key, data_object)
        else:
            self.__data.add_data(data_key, data_object)
    # endregion
