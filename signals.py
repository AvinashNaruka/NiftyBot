# signals.py
from data import get_nifty_ltp, get_nifty_ohlc
from indicators import add_indicators, get_trend
import math
import datetime

# ---- Normal CDF helper ----
def _norm_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

# ---- Black-Scholes (European) for call/put ----
def black_scholes_price(S, K, r, sigma, tau, option_type='call'):
    if tau <= 0 or sigma <= 0:
        # intrinsic only (approx)
        if option_type == 'call':
            return max(0.0, S - K)
        else:
            return max(0.0, K - S)
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * tau) / (sigma * math.sqrt(tau))
    d2 = d1 - sigma * math.sqrt(tau)
    if option_type == 'call':
        price = S * _norm_cdf(d1) - K * math.exp(-r * tau) * _norm_cdf(d2)
    else:
        price = K * math.exp(-r * tau) * _norm_cdf(-d2) - S * _norm_cdf(-d1)
    return max(price, 0.0)

# ---- helper: nearest strike round to 50 ----
def _round_strike(s):
    return int(round(s / 50.0) * 50)

# ---- expiry helper: next weekly Friday (approx) ----
def _days_to_expiry_weekly():
    today = datetime.date.today()
    # find next Friday
    days_ahead = 4 - today.weekday()  # Monday=0 ... Friday=4
    if days_ahead <= 0:
        days_ahead += 7
    exp = today + datetime.timedelta(days=days_ahead)
    # time to expiry in years (trading days approx -> use calendar days)
    tau = (exp - today).days / 365.0
    return tau, exp.isoformat()

# ---- main generate_signal ----
def generate_signal(assumed_iv=0.20, risk_free_rate=0.06):
    """
    Returns a dict:
    {
      trend, ltp, strike, option_type, est_premium, stoploss, targets, expiry
    }
    assumed_iv default 20% (0.20) if no market IV available.
    """
    # 1) get spot
    ltp = get_nifty_ltp()
    if ltp is None:
        return {"error": "Failed to fetch Nifty LTP"}

    # 2) get ohlc DF and add indicators
    df = get_nifty_ohlc()
    indicators_df = None
    if df is not None and len(df) >= 10:
        try:
            # our indicators module expects lower-case names
            df2 = df.rename(columns={c: c.lower() for c in df.columns})
            indicators_df = add_indicators(df2)
        except Exception as e:
            indicators_df = None

    trend = get_trend(indicators_df) if indicators_df is not None else "SIDEWAYS"

    # strike selection: nearest 50
    strike = _round_strike(ltp)
    # decide option side: buy call on UP, put on DOWN
    option_type = "CE" if trend == "UP" else "PE" if trend == "DOWN" else "CE"

    # expiry and tau
    tau, expiry = _days_to_expiry_weekly()
    # estimate premium using Black-Scholes
    # S = ltp, K = strike (for buying atm), sigma = assumed_iv
    S = float(ltp)
    K = float(strike)
    sigma = float(assumed_iv)
    r = float(risk_free_rate)

    opt_type_flag = 'call' if option_type == "CE" else 'put'
    est_premium = black_scholes_price(S, K, r, sigma, tau, option_type=opt_type_flag)

    # If premium too low (BS can give near 0 for ATM if tau small), set a floor
    premium_estimate = round(max(est_premium, 2.0), 2)

    # Stoploss / Targets: relative to premium
    stoploss = round(premium_estimate * 1.5, 2)   # example: wider stop
    target1 = round(premium_estimate * 1.6, 2)
    target2 = round(premium_estimate * 2.5, 2)

    confidence = 0.6
    if trend == "UP":
        confidence = 0.7
    elif trend == "DOWN":
        confidence = 0.7
    else:
        confidence = 0.45

    return {
        "trend": trend,
        "ltp": round(S, 2),
        "strike": strike,
        "option_type": option_type,
        "expiry": expiry,
        "tau_years": round(tau, 4),
        "assumed_iv": assumed_iv,
        "risk_free_rate": risk_free_rate,
        "entry_premium_est": premium_estimate,
        "stoploss": stoploss,
        "targets": [target1, target2],
        "confidence": confidence,
        "notes": "Premium is estimated (Black-Scholes) — use broker/market data for exact premium."
    }
