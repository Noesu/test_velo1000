import allure
import pytest_check as check

from pages.main_page import MainPage


@allure.suite("Main Page Tests")
@allure.title("Main page check")
@allure.feature("Smoke-tests")
def test_main_page_loads(page: MainPage) -> None:
    page_title: str = page.driver.title.strip()

    with allure.step("Page title check"):
        check.not_equal(page_title, "", "Page title is empty")
        check.is_in("Velo1000", page_title, "Page title doesn't contain website name")
    allure.attach(
        page.driver.get_screenshot_as_png(),
        name="screenshot_after_load",
        attachment_type=allure.attachment_type.PNG
    )
