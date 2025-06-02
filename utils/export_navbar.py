"""
Script for exporting the 'Каталог' dropdown menu (navbar__submenu) items from the website.

- Launches a Chrome browser using Selenium WebDriver
- Navigates to the BASE_URL
- Waits for all submenu links under 'Каталог' to be present
- Extracts the text content and href from each submenu link
- Saves the collected data as JSON to testdata/expected_navbar_submenu.json

This script is intended for manual execution and is useful for generating
up-to-date expected data for automated tests.

Run with:
    python utils/export_navbar.py
"""
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.settings import BASE_URL

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "testdata", "expected_navbar_submenu.json")


def export_navbar():
    driver = webdriver.Chrome()  # или другой нужный драйвер
    driver.get(BASE_URL)

    wait = WebDriverWait(driver, 10)
    submenu_links = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "ul.navbar__submenu li.navbar__submenu-item a.navbar__submenu-link")
    ))

    print(f'{len(submenu_links)} categories found:')
    for link in submenu_links:
        print(f"{link.get_attribute("textContent")} - {link.get_attribute('href')}")

    data = [
        {
            "text": link.get_attribute("textContent"),
            "href": link.get_attribute('href')
        }
        for link in submenu_links
    ]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Exported {len(data)} submenu items to {OUTPUT_FILE}")
    driver.quit()

if __name__ == "__main__":
    export_navbar()