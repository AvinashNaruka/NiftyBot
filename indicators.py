import pandas_ta as ta

def add_indicators(df):
    df["ema20"] = ta.ema(df["Close"], length=20)
    df["ema50"] = ta.ema(df["Close"], length=50)
    df["ema200"] = ta.ema(df["Close"], length=200)
    df["rsi"] = ta.rsi(df["Close"], length=14)

    macd = ta.macd(df["Close"])
    df["macd"] = macd["MACD_12_26_9"]
    df["signal"] = macd["MACDs_12_26_9"]

    return df


def get_trend(df):
    """Safe trend detection — NO ambiguous Series comparison"""

    last = df.iloc[-1]     # ALWAYS convert Series → scalar values

    ema20 = last["ema20"]
    ema50 = last["ema50"]
    ema200 = last["ema200"]

    if ema20 > ema50 and ema50 > ema200:
        return "UP"
    elif ema20 < ema50 and ema50 < ema200:
        return "DOWN"
    else:
        return "SIDEWAYS"
