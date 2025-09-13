"""
Smart Campus Assistant — Streamlit UI prototype

How to run:
1. Install dependencies: pip install streamlit pandas
2. Save this file as app.py and run: streamlit run app.py

This file is a UI/UX prototype for a campus conversational assistant covering:
- Schedules (classes, events)
- Facilities (buildings, rooms)
- Dining (menus, hours)
- Library services (search, loans)
- Administrative procedures (forms, contacts)

The conversational AI connection is represented by a placeholder function `ai_reply()`.
Replace it with your actual model / API call (OpenAI, local LLM, etc.).

This prototype focuses on layout, interactions, and microcopy for a smooth student experience.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Smart Campus Assistant", layout="wide")

# ---------- Sample data (replace with real DB queries) ----------

def sample_schedule():
    today = datetime.today().date()
    rows = []
    for i in range(5):
        rows.append({
            "Date": (today + timedelta(days=i)).isoformat(),
            "Time": f"{9+i}:00 - {10+i}:30",
            "Course": f"CS{100+i}: Intro Topic {i+1}",
            "Location": f"Bldg {chr(65+i)} - Room {100+i}"
        })
    return pd.DataFrame(rows)

def sample_dining():
    return pd.DataFrame([
        {"Venue": "Central Canteen", "Open": "7:30 - 20:00", "Today Special": "Grilled Veg Wrap"},
        {"Venue": "North Cafe", "Open": "8:00 - 18:00", "Today Special": "Masala Dosa"},
        {"Venue": "South Dining", "Open": "11:00 - 22:00", "Today Special": "Paneer Butter Masala"},
    ])

def sample_library():
    return pd.DataFrame([
        {"Title": "Introduction to Algorithms", "Author": "Cormen", "Status": "Available"},
        {"Title": "Learning Python", "Author": "Mark Lutz", "Status": "On Loan"},
        {"Title": "Design Patterns", "Author": "Gamma et al.", "Status": "Available"}
    ])

FACILITIES = [
    {"name":"Main Library","type":"Library","building":"Lib Block","open":"8:00-22:00"},
    {"name":"Auditorium A","type":"Auditorium","building":"Arts Center","open":"9:00-21:00"},
    {"name":"Gym","type":"Sports","building":"Sports Complex","open":"6:00-23:00"}
]

# ---------- Lightweight AI placeholder ----------

def ai_reply(user_message, context=None):
    """
    Replace this function with a real API call to your conversational model.
    Keep responses short and action-oriented (helpful microcopy):
    Example: "I found your next class: CS102 on Sep 14, 10:00 at Bldg B Room 202. Want directions?"
    """
    msg = user_message.lower()
    if "next class" in msg or "my schedule" in msg:
        return "I can show you your upcoming classes. Do you want today's schedule or the full week?"
    if "dining" in msg or "food" in msg or "canteen" in msg:
        return "Today's specials: Central Canteen — Grilled Veg Wrap. Want directions or menu?"
    if "library" in msg or "book" in msg:
        return "I can search the library catalog. What title or author are you looking for?"
    if "hours" in msg or "open" in msg:
        return "Which facility are you asking about? Try: 'library hours' or 'gym hours'."
    if "help" in msg or "admin" in msg:
        return "Administrative services: registration, transcripts, ID cards. Which one do you need?"
    return "Sorry — I didn't get that. Try: 'show my schedule', 'what's for lunch', or 'search library for Design Patterns'."

# ---------- Styling (simple) ----------

st.markdown("""
<style>
.sidebar .sidebar-content {
    padding-top: 20px;
}
.chat-box { max-height: 420px; overflow-y: auto; padding: 10px; border-radius: 8px; }
.bot { background-color: #f1f5f9; padding: 8px; border-radius: 8px; margin-bottom: 6px; }
.user { background-color: #dbeafe; padding: 8px; border-radius: 8px; margin-bottom: 6px; text-align: right; }
</style>
""", unsafe_allow_html=True)

# ---------- Layout ----------

with st.sidebar:
    st.header("Smart Campus Assistant")
    st.write("Quick actions")
    if st.button("Show today's schedule"):
        st.session_state['show_tab'] = 'schedule'
    if st.button("What's for lunch"):
        st.session_state['show_tab'] = 'dining'
    if st.button("Search library"):
        st.session_state['show_tab'] = 'library'
    st.markdown("---")
    st.write("Contact admin: admin@campus.edu")
    st.write("Feedback: Use the chat to report issues")

# Main area: two columns — left for content, right for chat
col1, col2 = st.columns([2, 1])

if 'show_tab' not in st.session_state:
    st.session_state['show_tab'] = 'home'

with col1:
    if st.session_state['show_tab'] == 'home':
        st.subheader("Welcome back 👋")
        st.write("Use the chat on the right for natural language queries, or select a module below.")
        modules = st.tabs(["Schedule","Facilities","Dining","Library","Admin"])

        with modules[0]:
            st.write("Quick view: next 5 events")
            df = sample_schedule()
            st.dataframe(df)

        with modules[1]:
            st.write("Campus facilities — find rooms, hours, and who manages them.")
            fac_df = pd.DataFrame(FACILITIES)
            st.table(fac_df)

        with modules[2]:
            st.write("Dining locations and today's specials")
            st.table(sample_dining())

        with modules[3]:
            st.write("Library — quick catalog preview")
            st.table(sample_library())

        with modules[4]:
            st.write("Administrative procedures and forms")
            st.write("- Register for courses\n- Request transcript\n- Student ID replacement")
            if st.button("Open admin forms (mock)"):
                st.info("This would open a secure forms flow integrated with SSO.")

    elif st.session_state['show_tab'] == 'schedule':
        st.subheader("My Schedule")
        st.write("Here's a sample of your upcoming classes and events")
        st.dataframe(sample_schedule())

    elif st.session_state['show_tab'] == 'dining':
        st.subheader("Dining")
        st.dataframe(sample_dining())

    elif st.session_state['show_tab'] == 'library':
        st.subheader("Library Search")
        query = st.text_input("Search catalog", key='lib_query')
        if st.button("Search"):
            # naive search against sample
            df = sample_library()
            res = df[df['Title'].str.contains(query, case=False, na=False) | df['Author'].str.contains(query, case=False, na=False)]
            if res.empty:
                st.info("No results found in demo catalog.")
            else:
                st.dataframe(res)

    elif st.session_state['show_tab'] == 'facilities':
        st.subheader("Facilities Directory")
        st.table(pd.DataFrame(FACILITIES))

    elif st.session_state['show_tab'] == 'admin':
        st.subheader("Administrative Services")
        st.write("Fill a short request form and we'll route it to the right office.")
        with st.form(key='admin_form'):
            name = st.text_input("Your name")
            email = st.text_input("Your campus email")
            service = st.selectbox("Service", ["Transcript","Registration","ID Card","Other"])
            details = st.text_area("Details")
            submitted = st.form_submit_button("Submit request")
        if submitted:
            st.success("Request submitted. Reference ID: R-" + datetime.now().strftime('%Y%m%d%H%M%S'))

# ---------- Chat area (right column) ----------
with col2:
    st.markdown("### Chat with the Assistant")

    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    chat_box = st.container()

    with chat_box:
        for idx, item in enumerate(st.session_state['chat_history']):
            if item['sender'] == 'user':
                st.markdown(f"<div class='user'>{item['message']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='bot'>{item['message']}</div>", unsafe_allow_html=True)

    user_input = st.text_input("Ask me about schedules, dining, library, or admin...", key='user_input')
    if st.button("Send") or (user_input and st.session_state.get('_enter_pressed', False)):
        msg = user_input.strip()
        if msg:
            st.session_state['chat_history'].append({'sender':'user','message':msg})
            # call AI (placeholder)
            reply = ai_reply(msg)
            st.session_state['chat_history'].append({'sender':'bot','message':reply})
            # optionally route to a module
            if 'schedule' in msg.lower():
                st.session_state['show_tab'] = 'schedule'
            if 'dining' in msg.lower() or 'lunch' in msg.lower():
                st.session_state['show_tab'] = 'dining'
            if 'library' in msg.lower() or 'book' in msg.lower():
                st.session_state['show_tab'] = 'library'
            # clear input
            st.session_state['user_input'] = ''
            st.experimental_rerun()

    st.markdown("---")
    st.write("Voice input, SSO, and push notifications are next-step integrations.")

# ---------- Footer / UX notes ----------

st.markdown("---")
st.caption("Prototype UI: Streamlit demo. Replace `ai_reply()` with your LLM API. For production, build authentication (SSO), RBAC, and secure backend services for data access.")

# ---------- End of file ----------
