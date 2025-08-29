# youtube_tracker.py
import streamlit as st
import pandas as pd
import os

FILE_NAME = "videos.csv"

# --- Helper functions ---
def load_data():
    if os.path.exists(FILE_NAME):
        return pd.read_csv(FILE_NAME)
    else:
        return pd.DataFrame(columns=["Video Name", "Estimated Time (hrs)"])

def save_data(video_name, est_time):
    df = load_data()
    new_entry = pd.DataFrame([[video_name, est_time]], columns=df.columns)
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(FILE_NAME, index=False)

# --- Streamlit UI ---
st.set_page_config(page_title="YouTube Tracker", page_icon="🎥", layout="centered")
st.title("🎥 YouTube Tracker")
st.write("Track your learning videos and time commitment.")

# Input form
with st.form("add_video_form"):
    video_name = st.text_input("Enter Video Name")
    est_time = st.number_input("Estimated Completion Time (hours)", min_value=0.0, step=0.5)
    submitted = st.form_submit_button("Add Video")
    if submitted and video_name.strip():
        save_data(video_name.strip(), est_time)
        st.success(f"Added: {video_name} ({est_time} hrs)")

# Show saved videos
st.subheader("📑 Saved Videos")
data = load_data()
if not data.empty:
    search = st.text_input("Search video")
    filtered = data[data["Video Name"].str.contains(search, case=False, na=False)] if search else data
    st.dataframe(filtered, use_container_width=True)
else:
    st.info("No videos saved yet. Add some above!")
