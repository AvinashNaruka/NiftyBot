# data.py
import requests

HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_nifty_ltp():
    try:
        url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=%5ENSEI"
        r = requests.get(url, headers=HEADERS, timeout=6)
        j = r.json()
        return float(j["quoteResponse"]["result"][0]["regularMarketPrice"])
    except Exception as e:
        print("LTP Error:", e)
        return None

def get_nifty_ohlc():
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI?interval=5m&range=5d"
        r = requests.get(url, headers=HEADERS, timeout=6).json()
        result = r["chart"]["result"][0]
        quote = result["indicators"]["quote"][0]
        import pandas as pd
        df = pd.DataFrame({
            "time": result["timestamp"],
            "open": quote["open"],
            "high": quote["high"],
            "low": quote["low"],
            "close": quote["close"]
        })
        df = df.dropna().reset_index(drop=True)
        return df
    except Exception as e:
        print("OHLC Error:", e)
        return None
