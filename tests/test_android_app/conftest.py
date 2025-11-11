import allure
import pytest
import allure_commons
from appium.options.android import UiAutomator2Options
from selene import browser
import os

import config
from selene_in_action.utils import allure as utils_allure
import dotenv
from appium import webdriver

dotenv.load_dotenv()
user_name = os.getenv('BROWSERSTACK_USERNAME')
accesskey = os.getenv('BROWSERSTACK_ACCESS_KEY')


@pytest.fixture(scope='function')
def mobile_management_android():
    options = UiAutomator2Options().load_capabilities({
        # Specify device and os_version for testing
        # "platformName": "android",
        "platformVersion": "12.0",
        "deviceName": "Samsung Galaxy S22 Ultra",

        # Set URL of the application under test
        "app": "bs://sample.app",

        # Set other BrowserStack capabilities
        'bstack:options': {
            "projectName": config.config.BROWSERSTACK_PROJECT_NAME,
            "buildName": config.config.BROWSERSTACK_BUILD_NAME,
            "sessionName": config.config.BROWSERSTACK_SESSION_NAME,

            # Set your access credentials
            "userName": user_name,
            "accessKey": accesskey
        }
    })

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

    utils_allure.attach_bstack_video(session_id, version_driver="app-")

    browser.quit()
