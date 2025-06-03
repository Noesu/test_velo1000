# from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
# from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC


class SearchResultsPage:
    PRODUCT_BLOCK = (By.CSS_SELECTOR, ".product__block")

    def __init__(self, driver, wait) -> None:
        self.driver = driver
        self.wait = wait

    def number_of_search_results(self) -> int:
        return len(self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_BLOCK)))
