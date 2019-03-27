"""
    Utilities to get a selenium web driver and to open the dash app.
    This is only meant for testing purpouses
"""

import os

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import src.constants as c
import src.utilities as u

SELENIUM_PATH_IN_TRAVIS = '/home/travis/selenium/chromedriver'

def get_chrome_webdriver(headless, driver_path=None):
    """
        Get a chrome webdriver.

        Args:
            headless:	bool to allow headless mode

        Returns:		chrome web driver
    """

    if headless:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox") #This make Chromium reachable
        options.add_argument("--no-default-browser-check") #Overrides default choices
        options.add_argument("--disable-default-apps")
        options.add_argument("--window-size=1920x1080")

        # Allow custom path for webdriver
        if driver_path is not None:
            return webdriver.Chrome(driver_path, chrome_options=options)

        # If none provided use default
        return webdriver.Chrome(chrome_options=options)

    # If headless then use local webdriver
    return webdriver.Chrome()



def wait_until_loaded(driver, max_retries=30):
    """
        It will wait until the dash page is loaded

        Args:
            max_retries:    number of retries (of 1 second)

        Returns:
            True if it was able to load the page
    """

    for _ in range(max_retries):
        sleep(1)

        if 'Updating...' not in driver.title:
            return True

    return False


def open_dash(headless=False):
    """
        Starts a chrome web driver and opens the dash app. Then it waits until the app is loaded

        Args:
            headless:	bool to allow headless mode

        Returns:		chrome web driver
    """

    # If run from travis it is better to run it headless
    if "/home/travis/" in os.getcwd():
        driver = get_chrome_webdriver(headless=True, driver_path=SELENIUM_PATH_IN_TRAVIS)

    # If not, allow both options
    else:
        driver = get_chrome_webdriver(headless)

    # First login and then open dash app (entering with credentials does not render correctly)
    driver.get(c.dash.LINK_ROOT_LOGIN.format(
        u.get_secret(c.io.VAR_USER),
        u.get_secret(c.io.VAR_PASSWORD)
    ))
    driver.get(c.dash.LINK_ROOT)

    wait_until_loaded(driver)

    return driver
