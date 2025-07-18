import streamlit as st
import pandas as pd

# App config
st.set_page_config(page_title="PAI Premier League", layout="wide", page_icon="🏆")
st.logo('images/tmp_bcff20e0-0f45-403b-a578-3114ce1d6427.png',size="medium")
# Session state initialization
def init_state(sport):
    for section in ["fixtures", "rules", "results"]:
        key = f"{sport}_{section}"
        if key not in st.session_state:
            st.session_state[key] = False

# Show section buttons with full width
def show_buttons(sport):
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📅 Fixtures", key=f"{sport}_btn_fixtures", use_container_width=True):
            reset_sections(sport)
            st.session_state[f"{sport}_fixtures"] = True
    with col2:
        if st.button("📜 Rules", key=f"{sport}_btn_rules", use_container_width=True):
            reset_sections(sport)
            st.session_state[f"{sport}_rules"] = True
    with col3:
        if st.button("📊 Results", key=f"{sport}_btn_results", use_container_width=True):
            reset_sections(sport)
            st.session_state[f"{sport}_results"] = True

# Reset section states
def reset_sections(sport):
    st.session_state[f"{sport}_fixtures"] = False
    st.session_state[f"{sport}_rules"] = False
    st.session_state[f"{sport}_results"] = False

# Format the badminton fixtures from the provided data
def format_badminton_fixtures(df):
    # Make sure df is properly formatted for display
    return df[["Category", "Group", "Team 1", "Team 2"]]

# Sort Badminton results (will be used when results data is available)
def sort_badminton_data(data):
    try:
        df = pd.DataFrame(data)
        if 'Matches Played' in df.columns:
            df[['Matches Played', 'Matches Won', 'Matches Lost', 'Points Won', 'Points Lost']] = \
                df[['Matches Played', 'Matches Won', 'Matches Lost', 'Points Won', 'Points Lost']].astype(int)
            df['Points Difference'] = df['Points Won'] - df['Points Lost']
            return df.sort_values(by=['Matches Won', 'Points Difference'], ascending=[False, False]).reset_index(drop=True)
        return df
    except Exception as e:
        st.error(f"Error formatting results data: {e}")
        return pd.DataFrame()

# Main Title
st.title("Prevalent AI Premier League")
st.markdown("""##### 7 Sports · 4 Teams · May & June 2025""")
st.markdown("---")

# Add the images of participating teams in a 4-column layout with resized logos
col1, col2, col3, col4 ,col5= st.columns(5)

# Display images of the teams (ensure the images are resized for better alignment)
with col3:
    st.image("images/logos.png", caption="Teams",width=400)

# Tabs for different sports
tabs = st.tabs(["🏸 Badminton", "🏏 Cricket", "⚽ Football", "🏓 Table Tennis", "🎯 Carroms","⛹️ Basket Ball","🏐 Volley Ball"])

# ---------- BADMINTON TAB ----------
with tabs[0]:
    sport = "badminton"
    init_state(sport)
    st.header("🏸 Badminton")
    show_buttons(sport)


    if st.session_state[f"{sport}_fixtures"]:
        st.subheader("📅 Fixtures")
        
        try:
            # Read the fixture data from the CSV file
            df_fixtures = pd.read_csv("csv/fixture.csv")
            
            # Get unique categories for selection
            categories = df_fixtures["Category"].unique().tolist()
            selected_cat = st.selectbox("Select Category", categories)
            
            # Filter and show the fixtures for the selected category
            filtered_fixtures = df_fixtures[df_fixtures["Category"] == selected_cat].reset_index(drop=True)
            
            # Display Group Summary
            st.subheader("Group Summary")
            
            # Get unique groups for this category
            groups = filtered_fixtures["Group"].unique().tolist()
            
            # Create a dictionary to map groups to teams
            group_teams = {}
            for group in groups:
                group_data = filtered_fixtures[filtered_fixtures["Group"] == group]
                teams = set(group_data["Team 1"].tolist() + group_data["Team 2"].tolist())
                group_teams[group] = sorted(list(teams))
            
            # Display groups and teams
            cols = st.columns(len(groups))
            for i, (group, teams) in enumerate(group_teams.items()):
                with cols[i % len(cols)]:
                    st.markdown(f"**{group}**")
                    for team in teams:
                        st.markdown(f"- {team}")
            
            st.markdown("---")
            
            # Filter out matches with scores (already played)
            upcoming_fixtures = filtered_fixtures[pd.isna(filtered_fixtures['Team 1 Score'])]
            played_fixtures = filtered_fixtures[pd.notna(filtered_fixtures['Team 1 Score'])]
            
            # Display upcoming fixtures
            if not upcoming_fixtures.empty:
                st.subheader("Upcoming Matches")
                teams=['All']
                teams.extend(upcoming_fixtures["Team 1"].unique())
                teams.extend(upcoming_fixtures["Team 2"].unique())
                selected_cat = st.selectbox("Select Team",teams)
                if selected_cat != 'All':
                    upcoming_fixtures = upcoming_fixtures[(upcoming_fixtures["Team 1"] == selected_cat) | (upcoming_fixtures["Team 2"] == selected_cat)]
                    st.dataframe(
                        upcoming_fixtures[["Group", "Team 1", "Team 2","Time","Court"]], 
                        use_container_width=True
                    )
                else:
                    st.dataframe(
                        upcoming_fixtures[["Group", "Team 1", "Team 2","Time","Court"]], 
                        use_container_width=True
                    )
            else:
                st.info("No upcoming fixtures found for this category.")
                
            # Display played fixtures
            if not played_fixtures.empty:
                st.subheader("Completed Matches")
                st.dataframe(
                    played_fixtures[["Group", "Team 1", "Team 1 Score", "Team 2 Score", "Team 2"]], 
                    use_container_width=True
                )
        except Exception as e:
            st.error(f"Error loading fixtures: {e}")
            st.info("Please ensure 'group_stage_matches_latest.csv' is in the app directory with proper formatting.")

    elif st.session_state[f"{sport}_rules"]:
        st.subheader("📜 Rules")
        st.markdown("""#### Badminton Tournament Rules

#### Group Stages
1. Each team will play against every other team in their group.
2. Each match will be played for one set only to 21 points.

#### Quarter-Finals, Semi-Finals, and Finals
1. Matches will be best of three sets.
2. Each set will be played to 15 points.

#### Qualification for Knockout Stages
##### Men's Division
1. There are 4 groups in the men's division.
2. The top 2 teams from each group will advance to the quarter-finals.

##### Women's Division
1. There are 2 groups in the women's division.
2. The top 2 teams from each group will advance to the semi-finals.

##### Mixed Division
1. There are 2 groups in the mixed division.
2. The top 2 teams from each group will advance to the semi-finals.

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
3. After 21 points for 15-set (for 21-set it will be 30), sudden death applies.

#### Service Rules
1. Service will be decided by a coin toss.
2. Serve must be made underhand, and the shuttle must be hit below the waist.
3. Excessive or exaggerated movements will be considered illegal or disruptive to the opponent's readiness.

#### Tie-Breaking Criteria
If teams have equal points after group stage matches, the following criteria will be used to determine rankings:

1. **Head-to-Head Result**: Compare the results of the matches played between the tied teams. The team with the better head-to-head record advances.
2. **Points Difference**: Calculate the difference between points scored and points conceded for each team. The team with the higher points difference advances.
3. **Points Scored**: Compare the total points scored by each team. The team with the higher total points scored advances.
4. **Lowest Points Conceded**: Compare the total points conceded by each team. The team with the lowest total points conceded advances.
5. **Fair Play Record**: If all other criteria fail to break the tie, use a fair play record (e.g., fewer fouls, warnings, or penalties).
""")

    elif st.session_state[f"{sport}_results"]:
        st.subheader("📊 Results")
        st.markdown("### 🥇 Champions of the Court")
        st.markdown("#### **Men’s Doubles**")
        st.markdown("- **🏆 Winners:** Nizam & Rakesh *(Vikings)*")
        st.markdown("- **🥈 Runners-up:** Jacob & Jazim *(Titans)*")
        st.markdown("#### **Women’s Doubles**")
        st.markdown("- **🏆 Winners:** Parvathi & Sithara *(Gladiators)*")
        st.markdown("- **🥈 Runners-up:** Dheena & Tanvi *(Spartans)*")
        st.markdown("#### **Mixed Doubles**")
        st.markdown("- **🏆 Winners:** Ashik & Sandra *(Gladiators)*")
        st.markdown("- **🥈 Runners-up:** Ananthu & Deepthi *(Spartans)*")
        try:
            # Load the fixtures CSV which also contains results
            df_matches = pd.read_csv("csv/fixture.csv")
            
            # Create tabs for different categories
            tab1, tab2, tab3 = st.tabs(["Mixed Doubles", "Women's Doubles", "Men's Doubles"])
            
            # Function to calculate team standings from matches
            def calculate_standings(category_df):
                # Create a dictionary to store team stats
                team_stats = {}
                
                # Process each match
                for _, row in category_df.iterrows():
                    team1 = row['Team 1']
                    team2 = row['Team 2']
                    score1 = row['Team 1 Score']
                    score2 = row['Team 2 Score']
                    
                    # Initialize team stats if not already present
                    for team in [team1, team2]:
                        if team not in team_stats:
                            team_stats[team] = {
                                'Team': team,
                                'Matches Played': 0,
                                'Matches Won': 0,
                                'Matches Lost': 0,
                                'Points Won': 0,
                                'Points Lost': 0,
                                'Points Difference': 0,
                                'Group': row['Group']
                            }
                    
                    # Only count completed matches (where scores are recorded)
                    if pd.notna(score1) and pd.notna(score2):
                        # Update matches played
                        team_stats[team1]['Matches Played'] += 1
                        team_stats[team2]['Matches Played'] += 1
                        
                        # Update points
                        team_stats[team1]['Points Won'] += int(score1)
                        team_stats[team1]['Points Lost'] += int(score2)
                        team_stats[team2]['Points Won'] += int(score2)
                        team_stats[team2]['Points Lost'] += int(score1)
                        
                        # Update wins/losses
                        if int(score1) > int(score2):
                            team_stats[team1]['Matches Won'] += 1
                            team_stats[team2]['Matches Lost'] += 1
                        else:
                            team_stats[team2]['Matches Won'] += 1
                            team_stats[team1]['Matches Lost'] += 1
                
                # Calculate points difference
                for team in team_stats:
                    team_stats[team]['Points Difference'] = team_stats[team]['Points Won'] - team_stats[team]['Points Lost']
                
                # Convert to DataFrame and sort
                standings_df = pd.DataFrame(list(team_stats.values()))
                if not standings_df.empty:
                    # Sort by group first, then by matches won, then by points difference
                    standings_df = standings_df.sort_values(
                        by=['Group', 'Matches Won', 'Points Difference'], 
                        ascending=[True, False, False]
                    )
                    
                    # If the DataFrame is empty or missing some columns, return an empty DataFrame with proper columns
                    if 'Team' not in standings_df.columns:
                        return pd.DataFrame(columns=['Team', 'Matches Played', 'Matches Won', 'Matches Lost', 
                                                     'Points Won', 'Points Lost', 'Points Difference', 'Group'])
                    
                    return standings_df
                else:
                    # Return empty DataFrame with correct columns
                    return pd.DataFrame(columns=['Team', 'Matches Played', 'Matches Won', 'Matches Lost', 
                                                 'Points Won', 'Points Lost', 'Points Difference', 'Group'])
            
            # Display standings for each category
            with tab1:
                st.subheader("Mixed Doubles Standings")
                mixed_matches = df_matches[df_matches['Category'] == 'Mixed']
                
                if not mixed_matches.empty:
                    mixed_standings = calculate_standings(mixed_matches)
                    
                    # Get unique groups
                    groups = mixed_standings['Group'].unique() if 'Group' in mixed_standings.columns else []
                    
                    for group in sorted(groups):
                        st.caption(f'**{group}**')
                        group_df = mixed_standings[mixed_standings['Group'] == group]
                        st.dataframe(group_df[['Team', 'Matches Played', 'Matches Won', 'Matches Lost', 
                                               'Points Won', 'Points Lost', 'Points Difference']], 
                                     use_container_width=True)
                else:
                    st.info("No match data available yet for Mixed Doubles.")
            
            with tab2:
                st.subheader("Women's Doubles Standings")
                womens_matches = df_matches[df_matches['Category'] == "Women's"]
                print(womens_matches)
                if not womens_matches.empty:
                    womens_standings = calculate_standings(womens_matches)
                    
                    # Get unique groups
                    groups = womens_standings['Group'].unique() if 'Group' in womens_standings.columns else []
                    
                    for group in sorted(groups):
                        st.caption(f'**{group}**')
                        group_df = womens_standings[womens_standings['Group'] == group]
                        st.dataframe(group_df[['Team', 'Matches Played', 'Matches Won', 'Matches Lost', 
                                              'Points Won', 'Points Lost', 'Points Difference']], 
                                    use_container_width=True)
                else:
                    st.info("No match data available yet for Women's Doubles.")
            
            with tab3:
                st.subheader("Men's Doubles Standings")
                mens_matches = df_matches[df_matches['Category'] == "Men's"]
                
                if not mens_matches.empty:
                    mens_standings = calculate_standings(mens_matches)
                    
                    # Get unique groups
                    groups = mens_standings['Group'].unique() if 'Group' in mens_standings.columns else []
                    
                    for group in sorted(groups):
                        st.caption(f'**{group}**')
                        group_df = mens_standings[mens_standings['Group'] == group]
                        st.dataframe(group_df[['Team', 'Matches Played', 'Matches Won', 'Matches Lost', 
                                              'Points Won', 'Points Lost', 'Points Difference']], 
                                    use_container_width=True)
                else:
                    st.info("No match data available yet for Men's Doubles.")
                    
            # Show recent match results
            st.subheader("Recent Match Results")
            completed_matches = df_matches[pd.notna(df_matches['Team 1 Score'])]
            if not completed_matches.empty:
                st.dataframe(
                    completed_matches[['Category', 'Group', 'Team 1', 'Team 1 Score', 'Team 2 Score', 'Team 2']], 
                    use_container_width=True
                )
            else:
                st.info("No completed matches yet.")
                
        except Exception as e:
            st.error(f"Error loading or processing results: {e}")
            st.info("Please ensure 'group_stage_matches_latest.csv' is properly formatted and available.")

# ---------- CRICKET TAB ----------
with tabs[1]:
    sport = "cricket"
    init_state(sport)
    st.header("🏏 Cricket")
    
    # Under construction banner
    st.warning("🚧 Cricket section under construction 🚧")
    
    show_buttons(sport)

    if st.session_state[f"{sport}_fixtures"]:
        st.subheader("📅 Fixtures")
        st.info("Cricket fixtures will be updated soon.")

    elif st.session_state[f"{sport}_rules"]:
        st.subheader("📜 Rules")
        st.markdown("Updates coming soon")

    elif st.session_state[f"{sport}_results"]:
        st.subheader("📊 Results")
        st.info("Results will be published after the first match.")

# ---------- FOOTBALL TAB ----------
with tabs[2]:
    sport = "football"
    init_state(sport)
    st.header("⚽ Football")
    
    # Under construction bannerS    
    show_buttons(sport)

    if st.session_state[f"{sport}_fixtures"]:
        st.subheader("📅 Fixtures")
        st.markdown("""#### Men’s 5s Fixtures

- **27-May-25**
  - ⏰ 8:00 PM – *Titans vs Spartans*  
  - ⏰ 8:30 PM – *Gladiators vs Vikings*

- **28-May-25**
  - ⏰ 8:00 PM – *Spartans vs Vikings*
  - ⏰ 8:30 PM – *Titans vs Gladiators*

- **29-May-25**
  - ⏰ 8:00 PM – *Spartans vs Gladiators*
  - ⏰ 8:30 PM – *Titans vs Vikings*

- **03-Jun-25**
  - ⏰ 8:00 PM – *Finalist 1 vs Finalist 2*

---

#### Women’s 5s Penalty Shootout Fixtures

- **29-May-25**
  - ⏰ 7:00 PM – *Gladiators vs Vikings*
  - ⏰ 7:15 PM – *Titans vs Spartans*
  - ⏰ 7:30 PM – *Titans vs Gladiators*
  - ⏰ 7:45 PM – *Spartans vs Vikings*

- **03-Jun-25**
  - ⏰ 7:00 PM – *Titans vs Vikings*
  - ⏰ 7:15 PM – *Spartans vs Gladiators*
  - ⏰ 7:45 PM – *Finalist 1 vs Finalist 2*

""")

    elif st.session_state[f"{sport}_rules"]:
        st.markdown("""
        ### Men's 5's Category – Tournament Rules ⚽

1. The tournament will follow a **league + knockout** format.
2. Team line-up for a match can have **up to 8 players**, including 5 starting players and 3 substitutes. Teams can register **up to 10 players**; only registered players will be allowed to play.
3. The team captain or designated representative must register the team before the **deadline – 20th May 2025**.
4. If a team fails to report **15 minutes before** the match start time, it will be considered a **walk-over**.
5. **Rolling substitutions** are allowed throughout the game, with no restrictions on the number.
6. Substitutions can be made during play or during breaks in the game.
7. There will be **no offside rule**.
8. If the ball leaves the pitch, **kick-in** from the sideline.
9. All **restarts after goals** are from the **middle of the field**.
10. Players can pass the ball to their own keeper, but the **goalkeeper is not allowed to pick it up** (standard back-pass rule applies).
11. In the **semi-final or final**, if a match ends in a draw, it will proceed to a **penalty shootout**. If the shootout remains tied after the initial 3 kicks, it will proceed to **sudden death**.
12. The goalkeeper must release the ball **within 6 seconds** of gaining control. Players taking throw-ins must also release the ball within 6 seconds of receiving it.
13. Goalkeeper's **throwing range** is limited to the **center of the pitch**.
14. For the penalty shootout, **only on-field players** are allowed to take the kick.
15. Players must wear **football jerseys with numbers**. Goalkeeper jersey color should be **different** from other players.
16. **Turf football boots** are required, and **shin guards are recommended**.
17. Any **walkover or disqualification** is considered a **3-0 win** for the opposition.
18. If a team **walks out in protest** during playtime, they will be **disqualified** from the tournament.
19. A player receiving **two yellow cards** in a single match will be shown a **red card** and will **miss the next match**.
20. The organizers will **not be responsible for any injuries** that may occur during the game.
21. The **committee members** have the ultimate authority to make decisions regarding any **changes or postponements**.
22. **Referee decisions are final** for all matches.
23. If **two teams end up with the same point** , League standing will be based the below order 
    - Goal difference
    - Goals scored
    - Head to head
    - Goals conceded
    - Fair play (Based on yellow and red cards)

---

### Women's Penalty Shootout – Tournament Rules 🥅

1. Each team will consist of a total of **5 players**, including a **goalkeeper**.
2. Teams may have **up to 3 additional reserve players**, if desired.
3. All matches, including the **group stage, semi-final, and final**, will be conducted as **penalty shootouts**.
    - Each team will take a series of **5 penalty kicks** to determine the winner.
    - The team with the **most goals** at the end of the shootout will be declared the winner.
4. If a match ends in a **tie** during the **knockout stage**, semi-final, or final, a **sudden-death penalty shootout** will take place.
    - Teams will alternate penalty kicks.
    - The **first team to score while the other misses** will be declared the winner.
5. The **committee members** have the ultimate authority to make decisions regarding any **changes or postponements**.
6. **Referee decisions are final** for all matches.
""")

    elif st.session_state[f"{sport}_results"]:
        st.subheader("📊 Results")
        mens_fixtures = [
                {"Date": "27-May-25", "Time": "8:00 PM", "Team 1": "Titans", "Team 2": "Spartans","Winner":""},
                {"Date": "27-May-25", "Time": "8:30 PM", "Team 1": "Gladiators", "Team 2": "Vikings","Winner":""},
                {"Date": "28-May-25", "Time": "8:00 PM", "Team 1": "Spartans", "Team 2": "Vikings","Winner":""},
                {"Date": "28-May-25", "Time": "8:30 PM", "Team 1": "Titans", "Team 2": "Gladiators","Winner":""},
                {"Date": "29-May-25", "Time": "8:00 PM", "Team 1": "Spartans", "Team 2": "Gladiators","Winner":""},
                {"Date": "29-May-25", "Time": "8:30 PM", "Team 1": "Titans", "Team 2": "Vikings","Winner":""},
                {"Date": "03-Jun-25", "Time": "8:00 PM", "Team 1": "Finalist 1", "Team 2": "Finalist 2","Winner":""},
            ]

        df_mens = pd.DataFrame(mens_fixtures)
        st.markdown("### Men's 5s Results")
        st.dataframe(df_mens, use_container_width=True)

        # Women's 5s Fixtures
        womens_fixtures = [
                {"Date": "29-May-25", "Time": "7:00 PM", "Team 1": "Gladiators", "Team 2": "Vikings","Winner":""},
                {"Date": "29-May-25", "Time": "7:15 PM", "Team 1": "Titans", "Team 2": "Spartans","Winner":""},
                {"Date": "29-May-25", "Time": "7:30 PM", "Team 1": "Titans", "Team 2": "Gladiators","Winner":""},
                {"Date": "29-May-25", "Time": "7:45 PM", "Team 1": "Spartans", "Team 2": "Vikings","Winner":""},
                {"Date": "03-Jun-25", "Time": "7:00 PM", "Team 1": "Titans", "Team 2": "Vikings","Winner":""},
                {"Date": "03-Jun-25", "Time": "7:15 PM", "Team 1": "Spartans", "Team 2": "Gladiators","Winner":""},
                {"Date": "03-Jun-25", "Time": "7:45 PM", "Team 1": "Finalist 1", "Team 2": "Finalist 2","Winner":""},
            ]
        st.markdown("### Women's 5s Results")
        df_womens = pd.DataFrame(womens_fixtures)
        st.dataframe(df_womens, use_container_width=True)



# ---------- TABLE TENNIS TAB ----------
with tabs[3]:
    sport = "tt"
    init_state(sport)
    st.header("🏓 Table Tennis")
    
    # Under construction banner    
    show_buttons(sport)

    if st.session_state[f"{sport}_fixtures"]:
        st.subheader("📅 Fixtures")
        st.markdown("""
### 🗓 21 July – MD 1 (Women)
- Deepthi – Sarah Jacob vs Parvathi Ambareesh – Arya Suresh  
- Gopika – Neena vs Ann Maria Malekunnel & Riya Shanavas  
- Pappy – Sandra vs Sithara – Pravitha  
- Karthi Ashok & Swetha Shenoy vs Ginu George & Amrutha Dinesh  

---

### 🗓 22 July – MD 2 (Women)
- Deepthi – Sarah Jacob vs Gopika – Neena  
- Parvathi Ambareesh – Arya Suresh vs Surya – Aleena  
- Pappy – Sandra vs Karthi Ashok & Swetha Shenoy  
- Sithara – Pravitha vs Merin – Sneha  

---

### 🗓 23 July – MD 3 (Women)
- Ann Maria Malekunnel & Riya Shanavas vs Surya – Aleena  
- Ginu George & Amrutha Dinesh vs Merin – Sneha  
- Deepthi – Sarah Jacob vs Ann Maria Malekunnel & Riya Shanavas  
- Pappy – Sandra vs Ginu George & Amrutha Dinesh  

---

### 🗓 24 July – MD 4 (Women)
- Parvathi Ambareesh – Arya Suresh vs Gopika – Neena  
- Surya – Aleena vs Gopika – Neena  
- Sithara – Pravitha vs Karthi Ashok & Swetha Shenoy  
- Merin – Sneha vs Karthi Ashok & Swetha Shenoy  

---

### 🗓 28 July – MD 5 (Women)
- Deepthi – Sarah Jacob vs Surya – Aleena  
- Parvathi Ambareesh – Arya Suresh vs Ann Maria Malekunnel & Riya Shanavas  
- Pappy – Sandra vs Merin – Sneha  
- Sithara – Pravitha vs Ginu George & Amrutha Dinesh  

---

### 🗓 29 July – MD 1 (Men)
- Aljo Ajith – Sajith MS vs Emmanuel Joseph – Alan  
- John – Jacob vs Rohaan George R & Shashi Salian  
- Adithya – Deepaklal vs Doeny – Ganesh  
- Jazim – Neeraj vs Akshay – Akash  

---

### 🗓 30 July – MD 2 (Men)
- Aljo Ajith – Sajith MS vs John – Jacob  
- Emmanuel Joseph – Alan vs Ashiq Mohammed & Sooraj Paul  
- Adithya – Deepaklal vs Jazim – Neeraj  
- Doeny – Ganesh vs Sidharth Nair & Pankaj Sherry Paret  

---

### 🗓 31 July – MD 3 (Men)
- Rohaan George R & Shashi Salian vs Ashiq Mohammed & Sooraj Paul  
- Aljo Ajith – Sajith MS vs Rohaan George R & Shashi Salian  
- Akshay – Akash vs Sidharth Nair & Pankaj Sherry Paret  
- Adithya – Deepaklal vs Akshay – Akash  

---

### 🗓 4 August – MD 4 (Men)
- Emmanuel Joseph – Alan vs John – Jacob  
- Ashiq Mohammed & Sooraj Paul vs John – Jacob  
- Doeny – Ganesh vs Jazim – Neeraj  
- Sidharth Nair & Pankaj Sherry Paret vs Jazim – Neeraj  

---

### 🗓 5 August – MD 5 (Men)
- Aljo Ajith – Sajith MS vs Ashiq Mohammed & Sooraj Paul  
- Emmanuel Joseph – Alan vs Rohaan George R & Shashi Salian  
- Adithya – Deepaklal vs Sidharth Nair & Pankaj Sherry Paret  
- Doeny – Ganesh vs Akshay – Akash  
""")

    elif st.session_state[f"{sport}_rules"]:
        st.subheader("📜 Rules")
        st.markdown("""
    ### Game Scoring
    - Games are played to **11 points**.
    - A team must win by at least **2 points**.
    - Matches are typically **best of 3 games**.

    ### Service Rules
    - Players alternate serves every **2 points**.
    - At **10-10 (deuce)**, service alternates **every point**.
    - To serve:
    - Toss the ball at least **6 inches (15 cm)** straight up from an **open palm**.
    - Strike it **on the way down**.
    - The serve must **bounce first on the server's side**, then on the **opponent's side**.
    - In **doubles**:
    - The serve must go from the **server's right court** to the **receiver's right court**.
    - **Partners must alternate hits** during a rally.

    ### Let Serves
    - If a serve **touches the net** but still lands correctly, it's a **"let"** and is replayed.
    - A total of **3 lets** are allowed.
    - After the **third let**, the **opponent is awarded a point**.

    ### Rally Rules
    - **Volleys are not allowed** — the ball must **bounce on your side** before you hit it.
    - If your shot **bounces back over the net without being touched** (due to spin), **you win the point**.
    - **Touching the ball** with your **paddle hand** (including fingers and hand below the wrist) is **allowed**.
    - Touching the ball with **any other part of the body** results in a **point for the opponent**.

    ### Table Contact
    - You may **not touch the table with your non-paddle hand** during play.
    - Touching the table with the **paddle hand** or **other parts of the body** is **allowed**, **as long as it doesn't move the table**.
    """)

    elif st.session_state[f"{sport}_results"]:
        st.subheader("📊 Results")
        st.info("No matches played yet.")

# ---------- CARROMS TAB ----------
with tabs[4]:
    sport = "carroms"
    init_state(sport)
    st.header("🎯 Carroms")
    
    # Under construction banner
    st.warning("🚧 Carroms section under construction 🚧")
    
    show_buttons(sport)

    if st.session_state[f"{sport}_fixtures"]:
        st.subheader("📅 Fixtures")
        st.info("Carroms fixtures will be updated soon.")

    elif st.session_state[f"{sport}_rules"]:
        st.subheader("📜 Rules")
        st.markdown("Updates coming soon")

    elif st.session_state[f"{sport}_results"]:
        st.subheader("📊 Results")
        st.info("Updates coming soon")

# ---------- Basket TAB ----------
with tabs[5]:
    sport = "Basket Ball"
    init_state(sport)
    st.header("Basket Ball")
    
    # Under construction banner
    st.warning("🚧 Basket Ball section under construction 🚧")
    
    show_buttons(sport)

    if st.session_state[f"{sport}_fixtures"]:
        st.subheader("📅 Fixtures")
        st.info("Basket Ball fixtures will be updated soon.")

    elif st.session_state[f"{sport}_rules"]:
        st.subheader("📜 Rules")
        st.markdown("Updates coming soon")

    elif st.session_state[f"{sport}_results"]:
        st.subheader("📊 Results")
        st.info("Updates coming soon")

# ---------- Volley TAB ----------
with tabs[6]:
    sport = "Volley Ball"
    init_state(sport)
    st.header("Volley Ball")
    
    # Under construction banner
    st.warning("🚧 Volley Ball section under construction 🚧")
    
    show_buttons(sport)

    if st.session_state[f"{sport}_fixtures"]:
        st.subheader("📅 Fixtures")
        st.info("Volley Ball fixtures will be updated soon.")

    elif st.session_state[f"{sport}_rules"]:
        st.subheader("📜 Rules")
        st.markdown("Updates coming soon")

    elif st.session_state[f"{sport}_results"]:
        st.subheader("📊 Results")
        st.info("Updates coming soon")

# Footer with page info
st.markdown("---")
st.caption("PAI Premier League 2025 Season 1 - Updated: May 2025")