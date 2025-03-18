import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Advanced ROI Calculator", layout="wide")
st.title("🚀 Advanced ROI Calculator")

# Revenue View Toggle (Monthly vs Annual)
period = st.radio("Choose Revenue View:", ["Monthly", "Annual"])
multiplier = 12 if period == "Annual" else 1

# Toggle for including/excluding Ad Grant & Paid Ads
st.markdown("### **Select Revenue Sources to Include**")
include_ad_grant = st.checkbox("Include Ad Grant Revenue", True)
include_paid_ads = st.checkbox("Include Paid Ads Revenue", True)

# Three sections for Current, Ad Grant, and Paid Ads & Lifetime Value
col1, col2, col3 = st.columns(3)

# --- Current Metrics ---
with col1:
    st.header("📍 Current Metrics")
    current_traffic = st.number_input('Monthly Traffic', min_value=0, value=10000, step=100)
    current_conversion_rate = st.number_input('Current Conversion Rate (%)', 0.1, 100.0, 5.0, 0.1)
    avg_donation = st.number_input('Average Donation ($)', 1.0, 5000.0, 50.0, 10.0)

# --- Google Ad Grant Metrics ---
with col2:
    st.header("🎯 With Google Ad Grant")
    ad_grant_traffic_pct = st.slider('Traffic Increase via Ad Grant (%)', 0, 500, 100, 10)
    ad_grant_conversion_rate = st.slider('Conversion Rate w/ Ad Grant (%)', 0.1, 100.0, 5.0, 0.1)

# --- Paid Ads & Lifetime Value ---
with col3:
    st.header("🚀 Paid Ads & Lifetime Value")

    paid_ads_budget = st.number_input('Monthly Paid Ads Budget ($)', 0.0, 100000.0, 2000.0, 100.0)
    avg_cpc = st.number_input('Average Cost per Click (CPC, $)', 0.01, 100.0, 2.0, 0.1)
    paid_ads_conversion_rate = st.slider('Paid Ads Conversion Rate (%)', 0.1, 100.0, 2.0, 0.1)
    paid_avg_donation = st.number_input('Average Donation from Paid Ads ($)', 1.0, 5000.0, 50.0, 10.0)

    st.markdown("### 🔄 Lifetime Donor Metrics")
    lifetime_retention_pct = st.slider('Annual Donor Retention (%)', 0.0, 100.0, 40.0, 1.0)
    lifetime_years = st.slider('Average Retention (Years)', 1, 10, 3, 1)
    avg_lifetime_value_per_donor = st.number_input('Avg. Lifetime Value per Donor ($)', 1.0, 10000.0, 500.0, 50.0)

# --- Revenue Calculations ---
ad_grant_traffic = current_traffic * (1 + ad_grant_traffic_pct / 100)
ad_grant_revenue = (ad_grant_traffic * (ad_grant_conversion_rate / 100) * avg_donation) * multiplier if include_ad_grant else 0

# Paid Ads Revenue Calculations
estimated_clicks = paid_ads_budget / avg_cpc
new_paid_donors = estimated_clicks * (paid_ads_conversion_rate / 100)
immediate_paid_ads_revenue = new_paid_donors * paid_avg_donation * multiplier if include_paid_ads else 0

# Lifetime Value from Paid Donors
lifetime_retained_donors = new_paid_donors * (lifetime_retention_pct / 100)
lifetime_paid_ads_revenue = (lifetime_retained_donors * avg_lifetime_value_per_donor * lifetime_years) if include_paid_ads else 0

# Total Revenue (Excluding Current)
total_new_revenue = ad_grant_revenue + immediate_paid_ads_revenue + lifetime_paid_ads_revenue
total_growth_pct = ((total_new_revenue) / current_traffic * 100) if current_traffic else 0

# --- Donor Breakdown Section ---
st.header("🧑‍🤝‍🧑 New Donor Acquisition Breakdown")

st.markdown(f"""
**Total New Donors Acquired:**
- **From Paid Ads:** `{new_paid_donors:,.0f}`
- **Retained Donors After {lifetime_years} Years:** `{lifetime_retained_donors:,.0f}`
- **Lifetime Donor Revenue Impact:** `${lifetime_paid_ads_revenue:,.2f}`
""")

# --- Gauges Visualization ---
fig = go.Figure()

fig.add_trace(go.Indicator(
    mode="gauge+number",
    value=ad_grant_revenue,
    title={'text': f"Ad Grant Revenue ({period})"},
    domain={'x': [0, 0.33]},
    gauge={'axis': {'range': [0, total_new_revenue * 1.2]}, 'bar': {'color': "blue"}}
))

fig.add_trace(go.Indicator(
    mode="gauge+number+delta",
    value=immediate_paid_ads_revenue,
    delta={'reference': 0, 'relative': True, 'valueformat': '.1%', 'increasing': {'color': 'green'}},
    title={'text': f"Immediate Paid Ads Revenue ({period})"},
    domain={'x': [0.34, 0.66]},
    gauge={'axis': {'range': [0, total_new_revenue * 1.2]}, 'bar': {'color': "green"}}
))

fig.add_trace(go.Indicator(
    mode="gauge+number+delta",
    value=total_new_revenue,
    delta={'reference': 0, 'relative': True, 'valueformat': '.1%', 'increasing': {'color': 'purple'}},
    title={'text': f"Total Revenue Increase ({period})"},
    domain={'x': [0.67, 1]},
    gauge={'axis': {'range': [0, total_new_revenue * 1.2]}, 'bar': {'color': "purple"}}
))

st.plotly_chart(fig, use_container_width=True)

# --- Revenue Growth Summary ---
st.header("📈 Revenue Growth Summary")
st.markdown(f"""
| Revenue Source                               | {period} Revenue                         |
|----------------------------------------------|------------------------------------------|
| 🎯 Ad Grant Revenue                          | `${ad_grant_revenue:,.2f}`               |
| 🚀 Immediate Paid Ads Revenue                | `${immediate_paid_ads_revenue:,.2f}`     |
| 🌟 Lifetime Paid Ads Revenue ({lifetime_years} yrs) | `${lifetime_paid_ads_revenue:,.2f}`   |
| **🎉 Total New Revenue (Excluding Current)** | **`${total_new_revenue:,.2f}`**         |
| **📊 Revenue Increase**                      | **`{total_growth_pct:.1f}% 🚀`**         |
""")
