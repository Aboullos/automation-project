from collections import KeysView
from os import listdir
from os.path import isfile, join


class Translator:

    def __init__(self, language_folder: str):
        files = [f for f in listdir(language_folder) if isfile(join(language_folder, f))]
        self.__words = dict()
        self.languages = list()
        for file_name in files:
            language_name = file_name.split('.')[0]
            self.languages.append(language_name)
            self.__words[language_name] = dict()
            with open(language_folder + '/' + file_name, 'r') as language_file:
                for line in language_file:
                    key, name = line.replace('\n', '').split('=')
                    self.__words[language_name][key] = name
        self.language = 'EN'

    def __getitem__(self, n: str) -> str:
        if n in self.__words[self.language].keys():
            return self.__words[self.language][n]
        else:
            return n

    def keys(self) -> KeysView:
        return self.__words[self.language].keys()
