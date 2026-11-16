"""
Indian Stock Forecaster – Frontend
Calls the FastAPI backend deployed on Render.
"""

import requests
import pandas as pd
import streamlit as st

API_URL = "https://indian-stock-forecaster-educational.onrender.com"

st.set_page_config(page_title="Indian Stock Forecaster", page_icon="📈")
st.title("📈 Indian Stock Forecaster")
st.caption("Educational Purpose Only — Not Investment Advice")

ticker = st.text_input(
    "Enter NSE Ticker (with .NS suffix)",
    value="RELIANCE.NS",
    placeholder="e.g. TCS.NS, HDFCBANK.NS, INFY.NS",
)

st.markdown("**Quick Pick:**")
cols = st.columns(5)
popular = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "SBIN.NS"]
for i, t in enumerate(popular):
    if cols[i].button(t.replace(".NS", ""), use_container_width=True):
        ticker = t

if st.button("🔮 Predict", type="primary", use_container_width=True):
    with st.spinner(f"Fetching prediction for {ticker}..."):
        try:
            resp = requests.get(f"{API_URL}/predict", params={"ticker": ticker}, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                col1, col2 = st.columns(2)
                col1.metric("Last Close", f"₹{data['last_close']:,.2f}")
                col2.metric("Day 5 Forecast", f"₹{data['predictions'][-1]:,.2f}",
                             delta=f"{data['predictions'][-1] - data['last_close']:+,.2f}")
                st.subheader("5-Day Forecast")
                forecast_df = pd.DataFrame({
                    "Day": [f"Day {i}" for i in range(1, 6)],
                    "Predicted Close (₹)": data["predictions"],
                })
                st.dataframe(forecast_df, use_container_width=True, hide_index=True)
                st.subheader("Forecast Trend")
                chart_data = pd.DataFrame({
                    "Day": range(0, 6),
                    "Price (₹)": [data["last_close"]] + data["predictions"],
                })
                st.line_chart(chart_data.set_index("Day"), use_container_width=True)
                st.info(data["disclaimer"])
            else:
                st.error(f"API Error: {resp.json().get('detail', 'Unknown error')}")
        except requests.exceptions.ConnectionError:
            st.error("Could not reach the API. Server may be starting up — try again in 30 seconds.")
        except Exception as e:
            st.error(f"Something went wrong: {e}")

st.divider()
st.caption("Built with Python · Streamlit · FastAPI · yfinance")
