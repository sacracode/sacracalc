
import streamlit as st
import requests
import matplotlib.pyplot as plt

# --- CONFIG ---
st.set_page_config(page_title="SacraCalc", layout="centered", initial_sidebar_state="collapsed")
st.markdown("## 🧿 SacraCalc – Compare Fiat vs BTC")

currency_rates = {'USD': 1, 'EUR': 1.1, 'CAD': 0.75, 'MXN': 0.059, 'BRICS': 0.2}
inflation_rates = {'USD': 0.04, 'EUR': 0.05, 'CAD': 0.03, 'MXN': 0.08, 'BRICS': 0.10}
btc_growth_rate = 0.45
market_news = {
    'USD': "🇺🇸 U.S. passed crypto laws to support investment and reduce legal uncertainty.",
    'EUR': "🇪🇺 Europe introduced MiCA rules to reduce scams and protect users.",
    'CAD': "🇨🇦 Canada supports crypto with official Bitcoin ETFs.",
    'MXN': "🇲🇽 Peso is impacted by U.S. inflation and local volatility.",
    'BRICS': "🌐 BRICS nations exploring digital and gold-backed currencies."
}

# --- FUNCTIONS ---
def get_btc_price_usd():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        return requests.get(url).json()['bitcoin']['usd']
    except:
        return 111000

# --- INPUTS ---
amount = st.number_input("💸 Amount:", min_value=10.0, max_value=1_000_000.0, value=100.0, step=10.0)
years = st.number_input("📅 Years:", min_value=0, max_value=50, value=1)
months = st.number_input("🌐 Months:", min_value=0, max_value=11, value=0)
currency = st.selectbox("💱 Currency:", list(currency_rates.keys()))
language = st.radio("🌍 Language:", ["English", "Español"])
calculate = st.button("🔍 Calculate")

# --- LOGIC ---
if calculate:
    total_years = years + (months / 12)
    btc_usd = get_btc_price_usd()
    fx = currency_rates[currency]
    inflation = inflation_rates[currency]
    fiat = amount

    adjusted = fiat * (1 - inflation) ** total_years
    btc_future_price = btc_usd * (1 + btc_growth_rate) ** total_years
    btc_now = (fiat * fx) / btc_usd
    btc_later = (adjusted * fx) / btc_future_price

    sats_now = int(btc_now * 100_000_000)
    sats_later = int(btc_later * 100_000_000)
    sats_diff = sats_now - sats_later

    adj_fiat = fiat * (1 - inflation) ** total_years
    btc_future_val = btc_now * btc_future_price / fx
    inflation_loss = fiat - adj_fiat
    future_cost = fiat / ((1 - inflation) ** total_years)
    power_loss_pct = (future_cost - fiat) / fiat * 100

    # OUTPUT
    if language == "English":
        st.markdown(f"### 💡 Your Setup:")
        st.markdown(f"- You entered: **{fiat:.2f} {currency}**")
        st.markdown(f"- Timeframe: **{years}y {months}m**")
        st.markdown(f"- Live BTC price: **${btc_usd:,.2f} USD**")
        st.markdown(f"- Inflation rate: **{inflation*100:.1f}%**")
        st.markdown(f"- BTC growth assumption: **{btc_growth_rate*100:.1f}%/yr**")

        st.markdown(f"### 📈 What This Means:")
        st.markdown(f"- BTC you could buy today: **{btc_now:.8f} BTC** ({sats_now:,} sats)")
        st.markdown(f"- BTC you could buy in {years}y {months}m: **{btc_later:.8f} BTC** ({sats_later:,} sats)")
        st.markdown(f"- Buying now gives you ≈ **{sats_diff:,} sats** more")

        st.markdown(f"### 💰 {currency} Projection:")
        st.markdown(f"- Your {fiat:.2f} {currency} after inflation: **{adj_fiat:.2f} {currency}**")
        st.markdown(f"- Inflation reduced your {fiat:.2f} to ≈ **{adj_fiat:.2f}**")
        st.markdown(f"- That's a projected loss of ≈ **{inflation_loss:.2f} {currency}**")

        st.markdown("### 🛒 Purchasing Power:")
        st.markdown(f"- What costs **{fiat:.2f} {currency}** today may cost **{future_cost:.2f} {currency}** in {years}y {months}m")
        st.markdown(f"- Your buying power loss = **{power_loss_pct:.1f}%**")

        st.markdown("### 🌍 Market Insight:")
        st.markdown(market_news[currency])

        st.markdown("### 📊 Confidence Meter:")
        st.markdown(f"Based on historical BTC growth (**45%/year**) and current inflation.")
        st.markdown(f"While past performance is no guarantee, it offers insight into future trends.")

    # --- PLOT ---
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(["Future (BTC)", "Future (Cash)"], [btc_future_val, adj_fiat], color=["green", "red"])
    ax.set_title(f"Projected Value in {currency}")
    ax.set_ylabel(f"{currency} Value")
    for i, val in enumerate([btc_future_val, adj_fiat]):
        ax.text(i, val + 1, f"{val:.0f}", ha='center', fontweight='bold')
    st.pyplot(fig)

    st.markdown("### 📱 [Learn More on TikTok](https://tiktok.com/@sacracode)")
