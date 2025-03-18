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
    paid_ads_conversion_rate = st.slider('Paid Ads Conversion Rate (%)', 0.1, 100.0, 2.0, 0.1)
    lifetime_lead_pct = st.slider('Leads Captured for Lifetime Value (%)', 0.1, 100.0, 10.0, 0.1)
    lifetime_value_amount = st.number_input('Avg. Lifetime Value per Lead ($)', 1.0, 5000.0, 500.0, 10.0)
    lifetime_years = st.slider('Lifetime Period (Years)', 1, 10, 3, 1)

# Calculations
ad_grant_traffic = current_traffic * (1 + ad_grant_traffic_pct / 100)
current_revenue = current_traffic * (current_conversion_rate / 100) * avg_donation * multiplier
ad_grant_revenue = ad_grant_traffic * (ad_grant_conversion_rate / 100) * avg_donation * multiplier
paid_ads_revenue = ad_grant_traffic * (paid_ads_conversion_rate / 100) * avg_donation * multiplier
lifetime_leads = ad_grant_traffic * (lifetime_lead_pct / 100)
lifetime_value_revenue = lifetime_leads * lifetime_value_amount * lifetime_years

total_projected_revenue = ad_grant_revenue + paid_ads_revenue + lifetime_value_revenue
total_growth_pct = ((total_projected_revenue - current_revenue) / current_revenue * 100) if current_revenue else 0

# Gauges Visualization
fig = go.Figure()

fig.add_trace(go.Indicator(mode="gauge+number", value=current_revenue, title={'text': f"Current Revenue ({period})"}, domain={'x': [0, 0.33]}, gauge={'axis': {'range': [0, total_projected_revenue*1.2]}, 'bar': {'color': "gray"}}))
fig.add_trace(go.Indicator(mode="gauge+number+delta", value=ad_grant_revenue, delta={'reference': current_revenue, 'relative': True, 'valueformat': '.1%', 'increasing': {'color': 'blue'}}, title={'text': f"Ad Grant Revenue ({period})"}, domain={'x': [0.34, 0.66]}, gauge={'axis': {'range': [0, total_projected_revenue*1.2]}, 'bar': {'color': "blue"}}))
fig.add_trace(go.Indicator(mode="gauge+number+delta", value=total_projected_revenue, delta={'reference': current_revenue, 'relative': True, 'valueformat': '.1%', 'increasing': {'color': 'green'}}, title={'text': f"Total Revenue ({period})"}, domain={'x': [0.67, 1]}, gauge={'axis': {'range': [0, total_projected_revenue*1.2]}, 'bar': {'color': "green"}}))

st.plotly_chart(fig, use_container_width=True)

# Revenue Growth Summary
st.header("📈 Revenue Growth Summary")
st.markdown(f"""
| Revenue Source                          | {period} Revenue                     |
|-----------------------------------------|--------------------------------------|
| 📍 Current Revenue                      | `${current_revenue:,.2f}`            |
| 🎯 Ad Grant Revenue                     | `${ad_grant_revenue:,.2f}`           |
| 🚀 Paid Ads Revenue                     | `${paid_ads_revenue:,.2f}`           |
| 🌟 Lifetime Value Revenue ({lifetime_years} yrs) | `${lifetime_value_revenue:,.2f}`   |
| **🎉 Total Projected Revenue**          | **`${total_projected_revenue:,.2f}`** |
| **📊 Revenue Increase**                 | **`{total_growth_pct:.1f}% 🚀`**      |
""")

# Streamlined Impact Section
impact_dict = {"🍽 Hunger Relief":"Meals Provided","🎓 Education":"Scholarships Awarded","🏥 Healthcare":"Patients Served","🐾 Animal Welfare":"Animals Rescued","🌎 Environment":"Trees Planted","💦 Clean Water":"Wells Built","🏠 Homelessness":"Beds Provided","👶 Child Welfare":"Children Supported","🎭 Arts & Museums":"Visits Enabled","📚 Libraries/Literacy":"Books Distributed","🏃 Youth & Sports":"Kids Sponsored","🛠 Job Training":"Individuals Trained","🏳️‍🌈 Equality & Inclusion":"Individuals Supported","🦽 Disabilities Support":"Mobility Devices Provided","🛡 Human Rights":"Campaigns Funded","🛐 Faith-based":"Communities Supported","🚨 Disaster Relief":"Emergency Kits Provided","⚖️ Legal Services":"Cases Supported"}

st.header("💡 Community Impact Forecast")
selected_vertical = st.selectbox("Choose your Nonprofit Vertical:", list(impact_dict.keys()))
impact_per_dollar = st.number_input(f"How many {impact_dict[selected_vertical]} per $1 donated?", 0.01, 100.0, 1.0, 0.1)
total_impact = total_projected_revenue * impact_per_dollar

st.success(f"By investing in marketing, you can provide **{int(total_impact):,} {impact_dict[selected_vertical]}** per {period.lower()} 🚀")
