import pandas_ta as ta

def add_indicators(df):
    df["ema20"] = ta.ema(df["Close"], 20)
    df["ema50"] = ta.ema(df["Close"], 50)
    df["ema200"] = ta.ema(df["Close"], 200)
    df["rsi"] = ta.rsi(df["Close"], 14)
    return df

def get_trend(df):
    last = df.iloc[-1]
    if last["ema20"] > last["ema50"] > last["ema200"]:
        return "UP"
    elif last["ema20"] < last["ema50"] < last["ema200"]:
        return "DOWN"
    return "SIDEWAYS"
