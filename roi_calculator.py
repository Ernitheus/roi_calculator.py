import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Advanced ROI Calculator", layout="wide")
st.title("🚀 Advanced ROI Calculator")

# Create three columns for clearer story
col1, col2, col3 = st.columns(3)

# --- Current Metrics ---
with col1:
    st.header("📍 Current Metrics")
    current_traffic = st.number_input('Monthly Traffic', min_value=0, value=10000, step=100)
    current_conversion_rate = st.number_input('Current Conversion Rate (%)', min_value=0.0, max_value=100.0, value=5.0, step=0.1)
    avg_donation = st.number_input('Average Donation ($)', min_value=1.0, value=50.0, step=1.0)

# --- Projected Ad Grant Metrics ---
with col2:
    st.header("🎯 With Google Ad Grant")
    ad_grant_traffic_pct = st.slider('Traffic Increase via Ad Grant (%)', 0, 500, 100, 10)
    ad_grant_conversion_rate = st.slider('Conversion Rate w/ Ad Grant (%)', 0.0, 100.0, 5.0, 0.1)

# --- Additional Growth Potential ---
with col3:
    st.header("🚀 Paid Ads & Lifetime Value")
    paid_ads_conversion_rate = st.slider('Paid Ads Conversion Rate (%)', 0.0, 100.0, 2.0, 0.1)
    lifetime_lead_pct = st.slider('Leads Captured for Lifetime Value (%)', 0.0, 100.0, 10.0, 1.0)
    lifetime_value_amount = st.number_input('Average Lifetime Value per Lead ($)', min_value=1.0, value=500.0, step=10.0)

# --- Calculations ---
# Ad Grant Metrics
ad_grant_traffic = current_traffic * (1 + ad_grant_traffic_pct / 100)
current_revenue = (current_traffic * current_conversion_rate / 100) * avg_donation
ad_grant_revenue = (ad_grant_traffic * ad_grant_conversion_rate / 100) * avg_donation

# Paid Ads and Lifetime Value Calculations
paid_ads_revenue = ad_grant_traffic * (paid_ads_conversion_rate / 100) * avg_donation
lifetime_leads = ad_grant_traffic * (lifetime_lead_pct / 100)
lifetime_value_revenue = lifetime_leads * lifetime_value_amount

total_projected_revenue = ad_grant_revenue + paid_ads_revenue + lifetime_value_revenue
total_growth_pct = ((total_projected_revenue - current_revenue) / current_revenue) * 100 if current_revenue else 0

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

# --- Detailed Revenue Summary ---
st.header("📈 Detailed Revenue Growth Summary")
st.markdown(f"""
| Metrics                     | Revenue               |
|-----------------------------|-----------------------|
| 📍 Current Revenue          | `${current_revenue:,.2f}`   |
| 🎯 Ad Grant Revenue         | `${ad_grant_revenue:,.2f}`  |
| 🚀 Paid Ads Revenue         | `${paid_ads_revenue:,.2f}`  |
| 🌟 Lifetime Value Revenue   | `${lifetime_value_revenue:,.2f}` |
| **🎉 Total Projected Revenue** | **`${total_projected_revenue:,.2f}`** |
| **📊 Total Revenue Increase** | **`{total_growth_pct:.1f}% 🚀`** |
""")


