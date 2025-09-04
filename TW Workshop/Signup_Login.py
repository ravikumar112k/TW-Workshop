import streamlit as st
import sqlite3
import importlib.util
import sys
import os

# ========== DATABASE SETUP ==========
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
                name TEXT,
                role TEXT,
                userid TEXT PRIMARY KEY,
                password TEXT,
                mail TEXT
            )''')
conn.commit()

# ========== HELPER FUNCTIONS ==========
def add_user(name, role, userid, password, mail):
    try:
        c.execute(
            "INSERT INTO users (name, role, userid, password, mail) VALUES (?, ?, ?, ?, ?)",
            (name.strip(), role.strip().lower(), userid.strip(), password, mail.strip())
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(userid, password):
    c.execute("SELECT * FROM users WHERE userid=? AND password=?", (userid.strip(), password))
    return c.fetchone()

# ========== UI SETUP ==========
st.set_page_config(page_title="Login / Signup", layout="wide")

# Shared button style
st.markdown("""
<style>
.stButton>button {
    background-color: #007BFF;
    color: white;
    font-size: 16px;
    padding: 10px 24px;
    border-radius: 6px;
    border: none;
    cursor: pointer;
    width: 100%;
    font-weight: 600;
}
.stButton>button:hover {
    background-color: #0056b3;
    color:white;
}
.auth-title {
    font-size: 1.8rem;
    font-weight: 700;
    color: #222;
    margin-bottom: 1rem;
    text-align: center;
}
.auth-subtitle {
    font-size: 1rem;
    color: #666;
    margin-bottom: 2rem;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ========== APP LOGIC ==========
if "page" not in st.session_state:
    st.session_state.page = "login"
if "user" not in st.session_state:
    st.session_state.user = None

# ---------- LOGIN PAGE ----------
def login_page():
    left, right = st.columns([2, 3])
    with left:
        st.image(
            "https://images.unsplash.com/photo-1519389950473-47ba0277781c?q=80&w=1400&auto=format&fit=crop",
            width="stretch",
        )
    with right:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.markdown('<div class="auth-title">🎓 Welcome back</div>', unsafe_allow_html=True)
        st.markdown('<div class="auth-subtitle">Login to continue learning</div>', unsafe_allow_html=True)

        userid = st.text_input("User ID")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = login_user(userid, password)
            if user:
                st.session_state.user = {
                    "name": user[0],
                    "role": user[1].strip().lower(),
                    "userid": user[2]
                }
                st.session_state.page = "main"
                st.rerun()
            else:
                st.error("❌ Invalid credentials.")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Create a new account"):
            st.session_state.page = "signup"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- SIGNUP PAGE ----------
def signup_page():
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    st.markdown('<div class="auth-title">📝 Join Us</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-subtitle">Create your free account</div>', unsafe_allow_html=True)

    name = st.text_input("Full Name")
    role = st.selectbox("Role", ["Student", "Teacher", "Admin"])
    userid = st.text_input("User ID")
    password = st.text_input("Password", type="password")
    mail = st.text_input("Email")

    if st.button("Sign Up"):
        role_db = role.strip().lower()
        if add_user(name, role_db, userid, password, mail):
            st.success("✅ Account created! Please login.")
            st.session_state.page = "login"
            st.rerun()
        else:
            st.error("⚠️ User ID already exists.")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- DASHBOARD PLACEHOLDERS ----------
def teacher_dashboard():
    course_path = os.path.join(os.getcwd(), "staff_dashboard.py")
    if os.path.exists(course_path):
        with open(course_path, "r", encoding="utf-8") as f:  # ✅ specify utf-8
            code = f.read()
            exec(code, globals())  # executes coursepage.py in the current session
    else:
        st.error("❌ staff_dashboard.py not found in the directory.")
        
def admin_dashboard():
    course_path = os.path.join(os.getcwd(), "admin_dashboard.py")
    if os.path.exists(course_path):
        with open(course_path, "r", encoding="utf-8") as f:  # ✅ specify utf-8
            code = f.read()
            exec(code, globals())  # executes coursepage.py in the current session
    else:
        st.error("❌ admin_dashboard.py not found in the directory.")
def student_dashboard():
    # Execute the code inside coursepage.py seamlessly
    course_path = os.path.join(os.getcwd(), "coursepage.py")
    if os.path.exists(course_path):
        with open(course_path, "r", encoding="utf-8") as f:  # ✅ specify utf-8
            code = f.read()
            exec(code, globals())  # executes coursepage.py in the current session
    else:
        st.error("❌ coursepage.py not found in the directory.")

# ---------- MAIN PAGE ----------
def main_page():
    role = st.session_state.user["role"]
    st.write(f"🎉 Logged in as **{st.session_state.user['name']}** ({role.title()})")

    if role == "student":
        student_dashboard()
    elif role in ["teacher", "staff"]:
        teacher_dashboard()
    elif role == "admin":
        admin_dashboard()
    else:
        st.error("⚠️ Role not recognized.")

# ---------- ROUTING ----------
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "signup":
    signup_page()
else:
    main_page()
