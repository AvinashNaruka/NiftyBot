import yfinance as yf
import requests

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
