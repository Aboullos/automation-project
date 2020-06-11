import os

from main.automation.configuration import AutomationConstants
from main.automation.model.utils.objects.DebugLogger import DebugLogger


class DataObject:

    __key: str = None
    __data: dict = None
    __logger: DebugLogger = DebugLogger()
    __NULL_POINTER_MESSAGE = 'NullPointerException: There is no row with value'

    # region Constructors
    def __init__(self, data: dict = None):
        if data is None:
            self.__data: dict = {}
        else:
            self.__data = data
            #if len(self.__data) is not 0:
            self.set_key(list(self.__data.keys())[0])

    # endregion

    # region Getters
    def size(self) -> int:
        return len(self.__data)

    def contains_key(self, key: str) -> bool:
        return key in self.__data.keys()

    def contains_value(self, value: str) -> bool:
        return value in self.__data.values()

    def get_key(self) -> str:
        return self.__key

    def get_key_set(self):
        return self.__data.keys()

    def get_row(self, value_key=None) -> dict:
        value_key = self.__key if value_key is None else value_key

        return self.__data.get(value_key)

    def get_data(self) -> dict:
        return self.__data

    def get_var(self, value_key: str, row_key: str = None):
        row_key = self.__key if row_key is None else row_key

        try:
            if row_key is not None:
                return self.get_row(row_key).get(value_key)
        except Exception:
            self.__logger.error(self.__NULL_POINTER_MESSAGE + ' \"' + str(row_key) + '\"')

        return None

    # endregion

    # region Setters
    def add_row(self, row_key: str, row: dict = None):
        if row_key not in self.__data:
            self.__data[row_key] = {} if row is None else row
            self.__key = row_key if self.__key is None and row is None else self.__key

    def set_key(self, key: str):
        if key not in self.__data:
            self.__logger.error(self.__NULL_POINTER_MESSAGE + '\"' + key + '\"')
        self.__key = key

    def set_value(self, value_key: str, value, row_key: str = None):
        row_key = self.__key if row_key is None else row_key

        if row_key is not None:
            self.get_row(row_key)[value_key] = value

    def duplicate_data_by_n(self, n: int):
        for i in range(1, n):
            for j in range(0, self.size()):
                self.duplicate_row(str(self.size() * i + j), str(j))

    def duplicate_row(self, new_row: str, row_key: str):
        __keys = self.__data[row_key]
        self.__data[new_row] = __keys

    def join_m_data(self, file_path):
        from main.automation.model.utils.FileUtils import FileUtils

        if file_path is not None and not os.path.isabs(file_path):
            file_path = AutomationConstants.RESOURCES_FOLDER + file_path
        __data_object: DataObject = DataObject(FileUtils.file_to_m_data(file_path))

        return __data_object

    def join_dm_data(self, file_path):
        from main.automation.model.utils.FileUtils import FileUtils

        if file_path is not None and not os.path.isabs(file_path):
            file_path = AutomationConstants.RESOURCES_FOLDER + file_path
        __data_object: DataObject = DataObject(FileUtils.file_to_dm_data(file_path))

        return __data_object

    def join_data(self, data_object):
        data_object: DataObject
        __keys = data_object.get_key_set()

        for k in __keys:
            self.add_row(k, data_object.get_row(k))

    # endregion
