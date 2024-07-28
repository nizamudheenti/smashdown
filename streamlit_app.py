import streamlit as st

st.title("Smashdown 2024")
# Set the background image
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://img.freepik.com/free-photo/badminton-concept-with-racket-shuttlecock_23-2149940923.jpg");
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""

st.markdown(background_image, unsafe_allow_html=True)