from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from typing import Optional, Union
import time

from selenium.webdriver.support.wait import WebDriverWait


class AuthModalComponent:
    MODAL_WEB_ELEMENT = (By.CSS_SELECTOR, "div.popup-auth__inner")
    MODAL_NAME = (By.CSS_SELECTOR, "h3.auth__title")
    MODAL_CLOSE_BTN = (By.CSS_SELECTOR, '.close-auth')
    MODAL_TAB_LINK = (By.CSS_SELECTOR, '.auth__tab .ajax-link')
    MODAL_REGISTRATION_TAB = (By.CSS_SELECTOR, ".auth__tab a[id='regst']")

    AUTH_EMAIL_FIELD = (By.CSS_SELECTOR, 'input[name="USER_LOGIN"]')
    AUTH_EMAIL_PLACEHOLDER = (By.XPATH, '//div[@class="input-style"][.//input[@name="USER_LOGIN"]]/label')
    AUTH_PASSWORD_FIELD = (By.CSS_SELECTOR, 'input[name="USER_PASSWORD"]')
    AUTH_PASSWORD_PLACEHOLDER = (By.XPATH, '//div[@class="input-style"][.//input[@name="USER_PASSWORD"]]/label')
    AUTH_PASSWORD_VISIBILITY_BTN = (By.CSS_SELECTOR, '.input-style .pass-view')
    AUTH_REMEMBER_ME_SWITCH = (By.CSS_SELECTOR, '.checkbox-bg')
    AUTH_FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, '.forgot-pass')
    AUTH_SUBMIT_BTN = (By.CSS_SELECTOR, 'button[type="submit"][name="Login"]')

    REG_FIRST_NAME_FIELD = (By.CSS_SELECTOR, 'input[name="REGISTER[NAME]"]')
    REG_FIRST_NAME_PLACEHOLDER = (By.XPATH, '//div[@class="input-style"][.//input[@name="REGISTER[NAME]"]]/label')
    REG_LAST_NAME_FIELD = (By.CSS_SELECTOR, 'input[name="REGISTER[LAST_NAME]"]')
    REG_LAST_NAME_PLACEHOLDER = (By.XPATH, '//div[@class="input-style"][.//input[@name="REGISTER[LAST_NAME]"]]/label')
    REG_EMAIL_FIELD = (By.CSS_SELECTOR, 'input[name="REGISTER[EMAIL]"]')
    REG_EMAIL_PLACEHOLDER = (By.XPATH, '//div[@class="input-style"][.//input[@name="REGISTER[EMAIL]"]]/label')
    REG_POLICY_CHECKBOX_LABEL = (By.CSS_SELECTOR, '.input-checkbox-circle')
    REG_POLICY_CHECKBOX_INPUT = (By.CSS_SELECTOR, '.input-checkbox-circle input')
    REG_POLICY_LINK = (By.CSS_SELECTOR, ".policy-info a")
    REG_SUBMIT_BTN = (By.CSS_SELECTOR, 'button[type="submit"][name="register_submit_button"]')

    REG_SUCCESSFUL = (By.CSS_SELECTOR, ".uk-modal-content p")
    REG_ERROR_TEXT = (By.CSS_SELECTOR, ".errortext")

    def __init__(self, driver, wait) -> None:
        self.driver = driver
        self.wait = wait

    def get_modal_window(self) -> WebElement:
        time.sleep(1)
        return self.wait.until(EC.visibility_of_element_located(self.MODAL_WEB_ELEMENT))

    def modal_window_not_visible(self, timeout: Union[int, float]):
        try:
            WebDriverWait(self.driver, timeout=timeout).until_not(
                EC.visibility_of_element_located(self.MODAL_WEB_ELEMENT))
            return True
        except TimeoutException:
            return False

    def get_close_modal_btn(self) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(self.MODAL_CLOSE_BTN))
            return True
        except TimeoutException:
            return False

    def get_modal_name(self) -> str:
        title_element: WebElement = self.wait.until(EC.visibility_of_element_located(self.MODAL_NAME))
        return title_element.text

    def get_modal_tab_link(self):
        inactive_tab_link: WebElement = self.wait.until(EC.element_to_be_clickable(self.MODAL_TAB_LINK))
        return inactive_tab_link.get_attribute('href')

    #  Modal window authorization tab items:
    def get_auth_email_field(self) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(self.AUTH_EMAIL_FIELD))
            return True
        except TimeoutException:
            return False

    def get_auth_email_placeholder_text(self) -> str:
        placeholder: WebElement = self.wait.until(EC.presence_of_element_located(self.AUTH_EMAIL_PLACEHOLDER))
        return placeholder.text

    def get_auth_password_field(self) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(self.AUTH_PASSWORD_FIELD))
            return True
        except TimeoutException:
            return False

    def get_auth_password_placeholder_text(self) -> str:
        placeholder: WebElement = self.wait.until(EC.presence_of_element_located(self.AUTH_PASSWORD_PLACEHOLDER))
        return placeholder.text

    def get_auth_password_visibility_btn(self) -> bool:
        try:
            self.wait.until(EC.presence_of_element_located(self.AUTH_PASSWORD_VISIBILITY_BTN))
            return True
        except TimeoutException:
            return False

    def get_auth_remember_me_switch(self) -> bool:
        try:
            self.wait.until(EC.element_to_be_clickable(self.AUTH_REMEMBER_ME_SWITCH))
            return True
        except TimeoutException:
            return False

    def get_auth_forgot_password_link(self) -> str:
        try:
            link: WebElement = self.wait.until(EC.visibility_of_element_located(self.AUTH_FORGOT_PASSWORD_LINK))
            return link.get_attribute("href")
        except Exception as e:
            return str(e)

    def auth_submit_btn_is_clickable(self) -> bool:
        try:
            self.wait.until(EC.element_to_be_clickable(self.AUTH_SUBMIT_BTN))
            return True
        except Exception:
            return False

    def get_auth_submit_btn_text_and_value(self) -> Optional[tuple[Optional[str], Optional[str]]]:
        try:
            button = self.wait.until(EC.element_to_be_clickable(self.AUTH_SUBMIT_BTN))
            button_text = button.text or None
            button_value = button.get_attribute("value")
            return button_text, button_value
        except Exception:
            return None

    #  Modal window registration tab items:
    def get_reg_first_name_field(self) -> bool:
        try:
            self.wait.until(EC.element_to_be_clickable(self.REG_FIRST_NAME_FIELD))
            return True
        except TimeoutException:
            return False

    def get_reg_first_name_placeholder_text(self) -> str:
        placeholder: WebElement = self.wait.until(EC.presence_of_element_located(self.REG_FIRST_NAME_PLACEHOLDER))
        return placeholder.text

    def get_reg_last_name_field(self) -> bool:
        try:
            self.wait.until(EC.element_to_be_clickable(self.REG_LAST_NAME_FIELD))
            return True
        except TimeoutException:
            return False

    def get_reg_last_name_placeholder_text(self) -> str:
        placeholder: WebElement = self.wait.until(EC.presence_of_element_located(self.REG_LAST_NAME_PLACEHOLDER))
        return placeholder.text

    def get_reg_email_field(self) -> bool:
        try:
            self.wait.until(EC.element_to_be_clickable(self.REG_EMAIL_FIELD))
            return True
        except TimeoutException:
            return False

    def get_reg_email_placeholder_text(self) -> str:
        placeholder: WebElement = self.wait.until(EC.presence_of_element_located(self.REG_EMAIL_PLACEHOLDER))
        return placeholder.text

    def get_reg_policy_checkbox(self) -> bool:
        try:
            self.wait.until(EC.element_to_be_clickable(self.REG_POLICY_CHECKBOX_LABEL))
            return True
        except TimeoutException:
            return False

    def get_reg_policy_link(self) -> Optional[str]:
        try:
            link = self.wait.until(EC.element_to_be_clickable(self.REG_POLICY_LINK))
            return link.get_attribute("href")
        except TimeoutException:
            return None

    def reg_submit_btn_is_clickable(self) -> bool:
        try:
            self.wait.until(EC.element_to_be_clickable(self.REG_SUBMIT_BTN))
            return True
        except Exception:
            return False

    def get_reg_submit_btn_text_and_value(self) -> Optional[tuple[Optional[str], Optional[str]]]:
        try:
            button = self.wait.until(EC.element_to_be_clickable(self.REG_SUBMIT_BTN))
            button_text = button.text or None
            button_value = button.get_attribute("value")
            return button_text, button_value
        except Exception:
            return None

    # Modal window successful registration

    def get_reg_successful_text(self) -> list[str]:
        try:
            elements: list[WebElement] = self.wait.until(EC.visibility_of_all_elements_located(self.REG_SUCCESSFUL))
            return [line.strip() for el in elements for line in el.text.splitlines() if line.strip()]
        except TimeoutException:
            return []

    # Modal window interactions

    def close_modal(self) -> None:
        button: WebElement = self.wait.until(EC.visibility_of_element_located(self.MODAL_CLOSE_BTN))
        button.click()

    def switch_modal_tab_to_registration(self) -> None:
        link: WebElement = self.wait.until(EC.element_to_be_clickable(self.MODAL_REGISTRATION_TAB))
        link.click()
        time.sleep(.5)

    def set_reg_first_name(self, first_name: str) -> bool:
        try:
            first_name_field: WebElement = self.wait.until(EC.element_to_be_clickable(self.REG_FIRST_NAME_FIELD))
            first_name_field.clear()
            first_name_field.send_keys(first_name)
            return first_name_field.get_attribute("value") == first_name
        except Exception:
            return False

    def set_reg_last_name(self, last_name: str) -> bool:
        try:
            last_name_field: WebElement = self.wait.until(EC.element_to_be_clickable(self.REG_LAST_NAME_FIELD))
            last_name_field.clear()
            last_name_field.send_keys(last_name)
            return last_name_field.get_attribute("value") == last_name
        except TimeoutException:
            return False

    def set_reg_email(self, email: str) -> bool:
        try:
            email_field: WebElement = self.wait.until(EC.element_to_be_clickable(self.REG_EMAIL_FIELD))
            email_field.clear()
            email_field.send_keys(email)
            return email_field.get_attribute("value") == email
        except TimeoutException:
            return False

    def set_reg_policy_checkbox(self, switch_on: bool) -> bool:
        try:
            checkbox: WebElement = self.wait.until(EC.presence_of_element_located(self.REG_POLICY_CHECKBOX_INPUT))
            if checkbox.is_selected() != switch_on:
                checkbox_label: WebElement = self.wait.until(EC.element_to_be_clickable(self.REG_POLICY_CHECKBOX_LABEL))
                checkbox_label.click()
                self.wait.until(EC.element_located_selection_state_to_be(self.REG_POLICY_CHECKBOX_INPUT, switch_on))
            return checkbox.is_selected()
        except Exception:
            return False

    def click_reg_submit(self) -> None:
        button: WebElement = self.wait.until(EC.element_to_be_clickable(self.REG_SUBMIT_BTN))
        button.click()

    def get_reg_error_messages(self) -> list[str]:
        try:
            element: WebElement = self.wait.until(EC.visibility_of_element_located(self.REG_ERROR_TEXT))
            return element.text.strip().splitlines()
        except TimeoutException:
            return []
