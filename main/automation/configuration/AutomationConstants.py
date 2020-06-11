import os

RESULT = "result"

TEST_SUCCESS = "SUCCESS"
TEST_FAILURE = "FAILURE"
TEST_UNDONE = "NOT EXECUTED"

MODIFIED_DATA_INITIAL_VALUE = "NOT_MODIFIED"

ROOT_PATH = os.path.normpath(os.path.dirname(os.path.realpath(__file__)) + "/../../..")
EXCEPTIONS_FOLDER = "exceptions/"
REPORTS_FOLDER = "reports/"
IMAGES_FOLDER = "images/"
DEBUG_IMAGES_FOLDER = "debug images/"
THUMBNAILS_FOLDER = "thumbnails/"
RESOURCES_FOLDER = "resources/"
TRANSLATIONS_FOLDER = 'translations/'

TESTCASE_REPLACE = "[TESTCASE]"

SUITE_DATA = "suite_data"
GLOBAL_DATA = "global_data"
SCENARIO_DATA = "scenario_data"
TEST_DATA = "test_data"
CONFIGURATION_DATA = "configuration"

SCENARIO_DATA_SET = "scenarioData.csv"
GLOBAL_DATA_SET = "globalData"
REPORTING_LVL_VERBOSE = "verbose"
REPORTING_LVL_NORMAL = "normal"

MAIN_DRIVER = "main_driver"
PROJECT_ID = "project_id"

# Driver type
WEB = "WEB"
MOBILE_WEB = "MOBILE_WEB"
MOBILE_APP = "MOBILE_APP"

# Configuration file variable names
APP_PACKAGE = "app_package"
REPORTING_LVL = "reporting_level"

API_URL = "api_url"
GET_CSV = "get_csv"
SEND_CSV = "send_csv"
SEND_IMG = "send_img"
CREATE_JIRA_TICKETS = "create_jira_tickets"
JIRA_TEST_ID = "jira_test_id"
JIRA_URL = "jira_url"
JIRA_USER = "jira_user"
JIRA_SECRET = "jira_secret"
JIRA_PROJECT = "jira_project"

SUCCESS_ZEPHYR = "SUCCESS"

FAILURE_ZEPHYR = "FAILURE"
NOT_EXECUTED_ZEPHYR = "NOT_EXECUTED"
EXECUTION_FILTER = "execution_filter"
TEST_FILTER = "test_filter"

TEST_ID = "test_id"
REPORT_PATH = "report_path"
RETRY_ON_FAIL = "retry"
MAX_TRIES = "max_tries"
BUILD_GROUP = "build_group"
EXECUTION_CASE = "execution_case"

BROWSER = "browser"
TIMEOUT = "timeout"
REMOTE_MODE = "remote"
FORCE_CACHE = "force_cache"
DRIVER_DOWNLOAD = "download"
DRIVER_PLUGINS = "driver_plugins"
MAXIMIZE_ON_START = "maximize"
WINDOW_HEIGHT = "window_height"
WINDOW_WIDTH = "window_width"
SMALL_WINDOW_LIMIT = "small_window_limit"
SHOW_CONSOLE_LOG = "show_console_log"
DRIVER_LANGUAGE = "language"
MOBILE_LANGUAGE = "mobile_language"
EMULATION_BROWSER = "emulation_browser"
ANDROID_EMULATOR = "android_emulator"
PLATFORM = "platform"
PLATFORM_NAME = "platformName"
DEVICE = "device"
DEVICE_NAME = "device_name"
DEVICE_VERSION = "device_version"
USE_PROXY = "use_proxy"

SESSION_ID = "session_id"
IP = "ip"
PORT = "port"
MOBILE_PORT = "mobile_port"

WAIT_FOR_PAGE = "wait_for_page"
WAIT_FOR_ANGULAR = "wait_for_angular"
WAIT_FOR_JQUERY = "wait_for_jquery"
IMPLICIT_WAIT = "implicit_wait"
PAGE_LOAD_WAIT = "page_load_wait"
SCRIPT_WAIT = "script_wait"