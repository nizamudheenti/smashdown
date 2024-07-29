import streamlit as st
import pandas as pd

st.set_page_config(page_title="PAI-SMASHDOWN", layout="wide", page_icon="🏸")
st.logo('17898105.png', icon_image='17898105.png', link='https://smashdown.streamlit.app/')

# Title of the app
st.header('SMASHDOWN 2024 - PAI')
st.divider()

# Load the CSV file
file_path = "fixture.csv"
df = pd.read_csv(file_path)

columns = ['Fixture', 'Tournament Rules', 'Results']

# Create three columns for the buttons
col11, col22, col33 = st.columns(3)

# Initialize a variable to store the selected category
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = 'Fixture'

# Create buttons for each category
if col11.button('Fixture', use_container_width=True):
    st.session_state.selected_category = 'Fixture'
if col22.button('Tournament Rules', use_container_width=True):
    st.session_state.selected_category = 'Tournament Rules'
if col33.button('Results', use_container_width=True):
    st.session_state.selected_category = 'Results'

st.divider()

# Extract unique categories for the buttons
categories = df['Category'].unique()

if st.session_state.selected_category == 'Fixture':
    # Create four columns for the buttons
    col1, col2, col3, col4 = st.columns(4)
    # Initialize a variable to store the selected subcategory
    if 'selected_category1' not in st.session_state:
        st.session_state.selected_category1 = 'All'

    # Create buttons for each subcategory
    if col1.button('All', use_container_width=True):
        st.session_state.selected_category1 = 'All'
    if col2.button('Mixed Doubles', use_container_width=True):
        st.session_state.selected_category1 = 'Mixed Doubles'
    if col3.button('Women’s Doubles', use_container_width=True):
        st.session_state.selected_category1 = 'Women’s Doubles'
    if col4.button('Men’s Doubles', use_container_width=True):
        st.session_state.selected_category1 = 'Men’s Doubles'

    # Display the fixtures for the selected subcategory
    if st.session_state.selected_category1 != 'All':
        st.subheader(f"{st.session_state.selected_category1}")
        category_df = df[df['Category'] == st.session_state.selected_category1]
        x = category_df['Names'].apply(lambda x: x.split(' VS ')).to_list()
        y = []
        for i in range(len(x)):
            y = y + x[i]
        del x
        filter = st.selectbox("Filter", ['All']+list(set(y)))
        if filter=='All':
            st.dataframe(category_df[['Match Number', 'Names', 'Group', 'Court Number', 'Time']], hide_index=True, use_container_width=True)
        else:
            st.dataframe(category_df[category_df['Names'].str.contains(filter)][['Match Number', 'Names', 'Group', 'Court Number', 'Time']], hide_index=True, use_container_width=True)
        if st.session_state.selected_category1 == 'Men’s Doubles':
            with st.expander("Groups"):
                co1, co2, co3 = st.columns(3)
                co1.markdown(
                    """
                    Men A
                    - Bipin M V & Ananthu Sunil
                    - Emmanuel Joseph & Dion Paul George
                    - Laby K Joy & Rakesh S
                    - Gokul A A & Sajith M S"""
                )
                co2.markdown(
                    """
                    Men B
                    - Rakesh P B & Nizamudheen T I
                    - Muhammed Althaf & Sreekumar T H
                    - Harikrishnan & Jeen Michael
                    - Shashi Salian & Akshay CA
                    """
                )
                co3.markdown(
                    """
                    Men C
                    - Jacob George & Muhammed Jazim
                    - Jithin Odattu O C & Neeraj Jayaraj
                    - Anand Balakrishnan & Kumaresan Arumugham
                    - Kiran Joseph & Sidharth Nair
                    - John Thomas2 & Jubit John
                    """
                )
        if st.session_state.selected_category1 == 'Women’s Doubles':
            with st.expander("Groups"):
                co1, co2 = st.columns(2)
                co1.markdown(
                    """
                    Women A
                    - Shama Anjoom & Sarah Jacob
                    - Parvathi Ambareesh & Sithara Mohan
                    - Merin Jose & Sneha Achamma Cherian
                    - Cristeena & Amrutha"""
                )
                co2.markdown(
                    """
                    Women B
                    - Swetha Shenoy & Ginu George
                    - Amrita Surendran & Deepthi Dinakaran
                    - Pappy A Lakshmi & Arya Suresh
                    - Riya & Ann
                    """
                )
        if st.session_state.selected_category1 == 'Mixed Doubles':
            with st.expander("Groups"):
                co1, co2 = st.columns(2)
                co1.markdown(
                    """
                    Mixed A
                    - Pravitha V Namboothiri & Neeraj Gopan
                    - Alan & Sandra Sharon
                    - Mohammed Ashiq A & Denila Davis"""
                )
                co2.markdown(
                    """
                    Mixed B
                    - Pankaj Sherry Paret & Athira K B
                    - Catherine Pulickan & Aljo Ajith
                    - Vinju & Deepak
                    """
                )
    else:
        st.subheader("Full Fixture")
        st.dataframe(df[['Match Number', 'Names', 'Category', 'Group', 'Court Number', 'Time']], hide_index=True, use_container_width=True)
elif st.session_state.selected_category == 'Tournament Rules':
    st.subheader("Tournament Rules")
elif st.session_state.selected_category == 'Results':
    st.subheader("Results")
