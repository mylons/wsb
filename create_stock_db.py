import concurrent
from concurrent.futures.thread import ThreadPoolExecutor

from IPython import embed
import pandas as pd
import requests
import yfinance
from io import StringIO
import sqlite3

url_to_market =  {
"nasdaq": "https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download",
"amex": "https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=amex&render=download",
"nyse": "https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download"
}
futures_to_market = {}
stocks = {}
dfs = {}
cnx = sqlite3.connect('stocks.db')
with ThreadPoolExecutor(max_workers=len(url_to_market)) as executor:
    for market, url in url_to_market.items():
        futures_to_market[executor.submit(requests.get, url)] = market

    for future in concurrent.futures.as_completed(futures_to_market):
        market = futures_to_market[future]
        try:
            data = future.result().content
            dfs[market] = pd.read_csv(StringIO(data.decode()))
            dfs[market].to_sql(market, cnx)
        except Exception as exc:
            print(f"{market} generated an exception: {exc}")
        else:
            print(f"{market} page is {len(data)}")

cnx.close()

