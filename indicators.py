import pandas_ta as ta

def add_indicators(df):
    df["ema20"] = ta.ema(df["Close"], length=20)
    df["ema50"] = ta.ema(df["Close"], length=50)
    df["ema200"] = ta.ema(df["Close"], length=200)
    df["rsi"] = ta.rsi(df["Close"], length=14)

    macd = ta.macd(df["Close"])
    df = df.join(macd)

    return df


def get_trend(df):
    last = df.iloc[-1]

    # UP TREND
    if (last["ema20"] > last["ema50"]) and (last["ema50"] > last["ema200"]):
        return "UP"

    # DOWN TREND
    elif (last["ema20"] < last["ema50"]) and (last["ema50"] < last["ema200"]):
        return "DOWN"

    # SIDEWAYS
    else:
        return "SIDEWAYS"
