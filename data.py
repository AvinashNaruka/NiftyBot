import requests

YAHOO_URL = "https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI?interval=1m"


def get_nifty_ltp():
    """Fetch live NIFTY LTP from Yahoo Finance"""
    try:
        response = requests.get(YAHOO_URL, timeout=5)
        data = response.json()

        result = data["chart"]["result"][0]
        meta = result["meta"]

        ltp = meta["regularMarketPrice"]
        return ltp

    except Exception as e:
        print("LTP Error:", e)
        return None


def get_nifty_ohlc():
    """Fetch last OHLC candle"""
    try:
        response = requests.get(YAHOO_URL, timeout=5)
        data = response.json()

        result = data["chart"]["result"][0]
        indicators = result["indicators"]["quote"][0]

        timestamps = result["timestamp"]
        opens = indicators["open"]
        highs = indicators["high"]
        lows = indicators["low"]
        closes = indicators["close"]

        # Last candle
        ohlc = {
            "open": opens[-1],
            "high": highs[-1],
            "low": lows[-1],
            "close": closes[-1]
        }

        return ohlc

    except Exception as e:
        print("OHLC Error:", e)
        return None
