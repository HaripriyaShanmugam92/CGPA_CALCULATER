import streamlit as st

# Theme configuration
st.set_page_config(page_title="CGPA Calculator", layout="centered")

# Mapping grades to grade points
GRADE_POINTS = {
    "O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "C": 5, "U": 0
}

# Function to calculate SGPA
def calculate_sgpa(grades, credits):
    total_points = sum(GRADE_POINTS[grade] * credit for grade, credit in zip(grades, credits))
    total_credits = sum(credits)
    return round(total_points / total_credits, 2) if total_credits > 0 else 0.0

# Function to calculate CGPA
def calculate_cgpa(previous_cgpa, previous_credits, current_sgpa, current_credits):
    total_points = (previous_cgpa * previous_credits) + (current_sgpa * current_credits)
    total_credits = previous_credits + current_credits
    return round(total_points / total_credits, 2) if total_credits > 0 else 0.0

# UI: Title
st.title("🎓 SGPA & CGPA Calculator")

# Horizontal Grade Table
st.markdown("### 📊 Grade-to-Point Table")
grade_row = " | ".join(GRADE_POINTS.keys())  
points_row = " | ".join(map(str, GRADE_POINTS.values()))  

st.markdown(f"""
| {grade_row} |
| {' | '.join(['---'] * len(GRADE_POINTS))} |
| {points_row} |
""")

# Previous semester details
is_first_semester = st.radio("📌 Is this your first semester?", ("Yes", "No"))

previous_cgpa, previous_credits = 0, 0
if is_first_semester == "No":
    col1, col2 = st.columns(2)
    with col1:
        previous_cgpa = st.number_input("Enter Previous CGPA (out of 10)", min_value=0.0, max_value=10.0, step=0.01, value=0.0)
    with col2:
        previous_credits = st.number_input("Enter Total Credits from Previous Semesters", min_value=1, step=1, value=1)

st.subheader("📚 Current Semester Details")

# Input for subjects
num_subjects = st.number_input("Number of Subjects", min_value=1, step=1, value=5)
grades, credits = [], []

for i in range(1, num_subjects + 1):
    col1, col2 = st.columns(2)
    with col1:
        grade = st.selectbox(f"🎯 Grade for Subject {i}", list(GRADE_POINTS.keys()), key=f"grade_{i}")
    with col2:
        credit = st.number_input(f"📘 Credits for Subject {i}", min_value=1, step=1, value=3, key=f"credit_{i}")
    grades.append(grade)
    credits.append(credit)

# Calculate SGPA & CGPA
if st.button("📊 Calculate SGPA & CGPA"):
    current_sgpa = calculate_sgpa(grades, credits)
    current_credits = sum(credits)
    st.success(f"✅ Your Current Semester SGPA: **{current_sgpa}**")

    if is_first_semester == "No":
        cgpa = calculate_cgpa(previous_cgpa, previous_credits, current_sgpa, current_credits)
        st.success(f"🎓 Your Updated CGPA: **{cgpa}**")
    else:
        st.info("⚠️ Since this is your first semester, CGPA is the same as SGPA.")
