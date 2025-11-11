import dotenv
import pydantic_settings
from pydantic_settings.sources import DotenvType


class Config(pydantic_settings.BaseSettings):
    BROWSERSTACK_PROJECT_NAME: str = 'default_name'
    BROWSERSTACK_BUILD_NAME: str = 'default_build'
    BROWSERSTACK_SESSION_NAME: str = 'default_session'
    env_file: DotenvType = '.env'
    timeout: float = 10

# if you want to have optional .env file (without `.context` suffix)
# to allways override default values from .env.local, .env.test, .env.stage
# you may need it,
# as being ignored in .gitignore, – to store sensitive data (aka secrets)
dotenv.load_dotenv()
'''
# you may emphasize its "secrets" nature by naming it as .env.secrets:
dotenv.load_dotenv(dotenv.find_dotenv('.env.secrets'))
# sometimes people keep such secrets file outside of the project folder, 
# often – in home directory...
from pathlib import Path
dotenv.load_dotenv(Path.home().joinpath('.env.secrets').__str__())
'''

config = Config()
'''
# if you would keep .env file name for local context (instead of .env.local)
context = Config().context
config = Config(dotenv.find_dotenv('.env' if context == 'local' else f'.env.{context}'

# another example, utilizing custom path helper from selene_in_action.utils.path
from selene_in_action.utils import path
config = Config(_env_file=path.relative_from_root(f'.env.{Config().context}'))
'''
