
from utils.imports import *
from utils.common import elem_exists


class Listener(AbstractEventListener):
    """ """
    def before_click(self, element, driver):
        """ """
        try:
            error_block_identifiers = []
            for identifier in error_block_identifiers:
                if elem_exists(driver, identifier):
                    raise Exception("Error pop-up caught by Listener with error:\n "
                                    f"{driver.find_element(By.XPATH, identifier).text}")
        except Exception as exp:
            raise exp

    def after_click(self, element, driver):
        """ """
        try:
            error_block_identifiers = []
            for identifier in error_block_identifiers:
                if elem_exists(driver, identifier):
                    raise Exception("Error pop-up caught by Listener with error:\n "
                                    f"{driver.find_element(By.XPATH, identifier).text}")
        except Exception as exp:
            raise exp
