import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Habit Tracker", layout="wide")

# ---------------- CUSTOM UI ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0F172A, #020617);
}

section[data-testid="stSidebar"] {
    background-color: #020617;
    border-right: 1px solid #1E293B;
}

h1 {
    color: #F8FAFC;
    font-weight: 700;
}

h2, h3 {
    color: #E2E8F0;
}

.stButton>button {
    background: linear-gradient(135deg, #6366F1, #8B5CF6);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 10px 18px;
    transition: 0.25s;
}

.stButton>button:hover {
    transform: scale(1.05);
}

.stTextInput>div>div>input {
    background-color: #020617;
    color: white;
    border-radius: 10px;
    border: 1px solid #1E293B;
}

.stSuccess, .stInfo {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "habits" not in st.session_state:
    st.session_state.habits = []

# ---------------- SIDEBAR ----------------
st.sidebar.title("Dashboard")

username = st.sidebar.text_input("Name", "User")

st.sidebar.subheader("Goals")
weekly_goal = st.sidebar.slider("Weekly Goal", 1, 7, 5)

# Graph controls
st.sidebar.subheader("Graphs")
show_graphs = st.sidebar.checkbox("Show Graphs", True)
graph_type = st.sidebar.selectbox("Type", ["Bar", "Line", "Both"])

# Affirmations
affirmations = [
    "You're unstoppable.",
    "Consistency wins.",
    "Small steps matter.",
    "Keep going.",
    "You're improving daily.",
    "Discipline = freedom.",
    "Stay focused.",
    "Progress > perfection.",
    "You got this.",
    "Keep showing up.",
    "You're building something great.",
    "One step at a time.",
    "Stay locked in.",
    "No excuses.",
    "Keep grinding."
]

if st.sidebar.button("Motivate me"):
    st.sidebar.success(random.choice(affirmations))

if st.sidebar.button("Reset"):
    st.session_state.habits = []
    st.sidebar.warning("Data cleared")

# ---------------- MAIN ----------------
st.title("Habit Tracker")
st.write("")

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# Add habit
st.subheader("Add Habit")
habit_name = st.text_input("")

if st.button("Add"):
    if habit_name:
        st.session_state.habits.append({
            "name": habit_name,
            "days": {d: False for d in days}
        })
        st.toast("Habit added ✔️")
        st.toast(random.choice(affirmations))

st.write("")

# Track habits
st.subheader("Your Habits")

total_completed = 0

for i, habit in enumerate(st.session_state.habits):
    st.write(f"**{habit['name']}**")
    
    cols = st.columns(7)
    for j, d in enumerate(days):
        habit["days"][d] = cols[j].checkbox("", habit["days"][d], key=f"{i}{d}")
    
    completed = sum(habit["days"].values())
    total_completed += completed

st.write("")

# Table
if st.session_state.habits:
    df = pd.DataFrame([
        {"Habit": h["name"], **h["days"]}
        for h in st.session_state.habits
    ])
    
    st.subheader("Overview")
    st.dataframe(df)

# ---------------- GRAPHS ----------------
if show_graphs and st.session_state.habits:

    st.subheader("Progress")

    habit_progress = {
        h["name"]: sum(h["days"].values())
        for h in st.session_state.habits
    }

    progress_df = pd.DataFrame(
        list(habit_progress.items()),
        columns=["Habit", "Done"]
    )

    daily_counts = {d: 0 for d in days}
    for h in st.session_state.habits:
        for d in days:
            if h["days"][d]:
                daily_counts[d] += 1

    daily_df = pd.DataFrame(
        list(daily_counts.items()),
        columns=["Day", "Count"]
    )

    if graph_type == "Bar":
        st.bar_chart(progress_df.set_index("Habit"))

    elif graph_type == "Line":
        st.line_chart(daily_df.set_index("Day"))

    else:
        st.bar_chart(progress_df.set_index("Habit"))
        st.line_chart(daily_df.set_index("Day"))

# ---------------- BADGES ----------------
st.subheader("Badges")

badges = []

if total_completed >= 3:
    badges.append("Beginner")
if total_completed >= 10:
    badges.append("Consistent")
if total_completed >= 20:
    badges.append("Master")
if total_completed >= 30:
    badges.append("Elite")

if badges:
    st.write(" | ".join(badges))
else:
    st.write("No badges yet")

# ---------------- SUMMARY ----------------
st.subheader("Summary")

total_habits = len(st.session_state.habits)
max_possible = total_habits * 7

percent = (total_completed / max_possible * 100) if max_possible else 0

st.write(f"Habits: {total_habits}")
st.write(f"Completed: {total_completed}")
st.write(f"Progress: {round(percent,1)}%")

st.write("---")
st.caption("Keep going.")
