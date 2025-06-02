import allure
import json
import pytest_check as check

from pages.main_page import MainPage
from utils.json_loader import load_testdata_json


@allure.title("Main page check")
@allure.feature("Smoke-tests")
def test_main_page_loads(main_page: MainPage) -> None:
    page_title: str = main_page.driver.title.strip()

    with allure.step("Page title check"):
        check.not_equal(page_title, "", "Page title is empty")
        check.is_in("Velo1000", page_title, "Page title doesn't contain website name")
    allure.attach(
        main_page.driver.get_screenshot_as_png(),
        name="screenshot_after_load",
        attachment_type=allure.attachment_type.PNG
    )


@allure.title("Main page top header check")
@allure.feature("Smoke-tests")
def test_main_page_top_header(main_page: MainPage) -> None:
    logo_src: str = main_page.get_logo_src()
    logo_link: str = main_page.get_logo_link()
    logo_image: bytes = main_page.download_logo_as_bytes(logo_src)
    actual_top_header_menu: list[tuple[str, str]] = main_page.get_top_header_menu_items()

    with allure.step("Website logo present"):
        allure.attach(
            logo_image,
            name="logo_image",
            attachment_type=allure.attachment_type.PNG
        )
        check.is_true(main_page.logo_is_visible(), "Website logo is not visible")

    with allure.step("Website logo has correct path"):
        allure.attach(
            logo_src,
            name="actual_logo_src",
            attachment_type=allure.attachment_type.TEXT
        )
        check.is_true(logo_src.endswith("/local/templates/velo1000/images/logo.png"),
                      f"Unexpected logo src: {logo_src}"
                      )

    with allure.step("Website logo has correct link"):
        allure.attach(
            logo_link,
            name="actual_logo_link",
            attachment_type=allure.attachment_type.TEXT
        )
        check.equal(logo_link, main_page.base_url, f"Unexpected logo link: {logo_link}")

    with allure.step("Top header menu has correct items"):
        expected_top_header_items = load_testdata_json("expected_top_header_items.json")
        for text, href in actual_top_header_menu:
            if check.is_in(text, expected_top_header_items, f"Unexpected top header menu item: {text}"):
                expected_url = expected_top_header_items[text]
                check.is_true(href.endswith(expected_url), f"Unexpected top header url: {href}")
        allure.attach(
            json.dumps(actual_top_header_menu, ensure_ascii=False, indent=2),
            name="actual_top_header_menu",
            attachment_type=allure.attachment_type.JSON
        )


@allure.title("Main page navigation header check")
@allure.feature("Smoke-tests")
def test_main_page_nav_header(main_page: MainPage) -> None:
    logo_src: str = main_page.get_navigation_menu_logo_src()
    logo_link: str = main_page.get_navigation_menu_logo_link()
    logo_image: bytes = main_page.download_navigation_menu_logo_as_bytes(logo_src)
    actual_nav_header_menu: list[tuple[str, str]] = main_page.get_nav_header_menu_items()
    actual_nav_header_submenu: list[tuple[str, str]] = main_page.get_nav_header_submenu_items()

    with allure.step("Website navigation menu logo present"):
        allure.attach(
            logo_image,
            name="logo_image",
            attachment_type=allure.attachment_type.PNG
        )
        check.is_true(main_page.logo_is_visible(), "Website logo is not visible")

    with allure.step("Website navigation menu logo has correct path"):
        allure.attach(
            logo_src,
            name="actual_logo_src",
            attachment_type=allure.attachment_type.TEXT
        )
        check.is_true(logo_src.endswith("/local/templates/velo1000/images/velo1000.png"),
                      f"Unexpected logo src: {logo_src}"
                      )

    with allure.step("Website navigation menu logo has correct link"):
        allure.attach(
            logo_link,
            name="actual_logo_link",
            attachment_type=allure.attachment_type.TEXT
        )
        check.equal(logo_link, main_page.base_url, f"Unexpected logo link: {logo_link}")

    with allure.step("Navigation header menu has correct items"):
        expected_nav_header_items = load_testdata_json("expected_nav_header_items.json")
        for text, href in actual_nav_header_menu:
            check.is_in(text, expected_nav_header_items, f"Unexpected navigation header menu item: {text}")
            expected_url = expected_nav_header_items[text]
            check.is_true(href.endswith(expected_url), f"Unexpected navigation header url: {href}")
        allure.attach(
            json.dumps(actual_nav_header_menu, ensure_ascii=False, indent=2),
            name="actual_navigation_header_menu",
            attachment_type=allure.attachment_type.JSON
        )

    with allure.step("Navigation header submenu has correct items"):
        expected_submenu = load_testdata_json("expected_navbar_submenu.json")
        diff_lines = []
        for idx, (expected, actual) in enumerate(zip(expected_submenu, actual_nav_header_submenu), 1):
            diff_lines.append(f"{idx}. EXPECTED: {json.dumps(expected, ensure_ascii=False)}")
            diff_lines.append(f"   ACTUAL:   {json.dumps(actual, ensure_ascii=False)}")
        comparison_report = "\n".join(diff_lines)
        allure.attach(
            comparison_report,
            name="submenu_comparison",
            attachment_type=allure.attachment_type.TEXT
        )
        check.equal(expected_submenu, actual_nav_header_submenu, f"Unexpected navigation submenu: {expected_submenu}")


@allure.title("Test search bar UI")
@allure.feature("Smoke-tests")
def test_search_bar_ui(main_page: MainPage) -> None:

    with allure.step("Search button is present"):
        check.is_true(main_page.search_button_present(), "Search button is not present")

    with allure.step("Search field is reachable"):
        main_page.click_search_button()
        check.is_true(main_page.search_field_present(), "Search field is not reachable")
        allure.attach(
            main_page.driver.get_screenshot_as_png(),
            name="screenshot_after_search_button_click",
            attachment_type=allure.attachment_type.PNG
        )

    with allure.step("Submitting empty search does not change URL"):
        main_page.click_submit_search_button()
        check.is_false(main_page.url_changed_from_base(), "Url changed after submitting empty request")

    with allure.step("Search close button is operable"):
        allure.attach(
            main_page.driver.get_screenshot_as_png(),
            name="screenshot_before_cancel_search_button_click",
            attachment_type=allure.attachment_type.PNG
        )
        main_page.click_cancel_search_button()
        check.is_false(main_page.search_field_present(), "Search field does not close")


