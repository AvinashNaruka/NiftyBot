import yfinance as yf
import requests

def get_nifty_ltp():
    try:
        ticker = yf.Ticker("^NSEI")
        info = ticker.info
        return info.get("regularMarketPrice")
    except:
        return None

def get_nifty_ohlc():
    try:
        df = yf.download("^NSEI", period="5d", interval="5m", progress=False)
        df = df.reset_index()
        return df
    except:
        return None
