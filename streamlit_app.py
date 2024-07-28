import streamlit as st

import streamlit as st
import pandas as pd

# Title of the app
st.title('Badminton Tournament Fixtures')

# Load the Excel file
file_path = "fixture.csv"
df = pd.read_csv(file_path)

# Display the data category-wise
categories = df['Category'].unique()

for category in categories:
    st.header(f"{category}")
    category_df = df[df['Category'] == category]
    st.table(category_df[['Match Number', 'Names', 'Group', 'Court Number', 'Time']])