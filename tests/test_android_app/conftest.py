import pytest
from appium.options.android import UiAutomator2Options
from appium import webdriver
from selene import browser
import os
import dotenv
import project

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
            "projectName": project.config.BROWSERSTACK_PROJECT_NAME,
            "buildName": project.config.BROWSERSTACK_BUILD_NAME,
            "sessionName": project.config.BROWSERSTACK_SESSION_NAME,

            # Set your access credentials
            "userName": user_name,
            "accessKey": accesskey
        }
    })

    browser.config.driver = webdriver.Remote("http://hub.browserstack.com/wd/hub",
                                             options=options)  # Адрес для подключения к Browserstack
    browser.config.driver_remote_url = 'http://hub.browserstack.com/wd/hub'
    browser.config.driver_options = options
    browser.config.timeout = project.config.timeout

    yield

    browser.quit()
