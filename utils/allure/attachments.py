from typing import Union

import allure
import json
from selenium.webdriver.remote.webelement import WebElement

def attach_text(text: str, name: str) -> None:
    allure.attach(text, name=name, attachment_type=allure.attachment_type.TEXT)

def attach_element_screenshot(element: WebElement, name: str = "element screenshot") -> None:
    allure.attach(element.screenshot_as_png, name=name, attachment_type=allure.attachment_type.PNG)

def attach_screenshot(driver, name: str = "page screenshot") -> None:
    allure.attach(driver.get_screenshot_as_png(), name=name, attachment_type=allure.attachment_type.PNG)

def attach_image(image: bytes, name: str="image") -> None:
    allure.attach(image, name=name, attachment_type=allure.attachment_type.PNG)

def attach_json(data: Union[dict, list], name: str) -> None:
    try:
        json_text = json.dumps(data, ensure_ascii=False, indent=2)
        allure.attach(json_text, name=name, attachment_type=allure.attachment_type.JSON)
    except (TypeError, ValueError) as e:
        attach_text(str(e), name=f"{name}_error")