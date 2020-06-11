import os.path
import codecs
import json

from main.automation.configuration import AutomationConstants
from main.automation.model.utils.ArrayUtils import ArrayUtils
from main.automation.model.utils.StringUtils import StringUtils


class FileUtils:

    @staticmethod
    def get_file_path_from_relative(file_path: str, file_extensions=None) -> str:
        result = ""

        if isinstance(file_extensions, str):
            file_extensions = [file_extensions]
        elif file_extensions is None:
            file_extensions = ['']

        for extension in file_extensions:
            file_type_to_add = '' if file_path.endswith(extension) else extension

            if os.path.exists(file_path + file_type_to_add):
                result = file_path + file_type_to_add
            elif os.path.exists(AutomationConstants.ROOT_PATH + '/' + file_path + file_type_to_add):
                result = AutomationConstants.ROOT_PATH + '/' + file_path + file_type_to_add

        return result

    @staticmethod
    def file_to_m_data(file_path: str) -> dict:
        exist = False
        result = None

        if file_path:
            file_path = FileUtils.get_file_path_from_relative(file_path, ['.csv', '.json', '.properties', '.txt'])

            if file_path:
                exist = True

        if exist:
            if file_path.endswith(".csv"):
                result = FileUtils.csv_file_to_m_data(file_path)
            elif file_path.endswith(".json"):
                result = FileUtils.json_file_to_m_data(file_path)
            elif file_path.endswith(".properties") or file_path.endswith(".txt"):
                result = FileUtils.variables_file_to_array(file_path)

        return result

    @staticmethod
    def file_to_dm_data(file_path: str) -> dict:
        exist = False
        result = None

        if file_path is not None and file_path:
            file_path = FileUtils.get_file_path_from_relative(file_path, ('.csv', '.json'))

            if file_path:
                exist = True

        if exist:
            if file_path.endswith(".csv"):
                result = FileUtils.csv_file_to_dm_data(file_path)
            elif file_path.endswith(".json"):
                result = FileUtils.json_file_to_dm_data(file_path)

        return result

    @staticmethod
    def get_json_object_from_file(file_path: str) -> dict:
        return json.load(
            FileUtils.read_file(FileUtils.get_file_path_from_relative(file_path, '.json'))).getAdJsonObject()

    @staticmethod
    def dm_row_from_json_object_object(json_element: dict) -> dict:
        return {str(k): str(v) for k, v in json_element.items()}

    @staticmethod
    def json_object_to_data(json_object: dict, own_id: bool) -> dict:
        current_id = 0
        result: dict = {}

        if json_object is not None:
            if json_object['rows'] is None:
                result[json_object['name']] = FileUtils.dm_row_from_json_object_object(json_object['values'])
            else:
                for element in json_object['rows']:
                    if own_id:
                        key = str(element['name'])
                    else:
                        key = str(current_id) + ''
                        current_id += 1

                    result[key] = FileUtils.dm_row_from_json_object_object(element['values'])

        return result

    @staticmethod
    def json_file_to_m_data(file_path: str) -> dict:
        return FileUtils.json_object_to_data(FileUtils.get_json_object_from_file(file_path), False)

    @staticmethod
    def json_file_to_dm_data(file_path: str) -> dict:
        return FileUtils.json_object_to_data(FileUtils.get_json_object_from_file(file_path), True)

    @staticmethod
    def csv_file_to_matrix(file_path: str, own_id: bool = True) -> list:
        return FileUtils.csv_string_to_matrix(
            FileUtils.read_file(FileUtils.get_file_path_from_relative(file_path, '.csv')), own_id)

    @staticmethod
    def csv_string_to_matrix(csv_string: str, own_id: bool) -> list:
        n_lines: int = 0 if not csv_string \
            else csv_string.count('\n') + 1

        return FileUtils.csv_section_to_matrix(csv_string, 0, n_lines, own_id)

    @staticmethod
    def csv_section_to_matrix(text: str, initial_line: int, final_line: int, own_id: bool) -> list:
        n_id = 0
        text_array = StringUtils.string_to_array(text, '\n')
        matrix = [[]]

        if len(text_array) > 0:
            matrix = [[None] * (str(text_array[0]).count(";") + 1 + (0 if own_id else 1))] * (final_line - initial_line)

            for i in range(final_line):
                if i >= initial_line:
                    matrix[n_id] = StringUtils.string_to_array(
                        ('' if own_id else str(i - initial_line) + ';') + text_array[i], ';')
                    n_id += 1

        return matrix

    @staticmethod
    def append_matrix_to_csv_file(file_path: str, matrix: list):
        separator = ''

        if os.path.exists(file_path):
            text = FileUtils.read_file(file_path)

            if text is not None and text:
                separator = '\n'

        FileUtils.append_to_file(file_path, separator + ArrayUtils.matrix_to_csv_string(matrix))

    @staticmethod
    def append_to_file(file_path: str, text: str):
        try:
            file_handler = codecs.open(file_path, mode='a+', encoding='utf-8')
            file_handler.write(text)
            file_handler.close()
        except IOError as e:
            print("Error appending to file: {0}".format(e.strerror))

    @staticmethod
    def write_matrix_to_csv_file(file_path: str, matrix: list):
        FileUtils.write_file(file_path, ArrayUtils.matrix_to_csv_string(matrix))

    @staticmethod
    def write_file(file_path: str, text: str):
        try:
            file_handler = open(file_path, mode='w+', encoding='utf-8')
            file_handler.write(text)
            file_handler.close()
        except IOError as e:
            print("Error appending to file: {0}".format(e.strerror))

    @staticmethod
    def read_file(file_path: str, charset: str = 'utf-8') -> str:
        text: str = ''

        if file_path is not None and file_path:
            file_path = FileUtils.get_file_path_from_relative(file_path)

            try:
                file_handler = codecs.open(file_path, mode='r', encoding=charset)

                for line in file_handler.readlines():
                    text += line.replace('\r', '')

                file_handler.close()
            except IOError as e:
                print("Error accessing file: {0}".format(e.strerror))

        return text

    @staticmethod
    def delete_file(file_path: str) -> bool:
        try:
            os.remove(file_path)
            return not os.path.exists(file_path)
        except IOError:
            print("Error: File doesn't exist or can't find it")

    @staticmethod
    def csv_file_to_m_data(file_path: str) -> dict:
        result: dict = {}

        if file_path is not None and file_path:
            file_path = FileUtils.get_file_path_from_relative(file_path, '.csv')

            result = FileUtils.csv_string_to_m_data(FileUtils.read_file(file_path=file_path))

        return result

    @staticmethod
    def csv_string_to_m_data(csv_string: str) -> dict:
        result: dict = {}

        if csv_string is not None:
            csv_lines = csv_string.split('\n')
            key_array = StringUtils.string_to_array('row;' + csv_lines[0], ';')

            for i in range(1, len(csv_lines)):
                result[str(i - 1)] = StringUtils.string_to_dm_row(key_array, StringUtils.string_to_array(
                    str(i - 1) + ';' + csv_lines[i], ';'))

        return result

    @staticmethod
    def csv_file_to_dm_data(file_path: str) -> dict:
        key_array: list = None
        result: dict = {}

        file_path = FileUtils.get_file_path_from_relative(file_path)

        try:
            file_handler = codecs.open(file_path, mode='r', encoding='utf-8')
            for line in file_handler.readlines():
                key = line[0: line.index(';') if line.index(';') >= 0 else len(line)]

                if key_array is None:
                    key_array = StringUtils.string_to_array(line, ';')
                else:
                    result[key] = StringUtils.string_to_dm_row(key_array, StringUtils.string_to_array(line, ';'))

            file_handler.close()
        except IOError as e:
            print("File not found: {0}".format(e.strerror))

        return result

    @staticmethod
    def variables_file_to_array(file_path: str) -> dict:
        line_list: list = []
        aux_dict: dict = {}
        result: dict = {}

        file_path = FileUtils.get_file_path_from_relative(file_path)

        try:
            file_handler = codecs.open(file_path, mode='r', encoding='utf-8')

            for line in file_handler.readlines():
                if line and line[0] != '#':
                    line_list.append(line.replace('\n', '').replace('\r', ''))

            for i in line_list:
                if '=' in i and len(i.split('=')) == 2:
                    aux_dict[StringUtils.string_to_array(i, '=')[0]] = StringUtils.string_to_array(i, '=')[1]

                    file_handler.close()

            result['row'] = aux_dict
        except IOError as e:
            print("File not found: {0}".format(e.strerror))

        return result
