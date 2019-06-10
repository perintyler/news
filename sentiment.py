from articles import getArticles
from textblob import TextBlob
import datetime
from functools import reduce
from articles import getArticles

# uses NLTK to get the average sentiment (polarity and subjectivity) of the given articles
def getAverageSentiment(articles):
    sentiments = list(map(lambda article: TextBlob(article).sentiment, articles))
    polarity_sum = reduce(lambda sum, sentiment: sum + sentiment.polarity, sentiments, 0)
    subjectivity_sum = reduce(lambda sum, sentiment: sum + sentiment.subjectivity, sentiments, 0)
    num_articles = len(articles)
    avg_polarity = polarity_sum / num_articles
    avg_subjectivity = subjectivity_sum / num_articles
    return avg_polarity, avg_subjectivity

def getSentimentForDate(key_word, source, date):
    articles = getArticles(key_word, source, date)
    if articles:
        # get the day's average sentiment and add the results to the timeline list
        polarity, subjectivity = getAverageSentiment(articles)
        return {
            'date': date,
            'source': source,
            'polarity': polarity,
            'subjectivity': subjectivity,
            'num_articles': len(articles)
        }

def generateSentimentTimeline(key_word, source, last_date):
    timeline = SentimentTimeline(key_word, source)
    date = last_date - datetime.timedelta(days=1)
    while not timeline.threshold_reached:
        print(f'date: {date}')
        analyze_next_date = timeline.setDate(date)
        date -= datetime.timedelta(days=1)
    return timeline.get()
