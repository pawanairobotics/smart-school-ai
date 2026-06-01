import streamlit as st
import pandas as pd

# Google Sheet का Public URL (इसे अपनी Sheet ID से बदलें)
SHEET_ID = "1--lnxYLF1ftOmmD0Neb5nitQjaxgWv7C5eRXQaPvxNs" 
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Sheet1"

st.set_page_config(page_title="Smart Exam Portal", layout="centered")
st.title("🎓 Smart School Exam Portal")

# डेटा लोड करने का फंक्शन
@st.cache_data(ttl=60)
def load_data():
    return pd.read_csv(SHEET_URL)

try:
    df = load_data()
    
    st.sidebar.title("Login Panel")
    role = st.sidebar.radio("Login as:", ["Student"])
    
    st.header("Online Examination")
    name = st.text_input("अपना नाम लिखें:")
    
    if name:
        user_answers = {}
        # 4 ऑप्शंस के साथ सवाल डिस्प्ले करें
        for i, row in df.iterrows():
            user_answers[i] = st.radio(
                f"Q{i+1}: {row['Question']}", 
                [row['Opt1'], row['Opt2'], row['Opt3'], row['Opt4']], 
                key=i
            )
        
        if st.button("Submit Exam"):
            score = 0
            for i, row in df.iterrows():
                if user_answers[i] == row['CorrectAnswer']:
                    score += 1
            
            st.balloons()
            st.success(f"बहुत बढ़िया {name}! आपका स्कोर: {score}/{len(df)}")
            
except Exception as e:
    st.warning("कृपया अपनी Google Sheet ID सही से सेटअप करें।")
