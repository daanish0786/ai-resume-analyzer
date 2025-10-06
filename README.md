
# AI Resume Analyzer (Streamlit)

Analyze how well a resume matches a job description using sentence-transformer embeddings, cosine similarity, and simple ATS checks. Built to be easy to run and deploy.

## Features
- PDF resume parsing (via `pdfplumber`)
- Embeddings with `sentence-transformers` (`all-MiniLM-L6-v2`)
- Match score (cosine similarity)
- Missing/underused keyword suggestions
- Basic ATS & hygiene checks (filename, sections, length, links)
- Optional: LLM suggestions for bullet rewrites (OpenAI)

---

## 1) Setup

### Prereqs
- Python 3.9+ installed
- (Optional) Git & GitHub account (for deployment)

### Create and activate a virtual env (macOS/Linux)
```bash
python3 -m venv .venv
source .venv/bin/activate
```

(Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Install dependencies
```bash
pip install -r requirements.txt
```

If you plan to use the optional OpenAI rewrite suggestions, create a `.env` file:
```
OPENAI_API_KEY=sk-...
```

---

## 2) Run
```bash
streamlit run app.py
```
Open the local URL Streamlit shows (usually http://localhost:8501).

- Paste a job description into the text box.
- Upload your resume PDF.
- Click **Analyze**.

---

## 3) Project structure
```
ai-resume-analyzer/
├─ app.py
├─ requirements.txt
├─ .gitignore
├─ .env.example
├─ README.md
├─ src/
│  ├─ extract.py
│  ├─ embed.py
│  ├─ match.py
│  ├─ ats.py
│  └─ rewrite.py
└─ sample_data/
   ├─ jd_swe_intern.txt
   └─ (add your own resume.pdf when testing)
```

---

## 4) Notes
- The first run will download the sentence-transformers model; this can take a minute.
- The similarity score is a helpful heuristic but not a perfect "ATS pass" guarantee.
- Keywords shown are a simple diff; always tailor responsibly and truthfully.

---

## 5) Optional: Deployment (Streamlit Community Cloud)
1. Push this folder to a **public GitHub repository**.
2. Go to https://share.streamlit.io/ (or Streamlit Cloud), connect your GitHub, choose the repo.
3. Set **Main file path** to `app.py`.
4. (Optional) Add a secret `OPENAI_API_KEY` for rewrite suggestions under **Advanced settings → Secrets**.
5. Deploy. Share the URL on your resume/LinkedIn.

---

## 6) Add to your resume
- Built a Streamlit NLP app that analyzes resume–JD fit using sentence-transformer embeddings and cosine similarity to produce a match score and keyword gap analysis.
- Implemented ATS checks (sections, contact/LinkedIn detection, filename hygiene, length) and report; avg inference time < 1.5s on CPU.
- Deployed on Streamlit Cloud with public demo and README documentation.

---

## 7) License
MIT
