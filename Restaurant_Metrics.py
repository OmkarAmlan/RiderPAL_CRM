import streamlit as st
import sqlite3
import pandas as pd
import altair as alt
import re

# -------------------------------
# Page Configuration and Header
# -------------------------------
st.set_page_config(
    page_title="RiderPal AI CRM",
    layout="wide"
)

st.title("RiderPal AI CRM Dashboard")
st.markdown("""
Welcome to the **RiderPal AI CRM Dashboard**. This interactive tool allows you to monitor and analyze delivery order data,
delivery routes, and key performance metrics for various restaurants. Use the sidebar to filter data by restaurant and
explore the detailed analytics below.
""")

# -------------------------------
# Sidebar: Restaurant Filter
# -------------------------------
st.sidebar.header("Restaurant Filter")
st.sidebar.markdown("""
Select a restaurant from the dropdown below to view its specific order details, route information, and performance metrics.
""")

# -------------------------------
# Database Connection and Data Fetching
# -------------------------------
con = sqlite3.connect("delivery.db")
cur = con.cursor()

def order_details_fetch():
    cur.execute("""SELECT * FROM order_details""")
    rows = cur.fetchall()
    order_details_df = pd.DataFrame(rows)
    order_details_df.columns = ['Order ID', 'Customer', 'Delivery Partner', 'Delivery Address', 
                                'Delivery Status', 'Order Time', 'Restaurant', 'Order Value']
    return order_details_df

def rider_details_fetch():
    cur.execute("""SELECT * FROM rider_details""")
    rows = cur.fetchall()
    rider_details_df = pd.DataFrame(rows)
    rider_details_df.columns = ['Delivery Partner', 'Current Location', 'Latitude', 'Longitude', 'Vehicle', 'Rating']
    return rider_details_df

def route_details_fetch():
    cur.execute("""SELECT * FROM route_details""")
    rows = cur.fetchall()
    route_details_df = pd.DataFrame(rows)
    route_details_df.columns = ['Order ID', 'Pickup Point', 'Pickup Latitude', 'Pickup Longitude', 
                                'Delivery Point', 'Delivery Latitude', 'Delivery Longitude', 
                                'Estimated Distance', 'Estimated Time']
    return route_details_df

# Fetch data from the database
order_details_df = order_details_fetch()
route_details_df = route_details_fetch()

# -------------------------------
# Clean Route Details Numeric Columns
# -------------------------------
# Extract numeric value from "Estimated Distance" (e.g., "2.5 km" -> 2.5)
route_details_df["Estimated Distance"] = (
    route_details_df["Estimated Distance"]
    .str.extract(r'([\d\.]+)')[0]
    .astype(float)
)

# Extract numeric value from "Estimated Time" (e.g., "15 minutes" -> 15)
route_details_df["Estimated Time"] = (
    route_details_df["Estimated Time"]
    .str.extract(r'(\d+)')[0]
    .astype(int)
)

# -------------------------------
# Restaurant Selection and Data Filtering
# -------------------------------
restaurants = order_details_df['Restaurant'].unique()
restaurant_choice = st.sidebar.selectbox(label="Select Restaurant", options=restaurants)
restaurants_filtered_df = order_details_df[order_details_df['Restaurant'] == restaurant_choice].reset_index(drop=True)

# Convert 'Order Time' column from string to datetime.
# Assuming the format is like "2:30 PM", we use the format '%I:%M %p'.
restaurants_filtered_df = restaurants_filtered_df.copy()  # avoid SettingWithCopyWarning
restaurants_filtered_df['Order Time'] = pd.to_datetime(
    restaurants_filtered_df['Order Time'],
    format='%I:%M %p',
    errors='coerce'
)

st.subheader(f"Order Details for **{restaurant_choice}**")
st.markdown("""
The table below shows all orders related to the selected restaurant, including customer details, delivery status, 
and order value. Expand the section to view the full data.
""")
with st.expander("View Order Details Table"):
    st.dataframe(restaurants_filtered_df)

# -------------------------------
# Calculate Order KPIs
# -------------------------------
total_orders = len(restaurants_filtered_df)
delivered_orders = restaurants_filtered_df[restaurants_filtered_df['Delivery Status'] == "Delivered"].shape[0]
orders_pending = total_orders - delivered_orders
total_revenue = restaurants_filtered_df['Order Value'].sum()
average_order_value = round(restaurants_filtered_df['Order Value'].mean(), 2)

st.subheader("Order KPIs")
st.markdown("The following key performance indicators provide an overview of the current order performance:")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(
        f"<div style='text-align: center;'>"
        f"<span style='font-size: 18px;'>Total Orders</span><br/>"
        f"<span style='font-size: 24px; font-weight: bold;'>{total_orders}</span>"
        f"</div>",
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        f"<div style='text-align: center;'>"
        f"<span style='font-size: 18px;'>Delivered Orders</span><br/>"
        f"<span style='font-size: 24px; font-weight: bold; color: green;'>{delivered_orders}</span>"
        f"</div>",
        unsafe_allow_html=True
    )
with col3:
    st.markdown(
        f"<div style='text-align: center;'>"
        f"<span style='font-size: 18px;'>Pending Orders</span><br/>"
        f"<span style='font-size: 24px; font-weight: bold; color: red;'>{orders_pending}</span>"
        f"</div>",
        unsafe_allow_html=True
    )
with col4:
    st.markdown(
        f"<div style='text-align: center;'>"
        f"<span style='font-size: 18px;'>Total Revenue (USD)</span><br/>"
        f"<span style='font-size: 24px; font-weight: bold; color: green;'>USD {total_revenue:.2f}</span>"
        f"</div>",
        unsafe_allow_html=True
    )
with col5:
    st.markdown(
        f"<div style='text-align: center;'>"
        f"<span style='font-size: 18px;'> AOV (USD)</span><br/>"
        f"<span style='font-size: 24px; font-weight: bold; color: green;'>USD {average_order_value}</span>"
        f"</div>",
        unsafe_allow_html=True
    )

# -------------------------------
# Order Value Analysis: Bar Chart
# -------------------------------
st.subheader("Order Value Analysis")
st.markdown("""
This bar chart represents the **Order Value** for each **Order ID**. Hover over the bars to see detailed information 
about each order's value.
""")
chart = alt.Chart(restaurants_filtered_df).mark_bar().encode(
    x=alt.X('Order ID:N', title='Order ID'),
    y=alt.Y('Order Value:Q', title='Order Value (USD)'),
    tooltip=['Order ID', 'Order Value']
).properties(
    title="Order Value per Order ID"
)
st.altair_chart(chart, use_container_width=True)

# -------------------------------
# Delivery Route Details
# -------------------------------
# Merge the route details with the filtered order details using the 'Order ID'
routes_filtered_df = route_details_df.merge(restaurants_filtered_df, on="Order ID")

st.subheader("Delivery Route Details")
st.markdown("""
The table below provides detailed route information for each order. It includes pickup and delivery points, 
the estimated distance (in km), and estimated delivery time (in minutes).
""")
with st.expander("View Route Details Table"):
    st.dataframe(routes_filtered_df)

# -------------------------------
# Delivery Route KPIs
# -------------------------------
st.subheader("Delivery Route KPIs")
st.markdown("Below are some key performance indicators for the delivery routes:")

# Calculate Delivery Route KPIs
total_routes = routes_filtered_df.shape[0]
avg_distance = round(routes_filtered_df['Estimated Distance'].mean(), 2) if total_routes > 0 else 0
avg_eta = round(routes_filtered_df['Estimated Time'].mean(), 2) if total_routes > 0 else 0
longest_distance = round(routes_filtered_df['Estimated Distance'].max(), 2) if total_routes > 0 else 0
shortest_eta = routes_filtered_df['Estimated Time'].min() if total_routes > 0 else 0

col1_route, col2_route, col3_route, col4_route, col5_route = st.columns(5)
with col1_route:
    st.markdown(
        f"<div style='text-align: center;'>"
        f"<span style='font-size: 18px;'>Total Routes</span><br/>"
        f"<span style='font-size: 24px; font-weight: bold;'>{total_routes}</span>"
        f"</div>",
        unsafe_allow_html=True
    )
with col2_route:
    st.markdown(
        f"<div style='text-align: center;'>"
        f"<span style='font-size: 18px;'>Avg. Distance (km)</span><br/>"
        f"<span style='font-size: 24px; font-weight: bold; color: green;'>{avg_distance}</span>"
        f"</div>",
        unsafe_allow_html=True
    )
with col3_route:
    st.markdown(
        f"<div style='text-align: center;'>"
        f"<span style='font-size: 18px;'>Avg. ETA (min)</span><br/>"
        f"<span style='font-size: 24px; font-weight: bold; color: green;'>{avg_eta}</span>"
        f"</div>",
        unsafe_allow_html=True
    )
with col4_route:
    st.markdown(
        f"<div style='text-align: center;'>"
        f"<span style='font-size: 18px;'>Longest Distance (km)</span><br/>"
        f"<span style='font-size: 24px; font-weight: bold; color: red;'>{longest_distance}</span>"
        f"</div>",
        unsafe_allow_html=True
    )
with col5_route:
    st.markdown(
        f"<div style='text-align: center;'>"
        f"<span style='font-size: 18px;'>Shortest ETA (min)</span><br/>"
        f"<span style='font-size: 24px; font-weight: bold; color: green;'>{shortest_eta}</span>"
        f"</div>",
        unsafe_allow_html=True
    )

# -------------------------------
# Order Frequency Analysis (Optional)
# -------------------------------
st.subheader("Order Frequency Analysis")
# Now that 'Order Time' is in datetime format, create a new column for 30-minute intervals.
restaurants_filtered_df['Time Interval'] = restaurants_filtered_df['Order Time'].dt.floor('30T')

time_chart = alt.Chart(restaurants_filtered_df).mark_line(point=True).encode(
    x=alt.X('Time Interval:T', title='Time Interval', timeUnit='hoursminutes'),
    y=alt.Y('count(Order ID):Q', title='Order Count'),
    tooltip=['Time Interval', 'count(Order ID)']
).properties(
    title="Order Count per 30-Minute Interval"
)


st.markdown("""
The histogram below shows the frequency of orders placed within each 30-minute interval. This analysis 
can help identify peak ordering times.
""")
st.altair_chart(time_chart, use_container_width=True)

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown("""
### End of Dashboard

Thank you for using the RiderPal AI CRM Dashboard. If you have any questions or need further assistance, 
please contact the system administrator.
""")
