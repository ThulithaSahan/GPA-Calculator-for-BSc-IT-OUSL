import streamlit as st
import pandas as pd
import sqlite3

# Function to convert marks -> Grade Point Value
def get_gpv(marks):
    if 85 <= marks <= 100: return 4.00
    elif 70 <= marks <= 84: return 4.00
    elif 65 <= marks <= 69: return 3.70
    elif 60 <= marks <= 64: return 3.30
    elif 55 <= marks <= 59: return 3.00
    elif 50 <= marks <= 54: return 2.70
    elif 45 <= marks <= 49: return 2.30
    elif 40 <= marks <= 44: return 2.00
    elif 35 <= marks <= 39: return 1.70
    elif 30 <= marks <= 34: return 1.30
    elif 20 <= marks <= 29: return 1.00
    else: return 0.00

# Ignore these subjects
ignore_list = ["ADE3430","COE3200","FDE3030","LTE3413"]

st.title("📊 GPA Calculator for BSc IT (OUSL)")

uploaded_file = st.file_uploader("Upload your Marks Sheet (Excel)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Normalize column names (lowercase, no spaces)
    df.columns = df.columns.str.strip().str.replace(" ", "").str.lower()

    st.write("✅ Columns detected:", df.columns.tolist())

    # Try to detect course code and marks columns
    if "coursecode" not in df.columns or "marks" not in df.columns:
        st.error("❌ Could not find required columns. Please make sure your Excel has 'Course Code' and 'Marks'.")
    else:
        # Filter out non-GPA subjects
        df = df[~df['coursecode'].isin(ignore_list)]

        total_points, total_credits = 0, 0
        results = []

        for _, row in df.iterrows():
            code = str(row['coursecode'])
            marks = row['marks']
            try:
                credits = int(code[1])   # 2nd digit = credits
            except:
                credits = 0  # fallback if code is weird

            gpv = get_gpv(marks)

            total_points += gpv * credits
            total_credits += credits
            results.append([code, marks, credits, gpv])

        gpa = round(total_points / total_credits, 2) if total_credits > 0 else 0

        result_df = pd.DataFrame(results, columns=["CourseCode", "Marks", "Credits", "GPV"])
        st.dataframe(result_df)
        st.success(f"🎓 Your GPA is: **{gpa}**")

        # Save results to SQLite
        conn = sqlite3.connect("marks.db")
        result_df.to_sql("marks", conn, if_exists="replace", index=False)
        conn.close()
