# staff_dashboard.py
import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Staff Dashboard", layout="wide")

# --------------------------
# Database helpers
# --------------------------
def get_connection():
    return sqlite3.connect("catalog.db", check_same_thread=False)

# --- Video functions ---
def add_video(category, title, url):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO videos (category, title, video_url) VALUES (?, ?, ?)", (category, title, url))
    conn.commit()
    conn.close()

def delete_video(video_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM videos WHERE id=?", (video_id,))
    conn.commit()
    conn.close()

def get_videos():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, category, title, video_url FROM videos")
    rows = c.fetchall()
    conn.close()
    return rows

# --- Student functions ---
def get_students():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, email, enrolled_category FROM students")
    rows = c.fetchall()
    conn.close()
    return rows

# --------------------------
# Staff UI
# --------------------------
st.title("👩‍🏫 Staff Dashboard")
st.markdown("Manage courses, videos, and student details here.")

tab1, tab2, tab3 = st.tabs(["➕ Add Video", "🗑️ Delete Video", "👨‍🎓 Student Details"])

# --------------------------
# Tab 1: Add Video
# --------------------------
with tab1:
    st.subheader("Add a New Video")
    category = st.text_input("Category (e.g., AI, Python, Databases)")
    title = st.text_input("Video Title")
    url = st.text_input("YouTube Video URL")
    if st.button("Add Video"):
        if category and title and url:
            add_video(category, title, url)
            st.success(f"✅ '{title}' added to {category}")
        else:
            st.error("Please fill all fields.")

# --------------------------
# Tab 2: Delete Video
# --------------------------
with tab2:
    st.subheader("Delete a Video")
    videos = get_videos()
    if not videos:
        st.info("No videos available.")
    else:
        for vid in videos:
            vid_id, cat, title, url = vid
            col1, col2, col3 = st.columns([3, 5, 2])
            with col1:
                st.text(cat)
            with col2:
                st.text(title)
            with col3:
                if st.button("Delete", key=f"delete_{vid_id}"):
                    delete_video(vid_id)
                    st.warning(f"❌ Deleted '{title}'")
                    st.experimental_rerun()

# --------------------------
# Tab 3: Student Details
# --------------------------
with tab3:
    st.subheader("Student Details")
    students = get_students()
    if not students:
        st.info("No students enrolled yet.")
    else:
        df = pd.DataFrame(students, columns=["ID", "Name", "Email", "Enrolled Category"])
        st.dataframe(df, use_container_width=True)
