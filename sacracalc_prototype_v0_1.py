
import streamlit as st
import requests
import plotly.graph_objects as go

# --- CONFIG ---
st.set_page_config(page_title="SacraCalc", layout="centered")
st.markdown("""
    <h1 style='text-align: center; color: #10B981;'>🧮 SacraCalc</h1>
    <h3 style='text-align: center; color: white;'>Visualiza cómo pierde valor tu dinero en fiat... y cómo Bitcoin podría protegerlo.</h3>
    <br>
""", unsafe_allow_html=True)

# --- DATA ---
currency_rates = {"USD": 1.0, "EUR": 1.1, "CAD": 0.75, "MXN": 0.059, "BRICS": 0.2}
inflation_rates = {"USD": 0.04, "EUR": 0.05, "CAD": 0.03, "MXN": 0.08, "BRICS": 0.10}
market_news = {
    "USD": "🇺🇸 U.S. passed crypto laws to support investment and reduce legal uncertainty.",
    "EUR": "🇪🇺 Europe introduced MiCA rules to reduce scams and protect users.",
    "CAD": "🇨🇦 Canada supports crypto with official Bitcoin ETFs.",
    "MXN": "🇲🇽 Peso is impacted by U.S. inflation and local volatility.",
    "BRICS": "🌐 BRICS countries exploring new digital and gold-backed currencies."
}
btc_growth_rate = 0.45

# --- FUNCTIONS ---
def get_btc_price_usd():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        return requests.get(url).json()["bitcoin"]["usd"]
    except:
        return 111000  # fallback

# --- UI INPUTS ---
amount = st.number_input("💰 Ingresar cantidad:", min_value=1.0, step=10.0, value=100.0)
years = st.number_input("🗓️ Años:", min_value=0, step=1, value=1)
months = st.number_input("🌙 Meses:", min_value=0, max_value=11, step=1, value=0)
currency = st.selectbox("🌍 Moneda:", list(currency_rates.keys()), index=3)
lang = st.radio("🗣️ Idioma:", ["Español", "English"], horizontal=True)

# --- CALCULATIONS ---
if st.button("🔍 Calcular"):

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

    # --- OUTPUT ---
    st.markdown("## 💡 Tu Configuración:")
    st.markdown(f"- Ingresaste: {fiat_input:.2f} {currency}")
    st.markdown(f"- Periodo: {years} años y {months} meses")
    st.markdown(f"- Precio actual BTC: ${btc_price_usd:,.2f} USD")
    st.markdown(f"- Inflación esperada: {inflation * 100:.1f}%")
    st.markdown(f"- Crecimiento BTC estimado: {btc_growth_rate * 100:.0f}% anual")

    st.markdown("## 📈 Proyección:")
    st.markdown(f"- Precio futuro estimado BTC en {currency}: {future_btc_price_local:,.2f} {currency}")
    st.markdown(f"- BTC que podrías comprar hoy: {btc_now:.8f} BTC ({sats_now:,} sats)")
    st.markdown(f"- BTC en {years}a {months}m: {btc_later:.8f} BTC ({sats_later:,} sats)")
    st.markdown(f"- Comprar hoy te da ≈ {sats_diff:,} sats más")

    st.markdown("## 💰 Valor Futuro:")
    st.markdown(f"- Tu dinero ajustado por inflación: {adjusted_fiat:.2f} {currency}")
    st.markdown(f"- Valor estimado si lo cambias a BTC: {btc_future_value:.2f} {currency}")

    st.markdown("## 🛒 Poder Adquisitivo:")
    st.markdown(f"- Lo que hoy cuesta {fiat_input:.0f} {currency}, podría costar {future_price_inflated:.2f} en {years}a {months}m")
    st.markdown(f"- Pérdida de poder adquisitivo ≈ {power_loss_pct:.1f}%")

    st.markdown("## 🌍 Contexto de Mercado:")
    st.markdown(market_news[currency])

    st.markdown("## 📊 Nivel de Confianza:")
    st.markdown("Basado en crecimiento histórico de BTC (45% anual) y tasas actuales de inflación.")
    st.markdown("Esto no garantiza el futuro, pero ofrece perspectiva.")

    # --- CHART ---
    labels = ["BTC en el futuro", "Efectivo con inflación"]
    values = [btc_future_value, adjusted_fiat]
    colors = ['green', 'red']

    fig = go.Figure(data=[go.Bar(
        x=labels,
        y=values,
        marker_color=colors,
        text=[f"{v:,.0f}" for v in values],
        textposition='outside'
    )])
    fig.update_layout(
        title="Proyección visual de valor 📉",
        yaxis_title=f"Valor en {currency}",
        height=400,
        paper_bgcolor='#0D1117',
        plot_bgcolor='#0D1117',
        font_color='white',
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig)

    # --- CTA ---
    st.markdown("""
        <div style='text-align: center; margin-top: 30px;'>
            <a href='https://www.tiktok.com/@sacracode' target='_blank'>
                <button style='padding: 0.7em 1.5em; background-color: #10B981; color: white; font-size: 16px; border: none; border-radius: 10px; cursor: pointer;'>
                    📲 Aprende más en TikTok
                </button>
            </a>
        </div>
    """, unsafe_allow_html=True)
