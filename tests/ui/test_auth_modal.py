import time

import allure
import pytest_check as check

from pages.components.auth_modal import AuthModalComponent


@allure.feature("Login modal")
@allure.story("Authorization tab layout")
def test_modal_auth_tab_elements_present(main_page):
    EXPECTED_AUTH_TAB_TITLE = "Авторизация"
    EXPECTED_AUTH_EMAIL_PLACEHOLDER = "Эл. почта"
    EXPECTED_AUTH_PASSWORD_PLACEHOLDER = "Пароль"
    EXPECTED_AUTH_FORGOT_PASSWORD_LINK = "/local/ajax/auth.php?forgot_password=yes&backurl=%2Flocal%2Fajax%2Fauth.php"
    EXPECTED_AUTH_SUBMIT_BUTTON_TEXT_AND_VALUE = "Войти"

    main_page.header_top.click_login_button()
    auth_modal = AuthModalComponent(main_page.driver, main_page.wait)

    with allure.step("Authorization tab is open"):
        modal_authorization_tab = auth_modal.get_modal_window()
        check.is_true(modal_authorization_tab, "Authorization tab doesn't showing up")
        allure.attach(
            modal_authorization_tab.screenshot_as_png,
            name="modal_authorization_tab",
            attachment_type=allure.attachment_type.PNG
        )

    with allure.step("Title is correct"):
        modal_tab_title = auth_modal.get_modal_name()
        check.equal(modal_tab_title,
                    EXPECTED_AUTH_TAB_TITLE.upper(),
                    f"Unexpected modal title: '{modal_tab_title}'. "
                    f"Expected: '{EXPECTED_AUTH_TAB_TITLE.upper()}'.")
        allure.attach(modal_tab_title,
            name="Authorization tab title",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Email field is visible and has correct placeholder"):
        check.is_true(auth_modal.get_auth_email_field(), "Email field not found")
        email_placeholder = auth_modal.get_auth_email_placeholder_text()
        check.equal(email_placeholder,
                    EXPECTED_AUTH_EMAIL_PLACEHOLDER,
                    f"Unexpected email placeholder text: '{email_placeholder}'. "
                    f"Expected: '{EXPECTED_AUTH_EMAIL_PLACEHOLDER}'."
                    )
        allure.attach(email_placeholder,
            name="Email placeholder",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Password field is visible, has correct placeholder and visibility button"):
        check.is_true(auth_modal.get_auth_password_field(), "Password field not found")
        password_placeholder = auth_modal.get_auth_password_placeholder_text()
        check.equal(password_placeholder,
                    EXPECTED_AUTH_PASSWORD_PLACEHOLDER,
                    f"Unexpected password placeholder text: '{password_placeholder}'. "
                    f"Expected: '{EXPECTED_AUTH_PASSWORD_PLACEHOLDER}'."
                    )
        check.is_true(auth_modal.get_auth_password_visibility_btn(), "Password visibility button not found")
        allure.attach(password_placeholder,
            name="Password placeholder",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Remember me switch is clickable"):
        check.is_true(auth_modal.get_auth_remember_me_switch(), "Remember me switch not clickable")

    with allure.step("Forgot password link is correct"):
        forgot_password_link = auth_modal.get_auth_forgot_password_link()
        check.is_true(forgot_password_link.endswith(EXPECTED_AUTH_FORGOT_PASSWORD_LINK),
                    f"Unexpected forgot password link: '{forgot_password_link}'. "
                    f"Expected: '{EXPECTED_AUTH_FORGOT_PASSWORD_LINK}'.")
        allure.attach(forgot_password_link,
            name="Forgot password link",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Submit button is clickable and have proper text and attribute"):
        button_attrs = auth_modal.get_auth_submit_btn_text_and_value()
        check.is_true(button_attrs, "Authorization submit button not found or not clickable")
        if button_attrs:
            button_text, button_value = button_attrs
            check.equal(button_text,
                        EXPECTED_AUTH_SUBMIT_BUTTON_TEXT_AND_VALUE.upper(),
                        f"Unexpected authorization submit button text: {button_text}. "
                        f"Expected: {EXPECTED_AUTH_SUBMIT_BUTTON_TEXT_AND_VALUE.upper()}")
            check.equal(button_value,
                        EXPECTED_AUTH_SUBMIT_BUTTON_TEXT_AND_VALUE,
                        f"Unexpected authorization submit button text: {button_value}. "
                        f"Expected: {EXPECTED_AUTH_SUBMIT_BUTTON_TEXT_AND_VALUE}")
        allure.attach(
            f"Button text: {button_text}. Button value: {button_value}",
            name="modal_authorization_tab",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Link for registration tab is correct"):
        registration_tab_link = auth_modal.get_modal_tab_link()
        check.is_true(registration_tab_link, "Link for registration tab not found")
        check.is_true(registration_tab_link.endswith(
            "/local/ajax/auth.php?register=yes&backurl=%2Flocal%2Fajax%2Fauth.php"
        ))
        allure.attach(
            registration_tab_link,
            name="registration_tab_link",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Modal window is closing up after authorization tab close button click"):
        auth_modal.close_modal_btn()
        check.is_true(auth_modal.modal_window_not_visible(), "Modal window not closed")
        allure.attach(
            main_page.driver.get_screenshot_as_png(),
            name="screenshot_after_close_button_click",
            attachment_type=allure.attachment_type.PNG
        )


@allure.feature("Login modal")
@allure.story("Registration tab layout")
def test_modal_reg_tab_elements_present(main_page):
    EXPECTED_REG_TAB_TITLE = "Регистрация"
    EXPECTED_REG_FIRST_NAME_PLACEHOLDER = "Имя:"
    EXPECTED_REG_LAST_NAME_PLACEHOLDER = "Фамилия:"
    EXPECTED_REG_EMAIL_PLACEHOLDER = "Адрес e-mail:"
    EXPECTED_REG_SUBMIT_BUTTON_TEXT_AND_VALUE = "Регистрация"

    main_page.header_top.click_login_button()
    auth_modal = AuthModalComponent(main_page.driver, main_page.wait)
    auth_modal.switch_modal_tab_to_registration()


    with allure.step("Registration tab is open"):
        modal_registration_tab = auth_modal.get_modal_window()
        check.is_true(modal_registration_tab, "Registration tab doesn't showing up")
        allure.attach(
            modal_registration_tab.screenshot_as_png,
            name="modal_registration_tab",
            attachment_type=allure.attachment_type.PNG
        )

    with allure.step("Title is correct"):
        modal_tab_title = auth_modal.get_modal_name()
        check.equal(modal_tab_title,
                    EXPECTED_REG_TAB_TITLE.upper(),
                    f"Unexpected modal title: {modal_tab_title}. "
                    f"Expected: {EXPECTED_REG_TAB_TITLE.upper()}")
        allure.attach(modal_tab_title,
            name="Registration tab title",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("First name field is clickable and has correct placeholder"):
        check.is_true(auth_modal.get_reg_first_name_field(), "First name field not found")
        first_name_placeholder = auth_modal.get_reg_first_name_placeholder_text()
        check.equal(first_name_placeholder,
                    EXPECTED_REG_FIRST_NAME_PLACEHOLDER,
                    f"Unexpected first name placeholder: {first_name_placeholder}. "
                    f"Expected: {EXPECTED_REG_FIRST_NAME_PLACEHOLDER}")
        allure.attach(first_name_placeholder,
            name="First name placeholder",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Last name field is clickable and has correct placeholder"):
        check.is_true(auth_modal.get_reg_last_name_field(), "Last name field not found")
        last_name_placeholder = auth_modal.get_reg_last_name_placeholder_text()
        check.equal(last_name_placeholder,
                    EXPECTED_REG_LAST_NAME_PLACEHOLDER,
                    f"Unexpected last name placeholder: {last_name_placeholder}. "
                    f"Expected: {EXPECTED_REG_LAST_NAME_PLACEHOLDER}")
        allure.attach(last_name_placeholder,
            name="Last name placeholder",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Email field is clickable and has correct placeholder"):
        check.is_true(auth_modal.get_reg_email_field(), "Email field not found")
        email_placeholder = auth_modal.get_reg_email_placeholder_text()
        check.equal(email_placeholder,
                    EXPECTED_REG_EMAIL_PLACEHOLDER,
                    f"Unexpected email placeholder: {email_placeholder}. "
                    f"Expected: {EXPECTED_REG_EMAIL_PLACEHOLDER}")
        allure.attach(email_placeholder,
            name="Email placeholder",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Registration policy checkbox is clickable and policy link is correct"):
        check.is_true(auth_modal.get_reg_policy_checkbox(), "Registration policy checkbox not clickable")
        policy_link = auth_modal.get_reg_policy_link()
        check.is_true(policy_link, "Policy link not found")
        check.is_false(policy_link.endswith("#"), "Found a stub (#) instead of a policy link")
        allure.attach(policy_link,
            name="Policy link",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Submit button is clickable and have proper text and attribute"):
        button_attrs = auth_modal.get_reg_submit_btn_text_and_value()
        check.is_true(button_attrs, "Authorization submit button not found or not clickable")
        if button_attrs:
            button_text, button_value = button_attrs
            check.equal(button_text,
                        EXPECTED_REG_SUBMIT_BUTTON_TEXT_AND_VALUE.upper(),
                        f"Unexpected authorization submit button text: {button_text}. "
                        f"Expected: {EXPECTED_REG_SUBMIT_BUTTON_TEXT_AND_VALUE.upper()}")
            check.equal(button_value,
                        EXPECTED_REG_SUBMIT_BUTTON_TEXT_AND_VALUE,
                        f"Unexpected authorization submit button text: {button_value}. "
                        f"Expected: {EXPECTED_REG_SUBMIT_BUTTON_TEXT_AND_VALUE}")
        allure.attach(
            f"Button text: {button_text}. Button value: {button_value}",
            name="modal_authorization_tab",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Link for authorization tab is correct"):
        authorization_tab_link = auth_modal.get_modal_tab_link()
        check.is_true(authorization_tab_link, "Link for authorization tab not found")
        check.is_true(authorization_tab_link.endswith(
            "/local/ajax/auth.php?login=yes"
        ))
        allure.attach(
            authorization_tab_link,
            name="authorization_tab_link",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Modal window is closing up after registration tab close button click"):
        auth_modal.close_modal_btn()
        check.is_true(auth_modal.modal_window_not_visible(), "Modal window not closed")
        allure.attach(
            main_page.driver.get_screenshot_as_png(),
            name="screenshot_after_close_button_click",
            attachment_type=allure.attachment_type.PNG
        )