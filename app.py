import streamlit as st
import pandas as pd
import re

# --- Map grades to GPV ---
grade_to_gpv = {
    "A+": 4.0,
    "A": 4.0,
    "A-": 3.7,
    "B+": 3.3,
    "B": 3.0,
    "B-": 2.7,
    "C+": 2.3,
    "C": 2.0,
    "C-": 1.7,
    "D+": 1.3,
    "D": 1.0,
    "E": 0.0,
    "F": 0.0
}

# --- Extract credits from course code ---
def extract_credits(code):
    match = re.search(r"(\d)", code)  # first digit after letters
    if match:
        return int(match.group(1))
    return 0

st.title("🎓 GPA Calculator - OUSL BSc IT")
st.write("Download your results from Myousl and upload here")

uploaded_file = st.file_uploader("Upload your marks Excel file", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # Check required columns
    if "Course Code" in df.columns and "Grade" in df.columns:
        results = []
        total_points = 0
        total_credits = 0

        for _, row in df.iterrows():
            code = str(row["Course Code"])
            grade = str(row["Grade"]).strip()

            credits = extract_credits(code)
            gpv = grade_to_gpv.get(grade, None)

            if gpv is not None:
                total_points += gpv * credits
                total_credits += credits
                results.append([code, grade, credits, gpv])

        # --- Display results ---
        if total_credits > 0:
            gpa = total_points / total_credits
            results_df = pd.DataFrame(results, columns=["Course Code", "Grade", "Credits", "GPV"])
            st.subheader("📊 Results")
            st.dataframe(results_df)
            st.success(f"✅ Your GPA: **{gpa:.2f}**")
        else:
            st.error("Could not calculate GPA. Please check your grades.")
    else:
        st.error("❌ Could not find required columns. Please make sure your Excel has 'Course Code' and 'Grade'.")
