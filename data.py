import requests

def get_nifty_ltp():
    try:
        url = "https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?symbol=NIFTY&resolution=1&from=1700000000&to=1800000000"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }

        res = requests.get(url, headers=headers, timeout=10)
        data = res.json()

        ltp = data["c"][-1]   # last closing price  
        return ltp

    except Exception as e:
        print("LTP Error:", e)
        return None
