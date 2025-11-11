from appium import webdriver
import pytest
from appium.options.ios import XCUITestOptions
from selene import browser
import os
import dotenv
import allure
import config
import allure_commons
from selene_in_action.utils import allure as utils_allure

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
        'projectName': config.config.BROWSERSTACK_PROJECT_NAME,
        'buildName': config.config.BROWSERSTACK_BUILD_NAME,
        'sessionName': config.config.BROWSERSTACK_SESSION_NAME,
        'deviceOrientation': 'portrait',
        'local': 'false',
        'debug': 'true',
        'networkLogs': 'true'  # Для отладки сетевых проблем
    })

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

    utils_allure.attach_bstack_video(session_id, version_driver='')

    browser.quit()
