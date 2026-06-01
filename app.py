import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Smart School Exam Portal", layout="centered")

# Initialize Session State
if 'questions' not in st.session_state:
    st.session_state.questions = None

st.title("🎓 Smart School Exam Portal")

# Sidebar Login
role = st.sidebar.radio("Select Login:", ["Teacher", "Student"])

# --- TEACHER PANEL ---
if role == "Teacher":
    st.header("Teacher Dashboard")
    st.info("Upload Excel file with columns: Question, Opt1, Opt2, Opt3, CorrectAnswer")
    uploaded_file = st.file_uploader("Upload Exam File (.xlsx)", type=["xlsx"])
    
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.session_state.questions = df
        st.success("Exam Uploaded Successfully!")
        st.write("Preview of Questions:", df.head())

# --- STUDENT PANEL ---
elif role == "Student":
    st.header("Student Exam Portal")
    if st.session_state.questions is not None:
        name = st.text_input("Enter your name:")
        if name:
            df = st.session_state.questions
            user_answers = {}
            
            # Display Questions
            for i, row in df.iterrows():
                user_answers[i] = st.radio(f"Q{i+1}: {row['Question']}", [row['Opt1'], row['Opt2'], row['Opt3']])
            
            if st.button("Submit Exam"):
                score = 0
                for i, row in df.iterrows():
                    if user_answers[i] == row['CorrectAnswer']:
                        score += 1
                st.balloons()
                st.success(f"Result for {name}: You scored {score} out of {len(df)}")
    else:
        st.warning("Exam not ready yet. Please wait for the teacher to upload the file.")
