import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Assuming you have a DataFrame named 'df' with the events and their corresponding dates
df = pd.DataFrame({
    'Event': ['Event 1', 'Event 2', 'Event 3', 'Event 4'],
    'Date': ['2023-01-15', '2023-02-10', '2023-02-28', '2023-03-20']
})

# Convert the 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Extract month and day from the date
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day

# Create a Dash application
app = dash.Dash(__name__)

# Set up the layout
app.layout = html.Div([
    html.H1('Events'),
    dcc.Dropdown(
        id='month-dropdown',
        options=[
            {'label': 'January', 'value': 1},
            {'label': 'February', 'value': 2},
            {'label': 'March', 'value': 3},
            # Add more options for other months...
        ],
        value=1,  # Default value for the dropdown
        clearable=False  # Disable the "clear" option
    ),
    dcc.Graph(id='event-scatter')
])

# Define the callback function to update the scatter plot based on the selected month
@app.callback(
    Output('event-scatter', 'figure'),
    [Input('month-dropdown', 'value')]
)
def update_event_scatter(selected_month):
    # Filter the DataFrame to include only events for the selected month
    filtered_df = df[df['Month'] == selected_month]

    # Create a scatter plot
    fig = go.Figure()

    # Add markers for each event
    fig.add_trace(go.Scatter(
        x=filtered_df['Month'],
        y=filtered_df['Day'],
        mode='markers',
        text=filtered_df['Event'],
        marker=dict(
            size=10,
            color='blue',
            symbol='circle',
        ),
    ))

    # Customize the layout
    fig.update_layout(
        title='Events',
        xaxis=dict(title='Month'),
        yaxis=dict(title='Day'),
    )

    return fig

# Run the Streamlit application
def run_dash_app():
    app.run_server(debug=False)

st.title('Streamlit with Dash')

if st.button('Launch Dash Application'):
    run_dash_app()
