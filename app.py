
import streamlit as st
from src.extract import read_pdf, clean_text
from src.embed import embed_single
from src.match import similarity, keyword_gap
from src.ats import basic_ats_checks
from src.rewrite import suggest_bullets
from src.report import build_report

def render_results(score, gaps, issues, jd_text):
    # ---- Match Score ----
    with card("🎯 Match Score"):
        st.subheader(f"{round(score*100, 1)} / 100")
        st.progress(min(max(score, 0), 1.0))
    end_card()

    # ---- Missing / Underused Keywords ----
    with card("🔑 Missing / Underused Keywords"):
        if gaps:
            st.write(", ".join(gaps))
        else:
            st.write("Looks good! No major gaps detected.")
    end_card()

    # ---- ATS & Hygiene Checks ----
    with card("✅ ATS & Hygiene Checks"):
       if issues:
        # Handle both dict and list formats safely
        if isinstance(issues, dict):
            for k, v in issues.items():
                st.write(f"- **{k}**: {v}")
        elif isinstance(issues, list):
            for item in issues:
                if isinstance(item, (list, tuple)) and len(item) == 2:
                    st.write(f"- **{item[0]}**: {item[1]}")
                else:
                    st.write(f"- {item}")
        else:
            st.write(str(issues))
       else:
        st.write("No obvious ATS issues detected.")
    end_card()


    # ---- Suggestions (Template) ----
    with card("✏️ Suggestions (Template)"):
        st.caption("These are template prompts to help you rewrite bullets without exaggerating.")
        tips = suggest_bullets("Software Engineer Intern", jd_text, [], gaps)
        for t in tips:
            st.write(f"- {t}")
    end_card()

    # ---- Success Message ----
    st.success("✅ Analysis complete! Scroll below to download your personalized report.")
    st.balloons()

    # ---- Download Report ----
    with card("⬇️ Download Report"):
        report_text = build_report(score, gaps, issues)
        st.download_button(
            label="💾 Download Report (.txt)",
            data=report_text.encode("utf-8"),
            file_name="ai_resume_analyzer_report.txt",
            mime="text/plain"
        )
    end_card()

    

    with st.sidebar:
        st.markdown("### About this app")
        st.write("Embeddings: `all-MiniLM-L6-v2` • Cosine similarity for match score • Simple ATS checks")
        st.caption("Built by Daanish Shaikh as a portfolio project.")



st.set_page_config(page_title="AI Resume Analyzer", page_icon="🧠")
# ---- Global Styles + Branded Header ----
st.markdown(
    """
    <style>
      /* Page background gradient */
      .stApp {
        background: radial-gradient(1200px 600px at 10% 10%, #111827 0%, #0E1117 40%, #0B0F14 100%) !important;
      }

      /* Card styling */
      .stCard {
        background: var(--secondary-background-color, #161B22);
        border-radius: 16px;
        padding: 20px 22px;
        box-shadow: 0 6px 14px rgba(0,0,0,0.35);
        border: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 18px;
      }

      /* Headings */
      h1, h2, h3 { letter-spacing: .2px; }
      .subtle { opacity: .8; }

      /* Buttons */
      .stButton>button {
        border-radius: 12px;
        padding: 0.6rem 1.1rem;
        font-weight: 600;
      }

      /* Sidebar */
      section[data-testid="stSidebar"] {
        background: #0B1220 !important;
        border-right: 1px solid rgba(255,255,255,0.06);
      }
    </style>

    <div style="text-align:center; margin: 8px 0 18px 0;">
      <div style="font-size:36px; font-weight:800;">
        🚀 <span style="color:#00A8E8">AI Resume Analyzer</span>
      </div>
      <div class="subtle" style="margin-top:6px;">
        by <b>Daanish Shaikh</b> • Embeddings · ATS Checks · Keyword Insights
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
# Custom CSS styling
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---- Card helper functions ----
def card(title: str):
    """Start a styled card with a section title"""
    st.markdown(f"<div class='stCard'><h3>{title}</h3>", unsafe_allow_html=True)
    return st.container()   # lets you put Streamlit elements inside

def end_card():
    """Close the styled card"""
    st.markdown("</div>", unsafe_allow_html=True)



st.write("Paste a job description and upload your resume PDF to get a match score, missing keywords, and ATS checks.")

jd = st.text_area("📄 Paste Job Description", height=220, placeholder="Paste JD here...")
up = st.file_uploader("📎 Upload your resume (PDF only)", type=["pdf"])

col1, col2 = st.columns(2)
with col1:
    run_btn = st.button("Analyze", type="primary")
with col2:
    st.caption("Tip: Use a 1-page resume for internships and early roles.")

if run_btn:
    if not jd:
        st.error("Please paste a job description.")
    elif not up:
        st.error("Please upload a PDF resume.")
    else:
        with st.spinner("Reading resume..."):
            resume_text = clean_text(read_pdf(up))
            jd_text = clean_text(jd)

        with st.spinner("Scoring… (downloading model on first run)"):
            r_vec = embed_single(resume_text)
            j_vec = embed_single(jd_text)
            score = similarity(r_vec, j_vec)
            gaps  = keyword_gap(jd_text, resume_text)
            issues = basic_ats_checks(resume_text, filename=up.name)

        # Save results for safe re-renders
        st.session_state["results"] = {
            "score": score, "gaps": gaps, "issues": issues, "jd_text": jd_text
        }

# Render if we have results (prevents NameError on reruns)
if "results" in st.session_state:
    r = st.session_state["results"]
    render_results(r["score"], r["gaps"], r["issues"], r["jd_text"])

