import streamlit as st
import pandas as pd
import os
import base64
from dotenv import load_dotenv
from utils.jd_utils import extract_job_description
from utils.resume_parser import extract_resume_data
from utils.groq_utils import get_match_score
from utils.email_utils import send_selection_email

# Load environment variables
load_dotenv()

# Streamlit page configuration
st.set_page_config(page_title="HireFlare", layout="wide")

# 💅 Custom CSS styling
st.markdown("""
    <style>
    .stApp {
        background-color: #0d1b2a;
        color: white;
    }
    h1 {
        color: #add8e6 !important;
        text-align: center;
    }
    div.stButton > button:first-child {
        background-color: #800080;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6em 1.2em;
        font-size: 16px;
    }
    div.stButton > button:first-child:hover {
        background-color: #a020f0;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown("<h1>🤖 HireFlare</h1>", unsafe_allow_html=True)
st.markdown("Upload a job description CSV file and candidate resumes to auto-match them using AI!")

# File upload inputs
jd_csv = st.file_uploader("📄 Upload Job Description CSV", type=["csv"])
resumes = st.file_uploader("📁 Upload Resume PDFs", type=["pdf"], accept_multiple_files=True)

if jd_csv:
    try:
        df = pd.read_csv(jd_csv, encoding='windows-1252')
        df.columns = [col.strip().lower() for col in df.columns]

        if 'title' not in df.columns or 'description' not in df.columns:
            st.error("❌ Your CSV must contain 'title' and 'description' columns.")
        else:
            job_titles = df['title'].dropna().unique().tolist()
            selected_title = st.selectbox("🧠 Choose Job Title", job_titles)

            if selected_title and resumes:
                job_desc = extract_job_description(df, selected_title)

                results = []
                for resume in resumes:
                    name, text, email = extract_resume_data(resume)
                    score = get_match_score(job_desc, text)
                    results.append({
                        "PDF": resume.name,
                        "Name": name,
                        "Email": email,
                        "Score": round(score, 2),
                        "File": resume
                    })

                results_df = pd.DataFrame(sorted(results, key=lambda x: x["Score"], reverse=True))
                st.success(f"✅ {len(results_df)} resumes processed.")
                st.dataframe(results_df.drop("File", axis=1))

                # Shortlist candidates with score >= 65
                shortlisted = results_df[results_df["Score"] >= 65]
                st.markdown(f"### 🏆 ✅ {len(shortlisted)} candidates shortlisted for {selected_title}!")

                st.markdown("---")
                st.markdown("### 📋 Shortlisted Candidate Details")
                for i, row in shortlisted.iterrows():
                    st.markdown(f"#### 👤 Name: {row['Name']}")
                    st.markdown(f"📧 Email: {row['Email']}")
                    st.markdown(f"📄 Resume: {row['PDF']}")
                    st.download_button(
                        label="⬇️ Download Resume",
                        data=row['File'].read(),
                        file_name=row['PDF'],
                        mime='application/pdf',
                        key=f"download_{i}"
                    )

                if not shortlisted.empty:
                    if st.button("📬 Send Selection Emails"):
                        for _, row in shortlisted.iterrows():
                            send_selection_email(row["Email"], row["Name"], selected_title)
                        st.success("✅ Emails sent successfully!")

    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")
