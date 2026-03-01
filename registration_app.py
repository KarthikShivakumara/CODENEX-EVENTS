import streamlit as st
import json
import uuid
import os
import smtplib
import base64
from email.mime.text import MIMEText

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(page_title="CodeNex Registration", page_icon="🚀")

# ======================================================
# BACKGROUND VIDEO
# ======================================================
video_path = os.path.join(os.path.dirname(__file__), "logo_intro.mp4")

if os.path.exists(video_path):
    with open(video_path, "rb") as f:
        video_bytes = f.read()
        encoded_video = base64.b64encode(video_bytes).decode()

    background_video_html = f"""
    <style>

    html, body, [data-testid="stAppViewContainer"] {{
        height: 100%;
        margin: 0;
        padding: 0;
        overflow-x: hidden;
    }}

    .stApp {{
        background: transparent;
    }}

    #bg-video {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        object-fit: cover;
        z-index: -10;
        opacity: 0.25;
        filter: brightness(0.75);
        pointer-events: none;
    }}

    .block-container {{
        position: relative;
        z-index: 10;
        padding: 2rem 4rem !important;
        max-width: 100% !important;
        background: transparent !important;
    }}

    h1, h2, h3, h4, label, p {{
        color: white !important;
    }}

    input, textarea {{
        background: rgba(255,255,255,0.15) !important;
        color: white !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
    }}

    div[data-baseweb="select"] > div {{
        background: rgba(255,255,255,0.15) !important;
        color: white !important;
    }}

    div[data-testid="stRadio"] label {{
        color: white !important;
    }}

    button[kind="primary"] {{
        background-color: black !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }}

    button[kind="primary"]:hover {{
        background-color: #111 !important;
    }}

    </style>

    <video autoplay loop muted playsinline id="bg-video">
        <source src="data:video/mp4;base64,{encoded_video}" type="video/mp4">
    </video>
    """

    st.markdown(background_video_html, unsafe_allow_html=True)

# ======================================================
# TITLE
# ======================================================
st.title("CodeNex Coding Relay - Registration")

# ======================================================
# CONFIG
# ======================================================

# import os
# SENDER_EMAIL = os.getenv("SENDER_EMAIL")
# APP_PASSWORD = os.getenv("APP_PASSWORD")
SENDER_EMAIL = "kk702227458@gmail.com"
APP_PASSWORD = "shycgirnmqfmbtfz"

ADMIN_ID = "codenex admin"
ADMIN_PASSWORD = "karthi@123"

# ======================================================
# PATH
# ======================================================
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
REG_FILE = "registrations_event1.json"

# ======================================================
# JSON HELPERS
# ======================================================
def load_json_safe(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r") as f:
            content = f.read().strip()
            if content == "":
                return []
            return json.loads(content)
    except:
        return []

def save_json_safe(path, data):
    temp_path = path + ".tmp"
    with open(temp_path, "w") as f:
        json.dump(data, f, indent=4)
    os.replace(temp_path, path)

# ======================================================
# EMAIL FUNCTION
# ======================================================
def send_access_mail(receiver, name, team, access_id):

    subject = "CodeNex Coding Relay - Access ID"

    body = f"""
Hello {name},

Registration Successful!

Team Name : {team}
Access ID : {access_id}

Use this ID during event login.

- CodeNex Team
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
    except:
        st.warning(f"Mail not sent to {receiver}")

# ======================================================
# SESSION
# ======================================================
if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = False

if "show_admin_login" not in st.session_state:
    st.session_state.show_admin_login = False

# ======================================================
# ADMIN BUTTON
# ======================================================
col1, col2 = st.columns([8,1])

with col2:
    if st.button("🔐 Admin"):
        st.session_state.show_admin_login = True

# ======================================================
# ADMIN LOGIN
# ======================================================
if st.session_state.show_admin_login and not st.session_state.admin_logged:

    st.subheader("Admin Login")

    admin_id = st.text_input("Admin ID")
    admin_pass = st.text_input("Password", type="password")

    if st.button("Login as Admin"):
        if admin_id == ADMIN_ID and admin_pass == ADMIN_PASSWORD:
            st.session_state.admin_logged = True
            st.success("Admin Login Successful")
            st.rerun()
        else:
            st.error("Invalid Credentials")

    st.stop()

# ======================================================
# ADMIN DASHBOARD
# ======================================================
if st.session_state.admin_logged:

    st.title("Admin Dashboard")

    data = load_json_safe(REG_FILE)

    if len(data) == 0:
        st.info("No registrations yet.")
    else:
        st.json(data)

    with open(REG_FILE, "rb") as f:
        st.download_button(
            label="Download Registration JSON",
            data=f,
            file_name="registrations_event1.json",
            mime="application/json"
        )

    if st.button("Logout"):
        st.session_state.admin_logged = False
        st.session_state.show_admin_login = False
        st.rerun()

    st.stop()

# ======================================================
# LOAD DATA
# ======================================================
data = load_json_safe(REG_FILE)

# ======================================================
# PARTICIPATION TYPE
# ======================================================
participation_type = st.radio(
    "Select Participation Type",
    ["Individual", "Team"]
)

# ======================================================
# INDIVIDUAL
# ======================================================
if participation_type == "Individual":

    st.subheader("Individual Details")

    name = st.text_input("Your Name")
    email = st.text_input("Your Email")

    if st.button("Register"):

        if not name or not email:
            st.error("Please fill all fields.")
            st.stop()

        for team in data:
            for member in team["members"]:
                if member["email"].lower() == email.lower():
                    st.error("You are already registered!")
                    st.stop()

        access_id = str(uuid.uuid4())[:8].upper()

        team_data = {
            "team_name": name,
            "access_id": access_id,
            "members": [{"name": name, "email": email}]
        }

        data.append(team_data)
        save_json_safe(REG_FILE, data)

        send_access_mail(email, name, name, access_id)

        st.success("Registration Successful!")
        st.info("Access ID sent to your mail.")

# ======================================================
# TEAM
# ======================================================
if participation_type == "Team":

    st.subheader("Team Registration")

    team_name = st.text_input("Team Name")
    team_size = st.selectbox("Select Team Size", [2, 3])

    members = []

    for i in range(team_size):
        st.markdown(f"### Member {i+1}")
        member_name = st.text_input(f"Member {i+1} Name", key=f"name_{i}")
        member_email = st.text_input(f"Member {i+1} Email", key=f"email_{i}")
        members.append((member_name, member_email))

    if st.button("Register Team"):

        if not team_name:
            st.error("Team Name is required.")
            st.stop()

        for name, email in members:
            if not name or not email:
                st.error("All member details required.")
                st.stop()

        entered_emails = {email.lower() for _, email in members}

        for team in data:

            if team["team_name"].lower() == team_name.lower():
                st.error("Team name already registered!")
                st.stop()

            existing_emails = {
                m["email"].lower() for m in team["members"]
            }

            if entered_emails & existing_emails:
                st.error("Member already registered!")
                st.stop()

        access_id = str(uuid.uuid4())[:8].upper()

        team_data = {
            "team_name": team_name,
            "access_id": access_id,
            "members": [
                {"name": name, "email": email}
                for name, email in members
            ]
        }

        data.append(team_data)
        save_json_safe(REG_FILE, data)

        for name, email in members:
            send_access_mail(email, name, team_name, access_id)

        st.success("Team Registration Successful!")
        st.info("Access ID sent to all team members.")
