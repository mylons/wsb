import threading
from time import sleep
from typing import List
from queue import Queue
import random

INPUT_COMMENTS = Queue()
OUTPUT_COMMENTS = Queue()
KEEP_WORKING = True


def worker():
    while KEEP_WORKING:
        client = get_client()
        try:
            item = INPUT_COMMENTS.get(timeout=2)
        except:
            break
        if isinstance(item, MoreComments):
            handle_more_comments(item)
        INPUT_COMMENTS.task_done()
        print(f"INPUT_COMMENTS={INPUT_COMMENTS.unfinished_tasks} OUTPUT_COMMENTS={OUTPUT_COMMENTS.unfinished_tasks}")
        try:
            for c in client.submission(id=item).comments:
                OUTPUT_COMMENTS.put(c.body)
        except Exception as e:
            pass
        sleep(random.randint(0, 5))

from datetime import datetime

from praw.models import MoreComments

from db import Stocks, MOST_COMMON_WORDS
import praw
import pytz

SOME_CLIENT = False

db = Stocks()
STOCKS = frozenset(db.nyse() + db.amex() + db.nasdaq())
SPECIAL_CASES = frozenset({'FDs'})

#THE_COMMENT = "https://www.reddit.com/r/wallstreetbets/comments/jyjyqt/posted_this_45_days_ago_now_we_have_a_ticker/"
THE_COMMENT = "https://www.reddit.com/r/wallstreetbets/comments/jzqior/what_are_your_moves_tomorrow_november_24_2020/"


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

def handle_more_comments(more: MoreComments):
    for comment in more.comments(update=True):
        if hasattr(comment, "body"):
            OUTPUT_COMMENTS.put(comment.body)
            print(f"INPUT_COMMENTS.size {INPUT_COMMENTS.unfinished_tasks} OUTPUT_COMMENTS.size {OUTPUT_COMMENTS.unfinished_tasks}")
        elif isinstance(comment, MoreComments):
            INPUT_COMMENTS.put(comment)
        else:
            print("wtf")


def queue_to_list(q):

    blah = q.get()
    output = []
    while blah and q.unfinished_tasks > 0:
        print(blah)
        output.append(blah)
        try:
            blah = q.get(timeout=1)
        except:
            break
    return output

if __name__ == '__main__':
    # TODO change time_bin to be EST time
    # TODO figure out how to store this data, probably k, v with key=date,value=json of stock values for now?
    # TODO automate running this. sub-tasks: detect duplicate comments

    for c in get_client().submission(url=THE_COMMENT).comments.list():
        if isinstance(c, MoreComments):
            INPUT_COMMENTS.put(c)
        else:
            OUTPUT_COMMENTS.put(c.body)

    threads = []
    for i in range(32):
        threads.append(threading.Thread(target=worker, daemon=True).start())

    INPUT_COMMENTS.join()
    import json
    output_json = json.dumps(queue_to_list(OUTPUT_COMMENTS))
    with open('the_moves.json', 'w') as f:
        f.write(output_json)

    print(len(output_json))
