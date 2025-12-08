import requests
import pandas as pd
from datetime import datetime, timedelta

# -----------------------------------------
# 1) GET LIVE NIFTY LTP (Direct NSE API)
# -----------------------------------------
def get_nifty_ltp():
    try:
        url = "https://www.nseindia.com/api/quote-equity?symbol=NIFTY%2050"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
            "Referer": "https://www.nseindia.com/"
        }

        session = requests.Session()
        response = session.get(url, headers=headers, timeout=5)
        data = response.json()

        return data["priceInfo"]["lastPrice"]

    except Exception as e:
        print("LTP Error:", e)
        return None


# ---------------------------------------------------------
# 2) GET OHLC (Past 5 days 5-minute candles from NSE API)
# ---------------------------------------------------------
def get_nifty_ohlc():
    try:
        url = "https://www.nseindia.com/api/chart-databyindex?index=NIFTY%2050"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
            "Referer": "https://www.nseindia.com/"
        }

        session = requests.Session()
        response = session.get(url, headers=headers, timeout=5)
        data = response.json()

        candles = data["grapthData"]

        df = pd.DataFrame(candles, columns=["time", "close"])
        df["time"] = pd.to_datetime(df["time"], unit="ms")

        # Since NSE API gives only CLOSE, we artificially create OHLC
        df["open"] = df["close"].shift(1).fillna(df["close"])
        df["high"] = df[["open", "close"]].max(axis=1)
        df["low"] = df[["open", "close"]].min(axis=1)

        df = df[["time", "open", "high", "low", "close"]]
        df = df.reset_index(drop=True)

        return df.tail(60)  # last 60 candles (5 hours)

    except Exception as e:
        print("OHLC Error:", e)
        return None


# ---------------------------------------------------------
# 3) OPTIONAL → GET OPTION CHAIN (Not used yet)
# ---------------------------------------------------------
def get_option_chain():
    try:
        url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
            "Referer": "https://www.nseindia.com/"
        }

        session = requests.Session()
        response = session.get(url, headers=headers, timeout=5)
        data = response.json()

        return data["records"]["data"]

    except Exception as e:
        print("Option Chain Error:", e)
        return None
