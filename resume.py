import streamlit as st
import pdfplumber
import docx
from docx import Document
from io import BytesIO
import matplotlib.pyplot as plt
import re

# ---------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="Resume Analyzer Pro",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Resume Analyzer & Career Guide")

# ---------------- ROLE DATABASE ----------------

ROLE_SKILLS = {
    "Python Developer": {
        "skills": ["python", "django", "flask", "api", "mysql", "git", "oop"],
        "roadmap": [
            "Learn Python Basics",
            "Master OOP",
            "Learn Django/Flask",
            "Build REST APIs",
            "Learn Databases",
            "Deploy Projects"
        ]
    },

    "Frontend Developer": {
        "skills": ["html", "css", "javascript", "react", "bootstrap", "git"],
        "roadmap": [
            "HTML & CSS",
            "JavaScript",
            "React",
            "UI Frameworks",
            "Git & GitHub",
            "Build Projects"
        ]
    },

    "Data Analyst": {
        "skills": ["python", "sql", "excel", "power bi", "tableau", "statistics"],
        "roadmap": [
            "Excel & SQL",
            "Python for Analysis",
            "Data Cleaning",
            "Visualization",
            "Power BI/Tableau",
            "Case Studies"
        ]
    }
}


# ---------------- TEXT EXTRACT ----------------

def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.lower()


def read_docx(file):
    doc = docx.Document(file)
    text = ""

    for para in doc.paragraphs:
        text += para.text + " "

    return text.lower()


def clean_text(text):
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    return text.lower()


# ---------------- MATCHING ----------------

def analyze_resume(text, role):

    skills = ROLE_SKILLS[role]["skills"]

    matched = []
    missing = []

    for s in skills:
        if s in text:
            matched.append(s)
        else:
            missing.append(s)

    percent = int((len(matched) / len(skills)) * 100)

    return percent, matched, missing


# ---------------- RESUME GENERATOR ----------------

def generate_resume(name, role, skills, email):

    doc = Document()

    doc.add_heading(name, level=1)
    doc.add_paragraph(role)
    doc.add_paragraph(email)

    doc.add_heading("Summary", level=2)
    doc.add_paragraph(
        f"Motivated {role} with strong skills in {', '.join(skills)}."
    )

    doc.add_heading("Skills", level=2)
    for s in skills:
        doc.add_paragraph(f"• {s}")

    doc.add_heading("Projects", level=2)
    doc.add_paragraph("• Resume Analyzer Project")
    doc.add_paragraph("• Portfolio Website")

    doc.add_heading("Education", level=2)
    doc.add_paragraph("Bachelor's Degree")

    return doc


# ---------------- UI ----------------

st.sidebar.header("⚙️ Options")

role = st.sidebar.selectbox(
    "Select Job Role",
    ROLE_SKILLS.keys()
)

upload = st.file_uploader(
    "📤 Upload Resume (PDF / DOCX)",
    type=["pdf", "docx"]
)


# ---------------- ANALYZE ----------------

if st.button("🚀 Analyze Resume"):

    if upload is None:
        st.warning("Please upload resume")
        st.stop()

    if upload.type == "application/pdf":
        text = read_pdf(upload)

    else:
        text = read_docx(upload)

    text = clean_text(text)

    score, matched, missing = analyze_resume(text, role)

    # -------- RESULT --------

    st.subheader("📊 Resume Score")

    st.metric("Match Percentage", f"{score}%")

    col1, col2 = st.columns(2)

    with col1:
        st.success("Matched Skills")
        for s in matched:
            st.write("✅", s)

    with col2:
        st.error("Missing Skills")
        for s in missing:
            st.write("❌", s)


    # -------- CHART --------

    st.subheader("📈 Skill Match Chart")

    labels = ["Matched", "Missing"]
    sizes = [len(matched), len(missing)]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    ax.axis("equal")

    st.pyplot(fig)


    # -------- ROADMAP --------

    st.subheader("🛣️ Career Roadmap")

    for i, step in enumerate(ROLE_SKILLS[role]["roadmap"], 1):
        st.write(f"Step {i} → {step}")


# ---------------- RESUME BUILDER ----------------

st.divider()

st.header("📝 Build Your Own Resume")

name = st.text_input("Your Name")
email = st.text_input("Email")
skills_input = st.text_input("Skills (comma separated)")

if st.button("📄 Generate Resume"):

    if not name or not email or not skills_input:
        st.warning("Fill all details")
        st.stop()

    skill_list = [s.strip() for s in skills_input.split(",")]

    resume_doc = generate_resume(
        name,
        role,
        skill_list,
        email
    )

    # Save in memory
    file = BytesIO()
    resume_doc.save(file)
    file.seek(0)

    st.success("Resume Created Successfully ✅")

    st.download_button(
        "⬇️ Download Resume",
        data=file,
        file_name="My_Resume.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
