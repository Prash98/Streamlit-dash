import streamlit as st

# Add an image to the sidebar
image_path = "image_1.png"
st.sidebar.header('Select the right option')
st.sidebar.image(image_path, caption='', use_column_width=True)


# Add content to the sidebar
st.sidebar.header('Sidebar')
st.sidebar.subheader('Options')

# Display options as separate lines
st.sidebar.write('Option 1')
st.sidebar.write('Option 2')
st.sidebar.write('Option 3')