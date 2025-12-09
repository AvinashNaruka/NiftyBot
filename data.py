# data.py

import requests

YAHOO_URL = "https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI?interval=1m"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}


def get_nifty_ltp():
    try:
        res = requests.get(YAHOO_URL, headers=HEADERS, timeout=5)
        data = res.json()

        result = data["chart"]["result"][0]
        close_prices = result["indicators"]["quote"][0]["close"]

        # Last valid close price = LTP
        close_prices = [c for c in close_prices if c is not None]
        if not close_prices:
            return None

        return close_prices[-1]

    except Exception as e:
        print("LTP ERROR:", e)
        return None



def get_nifty_ohlc():
    try:
        res = requests.get(YAHOO_URL, headers=HEADERS, timeout=5)
        data = res.json()

        result = data["chart"]["result"][0]
        quote = result["indicators"]["quote"][0]

        open_p = quote["open"][-1]
        high_p = quote["high"][-1]
        low_p = quote["low"][-1]
        close_p = quote["close"][-1]

        return {
            "open": open_p,
            "high": high_p,
            "low": low_p,
            "close": close_p
        }

    except Exception as e:
        print("OHLC ERROR:", e)
        return None
