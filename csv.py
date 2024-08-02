import streamlit as st
import pandas as pd
st.set_page_config(page_title="PAI-SMASHDOWN", layout="wide", page_icon="🏸")
# Load CSV
def load_data():
    return (pd.read_csv("C:/Users/NIZAM/OneDrive/Documents/GitHub/smashdown/csv/mixed_a.csv"),
            pd.read_csv("C:/Users/NIZAM/OneDrive/Documents/GitHub/smashdown/csv/mixed_b.csv"),
            pd.read_csv("C:/Users/NIZAM/OneDrive/Documents/GitHub/smashdown/csv/men_a.csv"),
            pd.read_csv("C:/Users/NIZAM/OneDrive/Documents/GitHub/smashdown/csv/men_b.csv"),
            pd.read_csv("C:/Users/NIZAM/OneDrive/Documents/GitHub/smashdown/csv/men_c.csv"),
            pd.read_csv("C:/Users/NIZAM/OneDrive/Documents/GitHub/smashdown/csv/women_a.csv"),
            pd.read_csv("C:/Users/NIZAM/OneDrive/Documents/GitHub/smashdown/csv/women_b.csv"))

# Save CSV
def save_data(mixed_a,mixed_b,men_a,men_b,men_c,women_a,women_b):
    return(mixed_a.to_csv("C:/Users/NIZAM/OneDrive/Documents/GitHub/smashdown/csv/mixed_a.csv", index=False),
           mixed_b.to_csv("C:/Users/NIZAM/OneDrive/Documents/GitHub/smashdown/csv/mixed_b.csv", index=False),
           men_a.to_csv("C:/Users/NIZAM/OneDrive/Documents/GitHub/smashdown/csv/men_a.csv", index=False),
           men_b.to_csv("C:/Users/NIZAM/OneDrive/Documents/GitHub/smashdown/csv/men_b.csv", index=False),
           men_c.to_csv("C:/Users/NIZAM/OneDrive/Documents/GitHub/smashdown/csv/men_c.csv", index=False),
           women_a.to_csv("C:/Users/NIZAM/OneDrive/Documents/GitHub/smashdown/csv/women_a.csv", index=False),
           women_b.to_csv("C:/Users/NIZAM/OneDrive/Documents/GitHub/smashdown/csv/women_b.csv", index=False))

# Main function to create the Streamlit app
def main():
    st.title("Badminton Tournament Points Table")
    st.divider()
    # Load data
    mixed_a,mixed_b,men_a,men_b,men_c,women_a,women_b= load_data()
    
    # Display editable table
    with st.expander("Mixed Doubles"):
        st.divider()
        edited_mixed_a = st.data_editor(mixed_a, num_rows="dynamic",use_container_width=True)
        st.divider()
        edited_mixed_b = st.data_editor(mixed_b, num_rows="dynamic",use_container_width=True)
        st.divider()
    with st.expander("Men's Doubles"):
        edited_men_a = st.data_editor(men_a, num_rows="dynamic",use_container_width=True)
        st.divider()
        edited_men_b = st.data_editor(men_b, num_rows="dynamic",use_container_width=True)
        st.divider()
        edited_men_c = st.data_editor(men_c, num_rows="dynamic",use_container_width=True)
        st.divider()
    with st.expander("Women's Doubles"):
        edited_women_a = st.data_editor(women_a, num_rows="dynamic",use_container_width=True)
        st.divider()
        edited_women_b = st.data_editor(women_b, num_rows="dynamic",use_container_width=True)
        st.divider()
    # Save button
    if st.button("Save"):
        save_data(edited_mixed_a,edited_mixed_b,edited_men_a,edited_men_b,edited_men_c,edited_women_a,edited_women_b)
        st.success("Points table updated successfully!")

# Run the app
if __name__ == "__main__":
    main()
