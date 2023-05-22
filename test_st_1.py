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

# Display an expander for each category with aggregated value
for category, value in grouped_df.iterrows():
    expander = st.expander(f"{category}: Aggregated Value - {value['Value']}")
    with expander:
        category_data = df[df['Category'] == category]
        st.dataframe(category_data)
