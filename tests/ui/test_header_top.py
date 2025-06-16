import allure
import pytest_check as check

from pages.components.auth_modal import AuthModalComponent
from utils.allure import attach_text, attach_json, attach_image, attach_screenshot, attach_element_screenshot
from utils.json_loader import load_testdata_json


@allure.suite("Header Top Component Tests")
@allure.feature("Smoke-tests")
@allure.story("Top header")
@allure.title("Top header visibility and correctness check")
def test_top_header_components(page) -> None:
    check_logo(page)
    check_menu_items(page)

def check_logo(main_page):
    logo_src: str = main_page.header_top.get_logo_src()
    logo_link: str = main_page.header_top.get_logo_link()
    logo_image: bytes = main_page.header_top.download_logo_as_bytes(logo_src)

    with allure.step("Website logo present"):
        attach_image(logo_image, "Logo image")
        check.is_true(main_page.header_top.logo_is_visible(), "Website logo is not visible")

    with allure.step("Website logo has correct path"):
        attach_text(logo_src, "actual logo src")
        check.is_true(logo_src.endswith("/local/templates/velo1000/images/logo.png"),
                      f"Unexpected logo src: {logo_src}"
                      )

    with allure.step("Website logo has correct link"):
        attach_text(logo_link, "actual logo link")
        check.equal(logo_link, main_page.base_url, f"Unexpected logo link: {logo_link}")


def check_menu_items(main_page) -> None:
    actual_top_header_menu: list[tuple[str, str]] = main_page.header_top.get_top_header_menu_items()

    with allure.step("Top header menu has correct items"):
        expected_top_header_items = load_testdata_json("expected_top_header_items.json")
        for text, href in actual_top_header_menu:
            if check.is_in(text, expected_top_header_items, f"Unexpected top header menu item: {text}"):
                expected_url = expected_top_header_items[text]
                check.is_true(href.endswith(expected_url), f"Unexpected top header url: {href}")
        attach_json(actual_top_header_menu, "actual top header menu")


@allure.suite("Header Top Component Tests")
@allure.feature("Smoke-tests")
@allure.story("Search button")
@allure.title("Test search bar opens with search button and closes with close button")
def test_search_button(page) -> None:
    with allure.step("Search button is present"):
        check.is_true(page.header_top.search_button_present(), "Search button is not present")

    with allure.step("Search field is reachable"):
        page.header_top.click_search_button()
        check.is_true(page.search_engine.search_field_present(), "Search field is not reachable")
        attach_screenshot(page.driver, "screenshot after search button click")

    with allure.step("Search close button is operable"):
        attach_screenshot(page.driver, "screenshot before cancel search button click")
        page.search_engine.click_cancel_search_button()
        assert not page.search_engine.search_field_present(), "Search field does not close"


@allure.suite("Header Top Component Tests")
@allure.feature("Smoke-tests")
@allure.story("Profile menu")
@allure.title("Test profile menu contains all necessary items")
def test_profile_menu(page) -> None:
    actual_profile_menu: list[tuple[str, str]] = page.header_top.get_profile_menu_items()
    expected_profile_menu = load_testdata_json("expected_profile_menu_guest.json")

    expected_texts = [item["text"] for item in expected_profile_menu]
    expected_hrefs = {item["text"]: item["href"] for item in expected_profile_menu}

    with allure.step("Profile menu has correct items"):
        for text, href in actual_profile_menu:
            if check.is_in(text, expected_texts, f"Unexpected top header menu item: {text}"):
                expected_href = expected_hrefs[text]
                check.is_true(href.endswith(expected_href), f"Unexpected top header url: {href}")
        attach_json(actual_profile_menu, "actual top header menu")


@allure.suite("Header Top Component Tests")
@allure.feature("Smoke-tests")
@allure.story("Authorization/registration modal")
@allure.title("Modal window is shown after clicking login button")
def test_login_button(page) -> None:
    with allure.step("Modal window is showing up after login button click"):
        page.header_top.click_login_button()
        auth_modal = AuthModalComponent(page.driver, page.wait)
        modal_window = auth_modal.get_modal_window()
        attach_element_screenshot(modal_window, "modal_window")
        check.is_true(modal_window, "Modal window doesn't showing up")



