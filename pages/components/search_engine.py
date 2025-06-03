import allure
import requests
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from typing import Optional

from pages.search_results_page import SearchResultsPage

class SearchEngine:
    SEARCH_FIELD_SUBMIT_BUTTON = (By.CSS_SELECTOR, ".form-actions .button-style.button-style--red")
    SEARCH_FIELD_CANCEL_BUTTON = (By.CSS_SELECTOR, ".form-actions .search-close-btn")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "div.button-header.button-search")
    SEARCH_FIELD = (By.ID, "input__search")

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait


    def search_field_present(self) -> bool:
        try:
            self.wait.until(EC.all_of(
                EC.element_to_be_clickable(self.SEARCH_FIELD),
                EC.visibility_of_element_located(self.SEARCH_FIELD_SUBMIT_BUTTON),
                EC.element_to_be_clickable(self.SEARCH_FIELD_SUBMIT_BUTTON),
                EC.visibility_of_element_located(self.SEARCH_FIELD_CANCEL_BUTTON),
                EC.element_to_be_clickable(self.SEARCH_FIELD_CANCEL_BUTTON)
            ))
            return True
        except TimeoutException:
            return False

    def click_submit_search_button(self):
        self.driver.find_element(*self.SEARCH_FIELD_SUBMIT_BUTTON).click()
        return SearchResultsPage(self.driver, self.wait)

    def click_cancel_search_button(self):
        self.driver.find_element(*self.SEARCH_FIELD_CANCEL_BUTTON).click()

    def insert_search(self, query: str):
        search_field = self.wait.until(EC.visibility_of_element_located(self.SEARCH_FIELD))
        search_field.send_keys(query)
