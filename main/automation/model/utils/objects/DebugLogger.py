import datetime
import inspect


class DebugLogger:

    __id: str = None
    __verbose = True

    def __init__(self, thread_id: str = None):
        self.__id = thread_id

    # region Getter & Setter
    def get_id(self):
        return self.__id

    def set_id(self, id_):
        self.__id = id_
        return self

    def set_verbose(self, __verbose):
        self.__verbose = __verbose
        return self
    # endregion

    # region Methods
    def begin(self):
        if self.__verbose:
            self.debug_begin(self.__id)

    def end(self):
        if self.__verbose:
            self.debug_end(self.__id)

    def info(self, *message: str):
        if self.__verbose:
            self.debug_info(*message, thread_id=self.__id)

    def error(self, *message: str):
        if self.__verbose:
            self.debug_error(*message, thread_id=self.__id)

    def print_stack_trace(self, exception):
        import traceback

        if self.__verbose and exception:
            print("Error:", exception)
            traceback.print_exc()
    # endregion

    # ------------------------------------------------------------------------------

    # region Static Methods
    @staticmethod
    def __get_class_name() -> str:
        return inspect.getouterframes(inspect.currentframe())[0][1].split('/')[-1]

    @staticmethod
    def __get_method_name() -> str:
        method_name = inspect.getframeinfo(inspect.stack()[DebugLogger.__get_layer_number()][0]).function

        return method_name if not str(method_name).startswith("__") else method_name[2:]

    @staticmethod
    def __get_line_number() -> int:
        return inspect.stack(inspect.getlineno(inspect.stack()[2][0]))

    @staticmethod
    def __get_layer_number():
        number: int = 0

        while True:
            class_name = inspect.stack()[number][1].replace('\\', '/').split('/')[-1]

            if 'DebugLogger.py' not in class_name:
                break

            number += 1

        if not (str(inspect.getframeinfo(inspect.stack()[number - 2][0]).function)
                .endswith(inspect.getframeinfo(inspect.stack()[number][0]).function)):
            number -= 1

        return number

    @staticmethod
    def __get_debug_line():
        time_stamp: str = datetime.datetime.now().strftime("%d.%m.%Y %H.%M.%S")

        line: int = inspect.getframeinfo(
            inspect.stack()[DebugLogger.__get_layer_number()][0]).lineno

        class_name = inspect.getframeinfo(
            inspect.stack()[DebugLogger.__get_layer_number()][0]).filename.replace('\\', '/').split('/')[-1]

        return time_stamp + " - " + class_name + ":" + str(line)

    @staticmethod
    def __message_to_string(*message):
        result_message: str = ""

        for i in range(len(*message)):
            if i != 0:
                result_message += " "

            result_message += str(list(*message)[i])

        return result_message

    @staticmethod
    def debug_begin(thread_id: str = None):
        print(DebugLogger.__get_debug_line() + ' - [BEGIN] ' + (
            "(" + thread_id + ")" if thread_id else '') + " - " + DebugLogger.__get_method_name())

    @staticmethod
    def debug_end(thread_id: str = None):
        print(DebugLogger.__get_debug_line() + ' - [END] ' + (
            "(" + thread_id + ")" if thread_id else '') + " - " + DebugLogger.__get_method_name())

    @staticmethod
    def debug_info(*message: str, thread_id: str = None):
        print(DebugLogger.__get_debug_line() + ' - [INFO] ' + (
            "(" + thread_id + ")" if thread_id else '') + " - " + DebugLogger.__message_to_string(message))

    @staticmethod
    def debug_error(*message: str, thread_id: str = None):
        print(DebugLogger.__get_debug_line() + ' - [ERROR] ' + (
            "(" + thread_id + ")" if thread_id else '') + " - " + DebugLogger.__message_to_string(message))
    # endregion
