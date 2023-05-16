import streamlit as st
import pandas as pd
from helper import *
import datetime
import plotly.express as px


st.set_page_config(page_title = "Real-Time DS Dashboard",layout='wide',initial_sidebar_state= 'expanded')
st.title('CGR Tower')
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html = True)

data = load_data('dummy_data.csv')
#st.dataframe(data)

c1,c2 = st.columns([5,1])
with c1:
    c = st.columns(5)
    with c[0]:
        pgs = st.multiselect('Product Group', options=list(data.product_group.unique()))
    with c[1]:
        pts = st.multiselect('Product Type',options=list(data.product_type.unique()))
    with c[2]:
        franchises = st.multiselect('Franchise',options=list(data.franchise.unique()))
    with c[3]:
        countries = st.multiselect('Country',options=list(data.country.unique()))
    with c[4]:
        genders = st.multiselect('Gender',options=list(data.gender.unique()))

with c2:
    min_date = datetime.date(2022,1,1)
    max_date = datetime.date.today()

    data['date'] = pd.to_datetime(data.date, dayfirst=True)



    selected_date = st.date_input('Select Date range',(min_date,max_date))
    # st.write(min_date)
    # st.write(max_date)
    # st.write(data['date'][0])

raw_data = data.copy()

if len(pgs)!= 0:
    raw_data = data[data['product_group'].isin(pgs)]
if len(pts)!= 0:
    raw_data = data[data['product_type'].isin(pts)]
if len(franchises)!= 0:
    raw_data = data[data['franchise'].isin(franchises)]
if len(countries)!= 0:
    raw_data = data[data['country'].isin(countries)]
if len(genders)!= 0:
    raw_data = data[data['gender'].isin(genders)]

# try:
#     raw_data = data[data['date'] < selected_date[1]]
#     raw_data = data[data['date'] > selected_date[0]]
# except:
#     c2.error('Pick date')

col1, col2, col3, col4, col5, col6 = st.columns(6)

test = data.sales.sum()



#st.metric('Sales',get_total_sales(data))

value_with_image(col1,'Total Sales', get_total_sales(raw_data))
value_with_image(col2,'Total Profit', get_total_profit(raw_data))
value_with_image(col3,'Discount', get_avg_discount(raw_data))
value_with_image(col4,'Sell-Through', get_sell_through(raw_data))
value_with_image(col5,'Unit Sold', get_sales_qty(raw_data))
value_with_image(col6,'Opportunity',get_opportunity(raw_data))

df_graph = data.groupby('country').agg({'daily_targets':'sum','sales_qty':'sum'}).reset_index()

#st.area_chart(df_graph,x='country',y=['daily_targets','sales_qty'])
# opp_dataframe = opp_df(raw_data)
# st.table(opp_dataframe)

st.dataframe(opp_df(raw_data), height=300, width=2000)

st.title('Opportunity Split')

col1, col2, col3 = st.columns(3)

with col1:

    donut_graph = create_donut_graph(opp_df(raw_data), 'product_group','opp')
    st.plotly_chart(donut_graph, use_container_width=True)
    st.write(f"Opportunity by Product Group")


with col2:
    donut_graph2 = create_donut_graph(opp_df(raw_data),'country','opp')
    st.plotly_chart(donut_graph2, use_container_width=True)
    st.write(f"Opportunity by Country")

with col3:
    donut_graph3 = create_donut_graph(opp_df(raw_data),'gender','opp')
    st.plotly_chart(donut_graph3, use_container_width=True)
    st.write(f"Opportunity by Gender")



# with c1:
#     c = st.columns(5)
#     with c[0]:
#     pgs = st.multiselect('Product Group', options = list(data.))





    # filtered_data['status'] = pd.cut(
    #     filtered_data['sell_through'],
    #     bins=[0, 0.33, 0.67, 1],
    #     labels=['slow', 'medium', 'fast']
    # )

