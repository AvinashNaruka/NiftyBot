# data.py
import requests

HEADERS = {"User-Agent": "Mozilla/5.0"}

# ---- EDIT THIS ONLY ----
# Yeh tumhari temporary manual LTP hogi
MANUAL_LTP = 26500.0    # Change this anytime (live market ke hisaab se)

# ------------------------------------------------------
# 1) LIVE LTP from Yahoo (primary)
# ------------------------------------------------------
def get_nifty_ltp():
    try:
        # Yahoo Live LTP (Spot)
        url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=%5ENSEI"
        r = requests.get(url, headers=HEADERS, timeout=5)
        data = r.json()

        ltp = data["quoteResponse"]["result"][0]["regularMarketPrice"]

        # Agar Yahoo ne None diya to niche fallback use hoga
        if ltp is None:
            raise Exception("Yahoo returned None")

        return float(ltp)

    except Exception as e:
        print("Yahoo LTP Error:", e)
        print("⚠ Using MANUAL LTP fallback:", MANUAL_LTP)
        return float(MANUAL_LTP)


# ------------------------------------------------------
# 2) OHLC (Chart candles) — Yahoo se aati hai
# ------------------------------------------------------
def get_nifty_ohlc():
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI?interval=5m&range=5d"
        r = requests.get(url, headers=HEADERS, timeout=5).json()

        result = r["chart"]["result"][0]
        q = result["indicators"]["quote"][0]

        o = q["open"][-1]
        h = q["high"][-1]
        l = q["low"][-1]
        c = q["close"][-1]

        # If any OHLC missing → manual fallback from LTP
        if any(v is None for v in [o, h, l, c]):
            return {
                "open": MANUAL_LTP,
                "high": MANUAL_LTP,
                "low": MANUAL_LTP,
                "close": MANUAL_LTP
            }

        return {"open": o, "high": h, "low": l, "close": c}

    except Exception as e:
        print("OHLC Error:", e)
        print("⚠ Using fallback OHLC from MANUAL LTP")

        return {
            "open": MANUAL_LTP,
            "high": MANUAL_LTP,
            "low": MANUAL_LTP,
            "close": MANUAL_LTP
        }
