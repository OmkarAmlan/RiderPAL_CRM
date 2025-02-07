import streamlit as st
import sqlite3
import pandas as pd
import altair as alt
import re

# -------------------------------
# Page Configuration and Header
# -------------------------------
st.set_page_config(page_title="Key Performance Index: Safety & Compliance", layout="wide")
st.title("Key Performance Index: Safety & Compliance")
st.markdown("""
This page provides an overview of safety and compliance performance metrics in our delivery operations. In the delivery context, key KPIs for safety and compliance include:

- **On-Time Delivery Rate:** Ratio of delivered orders to total orders.
- **Speed Compliance Rate:** Percentage of orders where the rider’s average speed is within the safe limit.
- **Incident Rate:** Number of safety incidents (accidents or complaints) relative to total orders.
- **Safety Training / Audit Compliance:** Percentage of riders who have completed required safety training or passed audits.

*Note:* Some KPIs are derived directly from our available data, while others are placeholders (in cases where additional incident or driver behavior data is not available).  
""")

# -------------------------------
# Database Connection and Data Fetching
# -------------------------------
con = sqlite3.connect("delivery.db")
cur = con.cursor()

def order_details_fetch():
    cur.execute("""SELECT * FROM order_details""")
    rows = cur.fetchall()
    df = pd.DataFrame(rows)
    df.columns = ['Order ID', 'Customer', 'Delivery Partner', 'Delivery Address', 
                  'Delivery Status', 'Order Time', 'Restaurant', 'Order Value']
    return df

def rider_details_fetch():
    cur.execute("SELECT * FROM rider_details")
    rows = cur.fetchall()
    df = pd.DataFrame(rows)
    df.columns = ['Delivery Partner', 'Current Location', 'Latitude', 'Longitude', 'Vehicle', 'Rating']

    # Ensure 'Rating' is properly extracted as a float
    df["Rating"] = df["Rating"].astype(str)  # Convert to string first
    # Extract the first valid float number from 'Rating' using regex
    df["Rating"] = df["Rating"].str.extract(r'(\d+\.\d+)')[0].astype(float)
    return df

def route_details_fetch():
    cur.execute("SELECT * FROM route_details")
    rows = cur.fetchall()
    df = pd.DataFrame(rows)
    df.columns = ['Order ID', 'Pickup Point', 'Pickup Latitude', 'Pickup Longitude', 
                  'Delivery Point', 'Delivery Latitude', 'Delivery Longitude', 
                  'Estimated Distance', 'Estimated Time']
    # Clean numeric columns:
    df["Estimated Distance"] = df["Estimated Distance"].str.extract(r'([\d\.]+)')[0].astype(float)
    df["Estimated Time"] = df["Estimated Time"].str.extract(r'(\d+)')[0].astype(int)
    return df

# Fetch data
order_details_df = order_details_fetch()
rider_details_df = rider_details_fetch()
route_details_df = route_details_fetch()

# -------------------------------
# Compute Safety & Compliance KPIs
# -------------------------------

# On-Time Delivery Rate: (Delivered Orders / Total Orders) * 100
total_orders = len(order_details_df)
delivered_orders = order_details_df[order_details_df["Delivery Status"] == "Delivered"].shape[0]
delivery_compliance_rate = round((delivered_orders / total_orders) * 100, 2) if total_orders else 0

# Speed Compliance Rate:
# Calculate the average speed for each order (assuming Estimated Time is in minutes and Estimated Distance in km)
# Average Speed (km/h) = (Estimated Distance * 60) / Estimated Time
speed_limit = 50  # Define the safe speed limit in km/h
route_details_df["avg_speed"] = route_details_df["Estimated Distance"] * 60 / route_details_df["Estimated Time"]
route_details_df["Speed_Compliant"] = route_details_df["avg_speed"] <= speed_limit
speed_compliant_orders = route_details_df["Speed_Compliant"].sum()
total_orders_route = len(route_details_df)
speed_compliance_rate = round((speed_compliant_orders / total_orders_route) * 100, 2) if total_orders_route else 0

# Incident Rate: Placeholder metric (for example, zero incidents)
incident_rate = 0

# Safety Training / Audit Compliance: Placeholder value (assume 100% for demonstration)
safety_training_completion = "100%"

# -------------------------------
# Helper Function to Create KPI Boxes
# -------------------------------
def kpi_box(title, value, value_color="black"):
    return f"""
    <div style="
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 10px;
        margin: 5px;
        text-align: center;
        ">
        <span style="font-size: 16px;">{title}</span><br/>
        <span style="font-size: 20px; font-weight: bold; color: {value_color};">{value}</span>
    </div>
    """

# -------------------------------
# Display Safety & Compliance KPIs
# -------------------------------
st.subheader("Safety & Compliance KPIs")

# Create columns to display the KPI boxes
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(kpi_box("On-Time Delivery Rate", f"{delivery_compliance_rate}%", "green"), unsafe_allow_html=True)
with col2:
    st.markdown(kpi_box("Speed Compliance Rate", f"{speed_compliance_rate}%", "green"), unsafe_allow_html=True)
with col3:
    st.markdown(kpi_box("Incident Rate", f"{incident_rate} / {total_orders} orders", "red"), unsafe_allow_html=True)
with col4:
    st.markdown(kpi_box("Safety Training Compliance", safety_training_completion, "green"), unsafe_allow_html=True)

# -------------------------------
# Additional Analysis (Optional)
# -------------------------------
st.markdown("""
### Additional Analysis

While the above KPIs provide a snapshot of our delivery safety and compliance performance, further analysis can include:
- **Detailed Incident Reporting:** Tracking and categorizing incidents to identify common issues.
- **Driver Behavior Analysis:** Incorporating telematics data (e.g., harsh braking, acceleration) for a deeper insight into driver safety.
- **Regular Safety Audits:** Ensuring drivers and vehicles meet safety and regulatory standards.
- **Comparative Analysis:** Benchmarking performance across regions or time periods.

For more on safety KPIs in the delivery industry, resources such as [Simply Fleet’s KPI insights](&#8203;:contentReference[oaicite:0]{index=0}) and [Onfleet’s delivery performance metrics](&#8203;:contentReference[oaicite:1]{index=1}) offer valuable perspectives.
""")

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown("""
### End of Safety & Compliance KPIs

Thank you for reviewing our key performance indices. For further details or inquiries, please contact the system administrator.
""")
