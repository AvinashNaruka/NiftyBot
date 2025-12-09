import requests

HEADERS = {"User-Agent": "Mozilla/5.0"}

# Real-Time LTP from Yahoo
def get_nifty_ltp():
    try:
        url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=%5ENSEI"
        r = requests.get(url, headers=HEADERS, timeout=5)
        data = r.json()
        return data["quoteResponse"]["result"][0]["regularMarketPrice"]
    except:
        return None


# Last 1-minute OHLC from Yahoo
def get_nifty_ohlc():
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI?interval=1m"
        r = requests.get(url, headers=HEADERS, timeout=5)
        data = r.json()

        result = data["chart"]["result"][0]
        q = result["indicators"]["quote"][0]

        return {
            "open": q["open"][-1],
            "high": q["high"][-1],
            "low": q["low"][-1],
            "close": q["close"][-1]
        }
    except:
        return None
