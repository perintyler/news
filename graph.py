from sentiment import getSentimentTimeline, start_date, end_date
import datetime
import numpy as np
import matplotlib.pyplot as plt
import random
import sys
from settings import key_word, sources

def graphSentiment(key_word, component):

    # map each source to its sentiment timeline, which is a list of the average
    # sentiment for each day of the month. Sentiment is represented as a
    # dict with a polarity value (-1 to 1, negative to positive), and a
    # subjectivity value (0 to 1, objective to opion based)
    # timelines = {id: getSentimentTimeline(key_word, id) for id in source_ids}

    # graph each source's timelines as a different color line line using pyplot
    for source in sources:
        #print(f'Getting sentiment timeline for {source}')
        timeline = getSentimentTimeline(key_word, source)
        # generate random RGB as a hex code string
        color = '#%06x' % random.randint(0, 0xFFFFFF)

        # get the number of days in the timeline
        num_days = (end_date-start_date).days

        # create the x axis dataset for the source which is a list every
        # day from the start date to the end date in the timeline
        x = [start_date + datetime.timedelta(days=i) for i in range(num_days)]

        # create the y data set which is the average sentiment for each day in the timeline
        y = [timeline[i][component] for  i in range(num_days)]
        plt.plot_date(x, y, linestyle='solid', color=color, label=source)

    # open the pyplot graph ui
    plt.show()

if __name__ == '__main__':
    graphSentiment('trump', 'subjectivity')
