import streamlit as st
import pandas as pd
from helper import *
import datetime
import plotly.express as px

import base64
from PIL import Image
import io



st.set_page_config(page_title = "Real-Time DS Dashboard",layout='wide',initial_sidebar_state= 'expanded')
st.title('CGR Tower')
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html = True)

data = load_data('dummy_data.csv')
#st.dataframe(data)

c1= st.columns(1)
with c1[0]:
    c = st.columns(6)
    with c[0]:
        st.markdown(f'<div class=my-header>Product Group</div>', unsafe_allow_html=True)
        pgs = st.multiselect("", options=list(data.product_group.unique()))
    with c[1]:
        st.markdown(f'<div class=my-header>Product Group</div>', unsafe_allow_html=True)
        pts = st.multiselect('',options=list(data.product_type.unique()))
    with c[2]:
        st.markdown(f'<div class=my-header>Product Group</div>', unsafe_allow_html=True)
        franchises = st.multiselect('',options=list(data.franchise.unique()))
    with c[3]:
        st.markdown(f'<div class=my-header>Product Group</div>', unsafe_allow_html=True)
        countries = st.multiselect('',options=list(data.country.unique()))
    with c[4]:
        st.markdown(f'<div class=my-header>Product Group</div>', unsafe_allow_html=True)
        genders = st.multiselect('',options=list(data.gender.unique()))
    with c[5]:
        min_date = datetime.date(2022,1,1)
        max_date = datetime.date.today()

        data['date'] = pd.to_datetime(data.date, dayfirst=True)
        data['date'] = data['date'].dt.date


        st.markdown(f'<div class=my-header>Select Date range</div>', unsafe_allow_html=True)
        selected_date = st.date_input('',(min_date,max_date))
    # st.write(min_date)
    # st.write(max_date)
    # st.write(data['date'][0])

raw_data = data.copy()

if len(pgs)!= 0:
    raw_data = raw_data[raw_data['product_group'].isin(pgs)]
if len(pts)!= 0:
    raw_data = raw_data[raw_data['product_type'].isin(pts)]
if len(franchises)!= 0:
    raw_data = raw_data[raw_data['franchise'].isin(franchises)]
if len(countries)!= 0:
    raw_data = raw_data[raw_data['country'].isin(countries)]
if len(genders)!= 0:
    raw_data = raw_data[raw_data['gender'].isin(genders)]

try:
    raw_data = raw_data[raw_data['date'] <= selected_date[1]]
    raw_data = raw_data[raw_data['date'] >= selected_date[0]]
except Exception as e:
    c1.error('Pick end date')

col1, col2, col3, col4, col5, col6 = st.columns(6)

#st.metric('Sales',get_total_sales(data))

value_with_image(col1,'Total Sales', get_total_sales(raw_data))
value_with_image(col2,'Total Profit', get_total_profit(raw_data))
value_with_image(col3,'Discount', get_avg_discount(raw_data))
value_with_image(col4,'Sell-Through', get_sell_through(raw_data))
value_with_image(col5,'Unit Sold', get_sales_qty(raw_data))
value_with_image(col6,'Opportunity',get_opportunity(raw_data))

col7, col8, col9 = st.columns(3)
value_status(col7,'Slow Status',sell_through_status(opp_df(raw_data)),'SLOW')
value_status(col8,'Medium Status',sell_through_status(opp_df(raw_data)),'MEDIUM')
value_status(col9,'Fast Status',sell_through_status(opp_df(raw_data)),'FAST')

df_graph = data.groupby('country').agg({'daily_targets':'sum','sales_qty':'sum'}).reset_index()

image_path = "image_1.png"

###

# Load the image using PIL or any other library
image = Image.open(image_path)

# Convert the image to bytes
image_bytes = io.BytesIO()
image.save(image_bytes, format='PNG')
image_bytes = image_bytes.getvalue()

# Encode the image bytes as base64
base64_image = base64.b64encode(image_bytes).decode()

# Display the image centered
# st.markdown(
#     f'<div style="display: flex; justify-content: center;"><img src="data:image/png;base64,{base64_image}" width="1000"></div>',
#     unsafe_allow_html=True
# )


####


#st.image(image_path,use_column_width=True, caption='Breakdown')


#st.area_chart(df_graph,x='country',y=['daily_targets','sales_qty'])
# opp_dataframe = opp_df(raw_data)
# st.table(opp_dataframe)

# grouped_data = raw_data.groupby(['product_group', 'country']).sales_qty.sum().reset_index()
# fig = px.treemap(grouped_data, path=['product_group', 'country'], values='sales_qty')
# st.plotly_chart(fig)


#st.dataframe(opp_df(raw_data), height=300, width=2000)


df_temp = sell_through_status(opp_df(raw_data))

new_columns = {
    'product': 'PRODUCT',
    'product_group': 'PRODUCT GROUP',
    'gender': 'GENDER',
    'country': 'COUNTRY',
    'sales_qty': 'SALES QTY',
    'daily_targets':  'DAILY TARGET',
    'rrp': 'RRP',
    'opp': 'OPPORTUNITY',
    'sell_through': 'SELL THROUGH',
    'status': 'STATUS'
}
df_temp = df_temp.rename(columns=new_columns)
df_temp['OPPORTUNITY'] = df_temp.apply(lambda x: round(x['OPPORTUNITY']), axis=1)
df_temp['SELL THROUGH'] = df_temp.apply(lambda x: round(x['SELL THROUGH']), axis=1)
df_temp['RRP'] = df_temp.apply(lambda x: round(x['RRP']), axis=1)
df_temp = df_temp[['PRODUCT','STATUS','OPPORTUNITY','SELL THROUGH','SALES QTY','RRP']]
#styled_df = df_temp.applymap(color_cells)

styled_df = df_temp.style.applymap(color_cells)
html = styled_df.to_html(escape=False, index=False)
styled_table = f'<div style="display: flex; justify-content: center; height: 300px; overflow: auto">{html}</div>'
st.markdown(styled_table, unsafe_allow_html=True)


#st.table(styled_df) #, height=300, width=2000

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


# df_temp = sell_through_status(raw_data)
# df_temp = df_temp.style.applymap(color_violation)
# st.dataframe(df_temp)




# with c1:
#     c = st.columns(5)
#     with c[0]:
#     pgs = st.multiselect('Product Group', options = list(data.))





    # filtered_data['status'] = pd.cut(
    #     filtered_data['sell_through'],
    #     bins=[0, 0.33, 0.67, 1],
    #     labels=['slow', 'medium', 'fast']
    # )

