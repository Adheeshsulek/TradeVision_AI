import cv2
import numpy as np
import streamlit as st
import plotly.graph_objects as go

from data_loader import get_data
from indicators import detect_trend

from patterns import (
    support_resistance,
    hammer,
    shooting_star,
    bullish_engulfing,
    doji,
    morning_star,
    evening_star,
    double_top,
    double_bottom,
    breakout,
    head_and_shoulders,
    ascending_triangle,
    
)

st.set_page_config(
    page_title="TradeVision AI",
    layout="wide"
)

st.title("📈 TradeVision AI")
uploaded_file = st.file_uploader(
    "Upload Trading Chart Screenshot",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:

    st.image(
        uploaded_file,
        caption="Uploaded Chart",
        width="stretch"
    )

if uploaded_file is not None:

    uploaded_file.seek(0)

    file_bytes = np.asarray(
        bytearray(
            uploaded_file.read()
        ),
        dtype=np.uint8
    )

    image = cv2.imdecode(
        file_bytes,
        cv2.IMREAD_COLOR
    )

    st.write(
        f"Image Shape: {image.shape}"
    )
    st.subheader("Screenshot Analysis")

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    brightness = np.mean(gray)

    if brightness > 120:
        screenshot_trend = "Bullish"
    else:
        screenshot_trend = "Bearish"

    st.success(
        f"Detected Trend: {screenshot_trend}"
    )

st.caption("AI-Powered Technical Analysis Dashboard")

# Load Data
stock = st.selectbox(
    "📊 Select Stock",
    [
        "RELIANCE.NS",
        "TCS.NS",
        "INFY.NS",
        "HDFCBANK.NS",
        "ICICIBANK.NS",
        "SBIN.NS",
        "LT.NS",
        "AXISBANK.NS",
        "KOTAKBANK.NS",
        "ITC.NS",
        "BHARTIARTL.NS",
        "ASIANPAINT.NS",
        "MARUTI.NS",
        "BAJFINANCE.NS",
        "HCLTECH.NS",
        "WIPRO.NS",
        "TECHM.NS",
        "SUNPHARMA.NS",
        "TITAN.NS",
        "ULTRACEMCO.NS",
        "NESTLEIND.NS",
        "POWERGRID.NS",
        "NTPC.NS",
        "ONGC.NS",
        "COALINDIA.NS",
        "ADANIENT.NS",
        "ADANIPORTS.NS",
        "TATAMOTORS.NS",
        "TATASTEEL.NS",
        "JSWSTEEL.NS",
        "HINDALCO.NS",
        "GRASIM.NS",
        "BAJAJFINSV.NS",
        "BAJAJ-AUTO.NS",
        "INDUSINDBK.NS",
        "EICHERMOT.NS",
        "CIPLA.NS",
        "DRREDDY.NS",
        "APOLLOHOSP.NS",
        "BRITANNIA.NS",
        "HEROMOTOCO.NS",
        "SHRIRAMFIN.NS",
        "BPCL.NS",
        "DIVISLAB.NS",
        "HDFCLIFE.NS",
        "SBILIFE.NS",
        "TATACONSUM.NS",
        "PIDILITIND.NS",
        "DABUR.NS",
        "AMBUJACEM.NS",
        "ZYDUSLIFE.NS"
    ]
)

df = get_data(stock)

st.success(f"Currently Analyzing: {stock}")

# Trend Detection
trend = detect_trend(df)

# Support & Resistance
highs, lows = support_resistance(df)

close = df["Close"].squeeze()

ema20 = close.ewm(span=20).mean()
ema50 = close.ewm(span=50).mean()

resistance_prices = close.iloc[highs]
support_prices = close.iloc[lows]

# Latest Candles
last = df.iloc[-1]
prev = df.iloc[-2]
third_last = df.iloc[-3]

# Candlestick Pattern Detection
candle_pattern = "None"

if doji(last):

    candle_pattern = "Doji"

elif hammer(last):

    candle_pattern = "Hammer"

elif shooting_star(last):

    candle_pattern = "Shooting Star"

elif bullish_engulfing(
    prev,
    last
):

    candle_pattern = "Bullish Engulfing"

elif morning_star(
    third_last,
    prev,
    last
):

    candle_pattern = "Morning Star"

elif evening_star(
    third_last,
    prev,
    last
):

    candle_pattern = "Evening Star"

# Chart Pattern Detection
double_top_detected = double_top(
    resistance_prices.values
)

double_bottom_detected = double_bottom(
    support_prices.values
)

head_shoulders_detected = head_and_shoulders(
    resistance_prices.values
)

triangle_detected = ascending_triangle(
    resistance_prices.values,
    support_prices.values
)

# Price & Resistance
latest_price = float(close.iloc[-1])

# Trade Setup Generator

entry_price = latest_price

# Smart Stop Loss

if len(support_prices) > 0:

    stop_loss = float(
        support_prices.iloc[-1]
    )

else:

    stop_loss = entry_price * 0.98


# Smart Targets

if len(resistance_prices) > 0:

    target_1 = float(
        resistance_prices.iloc[-1]
    )

else:

    target_1 = entry_price * 1.03


if len(resistance_prices) > 1:

    target_2 = float(
        resistance_prices.iloc[-2]
    )

else:

    target_2 = entry_price * 1.06


risk = abs(
    entry_price - stop_loss
)

reward = abs(
    target_2 - entry_price
)

if risk > 0:

    risk_reward = round(
        reward / risk,
        2
    )

else:

    risk_reward = 0

    

risk = entry_price - stop_loss

reward = target_2 - entry_price

risk_reward = round(
    reward / risk,
    2
)
if risk_reward >= 3:

    trade_quality = "Excellent"

elif risk_reward >= 2:

    trade_quality = "Good"

elif risk_reward >= 1:

    trade_quality = "Average"

else:

    trade_quality = "Poor"

if len(resistance_prices) > 0:
    latest_resistance = float(
        resistance_prices.iloc[-1]
    )
else:
    latest_resistance = latest_price

# Breakout
breakout_detected = breakout(
    latest_price,
    latest_resistance
)

# Confidence Score
confidence = 50

if trend == "Bullish":
    confidence += 15

if breakout_detected:
    confidence += 20

if candle_pattern != "None":
    confidence += 15

confidence = min(confidence, 100)

# Recommendation
recommendation = "WAIT"

if trend == "Bullish":
    recommendation = "BUY"

elif trend == "Bearish":
    recommendation = "SELL"

# Dashboard Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Trend",
        trend
    )

with col2:
    st.metric(
        "Pattern",
        candle_pattern
    )

with col3:
    st.metric(
        "Confidence",
        f"{confidence}%"
    )

with col4:
    st.metric(
        "Signal",
        recommendation
    )

st.progress(confidence)
st.subheader("📈 Price Chart")

fig = go.Figure()

fig.add_trace(
    go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Candlestick"
    )
)

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=ema20,
        mode="lines",
        name="EMA 20",
        line=dict(color="yellow")
    )
)

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=ema50,
        mode="lines",
        name="EMA 50",
        line=dict(color="cyan")
    )
)

# Draw Support Lines

for level in support_prices.tail(3):

    fig.add_hline(
        y=float(level),
        line_color="lime",
        line_width=2,
        line_dash="dot",
        annotation_text=f"Support {float(level):.2f}"
    )

# Draw Resistance Lines

for level in resistance_prices.tail(3):

    fig.add_hline(
        y=float(level),
        line_color="red",
        line_width=2,
        line_dash="dash",
        annotation_text=f"Resistance {float(level):.2f}"
    )

fig.update_layout(
    height=700,
    title="TradeVision AI Chart",
    xaxis_title="Date",
    yaxis_title="Price",
    template="plotly_dark",
    xaxis_rangeslider_visible=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Trade Setup")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric(
        "Entry",
        f"₹{entry_price:.2f}"
    )

with col2:
    st.metric(
        "Stop Loss",
        f"₹{stop_loss:.2f}"
    )

with col3:
    st.metric(
        "Target 1",
        f"₹{target_1:.2f}"
    )

with col4:
    st.metric(
        "Target 2",
        f"₹{target_2:.2f}"
    )

with col5:
    st.metric(
        "R:R",
        f"1:{risk_reward}"
    )

with col6:
    st.metric(
        "Quality",
        trade_quality
    )

# AI Summary
st.subheader("AI Trade Summary")

summary = f"""
Trend: {trend}

Current Price: ₹{latest_price:.2f}

Nearest Resistance: ₹{latest_resistance:.2f}

Breakout Status:
{"Bullish Breakout" if breakout_detected else "No Breakout"}

Detected Pattern:
{candle_pattern}

Recommendation:
{recommendation}
"""

st.info(summary)

# Pattern Detection
st.subheader("Pattern Detection")

patterns_found = False

if double_top_detected:
    st.error("Double Top Detected")
    patterns_found = True

if double_bottom_detected:
    st.success("Double Bottom Detected")
    patterns_found = True

if head_shoulders_detected:
    st.warning("Head & Shoulders Detected")
    patterns_found = True

if triangle_detected:
    st.info("Ascending Triangle Detected")
    patterns_found = True

if not patterns_found:
    st.info("No major chart patterns detected.")

# Breakout Status
st.subheader("Breakout Status")

if breakout_detected:
    st.success("Bullish Breakout Detected")

else:
    st.warning("No Breakout")

# Support Levels
st.subheader("Support Levels")

if len(support_prices) > 0:

    support_levels = support_prices.tail(5)

    for i, level in enumerate(
        support_levels,
        start=1
    ):
        st.write(
            f"Support {i}: ₹ {float(level):.2f}"
        )

else:
    st.write(
        "No support levels found."
    )

# Resistance Levels
st.subheader("Resistance Levels")

if len(resistance_prices) > 0:

    resistance_levels = resistance_prices.tail(5)

    for i, level in enumerate(
        resistance_levels,
        start=1
    ):
        st.write(
            f"Resistance {i}: ₹ {float(level):.2f}"
        )

else:
    st.write(
        "No resistance levels found."
    )

# Market Data
st.subheader("Recent Market Data")

st.dataframe(df.tail())