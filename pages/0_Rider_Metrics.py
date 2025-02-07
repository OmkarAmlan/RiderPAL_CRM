import streamlit as st
import sqlite3
import pandas as pd
import altair as alt
import re

# -------------------------------
# Page Configuration and Header
# -------------------------------
st.set_page_config(page_title="Rider Metrics", layout="wide")
st.title("Rider Metrics Dashboard")
st.markdown("""
This page displays performance metrics for each rider. Use the sidebar to select a rider and view detailed KPIs such as 
order counts, revenue, and delivery route performance.
""")

# -------------------------------
# Database Connection and Data Fetching
# -------------------------------
con = sqlite3.connect("delivery.db")
cur = con.cursor()

def rider_details_fetch():
    cur.execute("SELECT * FROM rider_details")
    rows = cur.fetchall()
    df = pd.DataFrame(rows)
    df.columns = ['Delivery Partner', 'Current Location', 'Latitude', 'Longitude', 'Vehicle', 'Rating']
    return df

def order_details_fetch():
    cur.execute("SELECT * FROM order_details")
    rows = cur.fetchall()
    df = pd.DataFrame(rows)
    df.columns = ['Order ID', 'Customer', 'Delivery Partner', 'Delivery Address', 
                  'Delivery Status', 'Order Time', 'Restaurant', 'Order Value']
    return df

def route_details_fetch():
    cur.execute("SELECT * FROM route_details")
    rows = cur.fetchall()
    df = pd.DataFrame(rows)
    df.columns = ['Order ID', 'Pickup Point', 'Pickup Latitude', 'Pickup Longitude', 
                  'Delivery Point', 'Delivery Latitude', 'Delivery Longitude', 
                  'Estimated Distance', 'Estimated Time']
    # Clean numeric columns:
    # Remove any non-numeric characters from Estimated Distance (e.g., "2.5 km" -> 2.5)
    df["Estimated Distance"] = df["Estimated Distance"].str.extract(r'([\d\.]+)')[0].astype(float)
    # Remove any non-numeric characters from Estimated Time (e.g., "15 minutes" -> 15)
    df["Estimated Time"] = df["Estimated Time"].str.extract(r'(\d+)')[0].astype(int)
    return df

# Fetch data from the database
rider_details_df = rider_details_fetch()
order_details_df = order_details_fetch()
route_details_df = route_details_fetch()

# -------------------------------
# Sidebar: Select Rider
# -------------------------------
riders = rider_details_df["Delivery Partner"].unique()
selected_rider = st.sidebar.selectbox("Select Rider", riders)

# -------------------------------
# Display Rider Basic Information
# -------------------------------
rider_info = rider_details_df[rider_details_df["Delivery Partner"] == selected_rider].iloc[0]
st.subheader(f"Metrics for Rider: **{selected_rider}**")
st.markdown(f"""
**Current Location:** {rider_info["Current Location"]}  
**Vehicle:** {rider_info["Vehicle"]}  
**Rating:** {rider_info["Rating"]}
""")

# -------------------------------
# Rider Orders and KPI Calculations
# -------------------------------
# Filter the orders assigned to the selected rider.
rider_orders_df = order_details_df[order_details_df["Delivery Partner"] == selected_rider].reset_index(drop=True)

# Calculate basic order KPIs.
total_orders = len(rider_orders_df)
delivered_orders = rider_orders_df[rider_orders_df["Delivery Status"] == "Delivered"].shape[0]
pending_orders = total_orders - delivered_orders

# Calculate revenue and average order value based on delivered orders.
total_revenue = rider_orders_df[rider_orders_df["Delivery Status"] == "Delivered"]["Order Value"].sum()
avg_order_value = round(
    rider_orders_df[rider_orders_df["Delivery Status"] == "Delivered"]["Order Value"].mean(), 2
) if delivered_orders > 0 else 0

# Merge with route details to calculate distance and time KPIs.
rider_routes = pd.merge(rider_orders_df, route_details_df, on="Order ID", how="left")
total_distance = rider_routes["Estimated Distance"].sum()
avg_distance = round(rider_routes["Estimated Distance"].mean(), 2) if total_orders > 0 else 0
total_estimated_time = rider_routes["Estimated Time"].sum()
avg_estimated_time = round(rider_routes["Estimated Time"].mean(), 2) if total_orders > 0 else 0

# -------------------------------
# Display KPI Metrics
# -------------------------------
st.subheader("Performance KPIs")

# Use columns to display each KPI in a neat layout.
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(
        f"<div style='text-align: center;'>"
        f"<span style='font-size: 16px;'>Total Orders</span><br/>"
        f"<span style='font-size: 20px; font-weight: bold;'>{total_orders}</span>"
        f"</div>",
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        f"<div style='text-align: center;'>"
        f"<span style='font-size: 16px;'>Delivered Orders</span><br/>"
        f"<span style='font-size: 20px; font-weight: bold; color: green;'>{delivered_orders}</span>"
        f"</div>",
        unsafe_allow_html=True
    )
with col3:
    st.markdown(
        f"<div style='text-align: center;'>"
        f"<span style='font-size: 16px;'>Pending Orders</span><br/>"
        f"<span style='font-size: 20px; font-weight: bold; color: red;'>{pending_orders}</span>"
        f"</div>",
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"<div style='text-align: center;'>"
        f"<span style='font-size: 16px;'>Total Distance (km)</span><br/>"
        f"<span style='font-size: 20px; font-weight: bold; color: green;'>{total_distance:.2f}</span>"
        f"</div>",
        unsafe_allow_html=True
    )
with col5:
    st.markdown(
        f"<div style='text-align: center;'>"
        f"<span style='font-size: 16px;'>Avg Distance (km)</span><br/>"
        f"<span style='font-size: 20px; font-weight: bold; color: green;'>{avg_distance:.2f}</span>"
        f"</div>",
        unsafe_allow_html=True
    )

st.subheader("Delivery Time Metrics")
col_time1, col_time2 = st.columns(2)
with col_time1:
    st.markdown(
        f"<div style='text-align: center;'>"
        f"<span style='font-size: 16px;'>Total Estimated Time (min)</span><br/>"
        f"<span style='font-size: 20px; font-weight: bold;'>{total_estimated_time}</span>"
        f"</div>",
        unsafe_allow_html=True
    )
with col_time2:
    st.markdown(
        f"<div style='text-align: center;'>"
        f"<span style='font-size: 16px;'>Avg Estimated Time (min)</span><br/>"
        f"<span style='font-size: 20px; font-weight: bold;'>{avg_estimated_time}</span>"
        f"</div>",
        unsafe_allow_html=True
    )

# -------------------------------
# Detailed Tables (Optional)
# -------------------------------
st.subheader("Order Details")
with st.expander("View Rider's Orders"):
    st.dataframe(rider_orders_df)

st.subheader("Route Details")
with st.expander("View Rider's Route Details"):
    st.dataframe(rider_routes)

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown("""
### End of Rider Metrics

Thank you for reviewing the rider performance metrics.
""")
