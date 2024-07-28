import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.logo('17898105.png',icon_image='17898105.png',link='https://smashdown.streamlit.app/')
# Title of the app
st.header('Smashdown 2024 - Prevalent AI')
st.divider()
# Load the Excel file
file_path = "fixture.csv"
df = pd.read_csv(file_path)

columns = ['Fixture','Tournament Rules','Results']

# Create four columns for the buttons
col11, col22, col33 = st.columns(3)

# Initialize a variable to store the selected category
selected_category = "Fixture"

# Create buttons for each category
if col11.button('Fixture',use_container_width=True):
    selected_category = 'Fixture'
if col22.button('Tournament Rules',use_container_width=True):
    selected_category = 'Tournament Rules'
if col33.button('Results',use_container_width=True):
    selected_category = 'Results'
st.divider()
# Extract unique categories for the buttons
categories = df['Category'].unique()

if selected_category=='Fixture':
    # Create four columns for the buttons
    col1, col2, col3, col4 = st.columns(4)
    # Initialize a variable to store the selected category
    selected_category1 = "All"

    # Create buttons for each category
    if col1.button('All',use_container_width=True):
        selected_category1 = 'All'
    if col2.button('Mixed Doubles',use_container_width=True):
        selected_category1 = 'Mixed Doubles'
    if col3.button('Women’s Doubles',use_container_width=True):
        selected_category1 = 'Women’s Doubles'
    if col4.button('Men’s Doubles',use_container_width=True):
        selected_category1 = 'Men’s Doubles'
    # Display the fixtures for the selected category
    if selected_category1 != 'All':
        st.subheader(f"{selected_category1}")
        category_df = df[df['Category'] == selected_category1]
        st.dataframe(category_df[['Match Number', 'Names', 'Group', 'Court Number', 'Time']], hide_index=True, use_container_width=True)
    else:
        st.subheader("Full Fixture")
        st.dataframe(df[['Match Number', 'Names', 'Category','Group', 'Court Number', 'Time']], hide_index=True, use_container_width=True)
elif selected_category=='Tournament Rules':
    st.subheader("Tournament Rules")
elif selected_category=='Results':
    st.subheader("Results")
