import streamlit as st
import pandas as pd

# Custom CSS to improve font size and styling
st.markdown("""
    <style>
        /* Title Styling */
        .title {
            font-size: 36px !important;
            font-weight: bold;
            color: #4CAF50;
            text-align: center;
            margin-bottom: 30px;
        }

        /* Section Header Styling */
        .section-header {
            font-size: 32px !important;
            font-weight: 600;
            color: #333333;
            margin-bottom: 25px;
            text-align: center;
        }

        /* Subsection Header Styling */
        .subsection-header {
            font-size: 28px !important;
            font-weight: 500;
            margin-bottom: 20px;
            color: #4CAF50;
        }

        /* Text and Form Input Styling */
        .stTextInput, .stTextArea, .stNumberInput {
            font-size: 20px !important;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #DDD;
        }

        .stSelectbox, .stMultiselect {
            font-size: 20px !important;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #DDD;
        }

        /* Button Styling */
        .stButton button {
            font-size: 20px !important;
            padding: 12px 25px;
            border-radius: 8px;
            background-color: #4CAF50;
            color: white;
            border: none;
            box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.1);
            cursor: pointer;
        }

        .stButton button:hover {
            background-color: #45a049;
            box-shadow: 0px 5px 20px rgba(0, 0, 0, 0.15);
        }

        /* Dataframe Styling */
        .stDataFrame {
            font-size: 20px !important;
            border-radius: 5px;
            border: 1px solid #DDD;
            box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.1);
        }

        /* Sidebar Styling */
        .sidebar .sidebar-content {
            font-size: 20px !important;
            padding: 15px;
            color: #333;
        }

        .sidebar .sidebar-header {
            font-size: 24px !important;
            color: #4CAF50;
            font-weight: bold;
            text-align: center;
        }

        /* Increase margin between sections */
        .stContainer {
            margin-top: 40px;
            margin-bottom: 40px;
        }

        /* Form Containers */
        .stForm {
            margin-bottom: 20px;
        }

        /* Margin for each section */
        .stMarkdown {
            margin-bottom: 30px;
        }

        /* Table Row Hover Effect */
        .stDataFrame .dataframe tbody tr:hover {
            background-color: #f5f5f5;
        }
        
        /* Adding rounded borders to form inputs */
        .stTextInput input, .stNumberInput input {
            border-radius: 5px;
            padding: 10px;
        }

    </style>
""", unsafe_allow_html=True)

# Initialize session state for storing global data
if 'contestants' not in st.session_state:
    st.session_state.contestants = pd.DataFrame({
        'ID': [1, 2, 3],
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Skills': ['Dance, Instrumental', 'Performance, Music', 'Dance, Music']
    })

if 'judges' not in st.session_state:
    st.session_state.judges = pd.DataFrame({
        'ID': [1, 2],
        'Name': ['Judge1', 'Judge2'],
        'Skills Judged': ['Dance, Music', 'Instrumental, Performance']
    })

if 'skill_weights' not in st.session_state:
    st.session_state.skill_weights = {'Dance': 30, 'Instrumental': 20, 'Performance': 25, 'Music': 25}

if 'scores' not in st.session_state:
    st.session_state.scores = pd.DataFrame(columns=['Judge', 'Contestant', 'Skill', 'Score'])

# Function to add scores by judges
def update_scores(judge_name, contestant_name, skill, score):
    new_score = pd.DataFrame([[judge_name, contestant_name, skill, score]], columns=['Judge', 'Contestant', 'Skill', 'Score'])
    st.session_state.scores = pd.concat([st.session_state.scores, new_score], ignore_index=True)

# Function to compute final scores
def calculate_final_scores():
    final_scores = {}
    for _, row in st.session_state.scores.iterrows():
        contestant = row['Contestant']
        score = row['Score'] * st.session_state.skill_weights.get(row['Skill'], 0) / 100
        if contestant not in final_scores:
            final_scores[contestant] = 0
        final_scores[contestant] += score
    return final_scores

# Application UI
def main():
    st.markdown('<div class="title">Competition Scoring System</div>', unsafe_allow_html=True)

    # Tabs for Admin and Judge
    roles = ['Admin', 'Judge']
    role = st.sidebar.selectbox("Select Role", roles)

    if role == 'Admin':
        admin_view()

    elif role == 'Judge':
        judge_view()

# Admin View: Admin can create contestants, judges, and modify data
def admin_view():
    st.markdown('<div class="section-header">Admin Panel</div>', unsafe_allow_html=True)

    st.subheader("Manage Contestants")
    contestant_options = st.selectbox("Select Contestant to Modify or Remove", st.session_state.contestants['Name'].tolist() + ["Add New Contestant"])
    
    if contestant_options == "Add New Contestant":
        with st.form("contestant_form"):
            contestant_name = st.text_input("Enter Contestant Name", max_chars=50)
            contestant_skills = st.text_input("Enter Contestant Skills (comma separated)", max_chars=100)
            submit = st.form_submit_button("Add Contestant")
            if submit:
                new_contestant = pd.DataFrame([[len(st.session_state.contestants)+1, contestant_name, contestant_skills]], 
                                              columns=['ID', 'Name', 'Skills'])
                st.session_state.contestants = pd.concat([st.session_state.contestants, new_contestant], ignore_index=True)
                st.success("Contestant added!")
    else:
        selected_contestant = st.session_state.contestants[st.session_state.contestants['Name'] == contestant_options]
        st.write("Selected Contestant Details")
        st.write(selected_contestant)
        
        # Option to Remove or Edit the Contestant
        action = st.radio("Choose Action", ['Edit Contestant', 'Remove Contestant'])
        
        if action == 'Edit Contestant':
            with st.form("edit_contestant_form"):
                new_name = st.text_input("Edit Name", value=selected_contestant['Name'].values[0])
                new_skills = st.text_input("Edit Skills (comma separated)", value=selected_contestant['Skills'].values[0])
                submit = st.form_submit_button("Update Contestant")
                if submit:
                    st.session_state.contestants.loc[st.session_state.contestants['Name'] == contestant_options, 'Name'] = new_name
                    st.session_state.contestants.loc[st.session_state.contestants['Name'] == contestant_options, 'Skills'] = new_skills
                    st.success("Contestant updated!")
        elif action == 'Remove Contestant':
            st.session_state.contestants = st.session_state.contestants[st.session_state.contestants['Name'] != contestant_options]
            st.success(f"Contestant {contestant_options} removed!")

    st.write("Contestant List")
    st.dataframe(st.session_state.contestants)

    st.subheader("Manage Judges")
    judge_options = st.selectbox("Select Judge to Modify or Remove", st.session_state.judges['Name'].tolist() + ["Add New Judge"])
    
    if judge_options == "Add New Judge":
        with st.form("judge_form"):
            judge_name = st.text_input("Enter Judge Name", max_chars=50)
            judge_skills = st.text_input("Enter Judge Skills (comma separated)", max_chars=100)
            submit = st.form_submit_button("Add Judge")
            if submit:
                new_judge = pd.DataFrame([[len(st.session_state.judges)+1, judge_name, judge_skills]],
                                         columns=['ID', 'Name', 'Skills Judged'])
                st.session_state.judges = pd.concat([st.session_state.judges, new_judge], ignore_index=True)
                st.success("Judge added!")
    else:
        selected_judge = st.session_state.judges[st.session_state.judges['Name'] == judge_options]
        st.write("Selected Judge Details")
        st.write(selected_judge)
        
        # Option to Remove or Edit the Judge
        action = st.radio("Choose Action", ['Edit Judge', 'Remove Judge'])
        
        if action == 'Edit Judge':
            with st.form("edit_judge_form"):
                new_name = st.text_input("Edit Name", value=selected_judge['Name'].values[0])
                new_skills = st.text_input("Edit Skills (comma separated)", value=selected_judge['Skills Judged'].values[0])
                submit = st.form_submit_button("Update Judge")
                if submit:
                    st.session_state.judges.loc[st.session_state.judges['Name'] == judge_options, 'Name'] = new_name
                    st.session_state.judges.loc[st.session_state.judges['Name'] == judge_options, 'Skills Judged'] = new_skills
                    st.success("Judge updated!")
        elif action == 'Remove Judge':
            st.session_state.judges = st.session_state.judges[st.session_state.judges['Name'] != judge_options]
            st.success(f"Judge {judge_options} removed!")

    st.write("Judge List")
    st.dataframe(st.session_state.judges)

    st.subheader("Skill Weights Management")
    for skill in st.session_state.skill_weights:
        weight = st.number_input(f"Weight for {skill}", min_value=1, max_value=100, value=st.session_state.skill_weights[skill])
        st.session_state.skill_weights[skill] = weight

    st.write("Current Skill Weights")
    st.write(st.session_state.skill_weights)

# Judge View: Judges can score contestants based on skills
def judge_view():
    st.markdown('<div class="section-header">Judge Panel</div>', unsafe_allow_html=True)
    
    judge_name = st.selectbox("Select Judge", st.session_state.judges['Name'].tolist())
    
    if judge_name:
        contestant_name = st.selectbox("Select Contestant", st.session_state.contestants['Name'].tolist())
        skill = st.selectbox("Select Skill", ['Dance', 'Instrumental', 'Performance', 'Music'])
        score = st.slider("Give Score (1-100)", min_value=1, max_value=100)
        
        if st.button("Submit Score"):
            update_scores(judge_name, contestant_name, skill, score)
            st.success("Score submitted successfully!")

        st.write("Scores Submitted:")
        st.dataframe(st.session_state.scores)

if __name__ == "__main__":
    main()
