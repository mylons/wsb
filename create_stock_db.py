
import pandas as pd
import requests
from io import StringIO
import sqlite3

url_to_market =  {
"nasdaq": "https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download",
"amex": "https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=amex&render=download",
"nyse": "https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download"
}

def clean_nasdaq(data):
    return StringIO('\n'.join([l[:-1] for l in data.split('\n')]))

headers = {
    "GET": "/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download HTTP/1.1",
    "Host": "old.nasdaq.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:82.0) Gecko/20100101 Firefox/82.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": 'en-US,en;q=0.5',
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}
markets = {}
stocks = {}
dfs = {}
cnx = sqlite3.connect('stocks.db')
for market, url in url_to_market.items():
    print(f"operating on {market} , {url}")
    markets[market] = requests.get(url, headers=headers).content.decode()

for market, data in markets.items():
    print(f"operating on {market}")
    try:
        dfs[market] = pd.read_csv(clean_nasdaq(data))
        dfs[market].to_sql(market, cnx)
    except Exception as exc:
        print(f"{market} generated an exception: {exc}")
    else:
        print(f"{market} page is {len(data)}")

cnx.commit()
cnx.close()

