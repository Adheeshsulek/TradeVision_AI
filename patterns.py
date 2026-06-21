import numpy as np
from scipy.signal import argrelextrema


def support_resistance(df):

    close = df['Close'].squeeze().values

    highs = argrelextrema(
        close,
        np.greater,
        order=5
    )[0]

    lows = argrelextrema(
        close,
        np.less,
        order=5
    )[0]

    return highs, lows


def hammer(candle):

    open_price = float(candle['Open'])
    close_price = float(candle['Close'])
    low_price = float(candle['Low'])

    body = abs(close_price - open_price)

    lower_shadow = min(
        open_price,
        close_price
    ) - low_price

    return lower_shadow > body * 2


def shooting_star(candle):

    open_price = float(candle['Open'])
    close_price = float(candle['Close'])
    high_price = float(candle['High'])

    body = abs(close_price - open_price)

    upper_shadow = (
        high_price -
        max(open_price, close_price)
    )

    return upper_shadow > body * 2


def bullish_engulfing(prev, current):

    prev_open = float(prev['Open'])
    prev_close = float(prev['Close'])

    curr_open = float(current['Open'])
    curr_close = float(current['Close'])

    return (
        prev_close < prev_open
        and curr_close > curr_open
        and curr_open < prev_close
        and curr_close > prev_open
    )


def double_top(high_values):

    if len(high_values) < 2:
        return False

    h1 = float(high_values[-1])
    h2 = float(high_values[-2])

    return abs(h1 - h2) < h1 * 0.02


def double_bottom(low_values):

    if len(low_values) < 2:
        return False

    l1 = float(low_values[-1])
    l2 = float(low_values[-2])

    return abs(l1 - l2) < l1 * 0.02


def breakout(price, resistance):

    return float(price) > float(resistance)


def head_and_shoulders(high_values):

    if len(high_values) < 3:
        return False

    left = float(high_values[-3])
    head = float(high_values[-2])
    right = float(high_values[-1])

    return (
        head > left
        and head > right
        and abs(left - right) < left * 0.03
    )


def ascending_triangle(high_values, low_values):

    if len(high_values) < 5 or len(low_values) < 5:
        return False

    recent_highs = high_values[-5:]
    recent_lows = low_values[-5:]

    highs_flat = np.std(recent_highs) < np.mean(recent_highs) * 0.01

    lows_rising = all(
        recent_lows[i] < recent_lows[i + 1]
        for i in range(len(recent_lows) - 1)
    )

    return highs_flat and lows_rising

def doji(candle):

    open_price = float(candle["Open"])
    close_price = float(candle["Close"])

    body = abs(
        close_price - open_price
    )

    return body < (open_price * 0.002)


def morning_star(
    first,
    second,
    third
):

    return (
        first["Close"] < first["Open"]
        and
        abs(
            second["Close"]
            - second["Open"]
        ) < (
            abs(
                first["Close"]
                - first["Open"]
            ) * 0.5
        )
        and
        third["Close"] > third["Open"]
    )


def evening_star(
    first,
    second,
    third
):

    return (
        first["Close"] > first["Open"]
        and
        abs(
            second["Close"]
            - second["Open"]
        ) < (
            abs(
                first["Close"]
                - first["Open"]
            ) * 0.5
        )
        and
        third["Close"] < third["Open"]
    )