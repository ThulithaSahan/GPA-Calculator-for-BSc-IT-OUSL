import streamlit as st
import pandas as pd
import sqlite3

# Grade to GPV mapping
grade_to_gpv = {
    "A+": 4.00, "A": 4.00, "A-": 3.70,
    "B+": 3.30, "B": 3.00, "B-": 2.70,
    "C+": 2.30, "C": 2.00, "C-": 1.70,
    "D+": 1.30, "D": 1.00, "E": 0.00
}

# Ignore these subjects
ignore_list = ["ADE3430","COE3200","FDE3030","LTE3413"]

st.title("📊 GPA Calculator for BSc IT (OUSL)")

uploaded_file = st.file_uploader("Upload your Marks Sheet (Excel)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Normalize column names
    df.columns = df.columns.str.strip()

    st.write("✅ Columns detected:", df.columns.tolist())

    if "Course Code" not in df.columns or "Grade" not in df.columns:
        st.error("❌ Could not find 'Course Code' and 'Grade' columns in your Excel.")
    else:
        # Remove ignored subjects
        df = df[~df["Course Code"].isin(ignore_list)]

        total_points, total_credits = 0, 0
        results = []

        for _, row in df.iterrows():
            code = str(row["Course Code"])
            grade = str(row["Grade"]).strip()

            try:
                credits = int(code[1])  # 2nd digit = credits
            except:
                credits = 0

            gpv = grade_to_gpv.get(grade, None)

            if gpv is not None:  # Only count valid grades
                total_points += gpv * credits
                total_credits += credits
                results.append([code, grade, credits, gpv])

        gpa = round(total_points / total_credits, 2) if total_credits > 0 else 0

        result_df = pd.DataFrame(results, columns=["Course Code", "Grade", "Credits", "GPV"])
        st.dataframe(result_df)
        st.success(f"🎓 Your GPA is: **{gpa}**")

        # Save to SQLite database
        conn = sqlite3.connect("marks.db")
        result_df.to_sql("marks", conn, if_exists="replace", index=False)
        conn.close()
