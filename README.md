## HireFlare
## ai resume shortlister 

## 📌 Overview
**An intelligent recruitment tool that reads job descriptions and candidate resumes (TXT/PDF/DOCX), calculates semantic similarity using embedding models, and shortlists top-matching candidates based on match score and keyword relevance.

## 📌 Features
-✅ Upload a job description CSV with multiple roles
-✅ Upload multiple resumes in .txt, .pdf, or .docx formats
-✅ Automatically extracts text and computes match scores
-✅ Uses Ollama LLMs or Hugging Face for embedding and comparison
-✅ Adds keyword-based bonus points
-✅ Shortlists and displays top candidates with names, scores & emails\
-✅ Option to email selected candidates about the next round
-✅ Built with Streamlit for a simple and fast UI


## 🚀 Technologies Used
- Programming Language: Python 
- Frontend :Streamlit= UI for uploading files, selecting roles, and displaying results 
- AI Models: Ollama (LLaMA3, Phi-3), mxbai-embed-large for embeddings 🤖
- Backend: Python=Core logic, text processing, and resume matching  
-Machine Learning / NLP: 1.SentenceTransformers (`all-MiniLM` or `mxbai-embed-large`)=Semantic embeddings for job-resume matching               
|                        2.scikit-learn= Cosine similarity calculation                             
|                        3.OpenAI / Ollama / Hugging Face =LLMs or embedding models for semantic understanding         
- Data Parsing: PyMuPDF for CV reading
- Database: SQLite 🗄️
- UI Tools: Streamlit, HTML/CSS for styling
- Emailing: SMTP for interview invites ✉️

## 📂 Project Structure
```
SmartHireX/
│── app.py                  # Streamlit UI
│── requirements.txt        # Python dependencies
│── README.md               # Project documentation
│
├── utils/                 # Multi-agent architecture components
│   ├── jd_utils.py       # JD Summarizer using LLaMA3
│   ├── resume_parser.py    # Matches resumes with job requirements
│   ├── groq_utils.py         # Filters candidates based on match score
│   ├── email_utils.py # Generates interview emails
│   ├── data_utils.py          # SQLite DB and helper functions
│
├── job_description.csv    # Uploaded job description(s)
├── resumes/                   # Folder containing candidate resumes (PDFs)
```

## 📊 Match Score Logic
-Top 3 resume chunks (by semantic similarity) averaged
-up to 2.2% bonus for matching keywords
– slight penalty if resume has < 3 relevant chunks



## 🔧 Installation & Setup
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/akshayabharathi139/HireFlare.git
   cd HireFlare
   ```

2. **Install Required Libraries:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Start Ollama & Pull LLaMA3 Model:**
   ```
   ollama run llama3
   ```
4. **Run the Streamlit App:**
   ```bash
   streamlit run app.py
   ```

##  How It Works
- Upload a job description CSV and CV folder.
- JD Summarizer (LLaMA3) extracts key requirements.
- Resume Extractor parses PDFs using PyMuPDF (fitz).
- Recruiting Agent scores candidates using embedding similarity.
- Shortlister filters top candidates based on match score.
- Interview Scheduler drafts personalized emails for selected candidates

---
### 📧 Contact
For any queries, reach out to **[akshayabharathi139@gmail.com](mailto:akshayabharathi139@gmail.com\)**.
