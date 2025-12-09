# signals.py

from data import get_nifty_ltp, get_nifty_ohlc
from indicators import add_indicators, get_trend


def _calculate_strike(ltp: float) -> int:
    """Round to nearest 50"""
    return int(round(ltp / 50) * 50)


def generate_signal() -> dict:
    """
    Returns signal dictionary for frontend.
    """

    # ============================
    # 1️⃣ GET LIVE NIFTY LTP
    # ============================
    ltp = get_nifty_ltp()
    if ltp is None:
        return {"error": "Failed to fetch Nifty LTP"}

    # ============================
    # 2️⃣ GET OHLC DATA (LAST CANDLE)
    # ============================
    ohlc = get_nifty_ohlc()
    if ohlc is None:
        return {"error": "Failed to fetch OHLC"}

    # Convert to DataFrame-like dict for indicators
    df = {
        "open": ohlc["open"],
        "high": ohlc["high"],
        "low": ohlc["low"],
        "close": ohlc["close"]
    }

    # ============================
    # 3️⃣ CALCULATE TREND
    # ============================
    trend = get_trend(df)

    # ============================
    # 4️⃣ STRIKE PRICE
    # ============================
    strike = _calculate_strike(ltp)

    # ============================
    # 5️⃣ OPTION TYPE
    # ============================
    option_type = "CE" if trend == "UP" else "PE"

    # ============================
    # 6️⃣ ENTRY – SL – TARGET LOGIC
    # ============================
    entry = round(ltp * 0.012, 2)     # Dummy example
    sl = round(entry * 0.85, 2)
    target = round(entry * 1.25, 2)

    # ============================
    # 7️⃣ FINAL RESPONSE
    # ============================
    return {
        "trend": trend,
        "ltp": ltp,
        "strike": strike,
        "option_type": option_type,
        "entry": entry,
        "sl": sl,
        "target": target
    }
