import streamlit as st
import pandas as pd
import plotly.express as px

# Load data (replace with your own data)
data = {
    'Level1': ['A', 'A', 'B', 'B', 'C', 'C'],
    'Level2': ['X', 'Y', 'X', 'Y', 'X', 'Y'],
    'Opportunity': [100, 80, 60, 40, 30, 20]
}

df = pd.DataFrame(data)

# Calculate total opportunity at each level
df['Total_Opportunity'] = df.groupby('Level1')['Opportunity'].transform('sum')

# Calculate percentage opportunity at each level
df['Percentage_Opportunity'] = df['Opportunity'] / df['Total_Opportunity'] * 100

# Streamlit app
st.title('Opportunity Breakdown')

# Display the dataframe
st.subheader('Data')
st.dataframe(df)

# Create a Treemap chart for opportunity breakdown
fig = px.treemap(df, path=['Level1', 'Level2'], values='Opportunity', 
                 color='Percentage_Opportunity', hover_data=['Percentage_Opportunity'],
                 color_continuous_scale='Blues', title='Opportunity Breakdown')

# Configure treemap layout
fig.update_traces(textinfo='label+value+percent parent')

# Display the Treemap chart
st.plotly_chart(fig)
