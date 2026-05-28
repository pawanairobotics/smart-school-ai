import streamlit as st

# 1. हेडर और टाइटल
st.title("🏫 Smart School AI Assistant")
st.write("बच्चों द्वारा बनाया गया भविष्य का एआई प्रोजेक्ट!")

# 2. मेनू बनाना (Sidebar)
menu = st.sidebar.selectbox("Choose AI Feature:", ["Mood Scanner", "Marks Analyst", "Security Shield"])

# 3. फीचर 1: Mood Scanner
if menu == "Mood Scanner":
    st.subheader("🎭 Student Mood Scanner")
    feedback = st.text_area("How was your day?")
    if st.button("Analyze Mood"):
        pos_words = ["good", "great", "awesome", "happy"]
        neg_words = ["bad", "boring", "sad", "worst"]
        words = feedback.lower().split()
        pos = sum(1 for w in words if w in pos_words)
        neg = sum(1 for w in words if w in neg_words)
        
        if pos > neg: st.success("😊 Positive Energy!")
        elif neg > pos: st.error("😡 Negative Alert!")
        else: st.info("😐 Neutral feedback.")

# 4. फीचर 2: Marks Analyst
elif menu == "Marks Analyst":
    st.subheader("📊 Class Rank Analyst")
    m1 = st.number_input("Student 1 Marks:", 0, 100)
    m2 = st.number_input("Student 2 Marks:", 0, 100)
    if st.button("Generate Report"):
        marks = [m1, m2]
        st.write(f"📈 Average: {sum(marks)/len(marks)}")
        st.write(f"🥇 Highest: {max(marks)}")

# 5. फीचर 3: Security Shield
elif menu == "Security Shield":
    st.subheader("🔐 Security Shield")
    pwd = st.text_input("Enter Password:", type="password")
    if st.button("Check Strength"):
        if len(pwd) >= 8 and any(c.isdigit() for c in pwd):
            st.success("🟢 Secure Password!")
        else:
            st.error("🔴 Too weak!")