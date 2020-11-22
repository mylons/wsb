from typing import List

from IPython import embed
from datetime import datetime
from collections import Counter, defaultdict
from db import Stocks, MOST_COMMON_WORDS
import praw
import pytz

SOME_CLIENT = False

db = Stocks()
STOCKS = frozenset(db.nyse() + db.amex() + db.nasdaq())
SPECIAL_CASES = frozenset({'FDs'})


def get_client(some_client=SOME_CLIENT):
    if not some_client:
        some_client = praw.Reddit(client_id='oeywuzwXgEQ24w',
                                  client_secret='kcnraVZX__t6pr3oGXeuosnqRFc',
                                  user_agent='mikeybullputs',
                                  api_request_delay=0.0)
        some_client.config
    return some_client


def filter_words(words: List[str],
                 stocks: set = STOCKS,
                 common_words: set = MOST_COMMON_WORDS,
                 special_cases: set = SPECIAL_CASES):
    result = []
    lower_stocks = set(w.lower() for w in stocks)
    for w in words:
        w = clean_word(w)
        # hard skips
        if w in special_cases:
            continue
        if w in common_words:
            continue
        if w in lower_stocks or w in stocks or w.upper() in stocks:
            # keep word
            result.append(w)
    return result


def clean_word(w: str):
    return w.replace('$', '')


def get_date_from_post(p):
    est = pytz.timezone('US/Eastern')
    utc = pytz.utc
    date = datetime.utcfromtimestamp(p.created_utc)
    date = date.replace(tzinfo=utc)
    return date.astimezone(est)


# json method


if __name__ == '__main__':
    # TODO change time_bin to be EST time
    # TODO figure out how to store this data, probably k, v with key=date,value=json of stock values for now?
    # TODO automate running this. sub-tasks: detect duplicate comments

    wsb = get_client().subreddit('wallstreetbets')

    word_counter = Counter()
    words = defaultdict(list)
    unfiltered_words = defaultdict(list)

    start = datetime.now()
    for post in wsb.hot(limit=200):
        # post object
        date = get_date_from_post(post)
        time_bin = f"{date.month}-{date.day}-{date.hour}"
        unfiltered_words[time_bin] += post.title.split() + post.selftext.split()
        print(f"at: {time_bin} num words: {len(unfiltered_words[time_bin])}", end="\r")
        client = get_client()
        post.comments.replace_more(limit=None)
        for comment in post.comments.list():
            date = get_date_from_post(comment)
            time_bin = f"{date.month}-{date.day}-{date.hour}"
            unfiltered_words[time_bin] += comment.body.split()
            print(f"at: {time_bin} num words: {len(unfiltered_words[time_bin])}", end="\r")
    print("processing in memory now")
    unfiltered_counters = {}
    filtered_counters = {}
    for time_bin in unfiltered_words:
        unfiltered_counters[time_bin] = Counter(unfiltered_words[time_bin])
        filtered_counters[time_bin] = Counter([w.lower() for w in filter_words(unfiltered_words[time_bin])])
    stop = datetime.now()
    print(f"start: {start}   stop: {stop}     stop - start: {stop - start}")
    embed()


    """
    special cases: FDs
    """