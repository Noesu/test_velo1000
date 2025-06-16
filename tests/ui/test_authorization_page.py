import allure
import pytest

from config.settings import USER_LOGIN, USER_PASSWORD
from pages.authorization_page import AuthorizationPage
from pages.main_page import MainPage
from utils.allure import attach_screenshot, attach_text


page_url = "https://velo1000.ru/personal/"

@pytest.fixture()
def auth_page(page):
    page.get(page_url)
    return AuthorizationPage(page.driver, page.wait)


@allure.suite("Separate Pages")
@allure.feature("Smoke-tests")
@allure.story("Page Layout")
class TestAuthorizationPageElements:

    @allure.title("Authorization Page Has correct URL")
    def test_page_is_loaded(self, auth_page):
        attach_screenshot(auth_page.driver)
        actual_url = auth_page.get_page_url()
        attach_text(actual_url, "Page URL")
        assert actual_url.endswith(page_url), f"Unexpected page URL: {actual_url}. Expected {page_url}"

    @allure.title("Authorization Page Displays Correct Breadcrumbs")
    def test_breadcrumbs_text(self, auth_page):
        actual_breadcrumbs: list[str] = auth_page.get_breadcrumbs_text()
        expected_breadcrumbs: list[str] = ["Главная", "Мой кабинет"]
        attach_text(' > '.join(actual_breadcrumbs), "Actual breadcrumbs")
        assert actual_breadcrumbs == expected_breadcrumbs, (
                f'Unexpected breadcrumbs: {actual_breadcrumbs}. Expected {expected_breadcrumbs}'
        )

    @allure.title("Authorization Page Displays Correct Title")
    def test_title_text(self, auth_page):
        actual_title: str = auth_page.get_page_title()
        expected_title: str = "Авторизация".upper()
        attach_text(actual_title, "Actual page title")
        assert actual_title == expected_title, f'Unexpected page title: {actual_title}. Expected {expected_title}'

    @allure.title("Authorization Page Has Login Field")
    def test_login_field_exists(self, auth_page):
        assert auth_page.is_login_field_enabled(), "Login field not found"

    @allure.title("Authorization Page Has Password Field")
    def test_password_field_exists(self, auth_page):
        assert auth_page.is_password_field_enabled(), "Password field not found"

    @allure.title("Authorization Page Has Remember Me Checkbox")
    def test_remember_me_checkbox_exists(self, auth_page):
        assert auth_page.is_remember_me_checkbox_clickable(), "Remember me checkbox is not clickable"

    @allure.title("Authorization Page Has Submit Button")
    def test_submit_button_exists(self, auth_page):
        assert auth_page.is_submit_button_clickable(), "Submit button is not clickable"
        actual_button_text = auth_page.get_submit_button_text()
        expected_button_text = "Войти".upper()
        assert expected_button_text == actual_button_text, (
            f"Unexpected submit button text: {actual_button_text}. "
            f"Expected {expected_button_text}"
        )

    @allure.title("Authorization Page Has Forgot Password Link")
    def test_forgot_password_and_registration_links(self, auth_page):
        expected_forgot_password_link = "/personal/?forgot_password=yes"
        expected_registration_link = "/personal/?register=yes"
        actual_forgot_password_link, actual_registration_link = auth_page.get_forgot_password_and_registration_links()
        attach_text(actual_forgot_password_link, "Forgot password link")
        attach_text(actual_registration_link, "Registration link")
        assert actual_forgot_password_link.endswith(expected_forgot_password_link), (
            f"Unexpected forgot password link: {actual_forgot_password_link}. "
            f"Expected: {expected_forgot_password_link}"
        )
        assert actual_registration_link.endswith(expected_registration_link), (
            f"Unexpected registration link: {actual_registration_link}. "
            f"Expected: {expected_registration_link}"
        )

@allure.suite("Separate Pages")
@allure.feature("Smoke-tests")
@allure.story("Page Interaction")
class TestAuthorizationPagePositiveCase:

    def test_authorization_successful(self, auth_page):
        auth_page.set_login_field(USER_LOGIN)
        auth_page.set_password_field(USER_PASSWORD)
        auth_page.click_submit_button()

        main_page = MainPage(auth_page.driver)
        attach_screenshot(auth_page.driver, "Screenshot after authorization submit")
        assert main_page.header_top.is_user_authorized(), (
            f"Authorization error! Actual login button text: {main_page.header_top.get_logged_in_btn_text()}. "
            f"Expected login button text: {main_page.header_top.EXPECTED_LOGGED_IN_BTN_TEXT}"
        )
