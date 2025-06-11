from dataclasses import dataclass
from faker import Faker
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.main_page import MainPage


faker = Faker()

@dataclass
class FakeUser:
    first_name: str
    last_name: str
    email: str

@pytest.fixture(scope="class")
def browser():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

@pytest.fixture(scope="class")
def main_page(browser):
    page = MainPage(browser)
    page.open()
    return page

@pytest.fixture
def fake_user():
    return FakeUser(
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        email=faker.email(),
    )

# @pytest.fixture
# def authorized_main_page(main_page):
#     main_page.header_top.click_login_button()
#     main_page.login_page.login("test_user", "secure_password")  # предполагается login_page и метод login
#     return main_page