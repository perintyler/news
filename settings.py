from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

# set api keys from .env file
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_HOST = os.getenv('MONGO_HOST')

key_word = 'Trump'

# The source ids for The News Api (https://newsapi.org/docs/endpoints/sources)
source_ids = [
    'cnn',
    'fox-news'
    'abc-news',
    # 'bbc-news',
    'cbc-news',
    # 'daily-mail',
    # 'national-review',
    # 'new-york-magazine',
    'the-hill',
    # 'the-huffington-post',
    # 'vice-news',
    'the-new-york-times',
    'politico',
    'associated-press',
    'msnbc',
    'the-washington-post',
    'reuters',
    'breitbart-news'
]
source = 'msnbc'
#source = source_ids[0] if datetime.today().day % 2 == 0 else source_ids[1]
