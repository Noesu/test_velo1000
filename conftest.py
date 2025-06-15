from dataclasses import dataclass
from faker import Faker
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.main_page import MainPage
from config.settings import USER_LOGIN, USER_PASSWORD


faker = Faker()

@dataclass
class FakeUser:
    first_name: str
    last_name: str
    email: str
    password: str

def _perform_login(page):
    wait = page.wait
    driver = page.driver
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "div.button-header.button-acc")))
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "div.button-header.button-acc"))).click()
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, 'input[name="USER_LOGIN"]'))).send_keys(USER_LOGIN)
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, 'input[name="USER_PASSWORD"]'))).send_keys(USER_PASSWORD)
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'button[type="submit"][name="Login"]'))).click()
    wait.until_not(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "div.popup-auth__inner")))

@pytest.fixture(scope="class")
def browser():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

@pytest.fixture(scope="class")
def page(request, browser):
    user_type = getattr(request, "param", "guest")
    page = MainPage(browser)
    page.open()
    if user_type == "user":
        _perform_login(page)
    return page

@pytest.fixture
def fake_user():
    return FakeUser(
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        email=faker.email(),
        password=faker.password()
    )
