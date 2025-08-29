# youtube_tracker.py
import streamlit as st
from supabase_py import create_client, Client

# --- Supabase config ---
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Streamlit UI ---
st.set_page_config(page_title="YouTube Tracker", page_icon="🎥", layout="centered")
st.title("🎥 YouTube Tracker")
st.write("Track your learning videos and time commitment.")

# Input form
with st.form("add_video_form"):
    video_name = st.text_input("Enter Video Name")
    est_time = st.number_input("Estimated Completion Time (hours)", min_value=0.0, step=0.5)
    status = st.selectbox("Status", ["Not Started", "In Progress", "Completed"])
    submitted = st.form_submit_button("Add Video")
    if submitted and video_name.strip():
        supabase.table("videos").insert({
            "video_name": video_name.strip(),
            "estimated_time": est_time,
            "status": status
        }).execute()
        st.success(f"Added: {video_name} ({est_time} hrs, {status})")

# Show saved videos
st.subheader("📑 Saved Videos")
response = supabase.table("videos").select("*").execute()
data = response.data if response.data else []

if data:
    search = st.text_input("Search video")
    filtered = [row for row in data if search.lower() in row["video_name"].lower()] if search else data
    st.table(filtered)
else:
    st.info("No videos saved yet. Add some above!")
