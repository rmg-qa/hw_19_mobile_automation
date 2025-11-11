from appium import webdriver
import pytest
from appium.options.ios import XCUITestOptions
from selene import browser
import os
import dotenv

import project

dotenv.load_dotenv()
user_name = os.getenv('BROWSERSTACK_USERNAME')
accesskey = os.getenv('BROWSERSTACK_ACCESS_KEY')


@pytest.fixture(scope='function')
def macos_management():
    options = XCUITestOptions()

    # Основные capabilities для Safari
    options.platform_name = 'ANY'
    options.browser_name = 'Safari'
    options.device_name = 'iPhone 14 Pro Max'
    options.platform_version = '16'
    options.automation_name = 'XCUITest'  #

    # BrowserStack специфичные capabilities
    options.set_capability('bstack:options', {
        'userName': user_name,
        'accessKey': accesskey,
        'projectName': project.config.BROWSERSTACK_PROJECT_NAME,
        'buildName': project.config.BROWSERSTACK_BUILD_NAME,
        'sessionName': project.config.BROWSERSTACK_SESSION_NAME,
        'deviceOrientation': 'portrait',
        'local': 'false',
        'debug': 'true',
        'networkLogs': 'true'  # Для отладки сетевых проблем
    })

    # Конфигурация Selene
    browser.config.driver = webdriver.Remote("http://hub.browserstack.com/wd/hub",
                                             options=options)  # Адрес для подключения к Browserstack
    browser.config.driver_remote_url = 'http://hub.browserstack.com/wd/hub'
    browser.config.driver_options = options
    browser.config.timeout = project.config.timeout

    yield

    browser.quit()
