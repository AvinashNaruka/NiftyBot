import pandas_ta as ta

def add_indicators(df):
    df["ema20"] = ta.ema(df["Close"], 20)
    df["ema50"] = ta.ema(df["Close"], 50)
    df["ema200"] = ta.ema(df["Close"], 200)
    df["rsi"] = ta.rsi(df["Close"], 14)

    macd = ta.macd(df["Close"])
    df = df.join(macd)

    return df


def get_trend(df):
    last = df.iloc[-1]

    # FIXED ambiguous comparison
    if (last["ema20"] > last["ema50"]) and (last["ema50"] > last["ema200"]):
        return "UP"

    elif (last["ema20"] < last["ema50"]) and (last["ema50"] < last["ema200"]):
        return "DOWN"

    return "SIDEWAYS"
