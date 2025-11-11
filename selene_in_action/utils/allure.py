import allure
import requests
import dotenv
import os


def attach_bstack_video(session_id, version_driver):
    dotenv.load_dotenv()
    user_name = os.getenv('BROWSERSTACK_USERNAME')
    accesskey = os.getenv('BROWSERSTACK_ACCESS_KEY')
    bstack_session = requests.get(
        f'https://api.browserstack.com/{version_driver}automate/sessions/{session_id}.json',
        auth=(user_name, accesskey),
    ).json()
    video_url = bstack_session['automation_session']['video_url']

    allure.attach(
        '<html><body>'
        '<video width="100%" height="100%" controls autoplay>'
        f'<source src="{video_url}" type="video/mp4">'
        '</video>'
        '</body></html>',
        name='video recording',
        attachment_type=allure.attachment_type.HTML,
    )
