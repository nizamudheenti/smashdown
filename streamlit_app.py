import streamlit as st

import streamlit as st
import pandas as pd

# Title of the app
st.title('Badminton Tournament Fixtures')

# Load the Excel file
file_path = "fixture.csv"
df = pd.read_csv(file_path)

# Extract unique categories for the dropdown
categories = df['Category'].unique()

# Create a dropdown for category selection
selected_category = st.selectbox('Select Category', categories)

# Display the fixtures for the selected category
st.header(f"{selected_category}")
category_df = df[df['Category'] == selected_category]
st.table(category_df[['Match Number', 'Names', 'Group', 'Court Number', 'Time']])
