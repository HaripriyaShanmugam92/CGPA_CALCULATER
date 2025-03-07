import streamlit as st

# Mapping grades to grade points
GRADE_POINTS = {
    "O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "C": 5, "U": 0
}

# Function to calculate SGPA for the current semester
def calculate_sgpa(grades, credits):
    total_points = sum(GRADE_POINTS[grade] * credit for grade, credit in zip(grades, credits))
    total_credits = sum(credits)
    return round(total_points / total_credits, 2) if total_credits > 0 else 0.0

# Function to calculate overall CGPA including previous semesters
def calculate_cgpa(previous_cgpa, previous_credits, current_sgpa, current_credits):
    total_points = (previous_cgpa * previous_credits) + (current_sgpa * current_credits)
    total_credits = previous_credits + current_credits
    return round(total_points / total_credits, 2) if total_credits > 0 else 0.0

# Streamlit UI
st.title("🎓 SGPA & CGPA Calculator")

# Step 1: Check if it's the first semester
is_first_semester = st.radio("Is this your first semester?", ("Yes", "No"))

# Initialize previous CGPA and credits
previous_cgpa = 0.0
previous_credits = 0

# Step 2: If not the first semester, get previous CGPA & credits
if is_first_semester == "No":
    col1, col2 = st.columns(2)
    with col1:
        previous_cgpa = st.number_input("Enter Previous CGPA (out of 10)", min_value=0.0, max_value=10.0, step=0.01, value=0.0)
    with col2:
        previous_credits = st.number_input("Enter Total Credits from Previous Semesters", min_value=1, step=1, value=1)

st.subheader("📌 Current Semester Details")

# Step 3: Number of subjects
num_subjects = st.number_input("Number of Subjects in Current Semester", min_value=1, step=1, value=5)

grades = []
credits = []

# Step 4: Input grades and credits for each subject
for sub in range(1, num_subjects + 1):
    col1, col2 = st.columns(2)
    with col1:
        grade = st.selectbox(f"🎯 Grade for Subject {sub}", list(GRADE_POINTS.keys()), key=f"grade_{sub}")
    with col2:
        credit = st.number_input(f"📘 Credits for Subject {sub}", min_value=1, step=1, value=3, key=f"credit_{sub}")

    grades.append(grade)
    credits.append(credit)

# Step 5: Calculate SGPA & CGPA
if st.button("📊 Calculate SGPA & CGPA"):
    current_sgpa = calculate_sgpa(grades, credits)
    current_credits = sum(credits)
    
    st.success(f"✅ Your Current Semester SGPA: **{current_sgpa}**")

    if is_first_semester == "No":
        cgpa = calculate_cgpa(previous_cgpa, previous_credits, current_sgpa, current_credits)
        st.success(f"🎓 Your Updated CGPA: **{cgpa}**")
    else:
        st.info("⚠️ Since this is your first semester, CGPA is the same as SGPA.")
