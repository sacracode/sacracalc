import streamlit as st
import requests
import plotly.graph_objects as go

# --- CONFIG ---
st.set_page_config(page_title="SacraCalc", layout="centered")
st.markdown("<h1 style='text-align: center;'>🧮 SacraCalc – Compare Fiat vs BTC</h1>", unsafe_allow_html=True)

currency_rates = {
    "USD": 1.0,
    "EUR": 1.1,
    "CAD": 0.75,
    "MXN": 0.059,
    "BRICS": 0.2
}

inflation_rates = {
    "USD": 0.04,
    "EUR": 0.05,
    "CAD": 0.03,
    "MXN": 0.08,
    "BRICS": 0.10
}

btc_growth_rate = 0.45

market_news = {
    "USD": "🇺🇸 U.S. passed crypto laws to support investment and reduce legal uncertainty.",
    "EUR": "🇪🇺 Europe introduced MiCA rules to reduce scams and protect users.",
    "CAD": "🇨🇦 Canada supports crypto with official Bitcoin ETFs.",
    "MXN": "🇲🇽 Peso is impacted by U.S. inflation and local volatility.",
    "BRICS": "🌐 BRICS countries exploring new digital and gold-backed currencies."
}

# --- FUNCTIONS ---
def get_btc_price_usd():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        return requests.get(url).json()["bitcoin"]["usd"]
    except:
        return 110000  # fallback

# --- UI ---
amount = st.number_input("🐮 Amount:", min_value=1.0, value=100.0, step=10.0)
years = st.number_input("📅 Years:", min_value=0, value=1)
months = st.number_input("🌐 Months:", min_value=0, max_value=11, value=0)
currency = st.selectbox("🪙 Currency:", options=list(currency_rates.keys()))
language = st.radio("🌍 Language:", options=["English", "Español"])
st.markdown("")

if st.button("🔍 Calculate"):

    btc_price_usd = get_btc_price_usd()
    rate = currency_rates[currency]
    inflation = inflation_rates[currency]
    total_years = years + (months / 12)

    fiat_input = amount
    fiat_usd = fiat_input * rate
    future_btc_price_usd = btc_price_usd * ((1 + btc_growth_rate) ** total_years)
    future_btc_price_local = future_btc_price_usd / rate

    btc_now = fiat_usd / btc_price_usd
    btc_later = fiat_usd * ((1 - inflation) ** total_years) / future_btc_price_usd

    sats_now = int(btc_now * 100_000_000)
    sats_later = int(btc_later * 100_000_000)
    sats_diff = sats_now - sats_later

    adjusted_fiat = fiat_input * ((1 - inflation) ** total_years)
    btc_future_value = btc_now * future_btc_price_usd / rate

    future_price_inflated = fiat_input / ((1 - inflation) ** total_years)
    power_loss_pct = ((future_price_inflated - fiat_input) / fiat_input) * 100

    # --- Output ---
    st.markdown("## 💡 Your Setup:")
    st.markdown(f"- You entered: {fiat_input:.2f} {currency}")
    st.markdown(f"- Timeframe: {years} years and {months} months")
    st.markdown(f"- Live BTC price: ${btc_price_usd:,.2f} USD")
    st.markdown(f"- Inflation rate ({currency}): {inflation * 100:.1f}%")
    st.markdown(f"- BTC growth assumption: {btc_growth_rate * 100:.0f}% annually")

    st.markdown("## 📈 What This Means:")
    st.markdown(f"- **Projected BTC price** in {currency}: {future_btc_price_local:,.2f} {currency}")
    st.markdown(f"- BTC you could buy today: {btc_now:.8f} BTC ({sats_now:,} sats)")
    st.markdown(f"- BTC you could buy in {years}y {months}m: {btc_later:.8f} BTC ({sats_later:,} sats)")
    st.markdown(f"- Buying now gives you ≈ {sats_diff:,} more sats")

    st.markdown("## 💰 Value Projection:")
    st.markdown(f"- Your {fiat_input:.2f} {currency} after inflation: {adjusted_fiat:.2f} {currency}")
    st.markdown(f"- BTC value of that in {years}y {months}m: {btc_future_value:.2f} {currency}")

    st.markdown("## 🛒 Purchasing Power:")
    st.markdown(f"- What costs {fiat_input:.0f} {currency} today may cost {future_price_inflated:.2f} {currency} in {years}y {months}m")
    st.markdown(f"- Your buying power loss = {power_loss_pct:.1f}%")

    st.markdown("## 🌍 Market Insight:")
    st.markdown(f"{market_news[currency]}")

    st.markdown("## 📊 Confidence Meter:")
    st.markdown("Based on historical BTC growth (45%/year) and current inflation.")
    st.markdown("While past performance is no guarantee, it offers insight into future trends.")

    # --- Chart ---
    labels = ["Future (BTC)", "Future (Cash)"]
    values = [btc_future_value, adjusted_fiat]
    colors = ['green', 'red']

    fig = go.Figure(data=[go.Bar(
        x=labels,
        y=values,
        marker_color=colors,
        text=[f"{v:,.0f}" for v in values],
        textposition='outside'
    )])
    fig.update_layout(title=f"Projected Value in {currency}", yaxis_title=f"{currency} Value", height=350)
    st.plotly_chart(fig)

    # --- CTA ---
    st.markdown("### 📲 [Learn More on TikTok](https://www.tiktok.com/@sacraverse)", unsafe_allow_html=True)
