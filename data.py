import yfinance as yf
import requests

def get_nifty_ltp():
    try:
        ticker = yf.Ticker("NSEI")
        info = ticker.info
        return info.get("regularMarketPrice")
    except:
        return None


def get_nifty_ohlc():
    try:
        df = yf.download("NSEI", period="5d", interval="5m", progress=False)

        # FIX: avoid empty dataframe from yfinance
        if df is None or df.empty:
            return None

        df = df.reset_index()
        return df
    except:
        return None


def get_option_chain():
    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        session = requests.Session()
        response = session.get(url, headers=headers)
        data = response.json()
        return data["records"]["data"]
    except:
        return None
