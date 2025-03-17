import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Google Ad Grant ROI Calculator", layout="wide")
st.title("🚀 Google Ad Grant ROI Calculator")

# Three columns: Metrics, Current KPIs, Projected KPIs
col_metrics, col_current, col_projected = st.columns(3)

with col_metrics:
    st.header("📍 Metrics")
    st.write("Monthly Traffic")
    st.write("Conversion Rate (%)")
    st.write("Average Donation Amount ($)")
    st.write("Traffic Increase via Ad Grant (%)")
    st.write("Paid Ads Conversion Rate (%)")
    st.write("Lifetime Lead Capture Rate (%)")
    st.write("Average Lifetime Value per Lead ($)")
    st.write("Lifetime Period (Years)")

with col_current:
    st.header("📉 Current KPIs")
    current_traffic = st.number_input('Current Monthly Traffic', min_value=0, value=10000, step=100)
    current_conversion_rate = st.number_input('Current Conversion Rate (%)', 0.1, 100.0, 5.0, 0.1)
    avg_donation = st.number_input('Average Donation Amount ($)', 1.0, value=50.0, step=1.0)

with col_projected:
    st.header("🎯 Projected KPIs")
    traffic_increase_pct = st.slider('Traffic Increase from Ad Grant (%)', 0, 500, 100, 10)
    paid_ads_conversion_rate = st.slider('Paid Ads Conversion Rate (%)', 0.0, 100.0, 2.5, 0.1)
    lifetime_capture_rate = st.slider('Lifetime Lead Capture Rate (%)', 0, 100, 10, 1)
    lifetime_years = st.slider('Lifetime Period (Years)', 1, 10, 3, 1)
    avg_lifetime_value = st.number_input('Avg. Lifetime Value per Lead ($)', min_value=1.0, value=500.0, step=10.0)

# --- Calculations ---
projected_traffic = current_traffic * (1 + traffic_increase_pct / 100)
current_revenue = current_traffic * (current_conversion_rate / 100) * avg_donation
ad_grant_revenue = projected_traffic * (current_conversion_rate / 100) * avg_donation
paid_ads_revenue = projected_traffic * (paid_ads_conversion_rate / 100) * avg_donation
lifetime_leads_captured = projected_traffic * (lifetime_capture_rate / 100)
lifetime_revenue = lifetime_leads_captured * avg_lifetime_value

total_projected_revenue = ad_grant_revenue + paid_ads_revenue + lifetime_revenue
revenue_growth_pct = ((total_projected_revenue - current_revenue) / current_revenue * 100) if current_revenue else 0

# --- Gauge Visual ---
fig = go.Figure()

fig.add_trace(go.Indicator(
    mode="gauge+number",
    value=current_revenue,
    title={'text': "Current Revenue ($)"},
    domain={'x': [0, 0.33], 'y': [0, 1]},
    gauge={'axis': {'range': [None, total_projected_revenue * 1.2]}, 'bar': {'color': "gray"}}
))

fig.add_trace(go.Indicator(
    mode="gauge+number+delta",
    value=ad_grant_revenue,
    delta={'reference': current_revenue, 'relative': True, 'valueformat': '.1%', 'increasing': {'color': 'blue'}},
    title={'text': "Ad Grant Revenue ($)"},
    domain={'x': [0.34, 0.66], 'y': [0, 1]},
    gauge={'axis': {'range': [None, total_projected_revenue * 1.2]}, 'bar': {'color': "blue"}}
))

fig.add_trace(go.Indicator(
    mode="gauge+number+delta",
    value=total_projected_revenue,
    delta={'reference': current_revenue, 'relative': True, 'valueformat': '.1%', 'increasing': {'color': 'green'}},
    title={'text': "Total Potential Revenue ($)"},
    domain={'x': [0.67, 1], 'y': [0, 1]},
    gauge={'axis': {'range': [None, total_projected_revenue * 1.2]}, 'bar': {'color': "green"}}
))

st.plotly_chart(fig, use_container_width=True)

# --- Revenue Growth Summary ---
st.header("📈 Revenue Growth Breakdown")

st.markdown(f"""
| Revenue Source                          | Amount                             |
|-----------------------------------------|------------------------------------|
| 📍 **Current Monthly Revenue**           | `${current_revenue:,.2f}`          |
| 🎯 **Ad Grant Revenue**                  | `${ad_grant_revenue:,.2f}`         |
| 🚀 **Paid Ads Revenue**                  | `${paid_ads_revenue:,.2f}`         |
| 💎 **Lifetime Value Revenue ({lifetime_years} yrs)** | `${lifetime_revenue:,.2f}`          |
| **🎉 Total Projected Revenue**           | **`${total_projected_revenue:,.2f}`** |
| **📊 Revenue Increase**                  | **`{revenue_growth_pct:.1f}% 🚀`**   |
""")
