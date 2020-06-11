import numpy

from main.automation.data.DataObject import DataObject


class ArrayUtils:

    @staticmethod
    def remove_rows_from_matrix(indexes, matrix, header: bool):
        for i in range(len(matrix) - 1, 0 if header else 1):
            if i + 0 if header else 1 in indexes:
                matrix = ArrayUtils.remove_row_from_matrix(matrix, i)

    @staticmethod
    def remove_row_from_matrix(matrix, row: int):
        return ArrayUtils.remove_row_from_matrix_row_position(matrix, row, row)

    @staticmethod
    def remove_row_from_matrix_row_position(matrix, initial_row: int, final_row: int):
        result = matrix

        if len(matrix) > 0 and initial_row <= final_row:
            result = []

            for index, row in enumerate(matrix):
                if index < initial_row or index > final_row:
                    result[index] = row

        return result

    @staticmethod
    def join_integer_array(indexes_1: list, indexes_2: list) -> list:
        return list(numpy.unique(indexes_1 + indexes_2))

    @staticmethod
    def intercept_integer_array(indexes_1: list, indexes_2: list) -> list:
        return [x for x in indexes_1 if x in indexes_2]

    @staticmethod
    def get_filter_index(filters: list, matrix: list) -> list:
        indexes = []

        for i in range(1, len(matrix)):
            remove: bool = True

            for j in range(0, len(filters)):
                if ArrayUtils.get_position_in_array(matrix[0], filters[j][0]) < 0 or \
                        ((str(filters[j][1]).startswith('!') and
                         not (matrix[i][ArrayUtils.get_position_in_array(matrix[0], filters[j][0])] == str(
                            filters[j][1])[1:]) or matrix[i][
                                 ArrayUtils.get_position_in_array(matrix[0], filters[j][0])] == filters[j][1])):
                    remove = False

            if remove:
                indexes.append(i)

        return indexes

    @staticmethod
    def check_filter(indexes: list, matrix: list, unparsed_filter: str, div: str) -> list:
        if unparsed_filter is not None and unparsed_filter and len(unparsed_filter.split('=')) > 1 \
                and len(unparsed_filter.split('=')[1].split(div)) > 0:
            unparsed_key: str = unparsed_filter.split('=')[0]
            parsed_key = unparsed_key

            if len(unparsed_key) > 0 and unparsed_key[0] == '|':
                parsed_key: str = parsed_key[1:]

            filters = []

            for f in unparsed_filter.split('=')[1].split(div):
                filters.append([parsed_key, f])

            aux_indexes: list = ArrayUtils.get_filter_index(filters, matrix)

            if '|' in unparsed_key.replace(parsed_key, ''):
                indexes = ArrayUtils.intercept_integer_array(indexes, aux_indexes)
            elif '|' not in unparsed_key.replace(parsed_key, ''):
                indexes = ArrayUtils.join_integer_array(indexes, aux_indexes)

        return indexes

    @staticmethod
    def get_filters_indexes(filter_: str, matrix: list) -> list:
        div = ',' if ',' in filter_ else '\\.'
        indexes = []
        unparsed_filters = filter_.split('\\]')

        if len(unparsed_filters) > 0:
            unparsed_filters[0] = unparsed_filters[0].replace('[', '')
            unparsed_filters[len(unparsed_filters) - 1] = unparsed_filters[len(unparsed_filters) - 1].replace(']', '')

            for f in unparsed_filters:
                indexes = ArrayUtils.check_filter(indexes, matrix, f, div)

        return indexes

    @staticmethod
    def string_in_array(array: list, string: str) -> bool:
        return string in array

    @staticmethod
    def concat(first_array: list, second_array: list) -> list:
        return first_array + second_array

    @staticmethod
    def remove_element_from_array(array: list, value: str) -> list:
        result = array

        if result is not None:
            result = [x for x in array if x is not value]

        return result

    @staticmethod
    def add_index_to_matrix(matrix: [[]]):
        for matrix_index in range(len(matrix)):
            aux_array = [(len(matrix[matrix_index]) + 1)]
            aux_array[0] = str(matrix_index)

            for i in range(1, len(matrix[matrix_index])):
                aux_array[i] = matrix[matrix_index][i - 1]

            matrix[matrix_index] = aux_array

        return matrix

    @staticmethod
    def add_column_string_to_matrix(matrix: [[]], string: str, index: int = -1):
        index = len(matrix[0]) + index + 1 if index < 0 else index

        for matrix_index in range(len(matrix)):
            matrix[matrix_index].insert(index, string)

        return matrix

    @staticmethod
    def add_column_array_to_matrix(matrix: list, array: list, index: int = -1) -> list:
        index = len(matrix[0]) + index + 1 if index < 0 else index

        for matrix_index in range(len(matrix)):
            matrix[matrix_index].insert(index, array[matrix_index])

        return matrix

    @staticmethod
    def add_matrix_to_matrix(matrix: list, added_matrix: list) -> list:
        if matrix is None:
            return added_matrix

        if added_matrix is None:
            return matrix

        result = matrix

        if len(matrix) > 0 and len(added_matrix) > 0 and len(matrix[0]) == len(added_matrix[0]):
            result = matrix + added_matrix

        return result

    @staticmethod
    def remove_column_from_matrix(matrix: list, initial_row: int, final_row: int) -> list:
        result = matrix

        if initial_row == final_row and final_row != len(matrix):
            final_row += 1

        if initial_row <= final_row and len(matrix) > 0:
            for value in matrix:
                for i in range(initial_row, final_row):
                    value.pop(i)

        return result

    @staticmethod
    def matrix_to_csv_string(matrix: list) -> str:
        result = ''

        for index, sub_matrix in enumerate(matrix):
            for i, value in enumerate(sub_matrix):
                if i is not 0:
                    result += ';'
                if value is not None:
                    result += str(value)

            if index + 1 < len(matrix):
                result += '\n'

        return result

    @staticmethod
    def array_to_d_m_row(key_array: list, value_array: list) -> dict:
        return dict(zip(key_array, value_array))

    @staticmethod
    def matrix_to_d_m_data(matrix: list) -> DataObject:
        from main.automation.model.utils.FileUtils import FileUtils

        return DataObject(FileUtils.csv_string_to_m_data(ArrayUtils.matrix_to_string(matrix, '\n', ';')))

    @staticmethod
    def sub_array(array: list, initial_pos: int, final_pos: int) -> list:
        return [array[x] for x in range(initial_pos, final_pos)]

    @staticmethod
    def array_to_string(array: list, divider: str = ' ') -> str:
        result = ''

        for index, value in enumerate(array):
            if index != 0:
                result += divider
            result += value

        return result

    @staticmethod
    def matrix_to_string(matrix: list, line_div: str = '\n', column_div: str = '\t'):
        result: str = str()

        for index, value in enumerate(matrix):
            if index is not 0:
                result += line_div
            result += ArrayUtils.array_to_string(value, column_div)

        return result

    @staticmethod
    def contains(array: list, string: str) -> bool:
        return string in array

    @staticmethod
    def matrix_column_to_row(matrix: list, row_index: int) -> list:
        return [matrix[index][row_index] for index, value in enumerate(matrix)]

    @staticmethod
    def remove_rows_containing_value(matrix: [[]], value, index: int) -> list:
        return ArrayUtils.remove_rows_containing(matrix, [value], index)

    @staticmethod
    def remove_rows_containing(matrix: [[]], contains_array: list, index: int) -> [[]]:
        new_array = list()

        if index < 0:
            index += len(matrix[0])

        for i in range(len(matrix)):
            if matrix[i][index] not in contains_array:
                new_array.append(matrix[i])

        result = [[]] * len(new_array)
        for i in range(len(result)):
            result[i] = new_array[i]

        return result

    @staticmethod
    def remove_rows(matrix: list, list_: list):
        return [value for index, value in enumerate(matrix) if index not in list_]

    @staticmethod
    def count_occurrences(matrix: list, string: str, index: int) -> int:
        result = 0

        for value in matrix:
            result += 1 if value is not None and value[index] is not None and value[index] is string else 0

        return result

    @staticmethod
    def get_position_in_array(array: list, string: str):
        return array.index(string) if string in array else -1

    @staticmethod
    def string_array_to_int_array(array: list) -> list:
        return [int(value) for value in array]

    @staticmethod
    def integer_array_to_string_array(array: list) -> list:
        return [str(value) for value in array]

    @staticmethod
    def list_rows_containing_string3(matrix: list, string: str, index: int = -1) -> list:
        return [i for i, values in enumerate(matrix) if values[index] == string]
