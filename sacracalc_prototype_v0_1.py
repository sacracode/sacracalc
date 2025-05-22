import streamlit as st
import requests
import matplotlib.pyplot as plt

# --- CONFIG ---
st.set_page_config(page_title="SacraCalc", layout="centered")
st.markdown("## 🧮 SacraCalc – Compare Fiat vs BTC")

# Currency conversion and inflation data
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

market_news = {
    "USD": "🇺🇸 U.S. passed crypto laws to reduce legal uncertainty.",
    "EUR": "🇪🇺 Europe introduced MiCA rules to protect users.",
    "CAD": "🇨🇦 Canada supports Bitcoin ETFs and regulation.",
    "MXN": "🇲🇽 Peso is impacted by U.S. inflation and local volatility.",
    "BRICS": "🌍 BRICS exploring gold-backed and digital currencies."
}

btc_growth_rate = 0.45

# --- FUNCTIONS ---
def get_btc_price_usd():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        return requests.get(url).json()["bitcoin"]["usd"]
    except:
        return 111000  # fallback

# --- INPUTS ---
amount = st.number_input("💸 Amount:", min_value=1.0, value=100.0, step=10.0)
years = st.number_input("📅 Years:", min_value=0, value=1)
months = st.number_input("🕒 Months:", min_value=0, max_value=11, value=0)
currency = st.selectbox("🌍 Currency:", options=list(currency_rates.keys()))
language = st.radio("🌐 Language:", ["English", "Español"])

total_years = years + months / 12

if st.button("🔍 Calculate"):

    btc_price_usd = get_btc_price_usd()
    rate = currency_rates[currency]
    inflation = inflation_rates[currency]

    fiat_usd = amount * rate
    future_btc_price_usd = btc_price_usd * (1 + btc_growth_rate) ** total_years
    adjusted_fiat_usd = fiat_usd * (1 - inflation) ** total_years
    btc_now = fiat_usd / btc_price_usd
    btc_future = adjusted_fiat_usd / future_btc_price_usd
    sats_now = int(btc_now * 100_000_000)
    sats_future = int(btc_future * 100_000_000)
    sats_diff = sats_now - sats_future

    adjusted_fiat_local = adjusted_fiat_usd / rate
    future_btc_value_local = btc_now * future_btc_price_usd * rate
    future_cost = amount / ((1 - inflation) ** total_years)
    power_loss_pct = (future_cost - amount) / amount * 100

    # --- OUTPUT ---
    st.markdown(f"### 💡 Your Setup:")
    st.markdown(f"- You entered: **{amount:.2f} {currency}**")
    st.markdown(f"- Timeframe: **{int(years)}y {int(months)}m**")
    st.markdown(f"- Live BTC price: **${btc_price_usd:,.2f} USD**")
    st.markdown(f"- Inflation rate: **{inflation * 100:.1f}%**")
    st.markdown(f"- BTC growth assumption: **{btc_growth_rate * 100:.1f}% annually**")

    st.markdown(f"### 📈 What This Means:")
    st.markdown(f"- Future BTC price: **${future_btc_price_usd:,.2f} USD**")
    st.markdown(f"- BTC you could buy today: **{btc_now:.8f} BTC ({sats_now:,} sats)**")
    st.markdown(f"- BTC you could buy in {int(years)}y {int(months)}m: **{btc_future:.8f} BTC ({sats_future:,} sats)**")
    st.markdown(f"- Buying now gives you ≈ **{sats_diff:,} sats more**")

    st.markdown(f"### 💰 {currency} Projection:")
    st.markdown(f"- Your {amount:.2f} {currency} after inflation: **{adjusted_fiat_local:.2f} {currency}**")
    st.markdown(f"- Inflation reduced your {amount:.2f} {currency} to ≈ **{adjusted_fiat_local:.2f} {currency}**")
    st.markdown(f"- That's a projected loss of ≈ **{amount - adjusted_fiat_local:.2f} {currency}** in value")

    st.markdown(f"### 🛒 Purchasing Power:")
    st.markdown(f"- What costs {amount:.0f} {currency} today may cost **{future_cost:.2f} {currency}** in {int(years)}y {int(months)}m")
    st.markdown(f"- Your buying power loss = **{power_loss_pct:.1f}%**")

    st.markdown(f"### 🌍 Market Insight:")
    st.markdown(f"{market_news[currency]}")

    st.markdown("### 📊 Confidence Meter:")
    st.markdown("Based on historical BTC growth (45%/year) and current inflation.")
    st.markdown("While past performance is no guarantee, it offers insight into future trends.")

    # --- CHART ---
    fig, ax = plt.subplots(figsize=(6, 3))
    bars = ax.bar(["Future (BTC)", "Future (Cash)"], [future_btc_value_local, adjusted_fiat_local], color=["green", "red"])
    ax.set_ylabel(f"{currency} Value")
    ax.set_title(f"Projected Value in {currency}")
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{int(height)}", xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
    st.pyplot(fig)

    # CTA
    st.markdown("### 📱 [**Learn More on TikTok**](https://www.tiktok.com/@sacracode)")

