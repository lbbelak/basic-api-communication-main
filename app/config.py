from os import environ
from dotenv import load_dotenv

load_dotenv()
class Config():
    CMC_KEY :str = environ.get('CMC_KEY')
