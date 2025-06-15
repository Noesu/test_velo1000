from abc import ABC
from typing import Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException

class BaseProfileMenuPage(ABC):
    BREADCRUMBS = (By.CSS_SELECTOR, "div.breadcrumbs-item")
    TITLE = (By.CSS_SELECTOR, "h1.page-title")
    ALERT = (By.CSS_SELECTOR, "div.alert-danger")

    def __init__(self, driver, wait) -> None:
        self.driver = driver
        self.wait = wait

    def get_breadcrumbs_text(self) -> list[str]:
        elements: list[WebElement] = self.wait.until(EC.visibility_of_all_elements_located(self.BREADCRUMBS))
        return [element.text for element in elements]

    def get_page_title(self) -> str:
        element: WebElement = self.wait.until(EC.visibility_of_element_located(self.TITLE))
        return element.text

    def get_alert_text(self) -> Optional[str]:
        try:
            element: WebElement = self.wait.until(EC.visibility_of_element_located(self.ALERT))
            return element.text
        except TimeoutException:
            return None