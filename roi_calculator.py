import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Google Ad Grant ROI Calculator", layout="wide")
st.title("🚀 Google Ad Grant ROI Calculator")

# Create two columns for Before and After
col1, col2 = st.columns(2)

with col1:
    st.header("📍 Current Metrics")
    current_traffic = st.number_input('Current Monthly Traffic', min_value=0, value=10000, step=100)
    current_conversion_rate = st.number_input('Current Traffic-to-Donor Conversion (%)',
                                              min_value=0.0, max_value=100.0, value=5.0, step=0.1)
    avg_donation = st.number_input('Average Donation Amount ($)', min_value=1.0, value=50.0, step=1.0)

with col2:
    st.header("🎯 Projected Metrics with Ad Grant")
    traffic_increase_pct = st.slider('Expected Ad Grant Traffic Increase (%)',
                                     min_value=0, max_value=500, value=100, step=10)
    projected_conversion_rate = st.slider('Projected Traffic-to-Donor Conversion (%)',
                                          min_value=0.0, max_value=100.0, value=5.0, step=0.1)

# Calculations
projected_traffic = current_traffic * (1 + traffic_increase_pct / 100)
current_donors = current_traffic * (current_conversion_rate / 100)
projected_donors = projected_traffic * (projected_conversion_rate / 100)

current_revenue = current_donors * avg_donation
projected_revenue = projected_donors * avg_donation
revenue_growth_pct = ((projected_revenue - current_revenue) / current_revenue) * 100 if current_revenue else 0

# Gauge Charts for Before vs After
fig = go.Figure()

# Current Revenue Gauge
fig.add_trace(go.Indicator(
    mode="gauge+number",
    value=current_revenue,
    title={'text': "Current Revenue ($)"},
    domain={'x': [0, 0.5], 'y': [0, 1]},
    gauge={'axis': {'range': [None, max(current_revenue, projected_revenue)*1.2]},
           'bar': {'color': "lightgray"}}
))

# Projected Revenue Gauge
fig.add_trace(go.Indicator(
    mode="gauge+number+delta",
    value=projected_revenue,
    delta={'reference': current_revenue, 'relative': True, 'valueformat': '.1%', 'increasing': {'color': 'green'}},
    title={'text': "Projected Revenue ($)"},
    domain={'x': [0.5, 1], 'y': [0, 1]},
    gauge={'axis': {'range': [None, max(current_revenue, projected_revenue)*1.2]},
           'bar': {'color': "green"},
           'steps': [{'range': [0, current_revenue], 'color': "lightgray"},
                     {'range': [current_revenue, projected_revenue], 'color': "lightgreen"}]}
))

st.plotly_chart(fig, use_container_width=True)

# Revenue Summary
st.header("📈 Revenue Growth Summary")
st.markdown(f"""
- **Current Monthly Revenue:** ${current_revenue:,.2f}
- **Projected Monthly Revenue:** ${projected_revenue:,.2f}
- **Expected Revenue Increase:** {revenue_growth_pct:.1f}% 🚀
""")
