# app.py
import streamlit as st
from urllib.parse import urlparse, parse_qs
from typing import Dict, List
import os

st.set_page_config(page_title="Courses", layout="wide")

# ---------------------------------------
# Helper: convert any YT link to embed URL
# ---------------------------------------

def show_profile():
    # Sample user data for the profile
    user_name = "John Doe"
    profile_picture = "https://www.w3schools.com/howto/img_avatar.png"  # Example image URL
    user_bio = "A passionate developer and tech enthusiast."

    st.markdown(
    """
    <style>
    .profile-button>button {
        background-color: #007BFF; /* Blue background */
        color: white; /* White text */
        border: none; /* Remove the border */
        border-radius: 50%; /* Make it round */
        padding: 15px 30px; /* Adjust size to make it round */
        font-size: 16px; /* Font size */
        position: fixed; /* Fixed position */
        top: 10px; /* Distance from the top */
        right: 100px; /* Distance from the right */
        cursor: pointer; /* Pointer cursor on hover */
        width: 50px; /* Width */
        height: 50px; /* Height */
    }
    
    .profile-button>button:hover {
        background-color: #0056b3; /* Darker blue on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
    )

    st.button("👤Profile", key="profile_button", help="Click to view your profile")
    # # Create a "View Profile" button
    # if st.button("View Profile"):
    #     # Display the user's profile information when the button is clicked
    #     st.image(profile_picture, width=150)  # Profile picture
    #     st.markdown(f"### {user_name}")  # Display user name
    #     st.markdown(f"*Bio:* {user_bio}")  # Display bio

show_profile()
     
def yt_embed_url(url: str) -> str:
    """
    Convert a YouTube watch/short/shorts/youtu.be URL to an embed URL
    with modest branding.
    """
    parsed = urlparse(url)
    host = parsed.netloc.replace("www.", "")
    video_id = None

    if host in {"youtube.com", "m.youtube.com"}:
        if parsed.path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [None])[0]
        elif parsed.path.startswith("/embed/"):
            video_id = parsed.path.split("/embed/")[-1]
        elif parsed.path.startswith("/shorts/"):
            video_id = parsed.path.split("/shorts/")[-1]
    elif host == "youtu.be":
        video_id = parsed.path.lstrip("/")

    return (
        f"https://www.youtube-nocookie.com/embed/{video_id}?rel=0&modestbranding=1"
        if video_id else url
    )

# ---------------------------------------
# Catalog (your videos)
# ---------------------------------------
CATALOG: Dict[str, List[Dict[str, str]]] = {
    "AI": [
        {"title": "Artificial Intelligence Fundamentals", "video_url": "https://www.youtube.com/watch?v=ad79nYk2keg&list=PLEiEAq2VkUULyr_ftxpHB6DumOq1Zz2hq"},
        {"title": "What is Artificial Intelligence?", "video_url": "https://www.youtube.com/live/sp_OMFCfGMw?si=wo1_jix1ejxg4Ogq"},
        {"title": "Lecture 1", "video_url": "https://www.youtube.com/live/anTjbDH6y-Y?si=fBIzsP6cGuqDu0v7"},
        {"title": "Lecture 2", "video_url": "https://youtu.be/bZP4VXpCk6A?si=SwCrzRKEGF6YeMSz"},
        {"title": "Lecture 3", "video_url": "https://youtu.be/uh5LCXOBmSI?si=baaWZfst_FKhcoMk"},
        {"title": "Lecture 4", "video_url": "https://youtu.be/15PK38MUEPM?si=JFeB_2Ktj62n8PHL"},
        {"title": "Lecture 5", "video_url": "https://youtu.be/FWOZmmIUqHg?si=kvmd_AziaUN3tR2W"},
        {"title": "Lecture 6", "video_url": "https://youtu.be/VNz3KGoAhG4?si=d19k_w_f4RZxAOPo"},
        {"title": "Lecture 7", "video_url": "https://youtu.be/YhSeTEumjVA?si=qPsVT2l5RjBeHy-F"},
        {"title": "Lecture 8", "video_url": "https://youtu.be/9dFhZFUkzuQ?si=dmwhG-SiIPknSHo1"},
        {"title": "Lecture 9", "video_url": "https://youtu.be/HKcO3-6TYr0?si=ab0smBpoJGKL3p1Z"},
    ],
    "Python": [
        {"title": "Python for Data & Apps", "video_url": "https://www.youtube.com/watch?v=Y8Tko2YC5hA"},
        {"title": "Introduction to Python Course(Beginner)", "video_url": "https://www.youtube.com/watch?v=6i3EGqOBRiU&list=PLdo5W4Nhv31bZSiqiOL5ta39vSnBxpOPT"},
        {"title": "Python Programming", "video_url": "https://youtu.be/DInMru2Eq6E?si=3VGs0uJwR-izD3z9"},
        {"title": "History of Python" , "video_url": "https://youtu.be/1UzSDMJRh8c?si=ne6cuFs1R8_n1Dy2"},
        {"title": "Install Python", "video_url": "https://youtu.be/La1BdF_sunw?si=YZI1dxCEPA6chj9B"},
        {"title": "First Python Program", "video_url": "https://youtu.be/lygaoUnJKF4?si=SL9mLy6fAEGBGaWt"},
        {"title": "Coding excercise", "video_url": "https://youtu.be/FP6qQgJI5f4?si=OOFLTDd-mTqpRwM7"},
        {"title": "Print in Python", "video_url": "https://youtu.be/6Nu9cvINQLk?si=jM0q5E9_AQicJyzK"},
        {"title": "Input function in python", "video_url": "https://youtu.be/sa97IyIOHxU?si=ZkQNGKSABK8oBesF"},
        {"title": "Variables in python", "video_url": "https://youtu.be/a43BIxiZ5EM?si=w73O54wZpyTx7My4"},
    ],
    "Data Science": [
        {"title": "Intro to Data Science", "video_url": "https://www.youtube.com/watch?v=JL_grPUnXzY"},
        {"title": "Statistics for data science", "video_url": "https://www.youtube.com/watch?v=npgbI8KYvN8"},
        {"title": "Data Visualization Basics", "video_url": "hhttps://www.youtube.com/watch?v=cl1H0gY0mVo"},
        {"title": "Hypothesis testing in Data Science", "video_url": "https://www.youtube.com/watch?v=fb8BSFr0isg"},
        {"title": "Z score", "video_url": "https://www.youtube.com/watch?v=okhrFgaUwio"},
        {"title": "Logarithm", "video_url": "https://www.youtube.com/watch?v=KzQQCtgzQbw"},
        {"title": "Distributions in Data science", "video_url": "https://www.youtube.com/watch?v=xtTX69JZ92w"},
        {"title": "Standard Deviations", "video_url": "https://www.youtube.com/watch?v=yCDevFTNbC0"},
        {"title": "Statistics in data science", "video_url": "https://www.youtube.com/watch?v=8ZI55Inh1_A"},
    ],
    "Machine Learning": [
        {"title": "Machine Learning Essentials", "video_url": "https://www.youtube.com/watch?v=gmvvaobm7eQ&list=PLeo1K3hjS3uvCeTYTeyfe0-rN5r8zn9rw"},
        {"title": "Lecture 1", "video_url": "https://www.youtube.com/watch?v=8jazNUpO3lQ&list=PLeo1K3hjS3uvCeTYTeyfe0-rN5r8zn9rw&index=2"},
        {"title": "Lecture 2", "video_url": "https://youtu.be/J_LnPL3Qg70?si=gbYl9t5jBWab6vDC"},
        {"title": "Lecture 3", "video_url": "https://youtu.be/vsWrXfO3wWw?si=HQHLmiqgSRSYmvUC"},
        {"title": "Lecture 4", "video_url": "https://youtu.be/KfnhNlD8WZI?si=0z_v6QOhI9yCSYM_"},
        {"title": "Lecture 5", "video_url": "https://youtu.be/fwY9Qv96DJY?si=NMK9oKkkgLxheZnK"},
        {"title": "Lecture 6", "video_url": "https://youtu.be/FB5EdxAGxQg?si=0wNCe8OT8g93Qlnb"},
        {"title": "Lecture 7", "video_url": "https://youtu.be/ok2s1vV9XW0?si=UzZJ8wifVDIQlBXv"},
        {"title": "Lecture 8", "video_url": "https://youtu.be/EItlUEPCIzM?si=rQVr-tfRHWQEZOVf"},
    ],
    "Databases": [
        {"title": "Introduction to database", "video_url": "https://www.youtube.com/watch?v=6Iu45VZGQDk&list=PLBlnK6fEyqRi_CUQ-FXxgzKQ1dwr_ZJWZ"},
        {"title": "DBMS Characteristics", "video_url": "https://www.youtube.com/watch?v=wClEbCyWryI&list=PLBlnK6fEyqRi_CUQ-FXxgzKQ1dwr_ZJWZ&index=2"},
        {"title": "Database Users", "video_url": "https://youtu.be/qoAL4MA3P08?si=JGIgc0M8eAQiq__8"},
        {"title": "DBMS Architecture", "video_url": "https://youtu.be/dftMGbbULhE?si=V35ZIgcGp4hEylUm"},
        {"title": "Introduction to Relational Data Model", "video_url": "https://youtu.be/Q45sr5p_NmQ?si=Sm0Aohn2_CYuC-Ar"},
        {"title": "Introduction to SQL", "video_url": "https://youtu.be/Zqo-qNNMmdA?si=gfjJ7UBuXOT80k-g"},
        {"title": "Relational Algebra Queries - 1", "video_url": "https://youtu.be/Dgq01JAWw4Y?si=GrEhXtra1-rreGPb"},
        {"title": "Relational Algebra Queries - 2", "video_url": "https://youtu.be/4y4tBfnPlS8?si=DLjZEsnwYmRZmhZ2"},
        {"title": "Interfaces & Classification", "video_url": "https://youtu.be/DkEMtOFMNQE?si=zI0_346xnUS9NFYV"},
        {"title": "Database System Environment", "video_url": "https://youtu.be/rqcTHitakDM?si=ugPZymP_C0O-sf8n"},
        {"title": "Database Design process", "video_url": "https://youtu.be/7m6gXeMDaHc?si=t4sO5ct0veqDZCy5"},
    ],
    "Digital Exercise": [
        {"title": "Parkinson’s Exercises", "video_url": "https://youtu.be/rdjTNOw4Qe4?si=YSo-Ixs8StZn94Ri"},
        {"title": "Strength and Balance Exercises", "video_url": "https://youtu.be/F4PxppoQmHs?si=c6iN9ciqm8ExqeO9"},
        {"title": "Face Symmertry", "video_url": "https://youtu.be/EcbonZR6lFE?si=-jdbu933m6eVrqTa"},
        {"title": "Hand Exercises", "video_url": "https://youtu.be/Ez2GeaMa4c8?si=7uonhElcF1VZJBGf"},
        {"title": "Exercises For Seniors", "video_url": "https://youtu.be/IL3E0SGEWl0?si=Yrie7-w9AUMQoiS7"},
    ],
}

CATEGORIES = list(CATALOG.keys())

# ---------------------------------------
# NEW: Category thumbnails (edit these URLs if you like)
# ---------------------------------------
CATEGORY_THUMBS: Dict[str, str] = {
    "AI": "https://trendsresearch.org/wp-content/uploads/2024/12/Future-of-AI.jpg",
    "Python": "https://365datascience.com/resources/blog/2017-11-Programming-in-900-words-min.png",
    "Data Science": "https://cdn.prod.website-files.com/63ccf2f0ea97be12ead278ed/644a18b637053fa3709c5ba2_what-is-data-science.jpg",
    "Machine Learning": "https://iticollege.edu/wp-content/uploads/2024/07/Machine-Learning-Basics.jpg",
    "Databases": "https://www.aceinfoway.com/blog/wp-content/uploads/2020/03/Best-Database-to-work-with-in-2020.jpg",
    "Digital Exercise": "https://assets.clevelandclinic.org/transform/LargeFeatureImage/ec0404a8-921d-4634-ae53-f43132da90d2/at-home-workout-digital-1457105479",
}

# Fixed Recommended (first item from each category, plus Deep Learning)
RECOMMENDED = [
    CATALOG["AI"][0],
    CATALOG["Python"][0],
    CATALOG["Data Science"][0],
    CATALOG["Databases"][0],
    CATALOG["Machine Learning"][0],  # pick first ML item; change if you want another
]

# ---------------------------------------
# Simple Router
# ---------------------------------------
if "route" not in st.session_state:
    st.session_state.route = "home"     # "home" or "category"
if "active_category" not in st.session_state:
    st.session_state.active_category = None

def go_home():
    st.session_state.route = "home"
    st.session_state.active_category = None
    # if hasattr(st, "rerun"):
    #     st.rerun()

def go_category(cat: str):
    st.session_state.route = "category"
    st.session_state.active_category = cat
    # if hasattr(st, "rerun"):
    #     st.rerun()

# ---------------------------------------
# UI Blocks
# ---------------------------------------
def render_recommended_players():
    
    st.subheader("Recommended")
    cols = st.columns(5)
    for i, item in enumerate(RECOMMENDED):
        with cols[i % 5]:
            with st.container(border=True):
                st.markdown(f"{item['title']}")
                st.video(yt_embed_url(item["video_url"]))
                st.caption("Recommended • Watch inline")

# def render_categories_as_grid():
#     st.subheader("Explore by Category")
#     cols = st.columns(5)
#     for i, cat in enumerate(CATEGORIES):
#         with cols[i % 5]:
#             with st.container(border=True):
#                 # NEW: category thumbnail on the card
#                 thumb = CATEGORY_THUMBS.get(cat)
#                 if thumb:
#                     st.image(thumb, use_container_width=True)
#                 st.markdown(f"### {cat}")
#                 st.caption("Curated videos for this topic")
#                 if st.button(f"Open {cat}", key=f"open_{cat}"):
#                     go_category(cat)

def render_categories_as_grid():
    st.subheader("Explore by Category")

    # Inject custom CSS for consistent card height
    st.markdown(
        """
        <style>
        .category-card {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding-bottom: 10px;
            padding-top: 0px;
        }
        .category-thumb {
            height: 150px;
            object-fit: cover;
            width: 100%;
            border-radius: 6px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(5)

    for i, cat in enumerate(CATEGORIES):
        with cols[i % 5]:
            with st.container(border=True):
                st.markdown('<div class="category-card">', unsafe_allow_html=True)

                thumb = CATEGORY_THUMBS.get(cat)
                if thumb:
                    st.markdown(
                        f'<img src="{thumb}" class="category-thumb" />',
                        unsafe_allow_html=True
                    )
                else:
                    # Empty placeholder with same size
                    st.markdown(
                        '<div class="category-thumb" style="background-color: #f0f0f0;"></div>',
                        unsafe_allow_html=True
                    )

                st.markdown(f"### {cat}")
                
                # Open button
                button_key = f"open_{cat}_{i}"
                st.button(f"Open {cat}", key=button_key, on_click=go_category, args=(cat,))

                # Pre-assessment button
                pre_assessment_key = f"pre_assessment_{cat}_{i}"
                st.button(
                    "Pre-assessment",
                    key=pre_assessment_key,
                    on_click=pre_assessment_function,
                    args=(cat,)
                )

                st.markdown('</div>', unsafe_allow_html=True)


# Callback for Pre-assessment button
def pre_assessment_function(cat):
    st.session_state.selected_category = cat
    st.session_state.go_to_test = True  # flag to trigger page switch


# --- Main script: handle navigation ---
if st.session_state.get("go_to_test"):
    st.session_state.go_to_test = False  # reset flag
    st.switch_page("pages/test.py")


def render_category_page(cat: str):
    # NEW: banner thumbnail at the top of the category page
    if st.button("← Back "):
        go_home()
    banner = CATEGORY_THUMBS.get(cat)
    if banner:
        st.image(banner, use_container_width=True)
    st.markdown(f"### {cat} Videos")

    items = CATALOG.get(cat, [])
    if not items:
        st.info("No videos yet in this category.")
    else:
        # 3-column grid of embedded players
        st.markdown(
            """
            <style>
            .stButton>button {
            background-color: #007BFF;  /* Blue background */
            color: white;               /* White text */
            font-size: 16px;            /* Text size */
            padding: 10px 24px;         /* Padding */
            border-radius: 5px;         /* Rounded corners */
            border: none;               /* Remove border */
            cursor: pointer;           /* Pointer cursor on hover */
            }
            .stButton>button:hover {
                background-color: #0056b3;  /* Darker blue on hover */
                color:white;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
        """
         <style>
         .stVideo {
            width: 100%;  /* Make the video width fill the available space */
            height: 300px; /* Set the fixed height */
            object-fit: cover;  /* Ensures aspect ratio is maintained */
            }
        </style>
        """,
        unsafe_allow_html=True
        )
        cols = st.columns(3)
        for i, item in enumerate(items):
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"{item['title']}")
                    st.video(yt_embed_url(item["video_url"]))

    st.markdown("---")
    
    st.markdown(
    """
    <style>
    .centered-button {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .stButton>button {
        font-size: 18px;
        padding: 10px 30px;
        background-color: #007BFF;
        color: white;
        border-radius: 5px;
        border: none;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #0056b3;  /* Darker blue on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([3, 2, 3])  # Create 3 columns with center as larger
    with col2:
        st.button("Take the Test & See How Awesome You Are!✍")
        
    

# ---------------------------------------
# Pages
# ---------------------------------------
if st.session_state.route == "home":
    left, right = st.columns([3, 2], vertical_alignment="center")
    with left:
        st.markdown("### 🎓 Master tomorrow’s skills today")
        st.markdown("Curated *AI, Data Science, Python, ML, and Databases* videos — watch inline.")
        # (Remove the next line if you don’t want it)
    with right:
        st.image(
            "https://images.unsplash.com/photo-1519389950473-47ba0277781c?q=80&w=1400&auto=format&fit=crop",
            use_container_width=True,
        )

    st.markdown("---")
    render_recommended_players()
    st.markdown("---")
    render_categories_as_grid()

else:
    render_category_page(st.session_state.active_category)

# ---------------------------------------
# Footer
# ---------------------------------------
st.markdown("---")
st.caption("© 2025 Your Academy • Built with Streamlit")