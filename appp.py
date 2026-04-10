import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Smart Habit Tracker", layout="wide")

st.title("🚀 Smart Habit Tracker Pro")

# ---------------- SESSION STATE ----------------
if "habits" not in st.session_state:
    st.session_state.habits = []

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Settings")

username = st.sidebar.text_input("Enter your name", "User")

st.sidebar.subheader("🎯 Goals")
weekly_goal = st.sidebar.slider("Weekly Goal (days)", 1, 7, 5)

# ---------------- GRAPH SETTINGS ----------------
st.sidebar.subheader("📊 Graph Settings")

show_graphs = st.sidebar.checkbox("Show Graphs", value=True)

graph_type = st.sidebar.selectbox(
    "Select Graph Type",
    ["Bar Chart", "Line Chart", "Both"]
)

# ---------------- AFFIRMATIONS ----------------
affirmations = [
    "🔥 You're unstoppable!",
    "💪 Discipline is your superpower!",
    "🌱 You are growing every day!",
    "🚀 Keep leveling up!",
    "🏆 Winners show up daily!",
    "✨ Consistency beats motivation!",
    "📈 You're improving 1% daily!",
    "💯 Stay locked in!",
    "🧠 Your future self thanks you!",
    "⚡ Small habits, massive change!",
    "🎯 Focus = Results!",
    "🔥 You're building momentum!",
    "🌟 Keep shining!",
    "💥 No excuses, just progress!",
    "🏅 You're doing better than you think!"
]

st.sidebar.subheader("🔔 Motivation")
if st.sidebar.button("Get Motivation"):
    st.sidebar.success(random.choice(affirmations))

# ---------------- RESET ----------------
if st.sidebar.button("🗑️ Reset All"):
    st.session_state.habits = []
    st.sidebar.warning("All habits cleared!")

# ---------------- MAIN ----------------
st.subheader(f"Welcome, {username}! 👋")

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# ---------------- ADD HABIT ----------------
st.subheader("➕ Add New Habit")
habit_name = st.text_input("Habit Name")

if st.button("Add Habit"):
    if habit_name:
        new_habit = {
            "name": habit_name,
            "days": {day: False for day in days}
        }
        st.session_state.habits.append(new_habit)
        st.success("Habit added! 🎉")
        st.info(random.choice(affirmations))

# ---------------- DISPLAY HABITS ----------------
st.subheader("📅 Track Your Habits")

total_completed = 0

for i, habit in enumerate(st.session_state.habits):
    st.write(f"### {habit['name']}")
    
    cols = st.columns(7)
    for j, day in enumerate(days):
        habit["days"][day] = cols[j].checkbox(
            day, 
            habit["days"][day], 
            key=f"{i}_{day}"
        )
    
    completed = sum(habit["days"].values())
    total_completed += completed

# ---------------- DATAFRAME ----------------
if st.session_state.habits:
    df = pd.DataFrame([
        {"Habit": h["name"], **h["days"]}
        for h in st.session_state.habits
    ])
    
    st.subheader("📊 Weekly Table")
    st.dataframe(df)

# ---------------- GRAPHS (CONTROLLED BY SIDEBAR) ----------------
if show_graphs and st.session_state.habits:

    st.subheader("📊 Progress Graphs")

    # Habit-wise completion
    habit_progress = {
        h["name"]: sum(h["days"].values())
        for h in st.session_state.habits
    }

    progress_df = pd.DataFrame(
        list(habit_progress.items()),
        columns=["Habit", "Completed Days"]
    )

    # Daily completion
    daily_counts = {day: 0 for day in days}
    for h in st.session_state.habits:
        for day in days:
            if h["days"][day]:
                daily_counts[day] += 1

    daily_df = pd.DataFrame(
        list(daily_counts.items()),
        columns=["Day", "Completed Habits"]
    )

    # Show graphs based on selection
    if graph_type == "Bar Chart":
        st.write("### 📈 Habit Completion")
        st.bar_chart(progress_df.set_index("Habit"))

    elif graph_type == "Line Chart":
        st.write("### 📅 Daily Consistency")
        st.line_chart(daily_df.set_index("Day"))

    elif graph_type == "Both":
        st.write("### 📈 Habit Completion")
        st.bar_chart(progress_df.set_index("Habit"))

        st.write("### 📅 Daily Consistency")
        st.line_chart(daily_df.set_index("Day"))

# ---------------- BADGES ----------------
st.subheader("🏆 Your Badges")

badges = []

if total_completed >= 3:
    badges.append("🥉 Beginner")
if total_completed >= 10:
    badges.append("🥈 Consistent")
if total_completed >= 20:
    badges.append("🥇 Habit Master")
if total_completed >= 30:
    badges.append("👑 Discipline King/Queen")

if badges:
    for b in badges:
        st.success(f"Unlocked: {b}")
else:
    st.info("Complete habits to unlock badges!")

# ---------------- SUMMARY ----------------
st.subheader("📌 Summary")

total_habits = len(st.session_state.habits)
max_possible = total_habits * 7

percent = (total_completed / max_possible * 100) if max_possible > 0 else 0

st.write(f"Total Habits: {total_habits}")
st.write(f"Completed: {total_completed}")
st.write(f"Progress: {round(percent, 2)}%")

# ---------------- FOOTER ----------------
st.write("---")
st.caption("🚀 Built with Streamlit | Keep Grinding!")
