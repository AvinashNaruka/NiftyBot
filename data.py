import requests

# ------------------------------------------------------
# GET NIFTY LTP from MoneyControl (Very Stable)
# ------------------------------------------------------
def get_nifty_ltp():
    try:
        url = "https://priceapi.moneycontrol.com/technicalPriceChartData/indianMarket/indices?symbol=NIFTY%2050"
        res = requests.get(url, timeout=10).json()

        return float(res["pricecurrent"])
    except Exception as e:
        print("LTP Error:", e)
        return None


# ------------------------------------------------------
# GET NIFTY OHLC (5-min candles) from MoneyControl
# ------------------------------------------------------
def get_nifty_ohlc():
    try:
        url = "https://priceapi.moneycontrol.com/technicalPriceChartData/indianMarket/indices?symbol=NIFTY%2050"
        res = requests.get(url, timeout=10).json()

        # MoneyControl returns full historical list
        data = res["candles"]

        import pandas as pd
        df = pd.DataFrame(data, columns=["time", "open", "high", "low", "close", "volume"])

        return df.tail(20)   # last 20 candles for analysis
    except Exception as e:
        print("OHLC Error:", e)
        return None
