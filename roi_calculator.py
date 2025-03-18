import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Advanced ROI Calculator", layout="wide")
st.title("🚀 Advanced ROI Calculator")

# Monthly or Annual Toggle
period = st.radio("Choose Revenue View:", ["Monthly", "Annual"])

multiplier = 12 if period == "Annual" else 1

# Three columns setup
col1, col2, col3 = st.columns(3)

# Current Metrics
with col1:
    st.header("📍 Current Metrics")
    current_traffic = st.number_input('Monthly Traffic', min_value=0, value=10000, step=100)
    current_conversion_rate = st.number_input('Current Conversion Rate (%)', 0.1, 100.0, 5.0, 0.1)
    avg_donation = st.number_input('Average Donation ($)', 1.0, value=50.0, step=1.0)

# Google Ad Grant Metrics
with col2:
    st.header("🎯 With Google Ad Grant")
    ad_grant_traffic_pct = st.slider('Traffic Increase via Ad Grant (%)', 0, 500, 100, 10)
    ad_grant_conversion_rate = st.slider('Conversion Rate w/ Ad Grant (%)', 0.1, 100.0, 5.0, 0.1)

# Paid Ads & Lifetime Value
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

# --- Clear Paid Ads Calculations ---
estimated_clicks = paid_ads_budget / avg_cpc
new_paid_donors = estimated_clicks * (paid_ads_conversion_rate / 100)

immediate_paid_ads_revenue = new_paid_donors * paid_avg_donation

lifetime_paid_ads_revenue = (new_paid_donors * (lifetime_retention_pct / 100) *
                             avg_lifetime_value_per_donor * lifetime_years)

total_paid_ads_revenue = immediate_paid_ads_revenue + lifetime_paid_ads_revenue

# Now include clearly in summary:
st.header("📈 Revenue Growth Summary")
st.markdown(f"""
| Revenue Source                             | {period} Revenue                         |
|--------------------------------------------|------------------------------------------|
| 📍 Current Revenue                         | `${current_revenue:,.2f}`                |
| 🎯 Ad Grant Revenue                        | `${ad_grant_revenue:,.2f}`               |
| 🚀 Immediate Paid Ads Revenue              | `${immediate_paid_ads_revenue:,.2f}`     |
| 🌟 Lifetime Paid Ads Revenue ({lifetime_years} yrs) | `${lifetime_paid_ads_revenue:,.2f}`        |
| **🎉 Total Projected Revenue**             | **`${current_revenue + ad_grant_revenue + total_paid_ads_revenue:,.2f}`** |
| **📊 Revenue Increase**                    | **`{((current_revenue + ad_grant_revenue + total_paid_ads_revenue - current_revenue) / current_revenue * 100):.1f}% 🚀`** |
""")
