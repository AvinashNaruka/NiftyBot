last = df.iloc[-1]

if (last["ema20"] > last["ema50"]) and (last["ema50"] > last["ema200"]):
    return "UP"

elif (last["ema20"] < last["ema50"]) and (last["ema50"] < last["ema200"]):
    return "DOWN"

return "SIDEWAYS"
