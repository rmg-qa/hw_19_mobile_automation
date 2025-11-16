from appium import webdriver
import pytest
from appium.options.ios import XCUITestOptions
import os
import dotenv
import allure
import config
import allure_commons
from selene_in_action.utils import allure as utils_allure
from selene import browser

dotenv.load_dotenv()
user_name = os.getenv('BROWSERSTACK_USERNAME')
accesskey = os.getenv('BROWSERSTACK_ACCESS_KEY')


@pytest.fixture(scope='function')
def macos_management():
    options = XCUITestOptions().load_capabilities({
        # Specify device and os_version for testing
        "platformName": "ios",
        "platformVersion": "17",
        "deviceName": "iPhone 15 Pro Max",

        # Set URL of the application under test
        "app": "bs://sample.app",

        # Set other BrowserStack capabilities
        'bstack:options': {
            "projectName": "IOS tests",
            "buildName": "browserstack-build-ios",

            # Set your access credentials
            "userName": user_name,
            "accessKey": accesskey
        }
    }
    )

    # Конфигурация Selene
    browser.config.timeout = config.config.timeout

    with allure.step('init app session'):
        browser.config.driver = webdriver.Remote(
            'http://hub.browserstack.com/wd/hub',
            options=options
        )

    browser.config.timeout = float(os.getenv('timeout', '10.0'))

    browser.config.wait_decorator = allure_commons._allure.step
    yield

    allure.attach(
        browser.driver.get_screenshot_as_png(),
        name='screenshot',
        attachment_type=allure.attachment_type.PNG,
    )

    allure.attach(
        browser.driver.page_source,
        name='screen xml dump',
        attachment_type=allure.attachment_type.XML,
    )

    session_id = browser.driver.session_id

    with allure.step('tear down app session'):
        browser.quit()

    utils_allure.attach_bstack_video(session_id, version_driver='app-')

    browser.quit()