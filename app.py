import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheet Connection Setup
# ध्यान दें: इसके लिए आपको बस अपनी JSON फाइल को GitHub पर 'credentials.json' नाम से अपलोड करना होगा
def connect_sheet():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    return client

st.title("🎓 Smart School Exam Portal")

# कनेक्ट करें
try:
    client = connect_sheet()
    sheet_db = client.open("School_Exam_DB") # अपनी Google Sheet का नाम यहाँ लिखें
    
    role = st.sidebar.radio("Login:", ["Student", "Teacher"])
    
    # --- STUDENT PANEL ---
    if role == "Student":
        sheet_q = sheet_db.worksheet("Questions")
        df = pd.DataFrame(sheet_q.get_all_records())
        
        name = st.text_input("अपना नाम लिखें:")
        if name:
            answers = {}
            for i, row in df.iterrows():
                answers[i] = st.radio(f"Q{i+1}: {row['Question']}", [row['Opt1'], row['Opt2'], row['Opt3'], row['Opt4']])
            
            if st.button("Submit Exam"):
                score = sum(1 for i, row in df.iterrows() if answers[i] == row['CorrectAnswer'])
                sheet_r = sheet_db.worksheet("Results")
                sheet_r.append_row([name, score, str(pd.Timestamp.now())])
                st.success(f"Result save ho gaya! Score: {score}")

    # --- TEACHER PANEL ---
    elif role == "Teacher":
        sheet_r = sheet_db.worksheet("Results")
        st.write("सारे बच्चों का रिजल्ट:", pd.DataFrame(sheet_r.get_all_records()))

except Exception as e:
    st.error("कनेक्शन में दिक्कत है। सुनिश्चित करें कि 'credentials.json' फाइल GitHub पर मौजूद है।")
