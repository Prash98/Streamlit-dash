import pandas as pd
import numpy as np
from numerize import numerize
import streamlit as st
import plotly.express as px

@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

def value_with_image(col,header,value):
    with col:
        st.metric(header,value)
    
def get_total_sales(df):
    try:
        value = numerize.numerize(df.sales.sum())
        return value
    except:
        return 0
    
def get_total_profit(df):
    try:
        profit = numerize.numerize(df.profit.sum())
        return profit
    except:
        return 0
    
def get_avg_discount(df):
    try:
        discount = int(df.discount.mean()*100)
        return discount
    except:
        return 0
    
def get_sell_through(df):
    try:
        r2 = df.groupby(['product']).agg({'sales_qty':'sum','daily_targets':'sum'}).reset_index()
        r2['sell_through'] = (r2['sales_qty']) /r2['daily_targets']
        ST = int(r2.sell_through.mean() * 100)
        return ST
    except:
        return 0
    
def get_opportunity(df):
    try:
        r1 = df.groupby(['product']).agg(({'sales_qty':'sum','daily_targets':'sum','rrp':'mean'}))
        r1['opp'] = ((r1['daily_targets'])- (r1['sales_qty'])) * (r1['rrp']) 
        r1['opp'] = r1.apply(lambda x: 0 if x['opp'] < 0 else x['opp'],axis=1)  
        #st.dataframe(r1)
        OPP = numerize.numerize(r1.opp.sum())
        return OPP
    except:
        return 0
    
def opp_df(df):
    try:
        r1 = df.groupby(['product','product_group','gender','country']).agg(({'sales_qty':'sum','daily_targets':'sum','rrp':'mean'}))
        r1['opp'] = ((r1['daily_targets'])- (r1['sales_qty'])) * (r1['rrp']) 
        r1['opp'] = r1.apply(lambda x: 0 if x['opp'] < 0 else x['opp'],axis=1) 
        #st.dataframe(r1)
        return r1
    except:
        return 0

    
def get_sales_qty(df):
    try:
        sales_qty = numerize.numerize(int(df.sales_qty.sum()))
        return sales_qty
    except:
        return 0
    

def create_donut_graph(df, group_var, sum_var):
    grouped_data = df.groupby(group_var)[sum_var].sum().reset_index()
    fig = px.pie(grouped_data, values=sum_var, names=group_var, hole=0.4)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=False)
    return fig



    
