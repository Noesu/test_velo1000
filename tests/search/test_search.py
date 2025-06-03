import allure
import pytest

from utils.json_loader import load_testdata_json

@pytest.mark.parametrize("case", load_testdata_json("testdata_search.json"))
@allure.title("Search bar query: {case[description]}")
@allure.feature("Smoke-tests")
@allure.story("Search engine")
def test_search_query(main_page, case):
    query = case["query"]
    expect_results = case.get("expect_results", False)
    description = case["description"]
    min_results = case.get("min_results", 0)
    expect_navigation = case.get("expect_navigation", True)

    with allure.step(f"{description}. Query:{query}"):
        main_page.header_top.click_search_button()
        main_page.search_engine.insert_search(query)
        try:
            search_results_page = main_page.search_engine.click_submit_search_button()
        except Exception:
            allure.attach(
                main_page.driver.get_screenshot_as_png(),
                name="screenshot_after_error_submitting_search_button",
                attachment_type=allure.attachment_type.PNG
            )

        if not expect_navigation:
            assert main_page.url_changed_from_base() == False, "Url changed after submitting empty request"

        else:
            if expect_results:
                assert search_results_page.number_of_search_results() >= min_results, f"No results for query: {query}"

        allure.attach(
            main_page.driver.get_screenshot_as_png(),
            name="screenshot_with_search_results",
            attachment_type=allure.attachment_type.PNG
        )
