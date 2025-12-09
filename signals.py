# signals.py

from data import get_nifty_ltp, get_nifty_ohlc
from indicators import add_indicators, get_trend
import math
import datetime


# ------------------------------
# Normal CDF function
# ------------------------------
def _norm_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


# ------------------------------
# Black-Scholes Formula
# ------------------------------
def black_scholes_price(S, K, r, sigma, tau, option_type="call"):
    if tau <= 0 or sigma <= 0:
        return max(0, S - K) if option_type == "call" else max(0, K - S)

    d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * tau) / (sigma * math.sqrt(tau))
    d2 = d1 - sigma * math.sqrt(tau)

    if option_type == "call":
        return S * _norm_cdf(d1) - K * math.exp(-r * tau) * _norm_cdf(d2)
    else:
        return K * math.exp(-r * tau) * _norm_cdf(-d2) - S * _norm_cdf(-d1)


# ------------------------------
# Round strike to nearest 50
# ------------------------------
def _round_strike(x):
    return int(round(x / 50) * 50)


# ------------------------------
# Weekly expiry (nearest Friday)
# ------------------------------
def _days_to_expiry_weekly():
    today = datetime.date.today()
    dow = today.weekday()  # Monday = 0 ... Friday = 4

    days = 4 - dow
    if days <= 0:
        days += 7

    expiry = today + datetime.timedelta(days=days)
    tau = (expiry - today).days / 365

    return tau, expiry.isoformat()


# ------------------------------
# MAIN SIGNAL GENERATOR
# ------------------------------
def generate_signal(manual_ltp=None):
    """
    manual_ltp (string or numeric):
        - If user enters LTP on website → use that.
        - If blank → use Yahoo LTP.
    """

    # 1️⃣ Decide which LTP to use
    if manual_ltp and manual_ltp != "" and manual_ltp != "null":
        try:
            ltp = float(manual_ltp)
        except:
            return {"error": "Invalid manual LTP entered"}
    else:
        ltp = get_nifty_ltp()

    if ltp is None:
        return {"error": "Unable to fetch LTP"}

    # 2️⃣ Get OHLC candles
    df = get_nifty_ohlc()
    if df is None:
        return {"error": "Unable to fetch OHLC data"}

    # Indicators
    try:
        df2 = df.rename(columns={c: c.lower() for c in df.columns})
        df_ind = add_indicators(df2)
        trend = get_trend(df_ind)
    except:
        trend = "SIDEWAYS"

    # 3️⃣ Strike selection
    strike = _round_strike(ltp)

    # 4️⃣ CE/PE selection
    if trend == "UP":
        option_type = "CE"
        bs_type = "call"
    elif trend == "DOWN":
        option_type = "PE"
        bs_type = "put"
    else:
        option_type = "CE"
        bs_type = "call"

    # 5️⃣ Expiry & Black-Scholes premium estimate
    tau, expiry = _days_to_expiry_weekly()
    assumed_iv = 0.20
    risk_free_rate = 0.06

    est = black_scholes_price(
        S=float(ltp),
        K=float(strike),
        r=risk_free_rate,
        sigma=assumed_iv,
        tau=tau,
        option_type=bs_type,
    )

    est = round(max(est, 2.0), 2)

    # 6️⃣ Stoploss & targets
    stoploss = round(est * 1.5, 2)
    target1 = round(est * 1.6, 2)
    target2 = round(est * 2.5, 2)

    # 7️⃣ Confidence level
    if trend in ["UP", "DOWN"]:
        conf = 0.70
    else:
        conf = 0.40

    # 8️⃣ Final response
    return {
        "trend": trend,
        "ltp": round(float(ltp), 2),
        "strike": strike,
        "option_type": option_type,
        "expiry": expiry,
        "assumed_iv": assumed_iv,
        "entry_premium_est": est,
        "stoploss": stoploss,
        "targets": [target1, target2],
        "confidence": conf,
        "note": "Premium is estimated using Black-Scholes. Manual LTP overrides Yahoo."
    }
