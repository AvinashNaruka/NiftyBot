from data import get_nifty_ltp, get_nifty_ohlc
from indicators import add_indicators, get_trend

def _calculate_strike(ltp: float) -> int:
    return int(round(ltp / 50) * 50)

def generate_signal() -> dict:
    try:
        ltp = get_nifty_ltp()
        if not ltp:
            return {"error": "Failed to fetch Nifty LTP"}

        df = get_nifty_ohlc()
        if df is None or len(df) < 5:
            return {"error": "Failed to fetch OHLC or insufficient data"}

        df = add_indicators(df)
        trend = get_trend(df)

        strike = _calculate_strike(ltp)
        option_type = "CE" if trend == "UP" else "PE"

        premium_est = 40.0
        stoploss = round(premium_est * 2, 2)
        target1 = round(premium_est * 1.4, 2)
        target2 = round(premium_est * 2.0, 2)

        return {
            "nifty_ltp": float(ltp),
            "trend": trend,
            "strike": strike,
            "option_type": option_type,
            "entry_premium": premium_est,
            "stoploss": stoploss,
            "targets": [target1, target2],
            "timeframe": "5m",
        }

    except Exception as e:
        return {"error": "internal", "message": str(e)}
