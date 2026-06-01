import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. Google Sheet से कनेक्ट करें
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🎓 Smart School Exam Portal")
role = st.sidebar.radio("Login:", ["Student", "Teacher"])

# --- STUDENT SECTION ---
if role == "Student":
    # Google Sheet से सवाल पढ़ें (Sheet का नाम 'Questions' रखें)
    df_questions = conn.read(worksheet="Questions", usecols=[0,1,2,3,4,5], ttl=5)
    
    name = st.text_input("अपना नाम लिखें:")
    if name:
        answers = {}
        for i, row in df_questions.iterrows():
            answers[i] = st.radio(f"Q{i+1}: {row['Question']}", [row['Opt1'], row['Opt2'], row['Opt3'], row['Opt4']])
        
        if st.button("Submit Exam"):
            score = sum(1 for i, row in df_questions.iterrows() if answers[i] == row['CorrectAnswer'])
            
            # रिजल्ट को 'Results' नाम की शीट में लिखें
            new_result = pd.DataFrame([{"Name": name, "Score": score, "Date": str(pd.Timestamp.now())}])
            existing_results = conn.read(worksheet="Results")
            updated_results = pd.concat([existing_results, new_result], ignore_index=True)
            conn.update(worksheet="Results", data=updated_results)
            
            st.success(f"रिजल्ट सेव हो गया! आपका स्कोर: {score}")

# --- TEACHER SECTION ---
elif role == "Teacher":
    st.header("Teacher Dashboard")
    results = conn.read(worksheet="Results")
    st.write("सारे बच्चों का रिजल्ट:", results)
