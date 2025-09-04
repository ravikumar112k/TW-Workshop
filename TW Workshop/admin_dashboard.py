import streamlit as st
import sqlite3
import pandas as pd

# --- Database Setup ---
def get_connection():
    conn = sqlite3.connect("users.db", check_same_thread=False)
    return conn

def get_all_users():
    conn = get_connection()
    query = "SELECT userid, name, role, mail FROM users"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def add_user(name, role, userid, password, mail):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (name, role, userid, password, mail) VALUES (?, ?, ?, ?, ?)",
                  (name, role, userid, password, mail))
        conn.commit()
    except sqlite3.IntegrityError:
        st.error("❌ UserID already exists!")
    conn.close()

def delete_user(userid):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE userid=?", (userid,))
    conn.commit()
    conn.close()

def update_user(userid, name, role, mail):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE users SET name=?, role=?, mail=? WHERE userid=?",
              (name, role, mail, userid))
    conn.commit()
    conn.close()

# --- Admin Dashboard UI ---
def admin_dashboard():
    st.title("👨‍💼 Admin Dashboard")
    st.write("Manage users in the system")

    menu = ["View Users", "Add User", "Update User", "Delete User"]
    choice = st.sidebar.radio("Navigation", menu)

    if choice == "View Users":
        st.subheader("📋 User List")
        users_df = get_all_users()
        st.dataframe(users_df)

    elif choice == "Add User":
        st.subheader("➕ Add New User")
        name = st.text_input("Name")
        role = st.selectbox("Role", ["student", "teacher", "admin"])
        userid = st.text_input("UserID")
        password = st.text_input("Password", type="password")
        mail = st.text_input("Email")

        if st.button("Add User"):
            if name and role and userid and password and mail:
                add_user(name, role, userid, password, mail)
                st.success(f"✅ User {name} added successfully!")
            else:
                st.warning("⚠️ Please fill in all fields")

    elif choice == "Update User":
        st.subheader("✏️ Update User")
        users_df = get_all_users()
        st.dataframe(users_df)

        userid = st.text_input("Enter UserID to update")
        new_name = st.text_input("New Name")
        new_role = st.selectbox("New Role", ["student", "teacher", "admin"])
        new_mail = st.text_input("New Email")

        if st.button("Update"):
            update_user(userid, new_name, new_role, new_mail)
            st.success(f"✅ User {userid} updated successfully!")

    elif choice == "Delete User":
        st.subheader("🗑️ Delete User")
        users_df = get_all_users()
        st.dataframe(users_df)

        userid = st.text_input("Enter UserID to delete")

        if st.button("Delete"):
            delete_user(userid)
            st.success(f"✅ User {userid} deleted successfully!")

if __name__ == "__main__":
    admin_dashboard()
