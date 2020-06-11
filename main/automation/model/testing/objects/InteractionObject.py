import os

from main.automation.configuration import AutomationConstants
from main.automation.data.DataObject import DataObject
from main.automation.model.testing.UserStory import UserStory
from main.automation.model.utils.FileUtils import FileUtils
from main.automation.model.utils.objects.DebugLogger import DebugLogger


class InteractionObject:

    __test_id: str
    _user_s: UserStory
    __logger: DebugLogger

    def __init__(self, user_story: UserStory = None):
        if user_story:
            self._user_s = user_story
            self.__test_id = user_story.get_test_id()

            self.__logger = DebugLogger(self.__test_id)
        else:
            self.__logger = DebugLogger()

    # Get data methods
    def _get_data(self, key: str) -> DataObject:
        return self._user_s.get_data(key)

    def _get_config_var(self, key: str):
        return self._user_s.get_config_var(key)

    def _get_suite_var(self, key: str):
        return self._user_s.get_suite_var(key)

    def _get_global_var(self, key: str):
        return self._user_s.get_global_var(key)

    def _get_scenario_var(self, key: str):
        result: str = None

        if self._user_s is not None and self._user_s.get_scenario() is not None:
            result = self._user_s.get_scenario_var(key=key)

        return result

    def _get_test_var(self, key: str):
        return self._user_s.get_test_var(key)

    def _get_var(self, key: str, row_key: str = None):
        if row_key is None:
            return self._user_s.get_var(key=key)
        return self._user_s.get_var(key=key, row_key=row_key)

    # Set data methods
    def _set_data(self, data: DataObject, key: str):
        return self._user_s.add_data(data, key)

    def _set_config_var(self, key: str, value: str):
        return self._user_s.set_config_var(key=key, value=value)

    def _set_suite_var(self, key: str, value: str):
        self._user_s.set_suite_var(key, value)

    def _set_global_var(self, key: str, value: str):
        self._user_s.set_global_var(key, value)

    def _set_scenario_var(self, key: str, value: str):
        self._user_s.set_scenario_var(key, value)

    def _set_test_var(self, key: str, value: str):
        self._user_s.set_test_var(key, value)

    # FileUtils
    @staticmethod
    def get_path_with_resources(file_path: str):
        if (not os.path.exists(file_path)
                and not AutomationConstants.ROOT_PATH + '/' + file_path
                and AutomationConstants.ROOT_PATH + '/' + AutomationConstants.RESOURCES_FOLDER + file_path):
            file_path = AutomationConstants.ROOT_PATH + '/' + AutomationConstants.RESOURCES_FOLDER + file_path

        return file_path

    @staticmethod
    def csv_file_to_m_data(file_path: str):
        return FileUtils.csv_file_to_m_data(InteractionObject.get_path_with_resources(file_path))

    @staticmethod
    def csv_file_to_d_m_data(file_path: str):
        return FileUtils.csv_file_to_dm_data(InteractionObject.get_path_with_resources(file_path))

    @staticmethod
    def json_file_to_m_data(file_path):
        return FileUtils.json_file_to_m_data(InteractionObject.get_path_with_resources(file_path))

    @staticmethod
    def json_file_to_d_m_data(file_path):
        return FileUtils.json_file_to_dm_data(InteractionObject.get_path_with_resources(file_path))

    @staticmethod
    def variables_file_to_array(file_path):
        return FileUtils.variables_file_to_array(InteractionObject.get_path_with_resources(file_path))

    @staticmethod
    def append_matrix_to_csv_file(file_path: str, matrix: list):
        FileUtils.append_matrix_to_csv_file(InteractionObject.get_path_with_resources(file_path), matrix)

    @staticmethod
    def write_matrix_to_csv_file(file_path: str, matrix: list):
        FileUtils.write_matrix_to_csv_file(InteractionObject.get_path_with_resources(file_path), matrix)

    @staticmethod
    def csv_file_to_matrix(file_path: str):
        return FileUtils.csv_file_to_matrix(InteractionObject.get_path_with_resources(file_path))

    @staticmethod
    def read_file(file_path: str):
        return FileUtils.read_file(InteractionObject.get_path_with_resources(file_path))

    @staticmethod
    def write_file(file_path: str, text: str):
        FileUtils.write_file(InteractionObject.get_path_with_resources(file_path), text)

    @staticmethod
    def append_to_file(file_path: str, text: str):
        FileUtils.append_to_file(InteractionObject.get_path_with_resources(file_path), text)

    def delete_file_from_report_folder(self, file_path: str):
        if not os.path.exists(file_path) and os.path.exists(self._user_s.get_report_path() + file_path):
            file_path = self._user_s.get_report_path() + file_path

        FileUtils.delete_file(file_path)

    # Debug
    def debug_begin(self):
        self.__logger.begin()

    def debug_end(self):
        self.__logger.end()

    def debug_info(self, *message: str):
        self.__logger.info(*message)

    def debug_error(self, *message: str):
        self.__logger.error(*message)

    def print_stack_trace(self, exception: Exception):
        self.__logger.print_stack_trace(exception)
        pass

    def set_debug_verbose(self, verbose: bool):
        self.__logger.set_verbose(verbose)
