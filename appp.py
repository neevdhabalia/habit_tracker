import streamlit as st
import pandas as pd
import random

st.title("✅ Smart Habit Tracker")

# Initialize session state
if "habits" not in st.session_state:
    st.session_state.habits = []

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# ---------------- AFFIRMATION LISTS ----------------
add_msgs = [
    "🌱 Every big change starts small!",
    "🚀 You're taking control of your life!",
    "💪 One habit closer to your best self!",
    "🔥 This is how success begins!",
    "✨ Future you will thank you for this!",
    "📈 Small habits → Big results!",
    "🧠 You're building discipline!",
    "🎯 Great choice! Stay consistent!",
    "⚡ Action beats intention — well done!",
    "🌟 You're leveling up!"
]

high_msgs = [
    "🔥 You're unstoppable right now!",
    "🚀 You're in the top 1% of consistency!",
    "💪 Discipline like this guarantees success!",
    "🏆 You're proving to yourself that you can do it!",
    "⚡ This level of focus is rare — keep it!",
    "🎯 You're not motivated, you're disciplined!",
    "🌟 You're becoming the person you wanted to be!",
    "🔥 This is what winning looks like!"
]

mid_msgs = [
    "👍 You're on the right track!",
    "📈 Progress is happening — don’t stop!",
    "💡 Stay consistent, results are coming!",
    "🚶 Keep going, you're building momentum!",
    "🌱 You're improving every single day!",
    "🎯 You're closer than you think!",
    "💪 Keep showing up — that's what matters!"
]

low_msgs = [
    "⚠️ It's okay to start slow — just don’t stop.",
    "🌱 Small steps still move you forward.",
    "💭 Tomorrow is a fresh start — use it.",
    "🔥 Discipline begins when motivation fades.",
    "⏳ You don’t need perfection, just effort.",
    "🚶 Start again — that's how winners are made.",
    "💡 One good day can change everything.",
    "⚡ Reset. Refocus. Go again."
]

# ---------------- ADD HABIT ----------------
st.header("➕ Add New Habit")

with st.form("habit_form"):
    habit_name = st.text_input("Habit Name")
    submitted = st.form_submit_button("Add Habit")

    if submitted:
        if habit_name:
            st.session_state.habits.append({
                "Habit": habit_name,
                **{day: False for day in days}
            })
            st.success("Habit added!")
            st.info(random.choice(add_msgs))

# ---------------- TRACK HABITS ----------------
st.header("📅 Track Your Week")

if len(st.session_state.habits) == 0:
    st.info("No habits added yet!")
else:
    df = pd.DataFrame(st.session_state.habits)

    for i, habit in df.iterrows():
        st.subheader(habit["Habit"])

        cols = st.columns(7)

        for j, day in enumerate(days):
            with cols[j]:
                checked = st.checkbox(day[:3], value=habit[day], key=f"{i}_{day}")
                st.session_state.habits[i][day] = checked

# ---------------- PROGRESS ----------------
st.header("📊 Progress Overview")

if len(st.session_state.habits) > 0:
    df = pd.DataFrame(st.session_state.habits)

    progress_data = []

    for _, row in df.iterrows():
        completed = sum([row[day] for day in days])
        percent = (completed / 7) * 100

        progress_data.append({
            "Habit": row["Habit"],
            "Progress (%)": percent
        })

    progress_df = pd.DataFrame(progress_data)

    st.dataframe(progress_df, use_container_width=True)

    st.subheader("📊 Habit Progress Chart")
    st.bar_chart(progress_df.set_index("Habit"))

    st.subheader("📈 Weekly Comparison View")
    st.line_chart(progress_df.set_index("Habit"))

# ---------------- SMART FEEDBACK ----------------
st.header("🧠 Smart Feedback")

if len(st.session_state.habits) > 0:
    avg_progress = progress_df["Progress (%)"].mean()

    if avg_progress >= 80:
        st.success("Excellent work! You're highly consistent!")
        st.success(random.choice(high_msgs))

    elif avg_progress >= 50:
        st.info("You're doing well, but there's room to improve.")
        st.info(random.choice(mid_msgs))

    elif avg_progress > 0:
        st.warning("You're getting started — stay consistent!")
        st.warning(random.choice(low_msgs))

    else:
        st.write("Start tracking habits to get feedback.")

# ---------------- MOTIVATION BUTTON ----------------
st.header("💬 Need Motivation?")

if st.button("Give Me Motivation"):
    all_msgs = high_msgs + mid_msgs + low_msgs + add_msgs
    st.success(random.choice(all_msgs))

# ---------------- BADGES ----------------
st.header("🏆 Achievements")

if len(st.session_state.habits) > 0:
    for habit in st.session_state.habits:
        completed = sum([habit[day] for day in days])
        percent = (completed / 7) * 100

        if percent == 100:
            badge = "🏆 Master"
        elif percent >= 70:
            badge = "🥇 Gold"
        elif percent >= 40:
            badge = "🥈 Silver"
        elif percent > 0:
            badge = "🥉 Bronze"
        else:
            badge = "🚀 Start"

        st.write(f"{habit['Habit']} → {badge} ({round(percent)}%)")