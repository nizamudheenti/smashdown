import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.logo('17898105.png',icon_image='17898105.png',link='https://smashdown.streamlit.app/')
# Title of the app
st.title('Smashdown 2024 - Prevalent AI')
st.divider()
# Load the Excel file
file_path = "fixture.csv"
df = pd.read_csv(file_path)

columns = ['Fixture','Tournament Rules','Results']

# Create four columns for the buttons
col11, col22, col32 = st.columns(3)

# Initialize a variable to store the selected category
selected_category = "Fixture"

# Create buttons for each category
if col11.button('Fixture',use_container_width=True):
    selected_category = 'Fixture'
if col22.button('Tournament Rules',use_container_width=True):
    selected_category = 'Tournament Rules'
if col33.button('Results',use_container_width=True):
    selected_category = 'Results'

# Extract unique categories for the buttons
categories = df['Category'].unique()

# Create four columns for the buttons
col1, col2, col3, col4 = st.columns(4)

# Initialize a variable to store the selected category
selected_category = "All"

# Create buttons for each category
if col1.button('All',use_container_width=True):
    selected_category = 'All'
if col2.button('Mixed Doubles',use_container_width=True):
    selected_category = 'Mixed Doubles'
if col3.button('Women’s Doubles',use_container_width=True):
    selected_category = 'Women’s Doubles'
if col4.button('Men’s Doubles',use_container_width=True):
    selected_category = 'Men’s Doubles'
st.divider()
# Display the fixtures for the selected category
if selected_category != 'All':
    st.header(f"{selected_category}")
    category_df = df[df['Category'] == selected_category]
    st.dataframe(category_df[['Match Number', 'Names', 'Group', 'Court Number', 'Time']], hide_index=True, use_container_width=True)
else:
    st.header("Full Fixture")
    st.dataframe(df[['Match Number', 'Names', 'Group', 'Court Number', 'Time']], hide_index=True, use_container_width=True)
