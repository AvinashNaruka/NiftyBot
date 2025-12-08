from data import get_nifty_ltp, get_nifty_ohlc
from indicators import add_indicators, get_trend


def _calculate_strike(ltp: float) -> int:
    """Round to nearest 50"""
    if not ltp:
        return None
    return int(round(ltp / 50) * 50)


def generate_signal() -> dict:
    try:
        # GET NIFTY LTP
        ltp = get_nifty_ltp()
        if ltp is None:
            return {"error": "Failed to fetch Nifty LTP"}

        # GET OHLC data
        df = get_nifty_ohlc()
        if df is None or len(df) < 10:
            return {"error": "OHLC data unavailable"}

        # Add Indicators
        df = add_indicators(df)

        # Remove rows with NaN to avoid Series comparison crash
        df = df.dropna()
        if len(df) < 5:
            return {"error": "Indicator calculation failed (NaN values)"}

        # Detect Trend SAFELY
        trend = get_trend(df)

        # Prepare strike price
        strike = _calculate_strike(ltp)
        if strike is None:
            return {"error": "Invalid LTP"}

        # BUILD FINAL SIGNAL
        signal = {
            "ltp": ltp,
            "strike": strike,
            "trend": trend,
        }

        return signal

    except Exception as e:
        return {
            "error": "internal",
            "message": str(e)
        }
