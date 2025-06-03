import allure
import requests
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from typing import Optional

# from pages.base_page import BasePage

class HeaderTop:
    LOGO = (By.CSS_SELECTOR, "a.logo-image")
    TOP_HEADER = (By.CSS_SELECTOR, ".header__menu-list li a")
    TOP_HEADER_HIDDEN_ELEMENTS = (By.CSS_SELECTOR, ".hidden-menu animate__animated")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "div.button-header.button-search")
    SEARCH_FIELD = (By.ID, "input__search")

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def logo_is_visible(self) -> bool:
        try:
            element: WebElement = self.wait.until(EC.visibility_of_element_located(self.LOGO))
            return element.is_displayed()
        except TimeoutException:
            return False

    @staticmethod
    def download_logo_as_bytes(src_url: str) -> bytes:
        try:
            response = requests.get(src_url, timeout=5)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            allure.attach(str(e),
                          name="logo_download_error",
                          attachment_type=allure.attachment_type.TEXT
                          )
            return b""

    def get_logo_src(self) -> Optional[str]:
        try:
            parent: WebElement = self.wait.until(EC.presence_of_element_located(self.LOGO))
            child_img: WebElement = parent.find_element(By.TAG_NAME, "img")
            return child_img.get_attribute("src")
        except TimeoutException:
            return None

    def get_logo_link(self) -> Optional[str]:
        try:
            element: WebElement = self.wait.until(EC.presence_of_element_located(self.LOGO))
            return element.get_attribute("href")
        except TimeoutException:
            return None

    def get_top_header_menu_items(self) -> list[tuple[str, Optional[str]]]:
        items: list[WebElement] = []

        try:
            items += self.wait.until(EC.presence_of_all_elements_located(self.TOP_HEADER))
        except TimeoutException:
            pass

        try:
            items += self.wait.until(EC.presence_of_all_elements_located(self.TOP_HEADER_HIDDEN_ELEMENTS))
        except TimeoutException:
            pass

        return [(item.text.strip(), item.get_attribute("href")) for item in items]


    def search_button_present(self) -> bool:
        try:
            self.wait.until(EC.all_of(
                EC.visibility_of_element_located(self.SEARCH_BUTTON),
                EC.element_to_be_clickable(self.SEARCH_BUTTON)
            ))
            return True
        except TimeoutException:
            return False

    def click_search_button(self) -> None:
        self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON)).click()