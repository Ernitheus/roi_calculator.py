import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Advanced ROI Calculator", layout="wide")
st.title("🚀 Advanced ROI Calculator")

# Columns setup
col_metrics, col_current, col_projected = st.columns(3)

# Column 1: Metrics labels
with col1 := col1:
    st.header("📍 Metrics")
    st.markdown("""
    - Monthly Traffic
    - Conversion Rate (%)
    - Avg. Donation Amount ($)
    - Traffic Increase via Ad Grant (%)
    - Paid Ads Conversion Rate (%)
    - Lifetime Lead Capture Rate (%)
    - Avg. Lifetime Value per Lead ($)
    """)

# Column 2: Current KPIs
with col2 := col2:
    st.header("📉 Current KPIs")
    current_traffic = st.number_input('Current Monthly Traffic', min_value=0, value=10000, step=100)
    current_conversion_rate = st.number_input('Current Conversion Rate (%)', min_value=0.1, max_value=100.0, value=5.0, step=0.1)
    avg_donation = st.number_input('Average Donation Amount ($)', min_value=1.0, value=50.0, step=1.0)

# Column 3: New KPIs
with col3 := col3:
    st.header("🎯 New KPIs (Projected)")
    traffic_increase_pct = st.slider('Ad Grant Traffic Increase (%)', 0, 500, 100, 10)
    paid_ads_conversion_rate = st.slider('Paid Ads Conversion Rate (%)', 0.0, 100.0, 2.5, 0.1)
    lifetime_capture_rate = st.slider('Lifetime Lead Capture Rate (%)', 0, 100, 10, 1)
    avg_lifetime_value = st.number_input('Average Lifetime Value per Lead ($)', min_value=1.0, value=500.0, step=10.0)

# Calculations
projected_traffic = current_traffic * (1 + traffic_increase_pct / 100)

current_revenue = current_traffic * (current_conversion_rate / 100) * avg_donation
ad_grant_revenue = projected_traffic * (current_conversion_rate / 100) * avg_donation
paid_ads_revenue = projected_traffic * (paid_ads_conversion_rate / 100) * avg_donation
lifetime_leads_captured = projected_traffic * (lifetime_capture_rate / 100)
lifetime_value_revenue = lifetime_leads_captured * avg_lifetime_value

total_new_revenue = ad_grant_revenue + paid_ads_revenue + lifetime_leads_captured * avg_lifetime_value
total_growth_pct = ((total_projected_revenue := (ad_grant_revenue + paid_ads_revenue + lifetime_leads_captured * avg_lifetime_value)) - current_revenue) / current_revenue * 100 if current_revenue else 0
current_revenue = current_traffic * (current_conversion_rate / 100) * avg_donation

# Visualization (Gauge charts)
fig = go.Figure()

fig.add_trace(go.Indicator(
    mode="gauge+number",
    value=current_revenue,
    title={'text': "Current Revenue ($)"},
    domain={'x': [0, 0.33]},
    gauge={'axis': {'range': [0, total_projected_revenue*1.2]}, 'bar': {'color': "gray"}}
))

fig.add_trace(go.Indicator(
    mode="gauge+number+delta",
    value=ad_grant_revenue,
    delta={'reference': current_revenue, 'relative': True, 'valueformat': '.1%', 'increasing': {'color': 'blue'}},
    title={'text': "Ad Grant Revenue ($)"},
    domain={'x': [0.34, 0.66]},
    gauge={'axis': {'range': [None, total_projected_revenue*1.2]}, 'bar': {'color': "blue"}}
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

# Revenue Summary
st.header("📈 Revenue Growth Breakdown")
st.markdown(f"""
| Revenue Source                 | Amount                          |
|--------------------------------|---------------------------------|
| 📍 Current Revenue             | `${current_revenue:,.2f}`       |
| 🎯 Ad Grant Revenue            | `${ad_grant_revenue:,.2f}`      |
| 🚀 Paid Ads Revenue            | `${paid_ads_revenue:,.2f}`      |
| 💎 Lifetime Leads Captured     | `{int(lifetime_leads_captured):,}` leads |
| 🌟 Lifetime Value Revenue      | `${lifetime_leads_captured * avg_lifetime_value:,.2f}` |
| **🎉 Total Projected Revenue** | **`${total_projected_revenue:,.2f}`** |
| **📊 Total Revenue Increase**  | **`{total_growth_pct:.1f}% 🚀`**  |
""")
