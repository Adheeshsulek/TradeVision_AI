def detect_trend(df):

    close = df["Close"].squeeze()

    ema20 = close.ewm(span=20).mean()

    current_price = float(close.iloc[-1])
    current_ema = float(ema20.iloc[-1])

    if current_price > current_ema:
        return "Bullish"

    elif current_price < current_ema:
        return "Bearish"

    return "Sideways"