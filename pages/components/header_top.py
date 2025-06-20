import allure
import requests
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from typing import Optional


class HeaderTop:
    LOGO = (By.CSS_SELECTOR, "a.logo-image")
    TOP_HEADER = (By.CSS_SELECTOR, ".header__menu-list li a")
    TOP_HEADER_HIDDEN_ELEMENTS = (By.CSS_SELECTOR, ".hidden-menu animate__animated")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "div.button-header.button-search")
    SEARCH_FIELD = (By.ID, "input__search")
    PROFILE_MENU_ITEMS = (By.CSS_SELECTOR, "div.button-header.button-profile .profile-popup__link")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "div.button-header.button-acc")
    LOGGED_IN = (By.CSS_SELECTOR, ".button-header.button-acc span")
    EXPECTED_LOGGED_IN_BTN_TEXT = "ВЫЙТИ"

    def __init__(self, driver, wait) -> None:
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

    def get_profile_menu_items(self) -> list[tuple[str, Optional[str]]]:
        try:
            items = self.wait.until(EC.presence_of_all_elements_located(self.PROFILE_MENU_ITEMS))
            return [(item.get_attribute("textContent"), item.get_attribute("href")) for item in items]
        except TimeoutException:
            return []

    def get_logged_in_btn_text(self) -> Optional[str]:
        try:
            element: WebElement = self.wait.until(EC.presence_of_element_located(self.LOGGED_IN))
            return element.text
        except TimeoutException:
            return None

    def is_user_authorized(self) -> bool:
        try:
            element: WebElement = self.wait.until(EC.presence_of_element_located(self.LOGGED_IN))
            return element.text == self.EXPECTED_LOGGED_IN_BTN_TEXT
        except TimeoutException:
            return False


    def click_login_button(self):
        login_button: WebElement = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_button.click()
