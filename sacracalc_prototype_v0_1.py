
import streamlit as st
import requests
import plotly.graph_objects as go

# --- CONFIG ---
st.set_page_config(page_title="SacraCalc", layout="centered")
st.markdown("<h1 style='text-align: center;'>🧮 SacraCalc – Compare Fiat vs BTC</h1>", unsafe_allow_html=True)

# --- CONSTANTS ---
currency_rates = {'USD': 1, 'EUR': 1.1, 'CAD': 0.75, 'MXN': 0.059, 'BRICS': 0.2}
inflation_rates = {'USD': 0.04, 'EUR': 0.05, 'CAD': 0.03, 'MXN': 0.08, 'BRICS': 0.10}
market_news = {
    'USD': "🇺🇸 U.S. passed crypto laws to reduce legal uncertainty.",
    'EUR': "🇪🇺 Europe introduced MiCA rules to protect users.",
    'CAD': "🇨🇦 Canada supports Bitcoin ETFs.",
    'MXN': "🇲🇽 Peso is impacted by U.S. inflation and local volatility.",
    'BRICS': "🌍 BRICS explore gold-backed digital currencies."
}
btc_growth_rate = 0.45

# --- FUNCTIONS ---
def get_btc_price_usd():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        return requests.get(url).json()['bitcoin']['usd']
    except:
        return 111000  # fallback value

# --- INPUTS ---
col1, col2 = st.columns(2)
with col1:
    fiat = st.number_input("💰 Amount:", min_value=10.0, max_value=1_000_000.0, value=100.0, step=10.0)
with col2:
    currency = st.selectbox("🌍 Currency:", options=list(currency_rates.keys()))

years = st.number_input("📅 Years:", min_value=0, value=1, step=1)
months = st.number_input("🌙 Months:", min_value=0, max_value=11, value=0, step=1)
language = st.radio("🌐 Language:", options=["English", "Español"], horizontal=True)
calculate = st.button("🔍 Calculate")

# --- CALCULATIONS ---
if calculate:
    total_years = years + (months / 12)
    rate = currency_rates[currency]
    inflation = inflation_rates[currency]
    btc_price_usd = get_btc_price_usd()
    btc_price_local = btc_price_usd * rate
    future_btc_price_usd = btc_price_usd * (1 + btc_growth_rate) ** total_years
    future_btc_price_local = future_btc_price_usd * rate

    fiat_usd = fiat * rate
    btc_now = fiat_usd / btc_price_usd
    adjusted_fiat_usd = fiat_usd * (1 - inflation) ** total_years
    btc_future = adjusted_fiat_usd / future_btc_price_usd

    sats_now = int(btc_now * 100_000_000)
    sats_future = int(btc_future * 100_000_000)
    sats_diff = sats_now - sats_future

    adjusted_fiat_local = fiat * (1 - inflation) ** total_years
    btc_value_future_local = btc_now * future_btc_price_local
    future_cost = fiat / ((1 - inflation) ** total_years)
    buying_power_loss = (future_cost - fiat) / fiat * 100

    if language == "English":
        st.markdown(f"### 💡 Your Setup:")
        st.write(f"- You entered: {fiat:.2f} {currency}")
        st.write(f"- Timeframe: {years} years and {months} months")
        st.write(f"- Live BTC price: ${btc_price_usd:,.2f} USD")
        st.write(f"- Inflation rate ({currency}): {inflation*100:.1f}%")
        st.write(f"- BTC growth assumption: {btc_growth_rate*100:.0f}% annually")

        st.markdown("### 📈 What This Means:")
        st.write(f"- **Projected BTC price** in {currency}: {future_btc_price_local:,.2f} {currency}")
        st.write(f"- BTC you could buy today: {btc_now:.8f} BTC ({sats_now:,} sats)")
        st.write(f"- BTC you could buy in {years}y {months}m: {btc_future:.8f} BTC ({sats_future:,} sats)")
        st.write(f"- Buying now gives you ≈ {sats_diff:,} more sats")

        st.markdown("### 💰 Value Projection:")
        st.write(f"- Your {fiat:.2f} {currency} after inflation: {adjusted_fiat_local:.2f} {currency}")
        st.write(f"- BTC value of that in {years}y {months}m: {btc_value_future_local:,.2f} {currency}")

        st.markdown("### 🛒 Purchasing Power:")
        st.write(f"- What costs {fiat:.0f} {currency} today may cost {future_cost:.2f} {currency} in {years}y {months}m")
        st.write(f"- Your buying power loss = {buying_power_loss:.1f}%")

        st.markdown("### 🌍 Market Insight:")
        st.write(market_news[currency])

        st.markdown("### 📊 Confidence Meter:")
        st.write("Based on historical BTC growth (45%/year) and current inflation.")
        st.write("While past performance is no guarantee, it offers insight into future trends.")

    # --- PLOTLY CHART ---
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Future (BTC)", "Future (Cash)"],
        y=[btc_value_future_local, adjusted_fiat_local],
        text=[f"{btc_value_future_local:,.0f}", f"{adjusted_fiat_local:,.0f}"],
        textposition='outside',
        marker_color=['green', 'red']
    ))
    fig.update_layout(title=f"Projected Value in {currency}", yaxis_title=f"{currency} Value", height=400)
    st.plotly_chart(fig)

    # --- CTA BUTTON ---
    st.markdown("<a href='https://tiktok.com/@sacracode' target='_blank'><button style='background-color:#000;color:white;padding:10px 16px;border-radius:5px;margin-top:10px;'>📲 Learn More on TikTok</button></a>", unsafe_allow_html=True)
