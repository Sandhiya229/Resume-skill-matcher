import streamlit as st
import pdfplumber
from docx import Document

# -------------------- PAGE SETUP --------------------
st.set_page_config(
    page_title="Resume Skill Matcher",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Resume Skill Matcher & Career Guide")

# -------------------- ROLE SKILL DATABASE --------------------
ROLE_SKILLS = {
    "Data Analyst": {
        "skills": ["python", "sql", "excel", "power bi", "tableau", "statistics", "pandas"],
        "projects": [
            "Sales Data Analysis Dashboard",
            "Customer Churn Analysis",
            "Financial Insights using Python"
        ]
    },
    "Python Developer": {
        "skills": ["python", "oop", "flask", "django", "api", "mysql", "git"],
        "projects": [
            "REST API using Flask",
            "Django Web Application",
            "Automation Script Project"
        ]
    },
    "Frontend Developer": {
        "skills": ["html", "css", "javascript", "react", "bootstrap", "git"],
        "projects": [
            "Portfolio Website",
            "React Dashboard App",
            "Landing Page Clone"
        ]
    }
}

# -------------------- SAMPLE RESUME CONTENT --------------------
RESUME_TEMPLATES = {
    "Frontend Developer": {
        "name": "John Doe",
        "title": "Frontend Developer",
        "contact": "📍 City | 📧 john@email.com | 📱 9876543210 | GitHub | LinkedIn",
        "summary": "Creative Frontend Developer with strong knowledge of HTML, CSS, JavaScript, and React. Passionate about building responsive and user-friendly web applications.",
        "skills": [
            "HTML, CSS, JavaScript, React, Bootstrap",
            "Git, GitHub, VS Code",
            "Responsive Design, API Integration"
        ],
        "experience": [
            "Frontend Developer – ABC Tech (2022–Present)\n• Built responsive UI using React\n• Improved performance by 30%",
            "Junior Developer – XYZ Web (2020–2022)\n• Developed static & dynamic pages\n• Fixed UI bugs"
        ],
        "education": "B.Sc Computer Science – 2020",
        "projects": [
            "Portfolio Website – Personal responsive website",
            "React Dashboard – Admin dashboard using React",
            "Landing Page Clone – Pixel perfect UI clone"
        ],
        "certifications": [
            "Frontend Development – FreeCodeCamp",
            "JavaScript Mastery – Udemy"
        ]
    },

    "Python Developer": {
        "name": "Jane Smith",
        "title": "Python Developer",
        "contact": "📍 City | 📧 jane@email.com | 📱 9876543210 | GitHub | LinkedIn",
        "summary": "Python Developer with experience in backend development, REST APIs, and automation.",
        "skills": [
            "Python, OOP, Flask, Django",
            "MySQL, REST APIs",
            "Git, Docker"
        ],
        "experience": [
            "Python Developer – ABC Solutions (2021–Present)\n• Built REST APIs\n• Automated data pipelines",
            "Junior Python Developer – XYZ Tech (2019–2021)\n• Wrote backend logic\n• Debugged applications"
        ],
        "education": "B.Sc Computer Science – 2019",
        "projects": [
            "Flask REST API",
            "Automation Scripts",
            "Django Web App"
        ],
        "certifications": [
            "Python for Everybody – Coursera",
            "Advanced Python – Udemy"
        ]
    },

    "Data Analyst": {
        "name": "Michael Johnson",
        "title": "Data Analyst",
        "contact": "📍 City | 📧 michael@email.com | 📱 9876543210 | GitHub | LinkedIn",
        "summary": "Detail-oriented Data Analyst skilled in data analysis, visualization, and reporting.",
        "skills": [
            "Python, SQL, Excel",
            "Power BI, Tableau",
            "Data Cleaning, Statistics"
        ],
        "experience": [
            "Data Analyst – ABC Analytics (2020–Present)\n• Created dashboards\n• Delivered business insights",
            "Junior Analyst – XYZ Corp (2018–2020)\n• Data cleaning\n• Report generation"
        ],
        "education": "B.Sc Statistics – 2018",
        "projects": [
            "Sales Dashboard",
            "Customer Segmentation",
            "Financial Analysis"
        ],
        "certifications": [
            "Google Data Analytics",
            "SQL for Data Science"
        ]
    }
}

# -------------------- FUNCTIONS --------------------
def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.lower()

def calculate_match(resume_text, role):
    skills = ROLE_SKILLS[role]["skills"]
    matched = [s for s in skills if s in resume_text]
    missing = [s for s in skills if s not in resume_text]
    percent = int((len(matched) / len(skills)) * 100)
    return percent, matched, missing

def generate_docx(role, data):
    doc = Document()

    doc.add_heading(data["name"], level=1)
    doc.add_paragraph(data["title"])
    doc.add_paragraph(data["contact"])

    doc.add_heading("Professional Summary", level=2)
    doc.add_paragraph(data["summary"])

    doc.add_heading("Skills", level=2)
    for s in data["skills"]:
        doc.add_paragraph(f"• {s}")

    doc.add_heading("Experience", level=2)
    for e in data["experience"]:
        doc.add_paragraph(e)

    doc.add_heading("Projects", level=2)
    for p in data["projects"]:
        doc.add_paragraph(f"• {p}")

    doc.add_heading("Education", level=2)
    doc.add_paragraph(data["education"])

    doc.add_heading("Certifications", level=2)
    for c in data["certifications"]:
        doc.add_paragraph(f"• {c}")

    return doc

# -------------------- USER INPUT --------------------
uploaded_file = st.file_uploader("📤 Upload Your Resume (PDF)", type=["pdf"])
selected_role = st.selectbox("🎯 Select Job Role", ROLE_SKILLS.keys())

if st.button("🚀 Analyze Resume"):
    if uploaded_file is None:
        st.warning("Please upload your resume")
        st.stop()

    resume_text = extract_text_from_pdf(uploaded_file)
    percent, matched, missing = calculate_match(resume_text, selected_role)

    st.subheader("📊 Resume Match Result")
    st.metric("Match Percentage", f"{percent}%")

    col1, col2 = st.columns(2)
    with col1:
        st.success("Matched Skills")
        for s in matched:
            st.write("✅", s)

    with col2:
        st.error("Missing Skills")
        for s in missing:
            st.write("❌", s)

    st.subheader("🧠 Suggested Projects")
    for p in ROLE_SKILLS[selected_role]["projects"]:
        st.write("•", p)

    # -------------------- DOWNLOAD SAMPLE RESUME --------------------
    doc = generate_docx(selected_role, RESUME_TEMPLATES[selected_role])

    st.download_button(
        "📥 Download Example Resume (DOCX)",
        data=doc._part.blob,
        file_name=f"{selected_role}_Sample_Resume.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
