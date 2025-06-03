import allure
import requests
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from typing import Optional

class HeaderNav:
    NAV_HEADER_MENU_LOGO = (By.CSS_SELECTOR, "a.header__nav-logo")
    NAV_HEADER_MENU = (By.CSS_SELECTOR, ".navbar__menu navbar__item")
    NAV_HEADER_MENU_HIDDEN_ELEMENTS = (By.CSS_SELECTOR, ".navbar__menu .navbar__item .navbar__link")
    NAV_HEADER_SUBMENU = (By.CSS_SELECTOR, "ul.navbar__submenu li.navbar__submenu-item a.navbar__submenu-link")


    def __init__(self, driver, wait) -> None:
        self.driver = driver
        self.wait = wait

    def logo_is_visible(self) -> bool:
        try:
            element: WebElement = self.wait.until(EC.visibility_of_element_located(self.NAV_HEADER_MENU_LOGO))
            return element.is_displayed()
        except TimeoutException:
            return False

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

    def get_nav_header_submenu_items(self) -> list[Optional[str, str]]:
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