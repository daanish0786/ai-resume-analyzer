
import re

def basic_ats_checks(resume_text: str, filename: str = "resume.pdf"):
    checks = []

    # filename hygiene (spaces can be messy)
    if re.search(r"\s", filename):
        checks.append(("Filename", "Use hyphens/underscores instead of spaces in the filename (e.g., Daanish-Shaikh-Resume.pdf)."))

    # contact info (very naive checks)
    if not re.search(r"\b[\w\.-]+@[\w\.-]+\.[A-Za-z]{2,}\b", resume_text):
        checks.append(("Contact Info", "Add a professional email address."))
    if not re.search(r"linkedin\.com/in/", resume_text, re.I):
        checks.append(("LinkedIn", "Include your LinkedIn profile URL in the header."))

    # length heuristic (rough approximation)
    words = len(resume_text.split())
    if words > 900:
        checks.append(("Length", "Try to keep it to one page for internships (brief bullets with impact & metrics)."))

    # required sections
    must_sections = ["education", "skills", "projects", "experience"]
    for sec in must_sections:
        if re.search(rf"\b{sec}\b", resume_text, re.I) is None:
            checks.append(("Sections", f"Consider adding a '{sec.title()}' section."))

    return checks
