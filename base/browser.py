import logging
import os

from configs.user_constants import *
from selenium import webdriver
from selenium.webdriver.ie.service import Service as IEService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.webdriver.firefox.options import Options as firefoxOptions
from selenium.webdriver.ie.options import Options as IEOptions
from utils.listeners import Listener
from utils.logging_util import AutoMethodLogger


os.environ['WDM_LOG'] = str(logging.NOTSET)
os.environ['WDM_LOCAL'] = '1'
os.environ['WDM_SSL_VERIFY'] = '0'


class Browser(AutoMethodLogger):
    """ """
    def __init__(self, logger):
        """ """
        super().__init__(logger)
        try:
            self._driver = None
            self._options = None
            self._prefs = None
            self.logger = logger
        except Exception as exp:
            raise exp

    def _set_properties(self):
        """ """
        try:
            self._options.add_argument("--no-sandbox")
            self._options.add_argument("--headless")
            self._options.add_argument("--disable_gpu")
            self._options.add_argument("--start-maximized")
            self._options.add_argument("--window-size=1920.1080")
            self._options.add_argument("--disable-extension")
            self._options.add_argument("--ignore-certificates-errors")
            self._options.add_experimental_option("prefs", {"download.default_directory": DOWNLOAD_DIRECTORY})
        except Exception as exp:
            raise exp

    def chrome(self):
        """ """
        try:
            self._options = chromeOptions()
            self._set_properties()
            service = ChromeService(executable_path=CHROME_DRIVER)
            chrome_driver = EventFiringWebDriver(webdriver.Chrome(service=service, options=self._options), Listener())
            chrome_driver.implicitly_wait(2)
            chrome_driver.get(ENV_URL)
        except Exception as exp:
            raise exp

    def firefox(self):
        """ """
        try:
            self._options = firefoxOptions()
            self._set_properties()
            service = FirefoxService(executable_path=FIREFOX_DRIVER)
            chrome_driver = EventFiringWebDriver(webdriver.Firefox(service=service, options=self._options), Listener())
            chrome_driver.implicitly_wait(2)
            chrome_driver.get(ENV_URL)
        except Exception as exp:
            raise exp

    def internet_explorer(self):
        """ """
        try:
            self._options = IEOptions()
            self._set_properties()
            service = IEService(executable_path=IE_DRIVER)
            chrome_driver = EventFiringWebDriver(webdriver.Ie(service=service, options=self._options), Listener())
            chrome_driver.implicitly_wait(2)
            chrome_driver.get(ENV_URL)
        except Exception as exp:
            raise exp

    def initialize_and_launch_browser(self, browser_type):
        """ """
        try:
            if browser_type.upper() == 'CHROME':
                self._driver = self.chrome()
            elif browser_type.upper() == 'IE':
                self._driver = self.internet_explorer()
            elif browser_type.upper() == 'FIREFOX':
                self._driver = self.firefox()
        except Exception as exp:
            raise exp
