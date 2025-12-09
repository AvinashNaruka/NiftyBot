# indicators.py
import pandas_ta as ta

def add_indicators(df):
    # expects pandas DataFrame with 'close' column
    df = df.copy()
    df['ema20'] = ta.ema(df['close'], length=20)
    df['ema50'] = ta.ema(df['close'], length=50)
    df['ema200'] = ta.ema(df['close'], length=200)
    df['rsi'] = ta.rsi(df['close'], length=14)
    macd = ta.macd(df['close'])
    # macd returns DataFrame columns: MACD_12_26_9, MACDh_12_26_9, MACDs_12_26_9
    df = df.join(macd)
    df = df.dropna().reset_index(drop=True)
    return df

def get_trend_from_row(row):
    # row is final row (pandas Series)
    ema20 = row.get('ema20')
    ema50 = row.get('ema50')
    ema200 = row.get('ema200')
    if ema20 is None or ema50 is None or ema200 is None:
        return "SIDEWAYS"
    if (ema20 > ema50) and (ema50 > ema200):
        return "UP"
    if (ema20 < ema50) and (ema50 < ema200):
        return "DOWN"
    return "SIDEWAYS"

def get_trend(df):
    if df is None or len(df) == 0:
        return "SIDEWAYS"
    last = df.iloc[-1]
    return get_trend_from_row(last)
