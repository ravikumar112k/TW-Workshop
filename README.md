In-house AI Education Agent
An adaptive AI-driven learning platform for enterprises that automates curriculum creation, delivers role-specific training, and personalizes learning pathways. The agent diagnoses individual skill levels, optimizes progression, and reduces manual effort in content preparation, grading, and compliance reporting.

# TW Workshop

Overview
TW Workshop is a **Streamlit-based learning management and training platform** designed for workshops.  
It provides role-specific dashboards for **Admins, Staff, and Students** to manage courses, tests, and user data efficiently.

Features
- **Admin Dashboard** (`admin_dashboard.py`): Manage courses, users, and platform settings.
- **Staff Dashboard** (`staff_dashboard.py`): Track student progress and manage uploaded content.
- **Student Access** (`Signup_Login.py`, `coursepage.py`): Students can sign up, log in, and access course materials.
- **Database Support**: Uses SQLite (`users.db`, `catalog.db`) for user and course data.
- **Environment Variables**: `.env` file for secure configuration management.
- **Sample Data Setup**: Scripts like `setup_db.py`, `setup_students.py`, and `insert_samples.py` help initialize the database with test data.

Project Structure
```
TW_Workshop/
└── TW Workshop/
    ├── .env                   # Environment variables
    ├── admin_dashboard.py      # Admin dashboard
    ├── catalog.db              # Course database
    ├── coursepage.py           # Student course page
    ├── insert_samples.py       # Insert sample data
    ├── old_coursepage.py       # Legacy course page
    ├── setup_db.py             # Initialize database
    ├── setup_students.py       # Setup student data
    ├── Signup_Login.py         # Signup & Login functionality
    ├── staff_dashboard.py      # Staff dashboard
    ├── users.db                # User database
    ├── pages/                  # Extra Streamlit pages
    │   └── test.py
```

Installation & Setup
1. Clone the repository or extract the project zip:
   ```bash
   git clone <your-repo-url>
   cd "TW Workshop"
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate    # On Mac/Linux
   venv\Scripts\activate     # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   *(If `requirements.txt` is missing, install manually:)*
   ```bash
   pip install streamlit sqlite3 python-dotenv
   ```

4. Set up environment variables in `.env` (example):
   ```ini
   SECRET_KEY=your_secret_key
   DEBUG=True
   ```

5. Initialize the database:
   ```bash
   python setup_db.py
   python setup_students.py
   python insert_samples.py
   ```

Running the App
To run specific dashboards:
```bash
streamlit run Signup_Login.py
streamlit run admin_dashboard.py
streamlit run staff_dashboard.py
streamlit run coursepage.py
```

Usage
- **Admins**: Use `admin_dashboard.py` to manage platform settings.  
- **Staff**: Use `staff_dashboard.py` to track student progress and manage uploads.  
- **Students**: Use `Signup_Login.py` to register/login and access `coursepage.py`.  

Notes
- Ensure `.env` is properly configured.  
- Use `users.db` and `catalog.db` for persistent data.  
- Old files like `old_coursepage.py` are for reference only.  

---
*This project is intended for training/workshop purposes. Extend features as per requirements.*



