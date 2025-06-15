"""
Script for exporting the Profile dropdown menu (.button-header.button-profile) items from the website for guest and
authorized user to separate files.

For guest user:
- Launches a Chrome browser using Selenium WebDriver
- Navigates to the BASE_URL
- Waits for all profile links under profile menu to be present
- Extracts the text content and href from each profile menu link
- Opens href and extracts breadcrumbs, title and alert from each page
- Saves the collected data as JSON to testdata/expected_profile_menu_guest.json

For authorized user:
- Launches a Chrome browser using Selenium WebDriver
- Navigates to the BASE_URL
- Opens modal authorization window and performs login
- Waits for all profile links under profile menu to be present
- Extracts the text content and href from each profile menu link
- Opens href and extracts breadcrumbs, title and alert from each page
- Saves the collected data as JSON to testdata/expected_profile_menu_user.json

This script is intended for manual execution and is useful for generating
up-to-date expected data for automated tests.

Run with:
    python utils/export_profile_menu.py
"""
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from config.settings import BASE_URL, USER_LOGIN, USER_PASSWORD

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))


def _perform_login(wait):
    print(f"Logging in as {USER_LOGIN}", end="")
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "div.button-header.button-acc")))
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "div.button-header.button-acc"))).click()
    print(".", end="")
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, 'input[name="USER_LOGIN"]'))).send_keys(USER_LOGIN)
    print(".", end="")
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, 'input[name="USER_PASSWORD"]'))).send_keys(USER_PASSWORD)
    print(".", end="")
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'button[type="submit"][name="Login"]'))).click()
    print(".")
    wait.until_not(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "div.popup-auth__inner")))
    print(f"Login successful")

def export_profile_menu_items(auth: bool = False):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.get(BASE_URL)

    wait = WebDriverWait(driver, 10)

    if auth:
        output_file = os.path.join(PROJECT_ROOT, "testdata", "expected_profile_menu_user.json")
        print(f"Creating {output_file}")
        _perform_login(wait)
    else:
        output_file = os.path.join(PROJECT_ROOT, "testdata", "expected_profile_menu_guest.json")
        print(f"Creating {output_file}")

    submenu_links = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "div.button-header.button-profile .profile-popup__link")
    ))
    print(f'{len(submenu_links)} menu items found:')

    menu_item_data = []
    breadcrumbs_list = []
    page_title_list = []
    alerts_list = []
    need_auth_list = []

    for item in submenu_links:
        text = item.get_attribute("textContent").strip()
        href = item.get_attribute('href')
        menu_item_data.append({"text": text, "href": href})

    for page in menu_item_data:
        print(f"Adding menu item: {page["text"]} - {page["href"]}")
        print("   loading page...")
        driver.get(page["href"])

        breadcrumbs_elements: list[WebElement] = wait.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.breadcrumbs-item")))
        breadcrumbs_text = [el.text for el in breadcrumbs_elements]
        breadcrumbs_list.append(breadcrumbs_text)
        print(f"   breadcrumbs found: {" > ".join(breadcrumbs_text)}")

        page_title: WebElement = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.page-title")))
        page_title_text = page_title.text
        page_title_list.append(page_title_text)
        print(f"   title found: {page_title_text}")

        try:
            alert_element: WebElement = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.alert-danger")))
            alert_text = alert_element.text
            print(f"   alert found: {alert_text}")
            alerts_list.append(alert_text)
            need_auth_list.append(True)
        except TimeoutException:
            alerts_list.append(None)
            print("   alert not found")
            need_auth_list.append(False)

    output = [
        {"text": item["text"],
         "href": item["href"],
         "breadcrumbs": breadcrumbs,
         "title": title,
         "alert": alert,
         "source": item["href"].split("/")[-2],
         "need_auth": need_auth}
        for item, breadcrumbs, title, alert, need_auth in zip(
            menu_item_data,
            breadcrumbs_list,
            page_title_list,
            alerts_list,
            need_auth_list
        )
    ]

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Exported {len(output)} submenu items to {output_file}")
    driver.quit()


if __name__ == "__main__":
    print(f"This script will export testdata for user profile menu.\n")
    export_profile_menu_items()
    export_profile_menu_items(auth=True)
