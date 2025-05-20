from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from pathlib import Path
import os

ROOT_PATH = Path(__file__).parent.parent
CHROME_DRIVER_NAME = "chromedriver"
CHROME_DRIVER_PATH = ROOT_PATH / "bin" / CHROME_DRIVER_NAME
FIREFOX_DRIVER_NAME = "geckodriver"
FIREFOX_DRIVER_PATH = ROOT_PATH / "bin" / FIREFOX_DRIVER_NAME


def make_chome_driver(*options):
    """"""
    chrome_options = webdriver.ChromeOptions()
    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    if os.environ.get("SELENIUM_HEADLESS") == "1":
        chrome_options.add_argument("--headless")

    chrome_service = Service(executable_path=CHROME_DRIVER_PATH)
    browser = webdriver.Chrome(chrome_options, chrome_service)

    return browser


def make_firefox_driver(*options):
    """"""
    firefox_options = webdriver.FirefoxOptions()
    if options is not None:
        for option in options:
            firefox_options.add_argument(option)

    if os.environ.get("SELENIUM_HEADLESS") == "1":
        firefox_options.add_argument("--headless")

    firefox_service = Service(executable_path=FIREFOX_DRIVER_PATH)
    browser = webdriver.Firefox(firefox_options, firefox_service)

    return browser


if __name__ == "__main__":
    # driver = make_chome_driver("--headless")
    # driver.implicitly_wait(10)
    # driver.get("https://www.google.com")
    # driver.quit()
    driver = make_firefox_driver("--headless")
    driver.implicitly_wait(10)
    driver.get("https://www.google.com")
    driver.quit()
