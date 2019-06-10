import db
from sentiment import getSentimentForDate
from datetime import datetime, timedelta
from settings import key_word, source

def storeSentimentValues():
    date = datetime.today()
    # date = lastDateQueried() - timedelta(days=1)
    document = getSentimentForDate(key_word, source, date)
    while(document != None):
        date = date - timedelta(days=1)
        db.storeSentiment(document)
        document = getSentimentForDate(key_word, source, date)


storeSentimentValues()
