from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import BASE_URL
from pages.components.header_top import HeaderTop
from pages.components.header_nav import HeaderNav
from pages.components.search_engine import SearchEngine

class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.base_url = BASE_URL
        self.header_top = HeaderTop(driver, self.wait)
        self.header_nav = HeaderNav(driver, self.wait)
        self.search_engine = SearchEngine(driver, self.wait)

    @property
    def wait(self) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout=3)

    def get(self, url) -> None:
        self.driver.get(url)

    def open(self) -> None:
        self.driver.get(BASE_URL)

    def find_element(self, locator: tuple[str, str]):
        return self.driver.find_element(*locator)

    def find_elements(self, locator: tuple[str, str]):
        return self.driver.find_elements(*locator)

    def url_changed_from_base(self) -> bool:
        try:
            self.wait.until(EC.url_changes(self.base_url))
            return True
        except TimeoutException:
            return False
