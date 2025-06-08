import allure
import pytest

from pages.components.auth_modal import AuthModalComponent
from pages.main_page import MainPage


@pytest.fixture(scope="class", autouse=True)
def open_auth_modal(request, main_page):
    tab = request.param
    request.cls.tab = tab
    main_page.header_top.click_login_button()
    auth_modal = AuthModalComponent(main_page.driver, main_page.wait)
    if tab == "register":
        auth_modal.switch_modal_tab_to_registration()
    request.cls.main_page = main_page
    request.cls.auth_modal = auth_modal

@allure.suite("Modal Window Tests")
@allure.feature("Login Modal")
@allure.story("Authorization Tab Layout")
@pytest.mark.usefixtures("open_auth_modal")
@pytest.mark.parametrize("open_auth_modal", ["auth"], indirect=True)
class TestAuthorizationTab:
    main_page: MainPage
    auth_modal: AuthModalComponent

    EXPECTED_AUTH_TAB_TITLE = "Авторизация"
    EXPECTED_AUTH_EMAIL_PLACEHOLDER = "Эл. почта"
    EXPECTED_AUTH_PASSWORD_PLACEHOLDER = "Пароль"
    EXPECTED_AUTH_FORGOT_PASSWORD_LINK = "/local/ajax/auth.php?forgot_password=yes&backurl=%2Flocal%2Fajax%2Fauth.php"
    EXPECTED_AUTH_SUBMIT_BUTTON_TEXT_AND_VALUE = "Войти"
    EXPECTED_REG_TAB_LINK = "/local/ajax/auth.php?register=yes&backurl=%2Flocal%2Fajax%2Fauth.php"

    @allure.title("Modal window")
    @allure.description("Verifies that the login modal is opened and visible to the user")
    def test_modal_is_displayed(self):
        modal = self.auth_modal.get_modal_window()
        allure.attach(modal.screenshot_as_png,
                      name="Modal screenshot",
                      attachment_type=allure.attachment_type.PNG
                      )
        assert modal, "Modal doesn't showing up"

    @allure.title("Title")
    @allure.description("Checks if the title matches the expected value")
    def test_title(self):
        modal_tab_title = self.auth_modal.get_modal_name()
        allure.attach(modal_tab_title,
                      name="Authorization tab title",
                      attachment_type=allure.attachment_type.TEXT
                      )
        assert modal_tab_title == self.EXPECTED_AUTH_TAB_TITLE.upper(), (
            f"Unexpected modal title: '{modal_tab_title}'. "
            f"Expected: '{self.EXPECTED_AUTH_TAB_TITLE.upper()}'."
        )

    @allure.title("Email field")
    @allure.description("Checks that the email field is rendered in the authorization form")
    def test_email_field_exists(self):
        assert self.auth_modal.get_auth_email_field(), "Email field not found"

    @allure.title("Email field placeholder")
    @allure.description("Checks if the placeholder in the email field matches the expected value")
    def test_email_field_placeholder(self):
        placeholder = self.auth_modal.get_auth_email_placeholder_text()
        allure.attach(placeholder,
                      name="Email placeholder",
                      attachment_type=allure.attachment_type.TEXT
                      )
        assert placeholder == self.EXPECTED_AUTH_EMAIL_PLACEHOLDER, (
            f"Unexpected email placeholder text: '{placeholder}'. "
            f"Expected: '{self.EXPECTED_AUTH_EMAIL_PLACEHOLDER}'."
        )

    @allure.title("Password field")
    @allure.description("Checks that the password field is visible")
    def test_password_field_exists(self):
        assert self.auth_modal.get_auth_password_field(), "Password field not found"

    @allure.title("Password field placeholder text")
    @allure.description("Checks if the placeholder in the password field matches the expected value")
    def test_password_field_placeholder(self):
        password_placeholder = self.auth_modal.get_auth_password_placeholder_text()
        allure.attach(password_placeholder,
                      name="Password placeholder",
                      attachment_type=allure.attachment_type.TEXT
                      )
        assert password_placeholder == self.EXPECTED_AUTH_PASSWORD_PLACEHOLDER, (
            f"Unexpected password placeholder text: '{password_placeholder}'. "
            f"Expected: '{self.EXPECTED_AUTH_PASSWORD_PLACEHOLDER}'."
        )

    @allure.title("Password field visibility button")
    @allure.description("Checks if the password field has visibility_btn")
    def test_password_field_visibility_btn(self):
        assert self.auth_modal.get_auth_password_visibility_btn(), "Password visibility button not found"

    @allure.title("Remember me switch")
    @allure.description("Checks if the remember me switch is clickable")
    def test_remember_me_switch(self):
        assert self.auth_modal.get_auth_remember_me_switch(), "Remember me switch not clickable"

    @allure.title("Forgot password link")
    @allure.description("Checks if the forgot password link is correct")
    def test_forgot_password_link(self):
        link = self.auth_modal.get_auth_forgot_password_link()
        allure.attach(link,
                      name="Forgot password link",
                      attachment_type=allure.attachment_type.TEXT
                      )
        assert link.endswith(self.EXPECTED_AUTH_FORGOT_PASSWORD_LINK), (
            f"Unexpected forgot password link: '{link}'. "
            f"Expected: '{self.EXPECTED_AUTH_FORGOT_PASSWORD_LINK}'."
        )

    @allure.title("Submit button")
    @allure.description("Checks if the submit button is clickable")
    def test_submit_button_exists(self):
        assert self.auth_modal.auth_submit_btn_is_clickable(), "Authorization submit button not found or not clickable"

    @allure.title("Submit button attributes")
    @allure.description("Checks if the submit button is clickable and its text and value matches the expected values")
    def test_submit_button_attrs(self):
        assert self.auth_modal.auth_submit_btn_is_clickable(), "Authorization submit button not found or not clickable"
        button_text, button_value = self.auth_modal.get_auth_submit_btn_text_and_value()
        allure.attach(
            f"Button text: {button_text}. Button value: {button_value}",
            name="submit_button_attrs",
            attachment_type=allure.attachment_type.TEXT
        )
        assert button_text == button_value.upper() == self.EXPECTED_AUTH_SUBMIT_BUTTON_TEXT_AND_VALUE.upper(), (
            f"Unexpected submit button text/value:\n"
            f"Actual button text: {button_text}. "
            f"Expected: {self.EXPECTED_AUTH_SUBMIT_BUTTON_TEXT_AND_VALUE.upper()}.\n"
            f"Actual button value: {button_value}. "
            f"Expected: {self.EXPECTED_AUTH_SUBMIT_BUTTON_TEXT_AND_VALUE}"
        )

    @allure.title("Registration tab link")
    @allure.description("Checks if the link for registration tab matches the expected value")
    def test_registration_tab_link_exists(self):
        link = self.auth_modal.get_modal_tab_link()
        allure.attach(
            link,
            name="registration_tab_link",
            attachment_type=allure.attachment_type.TEXT
        )
        assert link, "Link for registration tab not found"
        assert link.endswith(self.EXPECTED_REG_TAB_LINK), (
            f"Unexpected registration tab link in modal window: {link}. "
            f"Expected ending is: {self.EXPECTED_REG_TAB_LINK}"
        )


@allure.suite("Modal Window Tests")
@allure.feature("Login Modal")
@allure.story("Registration Tab Layout")
@pytest.mark.usefixtures("open_auth_modal")
@pytest.mark.parametrize("open_auth_modal", ["register"], indirect=True)
class TestRegistrationTab:
    main_page: MainPage
    auth_modal: AuthModalComponent

    EXPECTED_REG_TAB_TITLE = "Регистрация"
    EXPECTED_REG_FIRST_NAME_PLACEHOLDER = "Имя:"
    EXPECTED_REG_LAST_NAME_PLACEHOLDER = "Фамилия:"
    EXPECTED_REG_EMAIL_PLACEHOLDER = "Адрес e-mail:"
    EXPECTED_REG_SUBMIT_BUTTON_TEXT_AND_VALUE = "Регистрация"
    EXPECTED_AUTH_TAB_LINK = "/local/ajax/auth.php?login=yes"

    @allure.title("Modal window")
    @allure.description("Verifies that the login modal is opened and visible to the user")
    def test_modal_is_displayed(self):
        modal_registration_tab = self.auth_modal.get_modal_window()
        allure.attach(
            modal_registration_tab.screenshot_as_png,
            name="modal_registration_tab",
            attachment_type=allure.attachment_type.PNG
        )
        assert modal_registration_tab, "Modal doesn't showing up after switching to registration tab"

    @allure.title("Title")
    @allure.description("Checks if the title matches the expected value")
    def test_title(self):
        modal_tab_title = self.auth_modal.get_modal_name()
        allure.attach(modal_tab_title,
                      name="Registration tab title",
                      attachment_type=allure.attachment_type.TEXT
                      )
        assert modal_tab_title == self.EXPECTED_REG_TAB_TITLE.upper(), (
            f"Unexpected modal title: {modal_tab_title}. "
            f"Expected: {self.EXPECTED_REG_TAB_TITLE.upper()}"
        )

    @allure.title("First name field")
    @allure.description("Verifies that the first name field is present")
    def test_first_name_field_exists(self):
        assert self.auth_modal.get_reg_first_name_field(), "First name field not found"

    @allure.title("First name field placeholder")
    @allure.description("Checks if the placeholder in the first name field matches the expected value")
    def test_first_name_field_placeholder(self):
        placeholder = self.auth_modal.get_reg_first_name_placeholder_text()
        allure.attach(placeholder,
                      name="First name placeholder",
                      attachment_type=allure.attachment_type.TEXT
                      )
        assert placeholder == self.EXPECTED_REG_FIRST_NAME_PLACEHOLDER, (
            f"Unexpected first name placeholder: {placeholder}. "
            f"Expected: {self.EXPECTED_REG_FIRST_NAME_PLACEHOLDER}"
        )

    @allure.title("Last name field")
    @allure.description("Verifies that the last name field is present")
    def test_last_name_field_exists(self):
        assert self.auth_modal.get_reg_first_name_field(), "Last name field not found"

    @allure.title("Last name field placeholder")
    @allure.description("Checks if the placeholder in the last name field matches the expected value")
    def test_last_name_field_placeholder(self):
        placeholder = self.auth_modal.get_reg_last_name_placeholder_text()
        allure.attach(placeholder,
                      name="Last name placeholder",
                      attachment_type=allure.attachment_type.TEXT
                      )
        assert placeholder == self.EXPECTED_REG_LAST_NAME_PLACEHOLDER, (
            f"Unexpected first name placeholder: {placeholder}. "
            f"Expected: {self.EXPECTED_REG_LAST_NAME_PLACEHOLDER}"
        )

    @allure.title("Email field")
    @allure.description("Verifies that the email field is present")
    def test_email_field_exists(self):
        assert self.auth_modal.get_reg_first_name_field(), "Email field not found"

    @allure.title("Email field placeholder")
    @allure.description("Checks if the placeholder in the email field matches the expected value")
    def test_email_field_placeholder(self):
        placeholder = self.auth_modal.get_reg_email_placeholder_text()
        allure.attach(placeholder,
                      name="Email placeholder",
                      attachment_type=allure.attachment_type.TEXT
                      )
        assert placeholder == self.EXPECTED_REG_EMAIL_PLACEHOLDER, (
            f"Unexpected email placeholder: {placeholder}. "
            f"Expected: {self.EXPECTED_REG_EMAIL_PLACEHOLDER}"
        )

    @allure.title("Policy checkbox is clickable")
    @allure.description("Checks if the registration policy checkbox is clickable")
    def test_registration_policy_checkbox_exists(self):
        assert self.auth_modal.get_reg_policy_checkbox(), "Registration policy checkbox not clickable"

    @allure.title("Policy link")
    @allure.description("Checks if the policy link matches the expected value")
    def test_registration_policy_link(self):
        link = self.auth_modal.get_reg_policy_link()
        allure.attach(link,
            name="Policy link",
            attachment_type=allure.attachment_type.TEXT
        )
        assert link, "Policy link not found"
        assert link.endswith("#"), "Found a stub (#) instead of a policy link"

    @allure.title("Submit button")
    @allure.description("Checks if the submit button is clickable and its text and value matches the expected values")
    def test_submit_button_exists(self):
        assert self.auth_modal.reg_submit_btn_is_clickable(), "Registration submit button not found or not clickable"

    @allure.title("Submit button attributes")
    @allure.description("Checks if the submit button is clickable and its text and value matches the expected values")
    def test_submit_button_attrs(self):
        assert self.auth_modal.reg_submit_btn_is_clickable(), "Registration submit button not found or not clickable"
        button_text, button_value = self.auth_modal.get_reg_submit_btn_text_and_value()
        allure.attach(
            f"Button text: {button_text}. Button value: {button_value}",
            name="submit_button_attrs",
            attachment_type=allure.attachment_type.TEXT
        )
        assert button_text == button_value.upper() == self.EXPECTED_REG_SUBMIT_BUTTON_TEXT_AND_VALUE.upper(), (
            f"Unexpected submit button text/value:\n"
            f"Actual button text: {button_text}. "
            f"Expected: {self.EXPECTED_REG_SUBMIT_BUTTON_TEXT_AND_VALUE.upper()}.\n"
            f"Actual button value: {button_value}. "
            f"Expected: {self.EXPECTED_REG_SUBMIT_BUTTON_TEXT_AND_VALUE}"
        )

    @allure.title("Authorization tab link")
    @allure.description("Checks if the link for authorization tab matches the expected value")
    def test_authorization_tab_link_exists(self):
        link = self.auth_modal.get_modal_tab_link()
        allure.attach(
            link,
            name="authorization_tab_link",
            attachment_type=allure.attachment_type.TEXT
        )
        assert link, "Link for authorization tab not found"
        assert link.endswith(self.EXPECTED_AUTH_TAB_LINK), (
            f"Unexpected authorization tab link in modal window: {link}. "
            f"Expected ending is: {self.EXPECTED_AUTH_TAB_LINK}"
        )

@allure.suite("Modal Window Tests")
@allure.feature("Login Modal")
@allure.story("Modal Close Button Behavior")
@pytest.mark.parametrize("open_auth_modal", ["auth", "register"], indirect=True)
@pytest.mark.usefixtures("open_auth_modal")
class TestModalClose:
    main_page: MainPage
    auth_modal: AuthModalComponent
    tab: str

    def test_close_button_closes_modal(self):
        allure.dynamic.title(f"Close button closes modal (tab: {self.tab})")
        self.auth_modal.close_modal_btn()
        allure.attach(
            self.main_page.driver.get_screenshot_as_png(),
            name="screenshot_after_close_button_click",
            attachment_type=allure.attachment_type.PNG
        )
        assert self.auth_modal.modal_window_not_visible(), "Modal did not close after clicking close button"
