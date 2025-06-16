import allure
import itertools
import pytest
from selenium.webdriver.remote.webelement import WebElement

from config.settings import USER_LOGIN, USER_PASSWORD, USER_FIRST_NAME, USER_LAST_NAME
from pages.components.auth_modal import AuthModalComponent
from pages.main_page import MainPage


@pytest.fixture(scope="class")
def open_auth_modal_class(request, page):
    tab = request.param
    request.cls.tab = tab
    page.header_top.click_login_button()
    auth_modal = AuthModalComponent(page.driver, page.wait)
    if tab == "register":
        auth_modal.switch_modal_tab_to_registration()
    request.cls.page = page
    request.cls.auth_modal = auth_modal


@pytest.fixture(scope="function")
def open_auth_modal_function(request, page):
    try:
        existing_modal = AuthModalComponent(page.driver, page.wait)
        existing_modal.close_modal()
    except Exception:
        pass
    page.header_top.click_login_button()
    auth_modal = AuthModalComponent(page.driver, page.wait)
    auth_modal.switch_modal_tab_to_registration()
    request.cls.page = page
    request.cls.auth_modal = auth_modal


def attach_screenshot(modal: WebElement, name: str) -> None:
    """Attaches a screenshot of the modal window to Allure report."""
    allure.attach(modal.screenshot_as_png, name=name, attachment_type=allure.attachment_type.PNG)


@allure.suite("Modal Window Tests")
@allure.feature("Authorization")
@allure.story("Authorization Tab Layout")
@pytest.mark.usefixtures("open_auth_modal_class")
@pytest.mark.parametrize("open_auth_modal_class", ["auth"], indirect=True)
class TestAuthorizationTab:
    page: MainPage
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
        attach_screenshot(modal, "Modal screenshot")
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
        assert self.auth_modal.is_auth_email_field_visible(), "Email field not found"

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
        assert self.auth_modal.is_auth_password_field_visible(), "Password field not found"

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
        assert self.auth_modal.is_auth_password_visibility_btn_present(), "Password visibility button not found"

    @allure.title("Password visibility toggle button")
    @allure.description("Checks whether the password visibility toggle correctly shows and hides the password")
    def test_password_field_visibility_btn_working(self, fake_user):
        self.auth_modal.set_auth_password(fake_user.password)
        attach_screenshot(self.auth_modal.get_modal_window(), "Modal screenshot with inserted password")
        assert not self.auth_modal.is_auth_password_visible(), (
            "Password should be hidden by default, but it's visible"
        )

        self.auth_modal.click_auth_password_visibility_btn()
        attach_screenshot(self.auth_modal.get_modal_window(),
                          "Modal screenshot after visibility toggle clicked")
        assert self.auth_modal.is_auth_password_visible(), (
            "Password should be visible after clicking the visibility toggle, but it's still hidden"
        )

        self.auth_modal.click_auth_password_visibility_btn()
        attach_screenshot(self.auth_modal.get_modal_window(),
                          "Modal screenshot after visibility toggle clicked again")
        assert not self.auth_modal.is_auth_password_visible(), (
            "Password should be hidden again after toggling, but it's still visible"
        )

    @allure.title("Remember me checkbox")
    @allure.description("Checks if the remember me checkbox is clickable")
    def test_remember_me_checkbox(self):
        assert self.auth_modal.is_auth_remember_me_checkbox_clickable(), "Remember me switch not clickable"

    @allure.title("Remember me checkbox functionality")
    @allure.description("Click remember me checkbox and check its status after reopening modal")
    def test_remember_me_checkbox_working(self):
        attach_screenshot(self.auth_modal.get_modal_window(), "Modal screenshot before interaction")
        assert self.auth_modal.is_remember_me_checkbox_checked() == False, "Unexpected checkbox status. Expected False"

        attach_screenshot(self.auth_modal.get_modal_window(), (
            "Modal screenshot after remember me checkbox switch on"))
        assert self.auth_modal.set_auth_remember_me_checkbox(True) == True, "Unexpected checkbox status. Expected True"

        self.auth_modal.close_modal()
        self.page.header_top.click_login_button()
        attach_screenshot(self.auth_modal.get_modal_window(), "Modal screenshot after reopening")
        assert self.auth_modal.is_remember_me_checkbox_checked() == True, (
                f"Unexpected checkbox status after modal reopened. Expected True")

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
        assert self.auth_modal.is_auth_submit_btn_clickable(), "Authorization submit button not found or not clickable"

    @allure.title("Submit button attributes")
    @allure.description("Checks if the submit button is clickable and its text and value matches the expected values")
    def test_submit_button_attrs(self):
        assert self.auth_modal.is_auth_submit_btn_clickable(), "Authorization submit button not found or not clickable"
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
@allure.feature("Registration")
@allure.story("Registration Tab Layout")
@pytest.mark.usefixtures("open_auth_modal_class")
@pytest.mark.parametrize("open_auth_modal_class", ["register"], indirect=True)
class TestRegistrationTab:
    page: MainPage
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
        attach_screenshot(modal_registration_tab, "Modal screenshot before submit")
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
        assert self.auth_modal.is_reg_first_name_field_clickable(), "First name field not found"

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
        assert self.auth_modal.is_reg_first_name_field_clickable(), "Last name field not found"

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
        assert self.auth_modal.is_reg_first_name_field_clickable(), "Email field not found"

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
        assert self.auth_modal.is_reg_policy_checkbox_clickable(), "Registration policy checkbox not clickable"

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
        assert self.auth_modal.is_reg_submit_btn_clickable(), "Registration submit button not found or not clickable"

    @allure.title("Submit button attributes")
    @allure.description("Checks if the submit button is clickable and its text and value matches the expected values")
    def test_submit_button_attrs(self):
        assert self.auth_modal.is_reg_submit_btn_clickable(), "Registration submit button not found or not clickable"
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
@allure.feature("Close Button")
@allure.story("Modal Close Button Behavior")
@pytest.mark.parametrize("open_auth_modal_class", ["auth", "register"], indirect=True)
@pytest.mark.usefixtures("open_auth_modal_class")
class TestModalClose:
    page: MainPage
    auth_modal: AuthModalComponent
    tab: str

    def test_close_button_closes_modal(self):
        allure.dynamic.title(f"Close button closes modal (tab: {self.tab})")
        self.auth_modal.close_modal()
        allure.attach(
            self.page.driver.get_screenshot_as_png(),
            name="screenshot_after_close_button_click",
            attachment_type=allure.attachment_type.PNG
        )
        assert self.auth_modal.is_modal_window_not_visible(timeout=.5), "Modal did not close after clicking close button"


@allure.suite("Modal Window Tests")
@allure.feature("Registration")
@allure.story("Form Behavior Without Filling Mandatory Fields")
@pytest.mark.usefixtures("open_auth_modal_function")
class TestRegistrationFormNegativeCases:
    page: MainPage
    auth_modal: AuthModalComponent

    EXPECTED_AUTH_TAB_TITLE = "Регистрация"

    all_combinations = list(itertools.product([False, True], repeat=4))
    invalid_combinations = [combo for combo in all_combinations if not all(combo)]

    @allure.title("Negative registration test")
    @pytest.mark.parametrize("first_name, last_name, email, agree_checked", invalid_combinations)
    def test_submit_with_invalid_data(self, first_name, last_name, email, agree_checked, fake_user):
        attach_screenshot(self.auth_modal.get_modal_window(), "Modal screenshot before interaction")

        if first_name:
            assert self.auth_modal.set_reg_first_name(fake_user.first_name), "Unable to locate field or paste text"
        if last_name:
            assert self.auth_modal.set_reg_last_name(fake_user.last_name), "Unable to locate field or paste text"
        if email:
            assert self.auth_modal.set_reg_email(fake_user.email), "Unable to locate field or paste text"
        if agree_checked:
            assert self.auth_modal.set_reg_policy_checkbox(
                True) == agree_checked, f"Unable to set the checkbox {agree_checked}"
        attach_screenshot(self.auth_modal.get_modal_window(), "Modal screenshot before submit")

        self.auth_modal.click_reg_submit()

        if not agree_checked:
            assert self.auth_modal.get_modal_name().strip().lower() == self.EXPECTED_AUTH_TAB_TITLE.lower(), (
                "User registered without policy agreed"
            )
        else:
            error_text = self.auth_modal.get_reg_error_messages()
            allure.attach(
                "\n".join(error_text),
                name="Validation errors",
                attachment_type=allure.attachment_type.TEXT
            )

            if not first_name:
                assert 'Поле "Имя" обязательно для заполнения' in error_text
            if not last_name:
                assert 'Поле "Фамилия" обязательно для заполнения' in error_text
            if not email:
                assert 'Поле "Адрес e-mail" обязательно для заполнения' in error_text


@allure.suite("Modal Window Tests")
@allure.feature("Registration")
@allure.story("Form Behavior With Filling Mandatory Fields")
@pytest.mark.usefixtures("open_auth_modal_function")
class TestRegistrationFormPositiveCase:
    page: MainPage
    auth_modal: AuthModalComponent

    EXPECTED_LOGGED_IN_BTN_TEXT = "ВЫЙТИ"

    @allure.title("Positive registration test")
    def test_submit_with_correct_data(self, fake_user):
        assert self.auth_modal.set_reg_first_name(fake_user.first_name), "Unable to locate field or paste text"
        assert self.auth_modal.set_reg_last_name(fake_user.last_name), "Unable to locate field or paste text"
        assert self.auth_modal.set_reg_email(fake_user.email), "Unable to locate field or paste text"
        assert self.auth_modal.set_reg_policy_checkbox(True) == True, f"Unable to set the checkbox True"
        attach_screenshot(self.auth_modal.get_modal_window(), "Modal screenshot before submit")

        self.auth_modal.click_reg_submit()

        expected_text = [
            f"Здравствуйте, {fake_user.first_name} {fake_user.last_name}!",
            "Вы зарегистрированы и успешно вошли на сайт!",
            "Сейчас страница автоматически перезагрузится и вы сможете продолжить работу под своим именем."
        ]
        actual_text: list[str] = self.auth_modal.get_reg_successful_text()
        attach_screenshot(self.auth_modal.get_modal_window(), "Modal screenshot after submit")

        assert actual_text == expected_text, (f"Unexpected message text: {actual_text}. "
                                              f"Expected: {expected_text}")

        self.auth_modal.is_modal_window_not_visible(timeout=3)

        button_text = self.page.header_top.get_logged_in_btn_text()

        allure.attach(
            self.page.driver.get_screenshot_as_png(),
            name="screenshot_after_successful registration",
            attachment_type=allure.attachment_type.PNG
        )

        assert button_text == self.EXPECTED_LOGGED_IN_BTN_TEXT, (
            f"Error logging in! Actual login button text: {button_text}. "
            f"Expected login button text: {self.EXPECTED_LOGGED_IN_BTN_TEXT}"
        )


@allure.suite("Modal Window Tests")
@allure.feature("Authorization")
@allure.story("Form Behavior Without Filling Mandatory Fields")
@pytest.mark.usefixtures("open_auth_modal_class")
@pytest.mark.parametrize("open_auth_modal_class", ["auth"], indirect=True)
class TestAuthorizationFormNegativeCases:
    """Negative test cases for authorization tab in modal window with various invalid credential combinations."""

    page: MainPage
    auth_modal: AuthModalComponent

    @allure.title("Modal window")
    @allure.description("Checks that authorization fails when both email and password are invalid")
    def test_authorization_with_invalid_data(self, fake_user):
        attach_screenshot(self.auth_modal.get_modal_window(), "Modal screenshot before interaction")

        assert self.auth_modal.set_auth_email(fake_user.email), "Unable to locate email field or paste data"
        assert self.auth_modal.set_auth_password(fake_user.password), "Unable to locate password field or paste data"
        attach_screenshot(self.auth_modal.get_modal_window(), "Modal screenshot before submit")

        self.auth_modal.click_auth_submit()
        attach_screenshot(self.auth_modal.get_modal_window(), "Modal screenshot after submit")

        error_text = self.auth_modal.get_auth_error_messages()
        assert "Неверный логин или пароль." in error_text, f"Unexpected error text: {error_text}"

    @allure.title("Modal window")
    @allure.description("Checks that authorization fails when password is missing")
    def test_authorization_with_correct_email_and_without_password(self):
        attach_screenshot(self.auth_modal.get_modal_window(), "Modal screenshot before interaction")

        assert self.auth_modal.set_auth_email(USER_LOGIN), "Unable to locate email field or paste data"
        attach_screenshot(self.auth_modal.get_modal_window(), "Modal screenshot before submit")

        self.auth_modal.click_auth_submit()
        attach_screenshot(self.auth_modal.get_modal_window(), "Modal screenshot after submit")

        error_text = self.auth_modal.get_auth_error_messages()
        assert "Неверный логин или пароль." in error_text, f"Unexpected error text: {error_text}"

    @allure.title("Modal window")
    @allure.description("Checks that authorization fails when email is missing")
    def test_authorization_without_email_and_with_correct_password(self):
        attach_screenshot(self.auth_modal.get_modal_window(), "Modal screenshot before interaction")

        assert self.auth_modal.set_auth_password(USER_PASSWORD), "Unable to locate password field or paste data"
        attach_screenshot(self.auth_modal.get_modal_window(), "Modal screenshot before submit")

        self.auth_modal.click_auth_submit()
        attach_screenshot(self.auth_modal.get_modal_window(), "Modal screenshot after submit")

        error_text = self.auth_modal.get_auth_error_messages()
        assert "Неверный логин или пароль." in error_text, f"Unexpected error text: {error_text}"

    @allure.title("Modal window")
    @allure.description("Verifies that the authorization is impossible with valid email and invalid password")
    def test_authorization_with_correct_email_and_invalid_password(self, fake_user):
        attach_screenshot(self.auth_modal.get_modal_window(), "Modal screenshot before interaction")

        assert self.auth_modal.set_auth_email(USER_LOGIN), "Unable to locate email field or paste data"
        assert self.auth_modal.set_auth_password(fake_user.password), "Unable to locate password field or paste data"
        attach_screenshot(self.auth_modal.get_modal_window(), "Modal screenshot before submit")

        self.auth_modal.click_auth_submit()
        attach_screenshot(self.auth_modal.get_modal_window(), "Modal screenshot after submit")

        error_text = self.auth_modal.get_auth_error_messages()
        assert "Неверный логин или пароль." in error_text, f"Unexpected error text: {error_text}"

    @allure.title("Modal window")
    @allure.description("Verifies that the authorization is impossible with invalid email and valid password")
    def test_authorization_with_invalid_email_and_correct_password(self, fake_user):
        attach_screenshot(self.auth_modal.get_modal_window(), "Modal screenshot before interaction")

        assert self.auth_modal.set_auth_email(fake_user.email), "Unable to locate email field or paste data"
        assert self.auth_modal.set_auth_password(USER_PASSWORD), "Unable to locate password field or paste data"
        attach_screenshot(self.auth_modal.get_modal_window(), "Modal screenshot before submit")

        self.auth_modal.click_auth_submit()
        attach_screenshot(self.auth_modal.get_modal_window(), "Modal screenshot after submit")

        error_text = self.auth_modal.get_auth_error_messages()
        assert "Неверный логин или пароль." in error_text, f"Unexpected error text: {error_text}"


@allure.suite("Modal Window Tests")
@allure.feature("Authorization")
@allure.story("Form Behavior With Filling Mandatory Fields")
@pytest.mark.usefixtures("open_auth_modal_class")
@pytest.mark.parametrize("open_auth_modal_class", ["auth"], indirect=True)
class TestAuthorizationFormPositiveCases:
    page: MainPage
    auth_modal: AuthModalComponent

    @allure.title("Modal window")
    @allure.description("Checks that authorization successful with correct data")
    def test_authorization_with_correct_data(self):
        attach_screenshot(self.auth_modal.get_modal_window(), "Modal screenshot before interaction")

        assert self.auth_modal.set_auth_email(USER_LOGIN), "Unable to locate email field or paste data"
        assert self.auth_modal.set_auth_password(USER_PASSWORD), "Unable to locate password field or paste data"
        attach_screenshot(self.auth_modal.get_modal_window(), "Modal screenshot before submit")

        self.auth_modal.click_auth_submit()

        expected_text = [
            f"Здравствуйте, {USER_FIRST_NAME} {USER_LAST_NAME}!",
            "Спасибо за визит на наш сайт!",
        ]
        actual_text: list[str] = self.auth_modal.get_auth_successful_text()
        assert actual_text == expected_text, (f"Unexpected message text: {actual_text}. "
                                              f"Expected: {expected_text}")

        self.auth_modal.is_modal_window_not_visible(timeout=3)

        allure.attach(
            self.page.driver.get_screenshot_as_png(),
            name="screenshot_after_successful registration",
            attachment_type=allure.attachment_type.PNG
        )

        assert self.page.header_top.is_user_authorized(), (
            f"Authorization error! Actual login button text: {self.page.header_top.get_logged_in_btn_text()}. "
            f"Expected login button text: {self.page.header_top.EXPECTED_LOGGED_IN_BTN_TEXT}"
        )
