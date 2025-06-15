import allure
import pytest
import pytest_check as check
from typing import Optional

from pages.authorization_page import AuthorizationPage
from pages.contacts_page import ContactsPage
from pages.delivery_page import DeliveryPage
from pages.faq_page import FAQPage
from pages.return_rules_page import ReturnRulesPage
from pages.shops_page import ShopsPage
from utils.json_loader import load_testdata_json

menu_items_guest = load_testdata_json("expected_profile_menu_guest.json")
menu_items_user = load_testdata_json("expected_profile_menu_user.json")

test_data = [
    pytest.param("guest", item, id=f"guest: {item['source']}") for item in menu_items_guest
] + [
    pytest.param("user", item, id=f"user: {item['source']}") for item in menu_items_user
]

PAGE_CLASS_MAPPING = {
    "private": AuthorizationPage,
    "orders": AuthorizationPage,
    "shops": ShopsPage,
    "faq": FAQPage,
    "delivery": DeliveryPage,
    "return_rules": ReturnRulesPage,
    "contacts": ContactsPage,
}

def attach_page_screenshot(main_page, name):
    allure.attach(main_page.driver.get_screenshot_as_png(), name=name, attachment_type=allure.attachment_type.PNG)

def resolve_page(source: str, driver, wait):
    page_class = PAGE_CLASS_MAPPING.get(source)
    if page_class is None:
        raise ValueError(f"No page class found for source: {source}")
    return page_class(driver, wait)


@allure.suite("Profile Menu Component Tests")
@allure.feature("Smoke-tests")
@pytest.mark.parametrize("page,menu_item", test_data, indirect=["page"])
def test_profile_menu(page, menu_item, request):
    user_type = request.node.callspec.params["page"]
    allure.dynamic.story(f"Profile menu - {'Authorized' if user_type == 'user' else 'Guest'}")
    allure.dynamic.title(f"Menu item '{menu_item['source']}' for {user_type}")

    page.get(menu_item["href"])
    result = resolve_page(menu_item["source"], page.driver, page.wait)
    attach_page_screenshot(page, "Opened page")

    with allure.step("Breadcrumbs are valid on target page"):
        actual_breadcrumbs: list[str] = result.get_breadcrumbs_text()
        expected_breadcrumbs: list[str] = menu_item["breadcrumbs"]
        check.equal(actual_breadcrumbs, expected_breadcrumbs, (
            f"Unexpected breadcrumbs: {' > '.join(actual_breadcrumbs)} "
            f"Expected: {' > '.join(expected_breadcrumbs)}")
                    )

    with allure.step("Title is valid on target page"):
        actual_title: str = result.get_page_title()
        expected_title: str = menu_item["title"]
        check.equal(actual_title, expected_title, (
            f"Unexpected title: {actual_title}. "
            f"Expected: {expected_title}")
                    )

    with allure.step("Alert is valid or not present on target page"):
        expected_alert: Optional[str] = menu_item["alert"]
        actual_alert: Optional[str] = result.get_alert_text()
        check.equal(expected_alert, actual_alert, (
            f"Unexpected alert: {actual_alert}. "
            f"Expected: {expected_alert}")
                    )
