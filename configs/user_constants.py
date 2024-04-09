
import os
from datetime import datetime
from enum import Enum
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_SHEET = os.path.join(os.sep, BASE_DIR, "data\\input_date.xlsx")
LOG_FILE = os.path.join(os.sep, BASE_DIR, f"logs\\{datetime.today().strftime('%d_%B_%y')}.log")
PYTEST_JSON = os.path.join(os.sep, BASE_DIR, "result\\pytest.json")
CHROME_DRIVER = os.path.join(os.sep, BASE_DIR, "driver\\chromedriver.exe")
FIREFOX_DRIVER = os.path.join(os.sep, BASE_DIR, "driver\\firefoxdriver.exe")
IE_DRIVER = os.path.join(os.sep, BASE_DIR, "driver\\IEdriver.exe")
ENV_URL = "https://www.google.com/"
TMP_CMD_LINE_ARGS_JSON = os.path.join(os.sep, BASE_DIR, "data\\temp_cmd_line_args.json")
TEST_UPLOAD_FILE = os.path.join(os.sep, BASE_DIR, "driver\\IEdriver.exe")
DOWNLOAD_DIRECTORY = os.path.join(os.sep, BASE_DIR, "downloads")


def default_db_vars(Enum):
    """ Enum for database constants """
    DB_INSTANCE = ''
    DB_HOST = ''
    DB_USER = ''
    DB_PASS = ''
    DB_CONNECT_PORT = ''
