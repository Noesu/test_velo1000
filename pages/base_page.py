from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import BASE_URL

class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.base_url = BASE_URL

    @property
    def wait(self) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout=5)

    def open(self):
        self.driver.get(BASE_URL)

    def find_element(self, locator):
        return self.driver.find_element(*locator)

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)
