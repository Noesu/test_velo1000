from typing import Optional

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from pages.base_profile_menu_page import BaseProfileMenuPage

class AuthorizationPage(BaseProfileMenuPage):
    LOGIN_FIELD = (By.CSS_SELECTOR, "input[name='USER_LOGIN']")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "input[name='USER_PASSWORD']")
    REMEMBER_ME_CHECKBOX = (By.CSS_SELECTOR, "label.bx-filter-param-label")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "div.bx-authform-formgroup-container button.button-style[type='submit']")
    LINKS_CONTAINER = (By.CSS_SELECTOR, "div.bx-authform-link-container a")


    # Checkers

    def is_login_field_enabled(self) -> bool:
        field = self._get_login_field()
        if not field:
            return False
        try:
            return field.is_enabled()
        except Exception:
            return False

    def is_password_field_enabled(self) -> bool:
        field = self._get_password_field()
        if not field:
            return False
        try:
            return field.is_enabled()
        except Exception:
            return False

    def is_remember_me_checkbox_clickable(self) -> bool:
        try:
            self.wait.until(EC.element_to_be_clickable(self.REMEMBER_ME_CHECKBOX))
            return True
        except TimeoutException:
            return False

    def is_submit_button_clickable(self) -> bool:
        try:
            self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
            return True
        except TimeoutException:
            return False


    # Getters

    def _get_login_field(self) -> Optional[WebElement]:
        try:
            return self.wait.until(EC.presence_of_element_located(self.LOGIN_FIELD))
        except TimeoutException:
            return None

    def _get_password_field(self) -> Optional[WebElement]:
        try:
            return self.wait.until(EC.presence_of_element_located(self.PASSWORD_FIELD))
        except TimeoutException:
            return None


    def _get_submit_button(self) -> Optional[WebElement]:
        try:
            return self.wait.until(EC.presence_of_element_located(self.SUBMIT_BUTTON))
        except TimeoutException:
            return None

    def _get_remember_me_checkbox(self) -> Optional[WebElement]:
        try:
            return self.wait.until(EC.presence_of_element_located(self.REMEMBER_ME_CHECKBOX))
        except TimeoutException:
            return None

    def get_page_url(self) -> str:
        return self.driver.current_url

    def get_submit_button_text(self) -> Optional[str]:
        try:
            button: WebElement = self._get_submit_button()
            if button:
                return button.text
            return None
        except TimeoutException:
            return None

    def get_forgot_password_and_registration_links(self) -> list[Optional[str]]:
        try:
            links: list[WebElement] = self.wait.until(EC.visibility_of_all_elements_located(self.LINKS_CONTAINER))
            return [link.get_attribute("href") for link in links]
        except TimeoutException:
            return []


    # Actions

    def set_login_field(self, value: str) -> bool:
        field = self._get_login_field()
        if not field:
            return False
        field.clear()
        field.send_keys(value)
        return field.get_attribute("value") == value

    def set_password_field(self, value: str) -> bool:
        field = self._get_password_field()
        if not field:
            return False
        field.clear()
        field.send_keys(value)
        return field.get_attribute("value") == value

    def set_remember_me_checkbox(self, status: bool) -> bool:
        checkbox = self._get_remember_me_checkbox()
        if not checkbox:
            return False
        try:
            if checkbox.is_selected() != status:
                checkbox.click()
            self.wait.until(EC.element_selection_state_to_be(checkbox, status))
            return True
        except TimeoutException:
            return False

    def click_submit_button(self):
        button: WebElement = self._get_submit_button()
        button.click()

