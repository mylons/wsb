import json
from collections import Counter
from typing import List

from db import Stocks, MOST_COMMON_WORDS

SOME_CLIENT = False

db = Stocks()
STOCKS = frozenset(db.nyse() + db.amex() + db.nasdaq())
SPECIAL_CASES = frozenset({'FDs'})


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


data = json.load(open('the_moves.json', 'r'))
unfiltered_words = []
filtered_words = []

for comment in data:
    unfiltered_words += comment.split()

unfiltered_counters = {}
filtered_counters = {}

unfiltered_counters = Counter(unfiltered_words)
filtered_counters = Counter([w.lower() for w in filter_words(unfiltered_words)])
print("asdf")


for comment in data:
