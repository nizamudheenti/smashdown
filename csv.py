import streamlit as st
import pandas as pd
st.set_page_config(page_title="PAI-SMASHDOWN", layout="wide", page_icon="🏸")
# Load CSV
def load_data():
    return (pd.read_csv("C:/Users/nizamudheen.ti/OneDrive - prevalent.ai/Documents/GitHub/smashdown/csv/mixed_a.csv"),
            pd.read_csv("C:/Users/nizamudheen.ti/OneDrive - prevalent.ai/Documents/GitHub/smashdown/csv/mixed_b.csv"))

# Save CSV
def save_data(mixed_a,mixed_b):
    return(mixed_a.to_csv("C:/Users/nizamudheen.ti/OneDrive - prevalent.ai/Documents/GitHub/smashdown/csv/mixed_a.csv", index=False),
           mixed_b.to_csv("C:/Users/nizamudheen.ti/OneDrive - prevalent.ai/Documents/GitHub/smashdown/csv/mixed_b.csv", index=False))

# Main function to create the Streamlit app
def main():
    st.title("Badminton Tournament Points Table")
    st.divider()
    # Load data
    mixed_a,mixed_b = load_data()
    
    # Display editable table

    edited_mixed_a = st.data_editor(mixed_a, num_rows="dynamic",use_container_width=True)
    st.divider()
    edited_mixed_b = st.data_editor(mixed_b, num_rows="dynamic",use_container_width=True)
    
    # Save button
    if st.button("Save"):
        save_data(edited_mixed_a,edited_mixed_b)
        st.success("Points table updated successfully!")

# Run the app
if __name__ == "__main__":
    main()
