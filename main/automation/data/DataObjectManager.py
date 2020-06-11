from main.automation.data.DataObject import DataObject


class DataObjectManager:

    __key: str
    __mapped_data: dict = dict()

    def __init__(self, key=None, data=None):
        if key is not None and data is not None:
            self.__key = key

            if isinstance(data, DataObject):
                self.add_data(key, data)
            elif isinstance(data, dict):
                self.add_data(key, DataObject(data))

    # region Getters
    def get_data(self, data_key: str) -> DataObject:
        return self.__mapped_data.get(data_key)

    def get_key_set(self):
        return self.__mapped_data.keys()

    def size(self) -> int:
        return len(self.__mapped_data)

    def contains_key(self, data_key: str) -> bool:
        return data_key in self.__mapped_data.keys()

    def contains_value(self, data_value: str) -> bool:
        return data_value in self.__mapped_data.values()
    # endregion

    # region Setters
    def set_key(self, key: str):
        self.__key = key

    def add_data(self, key: str, data_object: DataObject):
        self.__mapped_data[key] = data_object

    def remove_data(self, key: str):
        if key in self.__mapped_data.keys():
            self.__mapped_data.pop(key)

    def replace_data(self, data_key: str, data_object: DataObject):
        self.remove_data(data_key)
        self.add_data(data_key, data_object)

    def add_m_data_from_file(self, key: str, file_name: str):
        from main.automation.model.utils.FileUtils import FileUtils

        self.add_data(key, DataObject(FileUtils.csv_file_to_m_data(file_name)))

    def add_dm_data_from_file(self, key: str, file_name: str):
        from main.automation.model.utils.FileUtils import FileUtils

        self.add_data(key, DataObject(FileUtils.csv_file_to_dm_data(file_name)))
        pass

    def get_var(self, key: str, row: str=None) -> str:
        result: str = None

        for _, data in self.__mapped_data.items():
            if row is None:
                row = data.get_key()

            if key in data.get_row(row).keys():
                result = data._get_var(key, row)
                break

        return result

    def set_value_in_row(self, row: str, key: str, value: str):
        mapped_keys = self.get_key_set()

        for k in mapped_keys:
            if self.__mapped_data.get(k).contains_key(row):
                data_key = k

                if self.__mapped_data.get(k).get_row(row).contains_key(key):
                    self.__mapped_data.get(k).set_value(row_key=row, value_key=key, value=value)
                    break
    # endregion
