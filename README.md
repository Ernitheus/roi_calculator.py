import streamlit as st
import plotly.graph_objects as go

st.title("🚀 Google Ad Grant ROI Calculator")

# --- User Inputs ---
current_traffic = st.number_input('Current Monthly Traffic', min_value=0, value=10000)
conversion_rate = st.slider('Current Donation Conversion Rate (%)', min_value=0.1, max_value=20.0, value=5.0, step=0.1)
traffic_increase_pct = st.slider('Expected Traffic Increase from Ad Grant (%)', min_value=10, max_value=500, value=50, step=10)
avg_donation = st.number_input('Average Donation Amount ($)', min_value=1, value=50)

# --- Calculations ---
new_traffic = current_traffic * (1 + traffic_increase_pct / 100)
current_donations = current_traffic * (conversion_rate / 100)
new_donations = new_traffic * (conversion_rate / 100)

current_revenue = current_donations * avg_donation
new_revenue = new_donations * avg_donation
revenue_increase_pct = ((new_revenue - current_revenue) / current_revenue) * 100 if current_revenue else 0

# --- Gauge (Speedometer) Visual ---
fig = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=new_revenue,
    delta={'reference': current_revenue, 'relative': True, 'valueformat':'.0%', 'increasing':{'color':'green'}},
    gauge={
        'axis': {'range': [None, max(new_revenue*1.2, current_revenue*2)]},
        'bar': {'color': "darkblue"},
        'steps': [
            {'range': [0, current_revenue], 'color': "lightgray"},
            {'range': [current_revenue, new_revenue], 'color': "lightgreen"}],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': current_revenue}},
    title={'text': "Projected Monthly Revenue ($)"}))

st.plotly_chart(fig, use_container_width=True)

# --- Summary ---
st.subheader("📈 Revenue Growth Summary:")
st.write(f"**Current Monthly Revenue:** ${current_revenue:,.2f}")
st.write(f"**Projected Monthly Revenue:** ${new_revenue:,.2f}")
st.write(f"**Revenue Increase:** {revenue_increase_pct:.1f}% 🚀")
