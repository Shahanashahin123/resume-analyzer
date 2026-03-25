import streamlit as st
from model import calculate_match, skill_match
from PyPDF2 import PdfReader
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI Resume Analyzer", page_icon="🤖")

st.title("🤖 AI Resume Analyzer & Job Matcher")

# -----------------------------
# PDF UPLOAD
# -----------------------------
uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

resume_text = ""

if uploaded_file:
    pdf = PdfReader(uploaded_file)
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            resume_text += text

# -----------------------------
# JOB DESCRIPTION
# -----------------------------
jd = st.text_area("Paste Job Description")

# -----------------------------
# ANALYZE
# -----------------------------
if st.button("Analyze"):

    if not resume_text or not jd:
        st.warning("Please upload resume and enter job description")
    else:
        score = calculate_match(resume_text, jd)
        matched, missing = skill_match(resume_text)

        # -----------------------------
        # SCORE
        # -----------------------------
        st.subheader("📊 Match Score")
        st.success(f"{score:.2f}%")
        st.progress(int(score))

        if score > 70:
            st.success("Strong Match ✅")
        elif score > 40:
            st.warning("Moderate Match ⚠️")
        else:
            st.error("Low Match ❌")

        # -----------------------------
        # SKILLS
        # -----------------------------
        st.subheader("✅ Matched Skills")
        for skill in matched:
            st.markdown(f"- {skill}")

        st.subheader("❌ Missing Skills")
        for skill in missing:
            st.markdown(f"- {skill}")

        # -----------------------------
        # SUGGESTIONS
        # -----------------------------
        st.subheader("💡 Suggestions")
        if missing:
            st.write("Add these skills to improve your resume:")
            for skill in missing:
                st.markdown(f"- {skill}")
        else:
            st.success("Excellent match!")

        # -----------------------------
        # VISUALIZATION
        # -----------------------------
        st.subheader("📈 Score Visualization")

        fig, ax = plt.subplots()
        ax.bar(["Match Score"], [score])
        ax.set_ylim(0, 100)
        st.pyplot(fig)

        # -----------------------------
        # RESUME INSIGHTS
        # -----------------------------
        st.subheader("📄 Resume Insights")

        word_count = len(resume_text.split())
        st.write(f"Word Count: {word_count}")

        if word_count < 100:
            st.warning("Resume too short")
        elif word_count < 300:
            st.info("Resume length is okay")
        else:
            st.success("Good resume length")

        # -----------------------------
        # ROLE RECOMMENDATION
        # -----------------------------
        st.subheader("🎯 Recommended Roles")

        text = resume_text.lower()

        if "machine learning" in text:
            st.write("→ Machine Learning Engineer")
        if "sql" in text:
            st.write("→ Data Analyst")
        if "react" in text:
            st.write("→ Frontend Developer")

        # -----------------------------
        # MULTIPLE JOB MATCHING
        # -----------------------------
        st.subheader("📌 Match with Other Roles")

        jobs = [
            "Python Developer with Machine Learning",
            "Data Analyst with SQL and Power BI",
            "Frontend Developer with React",
            "AI Engineer with NLP and Deep Learning"
        ]

        for job in jobs:
            job_score = calculate_match(resume_text, job)
            st.write(f"{job} → {job_score:.2f}%")

        # -----------------------------
        # DOWNLOAD REPORT
        # -----------------------------
        report = f"""
Match Score: {score:.2f}%

Matched Skills:
{matched}

Missing Skills:
{missing}
"""

        st.download_button(
            label="📥 Download Report",
            data=report,
            file_name="resume_analysis.txt",
            mime="text/plain"
        )