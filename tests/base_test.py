import os
import pytest

from configs.user_constants import SCREENSHOTS_DIR
from utils.logging_util import logger


@pytest.mark.usefixtures('cmd_line_args')
class BaseTest:
    """ """

    @classmethod
    def setup_class(cls):
        try:
            cls.logger = logger().config_logger()
            cls.screenshots_dir = SCREENSHOTS_DIR
            os.makedirs(cls.screenshots_dir, exist_ok=True)
        except Exception as exp:
            raise exp

