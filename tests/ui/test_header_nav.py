import allure
import json
import pytest_check as check

from utils.json_loader import load_testdata_json


@allure.feature("Smoke-tests")
@allure.story("Navigation header")
@allure.title("Main page navigation header visibility and correctness check")
def test_nav_header_components(main_page) -> None:
    check_nav_header_logo(main_page)
    check_nav_header_menu_items(main_page)
    check_nav_header_submenu_items(main_page)

def check_nav_header_logo(main_page):
    logo_src: str = main_page.header_nav.get_navigation_menu_logo_src()
    logo_link: str = main_page.header_nav.get_navigation_menu_logo_link()
    logo_image: bytes = main_page.header_nav.download_navigation_menu_logo_as_bytes(logo_src)

    with allure.step("Navigation header menu logo present"):
        allure.attach(
            logo_image,
            name="logo_image",
            attachment_type=allure.attachment_type.PNG
        )
        check.is_true(main_page.header_nav.logo_is_visible(), "Navigation header menu logo is not visible")

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

def check_nav_header_menu_items(main_page):
    actual_nav_header_menu: list[tuple[str, str]] = main_page.header_nav.get_nav_header_menu_items()

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

def check_nav_header_submenu_items(main_page):
    actual_nav_header_submenu: list[tuple[str, str]] = main_page.header_nav.get_nav_header_submenu_items()

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
