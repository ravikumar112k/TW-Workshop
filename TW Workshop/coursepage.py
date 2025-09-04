# app.py
import streamlit as st
import sqlite3
from urllib.parse import urlparse, parse_qs
from typing import Dict, List

st.set_page_config(page_title="Courses", layout="wide")

# ---------------------------------------
# Load catalog from SQLite DB
# ---------------------------------------
def load_catalog_from_db():
    conn = sqlite3.connect("catalog.db", check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT category, title, video_url FROM videos")
    rows = c.fetchall()
    conn.close()

    catalog = {}
    for cat, title, url in rows:
        if cat not in catalog:
            catalog[cat] = []
        catalog[cat].append({"title": title, "video_url": url})
    return catalog

# Override static catalog with DB-driven one
CATALOG: Dict[str, List[Dict[str, str]]] = load_catalog_from_db()
CATEGORIES = list(CATALOG.keys())

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
CATALOG: Dict[str, List[Dict[str, str]]] = load_catalog_from_db()
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