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
