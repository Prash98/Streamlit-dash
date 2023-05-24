import pandas as pd
import numpy as np
from numerize import numerize
import streamlit as st
import plotly.express as px



@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

def value_with_image(col,header,value,header_style="",value_style=""):
    with col:
        st.markdown(f'<div class="my-metric {header_style}">{header}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="my-value {value_style}">{value}</div>', unsafe_allow_html=True)

        #st.metric(header, value)
        #st.metric(label="", value="")
        #st.metric(header,value, style='my-metric')

def value_status(col,header,df,status_col,header_style="",value_style=""):
        #st.dataframe(df)
        df.groupby(['product']).agg({'status':'count'})
        df = df[df['status'] == status_col]
        value = df.status.count()
        with col:
            st.markdown(f'<div class="my-metric {header_style}">{header}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="my-value {value_style}">{value}</div>', unsafe_allow_html=True)
            #st.metric(header,value)

    
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
        discount = str(int(df.discount.mean()*100)) + '%'
        return discount
    except:
        return 0
    
def get_sell_through(df):
    try:
        r2 = df.groupby(['product']).agg({'sales_qty':'sum','daily_targets':'sum'}).reset_index()
        r2['sell_through'] = (r2['sales_qty']) /r2['daily_targets']
        ST = str(int(r2.sell_through.mean() * 100)) + '%'
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
    

def status(df):
    if df['sell_through'] > 1.15:   
        return 'FAST'
    elif df['sell_through'] > 0.85:
        return 'MEDIUM'
    else:
        return 'SLOW'
    
def sell_through_status(df):
    try:
        r2 = df.groupby(['product','product_group','gender','country']).agg({'sales_qty':'sum','daily_targets':'sum','rrp':'mean','opp':'sum'}).reset_index()
        r2['sell_through'] = (r2['sales_qty']) /(r2['daily_targets'])
        r2['status'] = r2.apply(lambda x: status(x),axis=1)
        return r2
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

def color_cells(value):
    color = 'red' if value == 'SLOW' else 'green' if value == 'FAST' else 'orange' if value == 'MEDIUM' else ""
    #return f'<span style="color: {color}">{value}</span>'
    return f'color: {color}'




    
