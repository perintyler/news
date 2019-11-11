from settings import TWITTER_CONSUMER_KEY, TWITTER_SECRET_KEY
import requests
from datetime import datetime, timedelta
import json
import base64

# Generates a bearer token (oauth 2.0) for twitter api
def generate_token():
    # create the auth headers using the twitter consumer api key and secret key
    key, secret = TWITTER_CONSUMER_KEY, TWITTER_SECRET_KEY
    auth_str = '{}:{}'.format(key, secret).encode('ascii')
    encoded_key = base64.b64encode(auth_str).decode('ascii')
    headers = {
        'Authorization': f'Basic {encoded_key}',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    # create the data object to be posted asking twitter for a client token
    data = {'grant_type': 'client_credentials'}

    auth_url = 'https://api.twitter.com/oauth2/token'
    response = requests.post(auth_url, headers=headers, data=data)
    if response.status_code != 200:
        raise Exception('Could not generate twitter bearer token')
    return response.json()['access_token']

def premium_keyword_search(keyword, search_settings={}):
    # create request headers, content type (JSON) and auth (api key)
    token = generate_token()
    headers = {
        'content-type': 'application/json',
        'authorization': f'Bearer {token}'
    }
    # create request data: search settings
    start_date = datetime.now()
    end_date = start_date - timedelta(days=1)
    start_date, end_date = format_date_string(start_date, end_date)
    default_settings = {
        'query': 'from:TwitterDev lang:en',
        'maxResults': '100',
        'fromDate': start_date,
        'toDate': end_date
    }
    # set the default search settings for any keys not included from params
    for key, val in default_settings.items():
        search_settings.setdefault(key, val)

    uri = 'https://api.twitter.com/1.1/tweets/search/30day'
    endpoint = f'{uri}/{keyword}.json'
    response = requests.post(endpoint, headers=headers, data=search_settings)
    return response.json()

# formats date time objects into Twitter API's accepted string format
def format_date_string(d0, d1):
    format = '%Y%m%d%H%M' #YYYYMMDDHHmm
    return d0.strftime(format), d1.strftime(format)

def keyword_search(keyword, num_results=2):
    token = generate_token()
    headers = {
        'content-type': 'application/json',
        'authorization': f'Bearer {token}'
    }
    search_params = {
        'q': keyword,
        'tweet_mode': 'extended', # so tweets won't be truncated
        'lang': 'en',
        'result_type': 'recent',
        'count': num_results
    }
    # make request
    uri = 'https://api.twitter.com/1.1'
    endpoint = f'{uri}/search/tweets.json?'
    # header_str, data_str = json.dumps(headers), json.dumps(search_settings)
    response = requests.get(endpoint, headers=headers, params=search_params)
    # get and parse the response
    if response.status_code != 200:
        raise Exception(f'Could not standard search for keyword={keyword}')
    return response.json()['statuses']

if __name__ == '__main__':

    tweets = keyword_search('Trump', num_results=10)
    for tweet in tweets:
        text_key = 'text' if tweet['truncated'] else 'full_text'
        if 'retweeted_status' in tweet:
            print(tweet['retweeted_status'][text_key])
        else:
            print(tweet[text_key])
