from data import get_nifty_ltp, get_nifty_ohlc
from indicators import add_indicators, get_trend

def _calculate_strike(ltp: float) -> int:
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
