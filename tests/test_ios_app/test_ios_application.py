import allure
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have


@allure.title('Запуск автотестов на IOS-устройстве')
def test_ios(macos_management):
    text_to_input = 'Hello,world!'
    browser.element((AppiumBy.ACCESSIBILITY_ID, "Text Button")).click()
    browser.element((AppiumBy.ACCESSIBILITY_ID, "Text Input")).send_keys(
        text_to_input + "\n")
    browser.element((AppiumBy.ACCESSIBILITY_ID, "Text Output")).should(
        have.exact_text(text_to_input)
    )