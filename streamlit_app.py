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

knockout = pd.read_csv("knockout.csv")

columns = ['Fixture', 'Tournament Rules', 'Results']

# Create three columns for the buttons
col11, col22, col33 = st.columns(3)

# Initialize a variable to store the selected category
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = 'Fixture'

# Create buttons for each category
if col11.button('Fixture', use_container_width=True):
    st.session_state.selected_category = 'Fixture'
if col22.button('Results', use_container_width=True):
    st.session_state.selected_category = 'Results'
if col33.button('Tournament Rules', use_container_width=True):
    st.session_state.selected_category = 'Tournament Rules'

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
        category_df = df[df['Category'] == st.session_state.selected_category1]
        x = category_df['Names'].apply(lambda x: x.split(' VS ')).to_list()
        y = []
        for i in range(len(x)):
            y = y + x[i]
        del x
        filter = st.selectbox("Filter", ['All']+list(set(y)))
        if filter=='All':
            st.write("")
            st.markdown("* Teams must be present and ready to play at least 30 minutes before the match start time. Otherwise, it would be considered a walkover.")
            st.markdown("##### Group Stage")
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
                    - John Thomas & Jubit John
                    """
                )
            st.markdown("##### Knock Out")
            st.dataframe(knockout[knockout['Category']=="Men's Doubles"][['Match Number', 'Names', 'Match', 'Court Number', 'Time']], hide_index=True, use_container_width=True)
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
            st.markdown("##### Knock Out")
            st.dataframe(knockout[knockout['Category']=="Women's Doubles"][['Match Number', 'Names', 'Match', 'Court Number', 'Time']], hide_index=True, use_container_width=True)
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
            st.markdown("##### Knock Out")
            st.dataframe(knockout[knockout['Category']=='Mixed Doubles'][['Match Number', 'Names', 'Match', 'Court Number', 'Time']], hide_index=True, use_container_width=True)
    else:
        st.write("")
        st.markdown("* Teams must be present and ready to play at least 30 minutes before the match start time. Otherwise, it would be considered a walkover.")
        st.markdown("##### Group Stage")
        st.dataframe(df[['Match Number', 'Names', 'Category', 'Group', 'Court Number', 'Time']], hide_index=True, use_container_width=True)
        st.markdown("##### Knock Out")
        st.dataframe(knockout[['Match Number', 'Names', 'Match', 'Court Number', 'Time']], hide_index=True, use_container_width=True)
elif st.session_state.selected_category == 'Tournament Rules':
    st.markdown("""### Match Format

##### Group Stages
1. Each team will play against every other team in their group.
2. Each match will be played for one set only to 21 points.

#### Quarter-Finals, Semi-Finals, and Finals
1. Matches will be best of three sets.
2. Each set will be played to 15 points.

#### General
1. Each match will begin promptly at the scheduled time.
2. Teams must be present and ready to play at least 20 minutes before the match start time. Otherwise, it would be considered a walkover.
3. Standard badminton rules apply unless otherwise stated.
4. All players are expected to exhibit good sportsmanship.

#### Safety
1. Players should wear appropriate sports attire and footwear.
2. Any injuries should be reported immediately to the tournament organizer.

#### Scoring System
1. Rally scoring will be used (a point is scored on every serve, regardless of which team served).
2. In the event of a tie at the end of a match, the first team to lead by 2 points wins.
3. After 30 sudden death.

#### Service Rules
1. Service will be decided by a coin toss.
2. Serve must be made underhand, and the shuttle must be hit below the waist.
3. Excessive or exaggerated movements will be considered illegal or disruptive to the opponent’s readiness.

#### Qualification for Quarter-Finals and Semi-Finals

##### Womens and Mixed
1. There are 2 groups.
2. The top 4 teams from each group will advance to the semi-finals.

##### Mens
1. Top 2 teams from each group qualify for quarters (Total 6 teams).
2. Remaining 2 teams are promoted based on their total scores in the group stage.
3. Teams with the highest total scores are promoted to the quarter-finals automatically.
4. Normalization is applied to remaining 2 teams if scores are the same.

##### Normalizing Purpose
To fairly compare teams across different groups by adjusting scores based on group performance.

**Method**:
                Normalized Score = (Points Scored - Points Conceded) / Total Matches Played

**Example**:
- **Team A**:
  - Points Scored: 210
  - Points Conceded: 180
  - Matches Played: 10
  - Normalized Score for Team A = (210 - 180) / 10 = 30 / 10 = 3
- **Team B**:
  - Points Scored: 200
  - Points Conceded: 190
  - Matches Played: 10
  - Normalized Score for Team B = (200 - 190) / 10 = 10 / 10 = 1

After calculating the normalized scores, teams with the highest normalized scores will be selected to advance. In this example, Team A has the highest normalized score of 3, so Team A would be the additional team selected for the semi-finals.

If teams have equal normalized scores after applying the normalization method, then we will use tie breaker criteria:
1. **Head-to-Head Result**: Compare the results of the matches played between the tied teams. The team with the better head-to-head record advances.
2. **Points Difference**: Calculate the difference between points scored and points conceded for each team. The team with the higher points difference advances.
3. **Points Scored**: Compare the total points scored by each team. The team with the higher total points scored advances.
4. **Lowest Points Conceded**: Compare the total points conceded by each team. The team with the lowest total points conceded advances.
5. **Fair Play Record**: If all other criteria fail to break the tie, use a fair play record (e.g., fewer fouls, warnings, or penalties).

""")
elif st.session_state.selected_category == 'Results':
    st.subheader("Results")
    tab1, tab2, tab3 = st.tabs(["Mixed Doubles", "Women's Doubles", "Men's Doubles"])
    with tab1:
        mixed_a_data = {
        'Team': ['Pravitha V Namboothiri & Neeraj Gopan', 'Alan & Sandra Sharon', 'Mohammed Ashiq A & Denila Davis'],
        'Matches Played': [0, 0, 0],
        'Matches Won': [0, 0, 0],
        'Matches Lost': [0, 0, 0],
        'Points Won': [0, 0, 0],
        'Points Lost': [0, 0, 0]
        }

        # Create DataFrame for Mixed A
        st.caption('Mixed A')
        st.dataframe(pd.DataFrame(mixed_a_data), hide_index=True, use_container_width=True)

        # Define the data for Mixed B
        mixed_b_data = {
            'Team': ['Pankaj Sherry Paret & Athira K B', 'Catherine Pulickan & Aljo Ajith', 'Vinju & Deepak'],
            'Matches Played': [0, 0, 0],
            'Matches Won': [0, 0, 0],
            'Matches Lost': [0, 0, 0],
            'Points Won': [0, 0, 0],
            'Points Lost': [0, 0, 0]
        }

        # Create DataFrame for Mixed B
        st.caption('Mixed B')
        st.dataframe(pd.DataFrame(mixed_b_data), hide_index=True, use_container_width=True)
    with tab2:
        mixed_a_data = {
        'Team': ['Shama Anjoom & Sarah Jacob','Parvathi Ambareesh & Sithara Mohan','Merin Jose & Sneha Achamma Cherian','Cristeena & Amrutha'],
        'Matches Played': [0, 0, 0,0],
        'Matches Won': [0, 0, 0,0],
        'Matches Lost': [0, 0, 0,0],
        'Points Won': [0, 0, 0,0],
        'Points Lost': [0, 0, 0,0]
        }

        # Create DataFrame for Mixed A
        st.caption('Women A')
        st.dataframe(pd.DataFrame(mixed_a_data), hide_index=True, use_container_width=True)

        # Define the data for Mixed B
        mixed_b_data = {
            'Team': ['Swetha Shenoy & Ginu George','Amrita Surendran & Deepthi Dinakaran','Pappy A Lakshmi & Arya Suresh','Riya & Ann'],
            'Matches Played': [0, 0, 0,0],
        'Matches Won': [0, 0, 0,0],
        'Matches Lost': [0, 0, 0,0],
        'Points Won': [0, 0, 0,0],
        'Points Lost': [0, 0, 0,0]
        }

        # Create DataFrame for Mixed B
        st.caption('Women B')
        st.dataframe(pd.DataFrame(mixed_b_data), hide_index=True, use_container_width=True)
    with tab3:
        mixed_a_data = {
        'Team': ['Bipin M V & Ananthu Sunil','Emmanuel Joseph & Dion Paul George','Laby K Joy & Rakesh S','Gokul A A & Sajith M S'],
        'Matches Played': [0, 0, 0,0],
        'Matches Won': [0, 0, 0,0],
        'Matches Lost': [0, 0, 0,0],
        'Points Won': [0, 0, 0,0],
        'Points Lost': [0, 0, 0,0]
        }

        # Create DataFrame for Mixed A
        st.caption('Men A')
        st.dataframe(pd.DataFrame(mixed_a_data), hide_index=True, use_container_width=True)

        # Define the data for Mixed B
        mixed_b_data = {
            'Team': ['Rakesh P B & Nizamudheen T I','Muhammed Althaf & Sreekumar T H','Harikrishnan & Jeen Michael','Shashi Salian & Akshay CA'],
            'Matches Played': [0, 0, 0,0],
            'Matches Won': [0, 0, 0,0],
            'Matches Lost': [0, 0, 0,0],
            'Points Won': [0, 0, 0,0],
            'Points Lost': [0, 0, 0,0]
        }

        # Create DataFrame for Mixed B
        st.caption('Men B')
        st.dataframe(pd.DataFrame(mixed_b_data), hide_index=True, use_container_width=True)

        # Define the data for Mixed B
        mixed_c_data = {
            'Team': ['Jacob George & Muhammed Jazim','Jithin Odattu O C & Neeraj Jayaraj','Anand Balakrishnan & Kumaresan Arumugham','Kiran Joseph & Sidharth Nair','John Thomas & Jubit John'],
            'Matches Played': [0, 0, 0,0,0],
            'Matches Won': [0, 0, 0,0,0],
            'Matches Lost': [0, 0, 0,0,0],
            'Points Won': [0, 0, 0,0,0],
            'Points Lost': [0, 0, 0,0,0]
        }

        # Create DataFrame for Mixed B
        st.caption('Men C')
        st.dataframe(pd.DataFrame(mixed_c_data), hide_index=True, use_container_width=True)
