import os

from main.automation.data.DataObject import DataObject
from main.automation.model.utils.ArrayUtils import ArrayUtils
from main.automation.model.utils.FileUtils import FileUtils
from main.automation.model.utils.StringUtils import StringUtils
from main.automation.model.utils.objects.DebugLogger import DebugLogger
from main.automation.model.utils.objects.HtmlElement import HtmlElement
from main.automation.configuration import AutomationConstants

style = "@import url(https://fonts.googleapis.com/css?family=Open+Sans);* { box-sizing: border-box; }html{  font-size: 62.5%;  text-size-adjust: 100%;}body {  font-family: 'Open Sans', sans-serif;  color: #4e4e4e;  height: 100%;  margin: 0;  font-size: 1.4rem;  line-height: 1.5;}/* STRUCTURE */.wrapper {  padding: 1.2rem 2.4rem;  max-width: 100%;  width: 100%;  margin: 0 auto;}header {  display: flex;  flex-flow: row wrap;  align-items: center;}header div {  flex: 1;  margin: 0 1.2rem 1.2rem 0;  padding: 0 1.2rem;}header div:last-child {  margin-right: 0;}@media screen and (max-width: 680px) {  header div {  flex-basis: 100%;      margin-right: 0;  }}@media screen and (min-width: 681px) {  header div {    flex-basis: 75%;  }  header div:last-child {    flex-basis: 20%;  }}.accordion .ac-button {cursor: pointer;}.boxes {  display: flex;  flex-flow: row wrap;  justify-content: center;}.boxes .box {  flex: 1;}.boxes .box:not(.result):not(.sum-up):not(.subtitle):not(h2):not(.case) {  margin: 0 1.2rem 1.2rem 0;  border-radius: 0.3rem;  padding: 1.2rem;}.boxes .box:last-child {  margin-right: 0;}.boxes .box .number {  line-height: 3.6rem;  font-weight: bold;}.boxes .box .number:not(.result) {  font-size: 4.5rem;  margin-bottom: 1.2rem;}.boxes .result {  font-size: 3rem;  margin-left: 1.2rem;  margin-bottom: 0.5rem;}.boxes .subtitle {  margin-left: 1.2rem;  margin-bottom: 0.5rem;}.boxes h2.box {  margin-left: 1.2rem;  margin-bottom: 0.5rem;}.boxes.thumbnails .box {  flex: none;  background-color: #F6F7F8;  border: 0.1rem solid #c2c2c2;  width: 9rem;  padding: 1.2rem 1.2rem 0.6rem;  text-align: center;}.boxes.thumbnails .box .number {  font-size: 2rem;  line-height: 2rem;}.exceptions .boxes.cases {  border-radius: 0.3rem;  background-color: #F6F7F8;  border: 0.1rem solid #c2c2c2;}.boxes.cases .box .number {  font-size: 2rem;  line-height: 2rem;}/* tablet */@media screen and (max-width: 980px) {  .boxes .box {    flex-basis: 40%;  }  .boxes .box:nth-child(2),  .boxes .box:nth-child(3) {    margin-right: 0;  }  .boxes.thumbnails .box:nth-child(2),  .boxes.thumbnails .box:nth-child(3) {    margin-right: 1.2rem;  }}/* mobile */@media screen and (max-width: 680px) {  .boxes .box {flex-basis: 100%;    margin-right: 0;  }  .boxes.thumbnails .box {    margin-right: 1.2rem;  }}.columns {  display: flex;  flex-flow: row wrap;  justify-content: center;}.columns-wrapper{  flex: 1;}.columns-wrapper .column{  background-color: #ffffff;  -webkit-box-shadow: 0px 5px 14px 0px rgba(255,255,255,0.5);  -moz-box-shadow: 0px 5px 14px 0px rgba(255,255,255,0.5);  box-shadow: 0px 5px 14px 0px rgba(255,255,255,0.5);}.columns-wrapper.exceptions {   margin-right: 0;}.column {  flex: 1;  padding: 1.2rem;  margin-bottom: 1.2rem;  border: 0.1rem solid #c2c2c2;  border-radius: 0.3rem;}/* tablet */@media screen and (min-width: 681px) {  .columns-wrapper {    margin-right: 2;    margin-left: 2;    flex-basis: 40%;  }  .columns-wrapper.exceptions {    flex-basis: 100%;  }  .columns .column {    flex-basis: 40%;  }  .columns-wrapper.exceptions .column{    flex-basis: 100%;  }  .columns .columns-wrapper:nth-child(2):not(.exceptions),  .columns .columns-wrapper.exceptions{    margin-right: 0;  }}/* mobile */@media screen and (max-width: 680px) {  .columns-wrapper{    background-color: #ffffff;  -webkit-box-shadow: 0px 5px 14px 0px rgba(109,174,229,1);  -moz-box-shadow: 0px 5px 14px 0px rgba(109,174,229,1);  box-shadow: 0px 5px 14px 0px rgba(109,174,229,1);    flex-basis: 100%;    margin-right: 0;    order: 1;  }  .columns-wrapper:nth-child(2):not(.exceptions){    order: 2;  }  .columns-wrapper.exceptions{    order: 3;    width: 100%;  }  .columns .column {    flex-basis: 100%;  }}.column h2{  padding-bottom: 0.6rem;  margin: 0 0 1.2rem 0;}/*COLORS*/.bg-white{  background-color: #ffffff;  -webkit-box-shadow: 0px 5px 14px 0px rgba(255,255,255,0.5);  -moz-box-shadow: 0px 5px 14px 0px rgba(255,255,255,0.5);  box-shadow: 0px 5px 14px 0px rgba(255,255,255,0.5);}.bg-yellow{  background-color: #E1BC29;  -webkit-box-shadow: 0px 5px 14px 0px rgba(198,162,15,0.5);  -moz-box-shadow: 0px 5px 14px 0px rgba(198,162,15,0.5);  box-shadow: 0px 5px 14px 0px rgba(198,162,15,0.5);}.bg-light-yellow{  background-color: #ffdb4c;  -webkit-box-shadow: 0px 5px 14px 0px rgba(255,241,186,0.5);  -moz-box-shadow: 0px 5px 14px 0px rgba(255,241,186,0.5);  box-shadow: 0px 5px 14px 0px rgba(255,241,186,0.5);}.bg-green{  background-color: #3BB273;  webkit-box-shadow: 0px 5px 14px 0px rgba(34,145,86,0.75);  -moz-box-shadow: 0px 5px 14px 0px rgba(34,145,86,0.75);  box-shadow: 0px 5px 14px 0px rgba(34,145,86,0.5);}.bg-light-green{  background-color: #5dd897;  webkit-box-shadow: 0px 5px 14px 0px rgba(163,255,206,0.75);  -moz-box-shadow: 0px 5px 14px 0px rgba(163,255,206,0.75);  box-shadow: 0px 5px 14px 0px rgba(163,255,206,0.5);}.bg-red{  background-color: #c62525;  -webkit-box-shadow: 0px 5px 14px 0px rgba(255,84,84,0.5);  -moz-box-shadow: 0px 5px 14px 0px rgba(255,84,84,0.5);  box-shadow: 0px 5px 14px 0px rgba(160,19,19,0.5);}.bg-light-red{  background-color: #e05555;  -webkit-box-shadow: 0px 5px 14px 0px rgba(252,118,118,0.5);  -moz-box-shadow: 0px 5px 14px 0px rgba(252,118,118,0.5);  box-shadow: 0px 5px 14px 0px rgba(252,118,118,0.5);}.clr-white{  color: #FFF;}.clr-red{  color: #CC444B;}/*TYPO*/h1{  font-size: 2.8rem;  margin: 0;}h2{  font-size: 2.2rem;}.boxes > h3{  margin: 0;  margin-top: 5;}/*FORMS*/.styled-select {  width: 30%;  height: 4rem;  overflow: hidden;  border: 1px solid #c2c2c2;  border-radius: 0.3rem;}.styled-select select {  background: transparent;  color: #4e4e4e;  width: 100%;  padding-left: 1rem;  font-size: 1.6rem;  line-height: 2rem;  border: 0;  border-radius: 0;  height: 4rem;}/*TABLES*/table{  border-collapse: collapse;  width: 100%;  background-color: #F8F8F9;}table thead tr th{  font-size: 1.6rem;  color: #507FA7;  text-align: center;}table tr td:first-of-type{  text-align: left;}div:not(.ac-content) > table tr{  border-bottom: 1px solid #c2c2c2;}thead:not(.ac-button) .boxes.cases .box:last-child {  margin-right: 40;}/* mobile */@media screen and (max-width: 680px) {  thead:not(.ac-button) .boxes.cases {    margin-right: 0;  }}img.responsive {  max-width: 100%;  height: auto;}.ac-button:hover svg{  fill: grey;}.boxes svg {  margin-top: 50%;}.exceptions .boxes.cases {  min-height: 40;  margin-bottom: 5;}.exceptions svg {  width: 40;  margin-top: 10;}.exceptions .box {  margin-top: 10;}.sum-up > .boxes > div > svg {  margin-right: 10;  margin-top: 10;}.sum-up > .boxes > h3 {  margin-right: 10;}.wrapper {  width: 98%;  margin-left: 1%;  margin-right: 1%;}.exceptions thead {  background: #ffffff;}.error {  color: #e05555;}.success {  color: #8aed80;}.wrapper > section > .columns-wrapper:not(.exceptions) {  margin-top: 20;}.sum-up {  color: white;}img.responsive {  cursor: pointer;}</style><style type='text/css' media='print'>body{font-family: Arial;}.columns{display: block;}.columns-wrapper{flex-basis: auto;}.column{flex-basis: auto;margin-bottom: 24px;padding: 12px;border: 1px solid #CCCCCC;}.boxes{display: block;padding: 12px 12px 0 12px;margin-bottom: 24px;}.boxes.thumbnails .box{display: inline-block;margin-right: 12px;margin-bottom: 12px;padding: 6px;border: 1px solid #e2e2e2;}.boxes svg{display: none;}tr:nth-child(even) {background: #CCC;}tr:nth-child(odd) {background: #FFF;}"


class CsvToHtml:

    _current_test_case = None
    _current_timestamp = None
    _report_path = None
    _data_matrix = None
    _translation_file = None
    _column_cases_order = None
    _test_stats: dict = None
    _logger = DebugLogger()
    _arrow = (HtmlElement("div")
              .add_child(HtmlElement("svg")
                         .add_attr("fill", "black")
                         .add_attr("fill-opacity", "0.4")
                         .add_attr("height", "15")
                         .add_attr("width", "30")
                         .create_child("path", "d='M0 0 L15 15 L30 0 Z'")))

    @staticmethod
    def _create_base_timestamp(test_cases, report_name, browser):
        return ("." + (AutomationConstants.TESTCASE_REPLACE if test_cases is None else report_name)
                + ("" if browser == "" else browser))

    @staticmethod
    def _get_date_format(date_format):
        import datetime
        return datetime.datetime.now().strftime(date_format)

    @staticmethod
    def _create_report_from_arguments(converter: 'CsvToHtml', args):
        browser = ""
        day = None
        month = None
        year = None
        report_name = None
        test_cases = None
        translation_file = None
        relevant_col = [-1]

        for argument in args:
            if str(argument).__contains__("=") and len(str(argument).split("=")) > 1:
                key = str(argument).split("=")[0]
                value = str(argument).split("=")[1]

                if key == "year":
                    year = value
                elif key == "month":
                    month = value
                elif key == "day":
                    day = value
                elif key == "date":
                    year = value.split(".")[0]
                    month = value.split(".")[1]
                    day = value.split(".")[2]
                elif key == "browser":
                    browser = value
                elif key == "report_name":
                    report_name = value
                elif key == "translation_file":
                    translation_file = value
                elif key == "relevant_columns":
                    relevant_col = value
                elif key == "test_cases":
                    test_cases = value.split(".") if "." in value else value.split(",")

        timestamp = CsvToHtml._create_base_timestamp(test_cases, report_name, browser)

        if not test_cases:
            test_cases = [report_name]
        if not year:
            year = CsvToHtml._get_date_format("yyyy")
        if not month:
            month = CsvToHtml._get_date_format("MM")
        if not day:
            day = CsvToHtml._get_date_format("dd")

        converter.set_report_path(AutomationConstants.ROOT_PATH + "/" + AutomationConstants.REPORTS_FOLDER
                                  + "/T" + year + month + day)
        converter.create_joint_report(year + "." + month + "." + day + timestamp,
                                      report_name, test_cases, relevant_col, translation_file)

    def _debug_info(self, *message):
        self._logger.info(*message)

    def _print_stack_trace(self, exception):
        self._logger.print_stack_trace(exception)

    def set_report_path(self, path):
        self._report_path = path

    def set_translation_file(self, translation_file):
        self._translation_file = translation_file

    def _create_report(self, timestamp, test_case, path, relevant_columns=-1, translation_file=None):
        self.set_report_path(path if path[-1] == "/" else path + "/")
        self.set_translation_file(translation_file)

        html_node: HtmlElement = self._create_test_case_wrapper(timestamp, test_case, relevant_columns)

        self._write_to_file(html_node, self._report_path + timestamp)

    def create_joint_report(self, timestamp, report_name, test_cases, relevant_columns, translation_file):
        self._debug_info("Generating report...")
        self.set_translation_file(translation_file)
        self.set_report_path(self._report_path if self._report_path[-1] == "/" else self._report_path + "/")

        timestamp_array = timestamp.split(".")
        for i in range(len(timestamp_array)):
            if not StringUtils.is_number(timestamp_array[i]):
                timestamp_array[i] = AutomationConstants.TESTCASE_REPLACE
                break

        timestamp = ArrayUtils.array_to_string(timestamp_array, ".")

        html_node: HtmlElement = self._create_joint_html_node(timestamp, report_name, test_cases, relevant_columns)

        if not os.path.exists(self._report_path):
            os.makedirs(self._report_path, exist_ok=True)

        self._write_to_file(html_node, self._report_path
                            + timestamp.replace(AutomationConstants.TESTCASE_REPLACE, report_name)
                            .replace("_headless", ""))

    def _translate_or_format(self, text):
        if self._translation_file:
            translation_object: DataObject = DataObject(
                FileUtils.file_to_m_data(AutomationConstants.RESOURCES_FOLDER + self._translation_file))

            if translation_object.get_var(text):
                result = translation_object.get_var(text)
            else:
                result = self._snake_case_to_natural(text)
        else:
            result = self._snake_case_to_natural(text)

        return result

    @staticmethod
    def _snake_case_to_natural(string: str) -> str:
        return string[0:1].upper() + string[1:].lower().replace("_", " ")

    @staticmethod
    def _initialize_dictionary(data_matrix) -> dict:
        result = dict()

        for i in range(len(data_matrix[0])):
            aux_dict = dict()

            for j in range(1, len(data_matrix)):
                if not aux_dict.get(data_matrix[j][i]):
                    aux_dict[data_matrix[j][i]] = [0, 0]

                if data_matrix[j][len(data_matrix[0]) - 3]:
                    if data_matrix[j][len(data_matrix[0]) - 3] == AutomationConstants.TEST_SUCCESS:
                        aux_dict[data_matrix[j][i]][0] += 1
                    elif data_matrix[j][len(data_matrix[0]) - 3] == AutomationConstants.TEST_FAILURE:
                        aux_dict[data_matrix[j][i]][1] += 1

            result[data_matrix[0][i]] = aux_dict

        return result

    @staticmethod
    def _get_column_order(data_matrix) -> dict:
        result = dict()

        for i in range(len(data_matrix[0])):
            column_order = []

            for j in range(1, len(data_matrix)):
                if data_matrix[j][i] and (data_matrix[j][i] not in column_order or len(column_order) == 0):
                    column_order.append(data_matrix[j][i])

            result[data_matrix[0][i]] = column_order

        return result

    def _create_images_table(self, column_results: dict, column_order: list, table_name) -> HtmlElement:
        container = HtmlElement("div")\
            .add_attr("class", "boxes thumbnails")\
            .add_attr("name", "table")

        for i in range(len(column_order)):
            test_variable = column_order[i]

            n_successes = column_results.get(column_order[i])[0]
            n_failures = column_results.get(column_order[i])[1]

            container.add_child(
                HtmlElement("div")
                    .add_attr("class", "box selectable")
                    .add_attr("name", test_variable)
                    .add_child(HtmlElement("img")
                               .add_attr("src", AutomationConstants.THUMBNAILS_FOLDER + test_variable + ".png")
                               .add_attr("alt",
                                         self._translate_or_format(test_variable).upper())
                               .add_attr("title",
                                         self._translate_or_format(test_variable).upper())
                               .add_attr("width", "50")
                               .add_attr("height", "50"))
                    .add_child(HtmlElement("div")
                               .add_attr("class", "number")
                               .create_child("span", "class=\"success\""
                                             + (" style=\"color: green;\"" if n_successes > 0 else ""), n_successes))
                    .add_child(HtmlElement("span")
                               .add_attr("class", "error")
                               .set_content(" / ")
                               .create_child("span",
                                             "style\"color: #CC444B;\"" if n_failures > 0 else "", n_failures)))

        return container

    def _create_table_by_index(self, column_results: dict, column_order: list, table_name) -> HtmlElement:
        table: HtmlElement = HtmlElement.create_table(len(column_order), 3)

        table.add_child_at(HtmlElement("thead")
                           .create_child("th", "", self._translate_or_format(table_name))
                           .create_child("th", "", self._translate_or_format("Success"))
                           .create_child("th", "", self._translate_or_format("Failure")), 0)

        table.get_child_by_tag("tbody").add_attr("name", "table")

        for i in range(len(column_order)):
            test_variable = column_order[i]

            n_successes = column_results.get(column_order[i])[0]
            n_failures = column_results.get(column_order[i])[1]

            row = table.get_child_by_tag("tbody").get_child(i)

            row.add_attr("class", "selectable")\
                .add_attr("name", test_variable)

            row.get_child(0).content = self._translate_or_format(test_variable)

            row.get_child(1).content = n_successes
            row.get_child(2).content = n_failures

            if n_successes > 0:
                row.get_child(1).add_attr("style", "color: green;")

            if n_failures > 0:
                row.get_child(2).add_attr("style", "color: red;")

        return table

    def _add_error_case(self, data_matrix, report_path, timestamp, accordion_content, index):
        table: HtmlElement = HtmlElement.create_table(1, 1)

        case_variables: HtmlElement = HtmlElement("div")\
            .add_attr("class", "boxes cases")

        for j in range(len(data_matrix[0]) - 4):
            case_variables.add_child(HtmlElement("div")
                                     .add_attr("class", "box case")
                                     .set_content(self._translate_or_format(data_matrix[0][j]) + ": "
                                                  + self._translate_or_format(data_matrix[index][j])))

        table.add_child_at(HtmlElement("thead")
                           .add_child(HtmlElement("tr")
                                      .add_child(HtmlElement("th")
                                                 .add_child(case_variables))), 0)

        image_path = "images/[ERROR] - " + timestamp + ".i" + str(index - 1) + ".png"
        exception = data_matrix[index][-1]
        exception = "" if not exception else exception

        if exception and exception.__contains__("."):
            exception = exception.split(".")[-1]

        if exception != "":
            table.get_child_by_tag("thead")\
                .add_attr("title", exception)

        if os.path.exists(report_path + image_path):
            table.add_attr("class", "accordion")\
                .get_child_by_tag("thead")\
                .add_attr("class", "ac-button")\
                .get_child_by_tag("tr")\
                .get_child_by_tag("th")\
                .get_child_by_tag("div")\
                .add_child(self._arrow)

            table.get_child_by_tag("tbody")\
                .add_attr("class", "ac-content")\
                .add_attr("style", "display: none;")\
                .get_child_by_tag("tr")\
                .get_child_by_tag("th")\
                .add_child(HtmlElement("img")
                           .add_attr("class", "responsive")
                           .add_attr("src", image_path)
                           .add_attr("alt", "Cannot load image"))
        else:
            table.remove_child_at(1)

        accordion_content.add_child(table)

    def _get_error_report_node(self, data_matrix, report_path, timestamp) -> HtmlElement:
        accordion_content = HtmlElement("div")\
            .add_attr("class", "ac-content")\
            .add_attr("style", "display: none;")

        for i in range(1, len(data_matrix)):
            if data_matrix[i][len(data_matrix[0]) - 3] and data_matrix[i][len(data_matrix[0]) - 3] == "FAILURE":
                self._add_error_case(data_matrix, report_path, timestamp, accordion_content, i)

        errors_node = (HtmlElement("div")
                       .add_attr("class", "accordion")
                       .add_child(HtmlElement("div")
                                  .add_attr("class", "boxes ac-button")
                                  .create_child("h2", "class=\"box\"", self._translate_or_format("Page Failures"))
                                  .add_child(self._arrow))
                       .add_child(accordion_content))

        return HtmlElement("div")\
            .add_attr("class", "columns-wrapper exceptions")\
            .add_child(HtmlElement("div")
                       .add_attr("class", "column bg-white")
                       .add_child(errors_node))

    def _create_header(self, test_case, n_successes, n_failures, wrapper_color):
        browser_element: HtmlElement = HtmlElement("")

        if self._column_cases_order[AutomationConstants.BROWSER]\
                and len(self._column_cases_order[AutomationConstants.BROWSER]) == 1:
            browser_element = (HtmlElement("h3").set_content(self._translate_or_format("Browser") + ": "
                               + self._translate_or_format(self._column_cases_order[AutomationConstants.BROWSER][0])))
        elif self._column_cases_order[AutomationConstants.BROWSER]\
                and len(self._column_cases_order[AutomationConstants.BROWSER] == 1):
            select: HtmlElement = HtmlElement("select")\
                .add_child(HtmlElement("option")
                           .add_attr("disabled", "")
                           .add_attr("selected", "")
                           .set_content(self._translate_or_format("Browser")))

            for i in range(len(self._column_cases_order[AutomationConstants.BROWSER])):
                select.add_child(HtmlElement("option")
                                 .set_content(self._translate_or_format(
                                                self._column_cases_order[AutomationConstants.BROWSER][i])))

            browser_element = HtmlElement("div")\
                .add_attr("class", "styled-select")\
                .add_child(select)

        success_style = " style=\"color: white;\"" if n_successes == 0 else ""
        failure_style = " style=\"color: white;\"" if n_failures == 0 else ""

        return HtmlElement("section")\
            .add_attr("class", "boxes ac-button")\
            .add_child(HtmlElement("div")
                       .add_attr("class", "box sum-up bg-" + wrapper_color)
                       .add_child(HtmlElement("div")
                                  .add_attr("class", "boxes")
                                  .create_child("h2", "class=\"box subtitle\"", self._translate_or_format(test_case))
                                  .add_child(browser_element))
                       .add_child(HtmlElement("div")
                                  .add_attr("class", "boxes")
                                  .add_child(HtmlElement("div")
                                             .add_attr("class", "box number result")
                                             .create_child("", "", str(n_successes + n_failures) + " (")
                                             .create_child("span", "class=\"success\"" + success_style,
                                                           str(n_successes))
                                             .create_child("", "", "/")
                                             .create_child("span", "class=\"error\"" + failure_style,
                                                           str(n_failures))
                                             .create_child("", "", ")"))
                                  .add_child(self._arrow)))

    def _create_table(self, index):
        have_images = True
        variables = self._column_cases_order[self._data_matrix[0][index]]

        for variable in variables:
            if not os.path.exists(self._report_path + AutomationConstants.THUMBNAILS_FOLDER + "/" + variable + ".png"):
                have_images = False
                break

        if have_images:
            variable_data = self._create_images_table(self._test_stats[self._data_matrix[0][index]],
                                                      self._column_cases_order[self._data_matrix[0][index]],
                                                      self._data_matrix[0][index])
        else:
            variable_data = self._create_table_by_index(self._test_stats[self._data_matrix[0][index]],
                                                        self._column_cases_order[self._data_matrix[0][index]],
                                                        self._data_matrix[0][index])

        return HtmlElement("div")\
            .add_attr("class", "column bg-white")\
            .add_attr("name", self._data_matrix[0][index])\
            .create_child("h2", "", self._translate_or_format(self._data_matrix[0][index]))\
            .add_child(variable_data)

    @staticmethod
    def _modify_accordion_content(accordion_content, timestamp, test_case, relevant_columns):
        return accordion_content

    @staticmethod
    def _modify_wrapper_content(wrapper, timestamp, test_case, relevant_columns):
        return wrapper

    @staticmethod
    def _modify_content(html_node, timestamp, test_case, relevant_columns):
        return html_node

    def _update_relevant_column(self, relevant_column):
        aux_relevant_column = relevant_column

        if aux_relevant_column == -1:
            aux_relevant_column = len(self._data_matrix[0]) - 3 \
                                  - (1 if AutomationConstants.BROWSER in self._data_matrix[0] else 0)
        elif aux_relevant_column > len(self._data_matrix[0]):
            aux_relevant_column = len(self._data_matrix[0])

        return aux_relevant_column

    @staticmethod
    def _get_wrapper_color(n_successes, n_failures):
        wrapper_color = "white"

        if n_successes > 0 and n_failures == 0:
            wrapper_color = "green"
        elif n_failures > 0 and n_successes == 0:
            wrapper_color = "red"
        elif n_successes > 0 and n_failures > 0:
            wrapper_color = "yellow"

        return wrapper_color

    def _add_relevant_tables(self, accordion_content, relevant_columns):
        for i in range(relevant_columns):
            if i == 0 or i == 1:
                accordion_content.create_child("div", "class=\"columns-wrapper\"")

            accordion_content.get_child(i % 2).add_child(self._create_table(i))

    def _create_test_case_wrapper(self, timestamp: str, test_case: str, relevant_column: int) -> HtmlElement:
        wrapper = None
        final_path = self._report_path + timestamp + ".csv"

        if os.path.exists(final_path):
            wrapper = (HtmlElement("div")
                       .add_attr("id", test_case))

            self._data_matrix = FileUtils.csv_file_to_matrix(final_path)
            self._data_matrix = ArrayUtils.remove_rows_containing(self._data_matrix,
                                                                  AutomationConstants.TEST_UNDONE, -3)

            if len(self._data_matrix) > 1:
                try:
                    self._test_stats = self._initialize_dictionary(self._data_matrix)
                    self._column_cases_order: dict = self._get_column_order(self._data_matrix)

                    self._copy_images_folder(self._report_path, self._test_stats)

                    relevant_column = self._update_relevant_column(relevant_column)

                    results_dict = self._test_stats[self._data_matrix[0][-3]]

                    n_success = results_dict[AutomationConstants.TEST_SUCCESS][0]\
                        if AutomationConstants.TEST_SUCCESS in results_dict else 0
                    n_failures = results_dict[AutomationConstants.TEST_FAILURE][1]\
                        if AutomationConstants.TEST_FAILURE in results_dict else 0

                    wrapper_color = CsvToHtml._get_wrapper_color(n_success, n_failures)

                    wrapper.add_attr("class", "wrapper column accordion bg-light-" + wrapper_color)

                    wrapper.add_child(self._create_header(test_case, n_success, n_failures, wrapper_color))

                    accordion_content = (HtmlElement("section")
                                         .add_attr("class", "columns ac-content"))

                    self._add_relevant_tables(accordion_content, relevant_column)

                    if self._column_cases_order[AutomationConstants.RESULT]\
                            .__contains__(AutomationConstants.TEST_FAILURE):
                        accordion_content.add_child(
                            self._get_error_report_node(self._data_matrix, self._report_path, timestamp))

                    self._modify_accordion_content(accordion_content, timestamp, test_case, relevant_column)

                    wrapper.add_child(accordion_content)
                except Exception as e:
                    self._print_stack_trace(e)

            self._modify_wrapper_content(wrapper, timestamp, test_case, relevant_column)

        return wrapper

    def _create_script_matrix(self, relevant_column):
        result = self._current_test_case + "_matrix = ["

        for i in range(len(self._data_matrix)):
            if i != 0:
                result += ", "

            result += "["

            for j in range(relevant_column):
                if j != 0:
                    result += ", "

                result += "'" + self._data_matrix[i][j] + "'"

            aux_result = ""

            if self._data_matrix[0].index(AutomationConstants.RESULT) >= relevant_column:
                aux_result += ", '" + (AutomationConstants.RESULT if i == 0 else self._data_matrix[i][-3]) + "'"

            result += aux_result + "]"

        return result + "];\n\n"

    def _create_joint_html_node(self, timestamp, report_name, test_cases, relevant_columns) -> HtmlElement:
        javascript_matrix = ""
        date = timestamp.split(".")[2] + "/" + timestamp.split(".")[1] + "/" + timestamp.split(".")[0]
        body = HtmlElement("body")
        html_node = (HtmlElement("html")
                     .add_child(HtmlElement("head")
                                .create_child("meta", "charset=\"UTF-8\"")
                                .create_child("title", "", self._translate_or_format("Test report"))
                                .create_child("style", "type=\"text/css\"", style))
                     .add_child(body
                                .add_child(HtmlElement("header")
                                           .add_child(HtmlElement("div")
                                                      .add_attr("class", "title")
                                                      .add_attr("align", "center")
                                                      .create_child("h1", "",
                                                                    self._translate_or_format(
                                                                        "Report [suitename] from [date]")
                                                                    .replace("[date]", date)
                                                                    .replace("[suitename]",
                                                                             self._translate_or_format(report_name)))))))

        for i in range(len(test_cases)):
            self._current_test_case = test_cases[i]
            self._current_timestamp = timestamp.replace(AutomationConstants.TESTCASE_REPLACE, self._current_test_case)

            aux_node = self._create_test_case_wrapper(self._current_timestamp, test_cases[i], relevant_columns[i])

            if self._data_matrix:
                aux_relevant_column = self._update_relevant_column(relevant_columns[i])

                javascript_matrix = self._create_script_matrix(aux_relevant_column)

            if len(test_cases) > 1:
                aux_node.get_child(1).add_attr("style", "display: none;")

            if aux_node:
                html_node.get_child_by_tag("body").add_child(aux_node)
            else:
                self._debug_info("HTML not created, file not found: " + self._report_path + timestamp + ".csv")

            self._data_matrix = None
            self._current_test_case = None
            self._current_timestamp = None

        (html_node.get_child_by_tag("body")
         .add_child(HtmlElement("script")
                    .add_attr("type", "text/javascript")
                    .set_content("var els = document.querySelectorAll('.accordion');\n"
                                 + "for(var i = 0; i < els.length; i++) {\n"
                                 + "\tels[i].querySelector('.ac-button').addEventListener('click', function() {\n"
                                 + "\t\tvar content = this.nextElementSibling;\n"
                                 + "\t\tif(content.getAttribute('style') == 'display: none;') {\n"
                                 + "\t\t\tcontent.removeAttribute('style');\n"
                                 + "\t\t} else {\n"
                                 + "\t\t\tcontent.setAttribute('style', 'display: none;');\n"
                                 + "\t\t}\n"
                                 + "\t});\n"
                                 + "}\n\n"
                                 + "var imgEls = document.querySelectorAll('img.responsive');\n"
                                 + "for(var i = 0; i < imgEls.length; i++) {\n"
                                 + "\timgEls[i].addEventListener('click', function() {\n"
                                 + "\t\tvar content = this.parentElement.parentElement.parentElement;\n"
                                 + "\t\tif(content.getAttribute('style') == 'display: none;') {\n"
                                 + "\t\t\tcontent.removeAttribute('style');\n"
                                 + "\t\t} else {\n"
                                 + "\t\t\tcontent.setAttribute('style', 'display: none;');\n"
                                 + "\t\t}\n"
                                 + "\t});\n"
                                 + "}")))

        (html_node.get_child_by_tag("body")
         .add_child(HtmlElement("script")
                    .add_attr("type", "text/javascript")
                    .set_content(javascript_matrix
                                 + "var els = document.querySelectorAll('.selectable');\n"
                                 + "for(var i = 0; i < els.length; i++) {\n"
                                 + "\tels[i].addEventListener('click', function() {\n"
                                 + "\t\tclassName = this.getAttribute('class');\n\n"
                                 + "\t\tif(className.indexOf('selected') > 0) {\n"
                                 + "\t\t\tthis.setAttribute('class', className.replace(' selected', ''));\n"
                                 + "\t\t\tthis.removeAttribute('style');\n"
                                 + "\t\t} else {\n"
                                 + "\t\t\tthis.setAttribute('class', className + ' selected');\n"
                                 + "\t\t\tthis.setAttribute('style', 'border-width: 5; border-color: #6b85af;');\n"
                                 + "\t\t}\n\n"
                                 + "\t\tvar wrapper = this.parentElement.parentElement;\n\n"
                                 + "\t\tif(this.tagName != 'DIV') {\n"
                                 + "\t\t\twrapper = wrapper.parentElement;\n"
                                 + "\t\t}\n\n"
                                 + "\t\tupdateTables(wrapper.parentElement.parentElement.parentElement);\n"
                                 + "\t});\n"
                                 + "}\n\n"
                                 + "function updateTables(wrapper) {\n"
                                 + "\tvar columns = [];\n"
                                 + "\tvar itemsSelected = [];\n"
                                 + "\tvar tables = wrapper.querySelectorAll('[name=\"table\"]');\n"
                                 + "\tvar matrix = window[wrapper.getAttribute('id') + '_matrix'];\n\n"
                                 + "\tfor(var i = 0; i < matrix[0].length - 1; i++) {\n"
                                 + "\t\tvar auxColumns = [];\n\n"
                                 + "\t\tfor(var j = 1; j < matrix.length; j++) {\n"
                                 + "\t\t\tif(auxColumns.length == 0 || auxColumns.indexOf(matrix[j][i]) < 0) {\n"
                                 + "\t\t\t\tauxColumns.push(matrix[j][i]);\n"
                                 + "\t\t\t}\n"
                                 + "\t\t}\n\n"
                                 + "\t\tcolumns.push(auxColumns);\n"
                                 + "\t}\n\n"
                                 + "\tvar auxTables = [];\n\n"
                                 + "\tfor(var i = 0; i < matrix[0].length; i++) {\n"
                                 + "\t\tfor(var j = 0; j < tables.length; j++) {\n"
                                 + "\t\t\tvar tableContainer = tables[j].parentElement;\n\n"
                                 + "\t\t\tif(tables[j].tagName != 'DIV') {\n"
                                 + "\t\t\t\ttableContainer = tableContainer.parentElement;\n"
                                 + "\t\t\t}\n\n"
                                 + "\t\t\tif(tableContainer.getAttribute('name') == matrix[0][i]) {\n"
                                 + "\t\t\t\tauxTables.push(tables[j]);\n"
                                 + "\t\t\t\tbreak;\n"
                                 + "\t\t\t}\n"
                                 + "\t\t}\n"
                                 + "\t}\n\n"
                                 + "\ttables = auxTables;\n\n"
                                 + "\tfor(var i = 0; i < tables.length; i++) {\n"
                                 + "\t\tvar auxItemsSelected = [];\n"
                                 + "\t\tvar elementsSelected = tables[i].querySelectorAll('* > .selected');\n\n"
                                 + "\t\tfor(var j = 0; j < elementsSelected.length; j++) {\n"
                                 + "\t\t\tauxItemsSelected.push(elementsSelected[j].getAttribute('name'));\n"
                                 + "\t\t}\n\n"
                                 + "\t\tif(auxItemsSelected.length > 0) {\n"
                                 + "\t\t\titemsSelected.push(auxItemsSelected);\n"
                                 + "\t\t} else itemsSelected.push(columns[i]);\n"
                                 + "\t}\n\n"
                                 + "\tfor(var i = 0; i < tables.length; i++) {\n"
                                 + "\t\tvar selected = tables[i].querySelectorAll('* > [name].selected').length > 0;\n"
                                 + "\t\tvar elements = tables[i].querySelectorAll('* > [name]');\n\n"
                                 + "\t\tfor(var j = 0; j < elements.length; j++) {\n"
                                 + "\t\t\tvar selectedMatrix = [];\n"
                                 + "\t\t\tfor(var k = 0; k < tables.length; k++) {\n"
                                 + "\t\t\t\tif(k == i) {\n"
                                 + "\t\t\t\t\tselectedMatrix.push([elements[j].getAttribute('name')]);\n"
                                 + "\t\t\t\t} else {\n"
                                 + "\t\t\t\t\tif(itemsSelected[k] != undefined && itemsSelected[k].length > 0) {\n"
                                 + "\t\t\t\t\t\tselectedMatrix.push(itemsSelected[k]);\n"
                                 + "\t\t\t\t\t} else {\n"
                                 + "\t\t\t\t\t\tselectedMatrix.push(columns[k]);\n"
                                 + "\t\t\t\t\t}\n"
                                 + "\t\t\t\t}\n"
                                 + "\t\t\t}\n\n"
                                 + "\t\t\tvar result = countRows(selectedMatrix, columns, matrix);\n"
                                 + "\t\t\tvar successSelector, failureSelector;\n\n"
                                 + "\t\t\tif(elements[j].tagName == 'DIV') {\n"
                                 + "\t\t\t\tsuccessSelector = 'span:nth-of-type(1)';\n"
                                 + "\t\t\t\tfailureSelector = 'span:nth-of-type(3)';\n"
                                 + "\t\t\t} else {\n"
                                 + "\t\t\t\tsuccessSelector = 'th:nth-of-type(2)';\n"
                                 + "\t\t\t\tfailureSelector = 'th:nth-of-type(3)';\n"
                                 + "\t\t\t}\n\n"
                                 + "\t\t\tif(!selected || elements[j].getAttribute('class').indexOf('selected') > 0) {"
                                 + "\n"
                                 + "\t\t\t\telements[j].querySelector(successSelector).textContent = result[0];\n"
                                 + "\t\t\t\telements[j].querySelector(failureSelector).textContent = result[1];\n"
                                 + "\t\t\t} else {\n"
                                 + "\t\t\t\telements[j].querySelector(successSelector).textContent = '0';\n"
                                 + "\t\t\t\telements[j].querySelector(failureSelector).textContent = '0';\n"
                                 + "\t\t\t}\n"
                                 + "\t\t}\n"
                                 + "\t}\n"
                                 + "}\n\n"
                                 + "function countRows(selectedMatrix, columns, matrix) {\n"
                                 + "\tvar success = 0;\n"
                                 + "\tvar failure = 0;\n\n"
                                 + "\tfor(var i = 1; i < matrix.length; i++) {\n"
                                 + "\t\tvar found = true;\n"
                                 + "\t\tfor(var j = 0; j < matrix[0].length; j++) {\n"
                                 + "\t\t\tvar foundInSelectedMatrix = false;\n"
                                 + "\t\t\tif(selectedMatrix[j] != undefined && selectedMatrix[j].length > 0) {\n"
                                 + "\t\t\t\tfor(var k = 0; k < selectedMatrix[j].length; k++) {\n"
                                 + "\t\t\t\t\tif(selectedMatrix[j][k] == matrix[i][j]) {\n"
                                 + "\t\t\t\t\t\tfoundInSelectedMatrix = true;\n"
                                 + "\t\t\t\t\t\tbreak;\n"
                                 + "\t\t\t\t\t}\n"
                                 + "\t\t\t\t}\n"
                                 + "\t\t\t} else foundInSelectedMatrix = true;\n\n"
                                 + "\t\t\tif(!foundInSelectedMatrix) found = false;\n"
                                 + "\t\t}\n\n"
                                 + "\t\tif(found && matrix[i][matrix[0].indexOf('result')] == 'SUCCESS') {\n"
                                 + "\t\t\tsuccess++;\n"
                                 + "\t\t} else if(found && matrix[i][matrix[0].indexOf('result')] == 'FAILURE') {\n"
                                 + "\t\t\tfailure++;\n"
                                 + "\t\t}\n"
                                 + "\t}\n\n"
                                 + "\treturn [success, failure];\n"
                                 + "}"
                                 )))

        self._modify_content(html_node, timestamp, test_cases, relevant_columns)

        return html_node

    def _write_to_file(self, html_node: HtmlElement, path):
        if html_node:
            try:
                FileUtils.write_file(path + ".html", html_node.to_string())

                self._debug_info("HTML created")
            except Exception as e:
                self._print_stack_trace(e)

    def _copy_image(self, file_name, origin_path, destination_path):
        from shutil import copyfile

        try:
            copyfile(os.path.join(origin_path, file_name), os.path.join(destination_path, file_name))
        except Exception as e:
            self._print_stack_trace(e)

    def _copy_images_folder(self, report_path, test_stats: dict):
        origin_path = AutomationConstants.ROOT_PATH + AutomationConstants.RESOURCES_FOLDER\
                      + AutomationConstants.THUMBNAILS_FOLDER
        destination_path = report_path + AutomationConstants.THUMBNAILS_FOLDER

        if os.path.exists(origin_path):
            files_needed = list()

            for key in test_stats.keys():
                for variable in test_stats.get(key).keys():
                    files_needed.append(variable)

            os.makedirs(destination_path, exist_ok=True)

            for file_name in os.listdir(origin_path):
                self._copy_image(file_name, origin_path, destination_path)
