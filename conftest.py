import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.main_page import MainPage


@pytest.fixture(scope="class")
def browser():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

@pytest.fixture
def main_page(browser):
    page = MainPage(browser)
    page.open()
    return page

@pytest.fixture
def authorized_main_page(main_page):
    main_page.header_top.click_login_button()
    main_page.login_page.login("test_user", "secure_password")  # предполагается login_page и метод login
    return main_page