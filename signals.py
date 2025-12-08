from data import get_nifty_ltp, get_nifty_ohlc
from indicators import add_indicators, get_trend


def _calculate_strike(ltp: float) -> int:
    """Round to nearest 50"""
    return int(round(ltp / 50) * 50)


def generate_signal() -> dict:
    try:
        # GET LTP
        ltp = get_nifty_ltp()
        if not ltp:
            return {"error": "Failed to fetch Nifty LTP"}

        # GET OHLC
        df = get_nifty_ohlc()
        if df is None or len(df) < 5:
            return {"error": "OHLC data missing"}

        # INDICATORS
        df = add_indicators(df)
        trend = get_trend(df)

        # Calculate strike prices
        strike = _calculate_strike(ltp)
        ce = strike + 50
        pe = strike - 50

        # FINAL SIGNAL
        signal = {
            "LTP": ltp,
            "Trend": trend,
            "Suggested_CE": ce,
            "Suggested_PE": pe,
        }

        return signal

    except Exception as e:
        return {"error": "internal", "message": str(e)}
