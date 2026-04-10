import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Smart Habit Tracker", layout="wide")

st.title("✅ Smart Habit Tracker")

# ---------------- SESSION STATE ----------------
if "habits" not in st.session_state:
    st.session_state.habits = []

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Settings")

username = st.sidebar.text_input("Enter your name", "User")

st.sidebar.subheader("🎯 Goals")
weekly_goal = st.sidebar.slider("Weekly Goal (days)", 1, 7, 5)
daily_target = st.sidebar.number_input("Daily Habit Target", 1, 10, 3)

st.sidebar.subheader("📊 Progress Summary")

total_habits = len(st.session_state.habits)
completed_today = sum([sum(habit["days"].values()) for habit in st.session_state.habits])

if total_habits > 0:
    completion_rate = (completed_today / (total_habits * 7)) * 100
else:
    completion_rate = 0

st.sidebar.write(f"Total Habits: {total_habits}")
st.sidebar.write(f"Completed: {completed_today}")
st.sidebar.write(f"Completion %: {round(completion_rate, 2)}%")

# ---------------- MOTIVATION ----------------
affirmations = [
    "🔥 You're building consistency!",
    "💪 Small steps = big results",
    "🌱 Growth takes time—keep going!",
    "🚀 You're ahead of yesterday!",
    "🏆 Discipline > Motivation",
    "✨ Keep showing up!",
    "📈 Progress, not perfection",
    "💯 You got this!",
    "🧠 Habits shape your future",
]

st.sidebar.subheader("🔔 Motivation")
if st.sidebar.button("Get Motivation"):
    st.sidebar.success(random.choice(affirmations))

# ---------------- RESET BUTTON ----------------
if st.sidebar.button("🗑️ Reset All Habits"):
    st.session_state.habits = []
    st.sidebar.warning("All habits cleared!")

# ---------------- MAIN APP ----------------
st.subheader(f"Welcome, {username}! 👋")

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# --- ADD HABIT ---
st.subheader("➕ Add New Habit")
habit_name = st.text_input("Habit Name")

if st.button("Add Habit"):
    if habit_name:
        new_habit = {
            "name": habit_name,
            "days": {day: False for day in days}
        }
        st.session_state.habits.append(new_habit)
        st.success("Habit added successfully! 🎉")

# --- DISPLAY HABITS ---
st.subheader("📅 Track Your Habits")

for i, habit in enumerate(st.session_state.habits):
    st.write(f"### {habit['name']}")
    
    cols = st.columns(7)
    for j, day in enumerate(days):
        habit["days"][day] = cols[j].checkbox(day[:3], habit["days"][day], key=f"{i}_{day}")

# ---------------- DATAFRAME VIEW ----------------
st.subheader("📊 Weekly Overview")

if st.session_state.habits:
    df = pd.DataFrame([
        {"Habit": habit["name"], **habit["days"]}
        for habit in st.session_state.habits
    ])
    st.dataframe(df)
