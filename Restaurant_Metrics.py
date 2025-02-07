import streamlit as st
import sqlite3
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="RiderPal AI CRM",
    layout="wide"
)

con=sqlite3.connect("delivery.db")
cur=con.cursor()
def order_details_fetch():
    cur.execute("""SELECT * FROM order_details""")
    rows=cur.fetchall()
    order_detials_df=pd.DataFrame(rows)
    order_detials_df.columns=['Order ID', 'Customer', 'Delivery Partner', 'Delivery Address', 'Delivery Status', 'Order Time', 'Restaurant', 'Order Value' ]
    return order_detials_df

def rider_details_fetch():
    cur.execute("""SELECT * FROM rider_details""")
    rows=cur.fetchall()
    rider_details_df=pd.DataFrame(rows)
    rider_details_df.columns=['Delivery Partner','Current Location','Latitude','Longitude','Vehicle','Rating']
    return rider_details_df

def route_details_fetch():
    cur.execute("""SELECT * FROM route_details""")
    rows=cur.fetchall()
    route_details_df=pd.DataFrame(rows)
    route_details_df.columns=['Order ID','Pickup Point','Pickup Latitude','Pickup Longitude','Delivery Point','Delivery Latitude','Delivery Longitude','Estimated Distance','Estimated Time']
    return route_details_df

order_details_df = order_details_fetch()
route_details_df = route_details_fetch()
restaurants = order_details_df['Restaurant'].unique()

restaurant_choice = st.sidebar.selectbox(label="Select Restaurant", options=restaurants)
restaurants_filtered_df = order_details_df[order_details_df['Restaurant'] == restaurant_choice].reset_index()
routes_filtered_df = route_details_df.merge(restaurants_filtered_df, on="Order ID")

st.write(restaurants_filtered_df)

# Plotting bar chart using Altair
st.subheader("Order Value per Order ID")
chart = alt.Chart(restaurants_filtered_df).mark_bar().encode(
    x=alt.X('Order ID:N', title='Order ID'),
    y=alt.Y('Order Value:Q', title='Order Value'),
    tooltip=['Order ID', 'Order Value']
).properties(
    title="Order Value per Order ID"
)

st.altair_chart(chart, use_container_width=True)
orders_pending=0
for i in range(len(restaurants_filtered_df)):
    if(restaurants_filtered_df['Delivery Status'][i]!="Delivered"):
        orders_pending+=1
        
average_order_value=round(sum(restaurants_filtered_df['Order Value'])/len(restaurants_filtered_df),2)
col1,col2=st.columns(2)
with col1:
    st.warning("Orders Pending: " + str(orders_pending))
with col2:
    st.success("Average Order Value: USD" + str(average_order_value))
    
    
st.write(routes_filtered_df)
# # Creating histogram for time vs order count
# st.subheader("Order Count per Time Interval")
# if restaurants_filtered_df['Order Time'].isna().sum() == 0:
#     restaurants_filtered_df['Time Interval'] = restaurants_filtered_df['Order Time'].dt.floor('30T')

#     time_chart = alt.Chart(restaurants_filtered_df).mark_bar().encode(
#         x=alt.X('Time Interval:T', title='Time Interval', timeUnit='hoursminutes'),
#         y=alt.Y('count(Order ID):Q', title='Order Count'),
#         tooltip=['Time Interval', 'count(Order ID)']
#     ).properties(
#         title="Order Count per 30-Minute Interval"
#     )

#     st.altair_chart(time_chart, use_container_width=True)
# else:
#     st.error("Error: Some 'Order Time' values could not be converted. Check data format.")
