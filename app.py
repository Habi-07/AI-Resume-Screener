import streamlit as st
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: rgb(59,130,246);

[data-testid="stHeader"] {
    background: #fff;
}
[data-testid="stSidebar"] {
    background-color: #fff;
}
.main-title {
    color: #0F172A;
    font-size: 42px;
    font-weight: 700;
    text-align: center;
}
.card {
    background-color: #fff;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.08);
    margin-bottom: 20px;
}
</style>
""",unsafe_allow_html=True)
import pandas as pd
from parser import extract_text_from_pdf
from skills import extract_skills, compare_skills
from scorer import (
    calculate_similarity,
    calculate_skill_match,
    calculate_final_score
)
from llm_analyzer import analyze_resume_with_llm
st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide"
)
st.title("📄 AI Resume Screening System")
st.write(
    "Analyze multiple resumes against a job description "
    "using skill matching, TF-IDF similarity and LLM analysis."
)
job_description = st.text_area(
    "📋 Job Description",
    height=200,
    placeholder=(
        "Example: Python developer with SQL, "
        "React, Git and Machine Learning skills."
    )
)
resumes = st.file_uploader(
    "📄 Upload Resume PDFs",
    type=["pdf"],
    accept_multiple_files=True
)
if st.button("🔍 Analyze Resumes"):
    if not resumes:
        st.warning(
            "Please upload at least one resume."
        )
    elif not job_description.strip():
        st.warning(
            "Please enter a job description."
        )
    else:
        results = []
        resume_texts = {}
        job_skills = extract_skills(
            job_description
        )
        for resume in resumes:
            resume_text = extract_text_from_pdf(
                resume
            )
            resume_texts[resume.name] = resume_text
            resume_skills = extract_skills(
                resume_text
            )
            matched_skills, missing_skills = (
                compare_skills(
                    resume_skills,
                    job_skills
                )
            )
            similarity_score = calculate_similarity(
                resume_text,
                job_description
            )
            skill_match = calculate_skill_match(
                resume_skills,
                job_skills
            )
            final_score = calculate_final_score(
                similarity_score,
                skill_match
            )
            results.append({
                "Candidate": resume.name,
                "Matching Score": final_score,
                "Skill Match": round(
                    skill_match * 100,
                    2
                ),
                "TF-IDF Similarity": round(
                    similarity_score * 100,
                    2
                ),
                "Matched Skills": ", ".join(
                    matched_skills
                ),

                "Missing Skills": ", ".join(
                    missing_skills
                )
            })
        df = pd.DataFrame(results)
        df = df.sort_values(
            by="Matching Score",
            ascending=False
        ).reset_index(drop=True)
        df.insert(
            0,
            "Rank",
            range(1, len(df) + 1)
        )
        st.session_state["results"] = df

        st.session_state["resume_texts"] = resume_texts

        st.session_state["job_description"] = (
            job_description
        )
if "results" in st.session_state:
    df = st.session_state["results"]
    st.divider()
    st.subheader(
        "🏆 Candidate Matching Ranking"
    )
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    st.divider()
    st.header(
        "📊 Screening Dashboard"
    )
    total_candidates = len(df)
    average_score = round(
        df["Matching Score"].mean(),
        2
    )
    highest_score = round(
        df["Matching Score"].max(),
        2
    )
    average_skill_match = round(
        df["Skill Match"].mean(),
        2
    )
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            "👥 Total Candidates",
            total_candidates
        )
    with col2:
        st.metric(
            "📊 Average Score",
            f"{average_score}%"
        )
    with col3:
        st.metric(
            "🎯 Highest Score",
            f"{highest_score}%"
        )
    with col4:
        st.metric(
            "🛠️ Avg Skill Match",
            f"{average_skill_match}%"
        )
    st.subheader(
        "📈 Candidate Matching Scores"
    )
    chart_data = df.set_index(
        "Candidate"
    )["Matching Score"]
    st.bar_chart(
        chart_data
    )
    st.divider()
    st.subheader(
        "👤 Candidate Details"
    )
    selected_candidate = st.selectbox(
        "Select a candidate",
        df["Candidate"].tolist()
    )
    candidate_data = df[
        df["Candidate"] == selected_candidate
    ].iloc[0]
    col1, col2 = st.columns(2)
    with col1:
        st.write(
            "### 🎯 Matching Score"
        )
        st.metric(
            "Score",
            f'{candidate_data["Matching Score"]}%'
        )
        st.write(
            "### 🛠️ Matched Skills"
        )
        if candidate_data["Matched Skills"]:

            st.success(
                candidate_data["Matched Skills"]
            )
        else:
            st.info(
                "No matched skills found."
            )
    with col2:
        st.write(
            "### 📚 TF-IDF Similarity"
        )
        st.metric(
            "Similarity",
            f'{candidate_data["TF-IDF Similarity"]}%'
        )
        st.write(
            "### ⚠️ Missing Skills"
        )
        if candidate_data["Missing Skills"]:
            st.warning(
                candidate_data["Missing Skills"]
            )
        else:
            st.success(
                "No missing required skills."
            )
    st.divider()
    csv = df.to_csv(
        index=False
    )
    st.download_button(
        "📥 Download Ranking CSV",
        csv,
        "candidate_ranking.csv",
        "text/csv"
    )
    st.divider()
    st.header(
        "🤖 AI Resume Analysis"
    )
    st.write(
        "Generate an LLM-based factual analysis "
        "for the selected candidate."
    )
    if st.button(
        "🤖 Generate AI Analysis"
    ):
        resume_text = (
            st.session_state["resume_texts"]
            [selected_candidate]
        )
        job_description = (
            st.session_state["job_description"]
        )
        with st.spinner(
            "Analyzing resume with AI..."
        ):

            analysis = analyze_resume_with_llm(
                resume_text,
                job_description
            )
        st.subheader(
            "AI Analysis"
        )
        st.markdown(
            analysis
        )
st.divider()
st.header("📄 Generate Candidate Report")
if st.button("📄 Generate PDF Report"):
    candidate_data = df[
        df["Candidate"] == selected_candidate
    ].iloc[0]
    resume_text = (
        st.session_state["resume_texts"]
        [selected_candidate]
    )
    job_description = (
        st.session_state["job_description"]
    )
    with st.spinner("Generating PDF report..."):
        # Generate LLM analysis
        llm_analysis = analyze_resume_with_llm(
            resume_text,
            job_description
        )
        output_path = (
            f"{selected_candidate}_report.pdf"
        )
    st.success("PDF report generated successfully!")

    with open(output_path, "rb") as pdf_file:

        st.download_button(
            "📥 Download PDF Report",
            pdf_file,
            file_name=output_path,
            mime="application/pdf"
        )