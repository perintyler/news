from pymongo import MongoClient
from pymongo import errors as mongo_errors
from settings import MONGO_HOST, key_word, source
import ssl

# setup the mongodb client
client = MongoClient(MONGO_HOST, ssl_cert_reqs=ssl.CERT_NONE)

# if non-existent, create new 'news' db and 'sentiment' collection
db = client[key_word]
collection = db[source]
failed_urls = db['unscrapable_urls']

def storeSentiment(sentiment):
    collection.insert_one(sentiment)

def lastDateQueried():
    last_document = db.query({}, { sort: { _id: -1 }, limit: 1 }, multi = False)
    last_date_str = last_document['date']
    return datetime.datetime(last_date_str)

def query(q, projection, multi = True):
    queried = []
    try:
        query_func = collection.find if multi else collection.findOne
        queried = query_func(q, projection)
    except mongo_errors.InvalidOperation:
        print(f'Invalid Query- q: {q}, projection: {projection}, multi: {multi}')
    except Exception as error:
        print(f'Something went wrong when querying.\n{repr(error)}')
    return queried

def storeUnscrapableArticle(url, source):
    document = { 'source': source, 'url': url }
    failed_urls.insert_one(document)

def getSentimentTimeline(source):
    source_collection = db[source]
    return source_collection.find()

if __name__ == '__main__':
    storeSentiment({'test_key': 'test_value'})
