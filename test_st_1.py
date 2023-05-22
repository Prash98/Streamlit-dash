import streamlit as st
import pandas as pd

# Create a sample DataFrame
data = {
    'Category': ['A', 'A', 'B', 'B', 'C', 'C'],
    'Value': [10, 20, 30, 40, 50, 60]
}
df = pd.DataFrame(data)

# Group the DataFrame by category and calculate the sum
grouped_df = df.groupby('Category').sum()

# Display the aggregated values directly at the top
for category, value in grouped_df.iterrows():
    st.write(f"{category}: {value['Value']}")

# Create an expander for the remaining content
expander = st.expander("More Details")
with expander:
    st.dataframe(df)
