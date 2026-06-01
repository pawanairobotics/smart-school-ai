import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.title("🎓 Smart School Exam Portal")

# Google Sheets से जुड़ें
conn = st.connection("gsheets", type=GSheetsConnection)

role = st.sidebar.radio("Login:", ["Student", "Teacher"])

# --- STUDENT ---
if role == "Student":
    # 'Questions' नाम की टैब से सवाल लाएं
    df = conn.read(worksheet="Questions")
    
    name = st.text_input("अपना नाम लिखें:")
    if name:
        answers = {}
        for i, row in df.iterrows():
            answers[i] = st.radio(f"Q{i+1}: {row['Question']}", [row['Opt1'], row['Opt2'], row['Opt3'], row['Opt4']])
        
        if st.button("Submit Exam"):
            score = sum(1 for i, row in df.iterrows() if answers[i] == row['CorrectAnswer'])
            
            # रिजल्ट को 'Results' टैब में जोड़ें
            new_data = pd.DataFrame([{"Name": name, "Score": score, "Date": str(pd.Timestamp.now())}])
            existing_data = conn.read(worksheet="Results")
            updated_df = pd.concat([existing_data, new_data], ignore_index=True)
            conn.update(worksheet="Results", data=updated_df)
            
            st.success(f"Result save हो गया! आपका स्कोर: {score}")

# --- TEACHER ---
elif role == "Teacher":
    st.header("Teacher Dashboard")
    results = conn.read(worksheet="Results")
    st.dataframe(results)
