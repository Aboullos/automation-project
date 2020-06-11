from random import random

from main.automation.model.utils.ArrayUtils import ArrayUtils


class StringUtils:

    @staticmethod
    def get_random_number_chain(length: int) -> str:
        result = ''

        for _ in range(length):
            result += (str(int(random.random() * 9)))

        return result

    @staticmethod
    def get_random_letter_charin(length: int) -> str:
        result = ''

        for _ in range(length):
            result += chr(65 + int(random.random() * 25) + (32 if random.random() > 0.5 else 0))

        return result

    @staticmethod
    def csv_string_to_matrix(csv_string) -> list:
        return StringUtils.string_to_matrix(csv_string, '\n', ';')

    @staticmethod
    def price_to_ascii(data: str) -> str:
        allowed_chars = ['€', '£', '?', '?', '?', '?']
        return ''.join([d for d in data if 43 < ord(d) < 65 or d in allowed_chars])

    @staticmethod
    def string_to_matrix(csv_string: str, row_div: str, col_div: str) -> list:
        result: list = list()

        if csv_string:
            n_rows: int = StringUtils.count_occurrences_in_string(csv_string, row_div) + 1

            for i in range(n_rows):
                result[i] = csv_string.split(row_div)[i].split(col_div)

        return result

    @staticmethod
    def correct_url_slashes2(url: str) -> str:
        first_part, second_part = '', url

        if url.startswith('http'):
            first_part = url[0:url.index('://') + 3]
            second_part = url[url.index('://') + 3:]

        second_part = second_part.replace('/+', '/')

        return first_part + second_part

    @staticmethod
    def snake_case_to_natural(snake_case_text):
        return snake_case_text[0:1].upper() + snake_case_text[1:].lower().replace("_", " ")

    @staticmethod
    def camel_case_to_natural(camel_case_text: str) -> str:
        camel_case_text = ''.join(map(lambda x: x if x.islower() else " " + x, camel_case_text))
        return camel_case_text[0].upper() + camel_case_text[1:].lower()

    @staticmethod
    def natural_to_camel_case2(natural_text: str) -> str:
        natural_text = ''.join(map(lambda x: x if x is not ' ' else '', natural_text.title()))
        return natural_text[0].lower() + natural_text[1:]

    @staticmethod
    def natural_to_snake_case(natural_text: str) -> str:
        return natural_text[:].lower().replace(' ', '_')

    @staticmethod
    def replace_text_in_between(text: str, replace_string: str, left_substring: str, right_substring: str) -> str:
        text_inside = StringUtils.string_to_array_dividers(text, left_substring, right_substring)[0]

        return text.replace(left_substring + text_inside + right_substring,
                            left_substring + replace_string + right_substring)

    @staticmethod
    def string_to_d_m_row_by_divider(text: str, divider: str) -> dict:
        key = text[0:text.index(divider)]
        result = {key: text[text.index(divider) + 1:]}

        return result

    @staticmethod
    def string_to_dm_row(key_array: list, value_array: list) -> dict:
        result = dict()

        for i in range(len(value_array)):
            result[key_array[i]] = value_array[i]

        return result

    @staticmethod
    def m_row_to_string(mapped_row: dict, divider: str) -> str:
        result: str = str()
        for i, v in enumerate(mapped_row.values()):
            if i != 0:
                result += divider
            result += str(v)
        return result

    @staticmethod
    def m_data_to_string(mapped_data: dict, divider: str = None) -> str:
        divider = ';' if divider is None else divider

        result: str = str()
        key_set: list = list(mapped_data.keys())

        for i in range(len(key_set)):
            mapped_row = mapped_data.get(key_set[i])

            if i == 0:
                result += 'row' + divider + ArrayUtils.array_to_string(list(mapped_row.keys()), divider)
            result += '\n' + key_set[i] + divider + StringUtils.m_row_to_string(mapped_row, divider)

        return str(result)

    @staticmethod
    def count_occurrences_in_string(text: str, compare_string: str, divider_compare: str = ',') -> int:
        count = 0

        for c in compare_string.split(divider_compare):
            count += text.count(c)

        return count

    @staticmethod
    def string_to_array(text: str, divider: str) -> list:
        return text.split(divider)

    @staticmethod
    def string_to_array_dividers(text: str, left_divider: str, right_divider: str) -> list:
        result: list = list()

        while left_divider in text:
            left = text.index(left_divider) + len(left_divider)
            right = text.index(right_divider, left)
            result.append(text[left:right])
            text = text[right + 1:]

        return result

    @staticmethod
    def get_last_element_from_array(array: list) -> str:
        return array[-1]

    @staticmethod
    def is_number(string_number: str) -> bool:
        return str.isdigit(string_number)
