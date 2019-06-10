import settings as env # loads api keys
from newsapi import NewsApiClient # queries articles
import newspaper # scrapes article contents
from datetime import timedelta
import sys
# Set up the news querying client (https://newsapi.org/docs)
client = NewsApiClient(api_key = env.NEWS_API_KEY)

# the minimum number of characters an article can have
# to perform sentiment analysis. Some articles are just
# videos and don't have enough substantial text to get
# a valid, reasonable value
min_char_length = 100

# Formats a datetime into the YYYY-MM-DD, the format used by newsapi
def formatDate(date):
    # add leading 0s to month and day if needed
    day = f'0{date.day}' if date.day < 10 else f'{date.day}'
    month = f'0{date.month}' if date.month < 10 else f'{date.month}'
    return f'{date.year}-{month}-{day}'


# returns a list of strings containing the contents of articles
# from the given source on the given date pertaining to the given keyword
def getArticles(keyword, source, date):
    # construct date strings to use for newsapi. The start date is the date
    # given and the end date is the next day.
    start_date = formatDate(date)
    end_date = formatDate(date + timedelta(days=1))

    article_data = [] # stores article data (ie urls, sources, authors)

    # iterate through all pages of the query results. News API is limited to
    # only 100 results, so the client throws an error before the last page
    # usually
    page = 1
    while(True):
        try:
            # get the next page of article data and add them to the article list
            query = client.get_everything(q = keyword, page=page, sources=source,
                                            from_param=start_date, to=end_date)
            article_data.extend(query['articles'])
            # increment page number before looping
            page += 1
        except:
            # either the last page was found or results were capped by API
            break

    articles = []
    # Iterate through articles and use their urls to scrape contents
    for data in article_data:
        # Get article contents using the scraper library (https://github.com/mattlisiv/newsapi-python)
        article = newspaper.Article(data['url'])
        try:
            # try downloading the article. The scraper library can handle
            # a lot of sources, but not everything
            article.download()
            article.parse()
        except:
            # scraper was unable to download and parse the article. Try the next article
            continue

        # make sure the article is long enough to be reasonably analyzed
        if(len(article.text) > min_char_length):
            articles.append(article.text)

    print(f'Got {len(articles)} articles from {source} on {date}')

    return articles
