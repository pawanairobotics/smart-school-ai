import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="Smart School AI", layout="wide")
st.title("🏫 Smart School AI Assistant - Comprehensive Dashboard")

# Session State for Data Storage
if 'students' not in st.session_state:
    st.session_state.students = pd.DataFrame(columns=["Name", "Marks", "Feedback"])

# Sidebar Menu
menu = st.sidebar.radio("Navigation", ["Dashboard", "Student Records", "Staff Portal", "Security AI"])

# --- 1. Dashboard ---
if menu == "Dashboard":
    st.header("Welcome to the Admin Dashboard")
    col1, col2 = st.columns(2)
    col1.metric("Total Students", len(st.session_state.students))
    col2.metric("System Status", "Online 🟢")

# --- 2. Student Records (Marks & Feedback) ---
elif menu == "Student Records":
    st.header("Student Management")
    with st.form("student_form"):
        name = st.text_input("Student Name")
        marks = st.number_input("Marks", 0, 100)
        feedback = st.text_area("Feedback/Note")
        submitted = st.form_submit_button("Add Record")
        if submitted:
            new_data = pd.DataFrame([[name, marks, feedback]], columns=["Name", "Marks", "Feedback"])
            st.session_state.students = pd.concat([st.session_state.students, new_data], ignore_index=True)
            st.success("Record Added!")
    
    st.table(st.session_state.students)

# --- 3. Staff Portal ---
elif menu == "Staff Portal":
    st.header("Staff Communication & AI Planner")
    role = st.selectbox("Staff Role", ["Teacher", "Principal", "Admin"])
    task = st.text_input("Enter Task for AI Planning:")
    if st.button("Generate Plan"):
        st.write(f"🤖 AI Task Plan for {role}: Create a schedule for '{task}' with break times, lesson objectives, and student assessment.")

# --- 4. Security AI ---
elif menu == "Security AI":
    st.header("School Cyber Security")
    pwd = st.text_input("Check Portal Password Strength:", type="password")
    if pwd:
        if len(pwd) > 8 and any(c.isdigit() for c in pwd):
            st.success("Strong Password")
        else:
            st.error("Weak Password - Needs digit & >8 chars")
