from selene import browser
import allure


@allure.title('Реализовал автотест на macOS, так как на ios-устройстве удаленно запустить автотест не получается')
def test_mac_os_wikipedia(macos_management):
    browser.open('https://www.wikipedia.org/')
    # Вводим поисковый запрос
    search_box = browser.element('#searchInput')
    search_box.type('QA_GURU').press_enter()
