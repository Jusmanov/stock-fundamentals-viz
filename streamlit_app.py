import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Stock Fundamentals", layout="wide")

st.title("visualizer for stock fundamentals")
st.markdown("financials, metrics, insights")

ticker_input = st.text_input("enter ticker", value="JPM").upper()
ticker = yf.Ticker(ticker_input)

try:
    info = ticker.info
except:
    st.error("Invalid ticker symbol or API limit reached.")
    st.stop()

header_col1, header_col2 = st.columns([4, 1])

with header_col1:
    st.subheader(f"{info.get('longName', ticker_input)} ({ticker_input})")
    st.markdown(f"**sector**: {info.get('sector', 'N/A')}")
    st.markdown(f"**industry**: {info.get('industry', 'N/A')}")
    st.markdown(f"**market cap**: ${info.get('marketCap', 0):,.0f}")

with header_col2:
    logo_url = info.get("logo_url")
    if logo_url:
        st.image(logo_url, width=100)

st.markdown("---")

st.subheader("ratios")
ratio_col1, ratio_col2, ratio_col3 = st.columns(3)

with ratio_col1:
    st.metric("P/E Ratio", f"{info.get('trailingPE', 'N/A')}")
    st.metric("P/B Ratio", f"{info.get('priceToBook', 'N/A')}")
    st.metric("Debt/Equity", f"{info.get('debtToEquity', 'N/A')}")

with ratio_col2:
    st.metric("ROE", f"{info.get('returnOnEquity', 'N/A'):.2%}" if info.get('returnOnEquity') else "N/A")
    st.metric("ROA", f"{info.get('returnOnAssets', 'N/A'):.2%}" if info.get('returnOnAssets') else "N/A")
    st.metric("Profit Margin", f"{info.get('profitMargins', 'N/A'):.2%}" if info.get('profitMargins') else "N/A")

with ratio_col3:
    st.metric("Revenue (TTM)", f"${info.get('totalRevenue', 0):,.0f}")
    st.metric("Gross Profit", f"${info.get('grossProfits', 0):,.0f}")
    st.metric("Free Cash Flow", f"${info.get('freeCashflow', 0):,.0f}")

st.markdown("---")

st.subheader("1y historical stock price")
hist_data = ticker.history(period="1y")

if hist_data.empty:
    st.warning("No historical price data available.")
else:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist_data.index, y=hist_data["Close"], mode='lines', name='Close Price'))
    fig.update_layout(
        title=f"{ticker_input} closing price (last 1y)",
        xaxis_title="date",
        yaxis_title="price",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.subheader("quarterly revenue vs. net income")

try:
    quarterly_financials = ticker.quarterly_financials.T
    rev = quarterly_financials["Total Revenue"]
    net = quarterly_financials["Net Income"]

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=rev.index, y=rev.values, name="Revenue"))
    fig2.add_trace(go.Bar(x=net.index, y=net.values, name="Net Income"))
    fig2.update_layout(
        barmode='group',
        title="quarterly revenue vs. net income",
        xaxis_title="quarter",
        yaxis_title="USD",
        template="plotly_white"
    )
    st.plotly_chart(fig2, use_container_width=True)
except:
    st.warning("Quarterly financials not available.")

st.markdown("---")

st.caption("Built with Python, Streamlit, and Yahoo Finance")
