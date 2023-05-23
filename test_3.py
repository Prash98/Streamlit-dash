import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load your dataset with dates and associated events
data = {
    'Date': ['2023-05-01', '2023-05-05', '2023-05-10'],
    'Event': ['Event 1', 'Event 2', 'Event 3']
}
df = pd.DataFrame(data)

# Convert the 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Create a calendar view using plotly
fig = go.Figure(data=go.Scatter(
    x=df['Date'],
    y=[1] * len(df),  # Set a constant y-value for all events
    mode='markers',
    marker=dict(size=10),
    text=df['Event'],
    hovertemplate='%{text}<extra></extra>',
))

fig.update_layout(
    title='Calendar View',
    xaxis=dict(
        calendar='gregorian',
        dtick='M1',
        tickformat='%Y-%m-%d',
        tickangle=45,
        tickfont=dict(size=10),
        range=[df['Date'].min() - pd.DateOffset(days=7), df['Date'].max() + pd.DateOffset(days=7)],
    ),
    yaxis=dict(visible=False),
    showgrid=True,
    gridwidth=1,
    gridcolor='lightgray',
    height=600,
)

# Display the calendar view using plotly in Streamlit
st.plotly_chart(fig)
