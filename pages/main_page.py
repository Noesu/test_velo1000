import allure
import requests
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from typing import Optional

from pages.base_page import BasePage


class MainPage(BasePage):
    LOGO = (By.CSS_SELECTOR, "a.logo-image")
    TOP_HEADER = (By.CSS_SELECTOR, ".header__menu-list li a")
    TOP_HEADER_HIDDEN_ELEMENTS = (By.CSS_SELECTOR, ".hidden-menu animate__animated")
    NAV_HEADER_MENU_LOGO = (By.CSS_SELECTOR, "a.header__nav-logo")
    NAV_HEADER_MENU = (By.CSS_SELECTOR, ".navbar__menu navbar__item")
    NAV_HEADER_MENU_HIDDEN_ELEMENTS = (By.CSS_SELECTOR, ".navbar__menu .navbar__item .navbar__link")
    NAV_HEADER_SUBMENU = (By.CSS_SELECTOR, "ul.navbar__submenu li.navbar__submenu-item a.navbar__submenu-link")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "div.button-header.button-search")
    SEARCH_FIELD = (By.ID, "input__search")
    SEARCH_FIELD_SUBMIT_BUTTON = (By.CSS_SELECTOR, ".form-actions .button-style.button-style--red")
    SEARCH_FIELD_CANCEL_BUTTON = (By.CSS_SELECTOR, ".form-actions .search-close-btn")
    PRODUCT_BLOCK = (By.CSS_SELECTOR, ".product__block")

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

    def get_nav_header_menu_items(self) -> list[tuple[str, Optional[str]]]:
        items: list[WebElement] = []

        try:
            items += self.wait.until(EC.presence_of_all_elements_located(self.NAV_HEADER_MENU))
        except TimeoutException:
            pass

        try:
            items += self.wait.until(EC.presence_of_all_elements_located(self.NAV_HEADER_MENU_HIDDEN_ELEMENTS))
        except TimeoutException:
            pass

        return [(item.text.strip(), item.get_attribute("href")) for item in items]

    @staticmethod
    def download_navigation_menu_logo_as_bytes(src_url: str) -> bytes:
        try:
            response = requests.get(src_url, timeout=5)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            allure.attach(str(e),
                          name="navigation_menu_logo_download_error",
                          attachment_type=allure.attachment_type.TEXT
                          )
            return b""

    def get_navigation_menu_logo_src(self) -> Optional[str]:
        try:
            parent: WebElement = self.wait.until(EC.presence_of_element_located(self.NAV_HEADER_MENU_LOGO))
            child_img: WebElement = parent.find_element(By.TAG_NAME, "img")
            return child_img.get_attribute("src")
        except TimeoutException:
            return None

    def get_navigation_menu_logo_link(self) -> Optional[str]:
        try:
            element: WebElement = self.wait.until(EC.presence_of_element_located(self.NAV_HEADER_MENU_LOGO))
            return element.get_attribute("href")
        except TimeoutException:
            return None

    def get_nav_header_submenu_items(self):
        try:
            elements: list[WebElement] = self.wait.until(
                EC.presence_of_all_elements_located(self.NAV_HEADER_SUBMENU)
            )
            items = [
                {
                    "text": el.get_attribute("textContent").strip(),
                    "href": el.get_attribute("href")
                }
                for el in elements if el.get_attribute("textContent").strip()
            ]
            return items
        except TimeoutException:
            return []

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

    def search_field_present(self) -> bool:
        try:
            self.wait.until(EC.all_of(
                EC.element_to_be_clickable(self.SEARCH_FIELD),
                EC.visibility_of_element_located(self.SEARCH_FIELD_SUBMIT_BUTTON),
                EC.element_to_be_clickable(self.SEARCH_FIELD_SUBMIT_BUTTON),
                EC.visibility_of_element_located(self.SEARCH_FIELD_CANCEL_BUTTON),
                EC.element_to_be_clickable(self.SEARCH_FIELD_CANCEL_BUTTON)
            ))
            return True
        except TimeoutException:
            return False

    def click_submit_search_button(self) -> None:
        self.driver.find_element(*self.SEARCH_FIELD_SUBMIT_BUTTON).click()

    def url_changed_from_base(self) -> bool:
        try:
            self.wait.until(EC.url_changes(self.base_url))
            return True
        except TimeoutException:
            return False

    def click_cancel_search_button(self):
        self.driver.find_element(*self.SEARCH_FIELD_CANCEL_BUTTON).click()

    def insert_search(self, query: str):
        search_field = self.wait.until(EC.visibility_of_element_located(self.SEARCH_FIELD))
        search_field.send_keys(query)

    def number_of_search_results(self) -> int:
        products = self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_BLOCK))
        return len(products)