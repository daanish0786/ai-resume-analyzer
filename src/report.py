def build_report(match_score: float, gaps: list[str], issues: list[tuple[str,str]]) -> str:
    lines = []
    lines.append("AI Resume Analyzer Report")
    lines.append("=" * 28)
    lines.append("")
    lines.append(f"Match Score: {round(match_score*100, 1)} / 100")
    lines.append("")
    lines.append("Missing / Underused Keywords:")
    if gaps:
        lines.append("  " + ", ".join(gaps))
    else:
        lines.append("  None detected.")
    lines.append("")
    lines.append("ATS & Hygiene Checks:")
    if issues:
        for k, v in issues:
            lines.append(f"  - {k}: {v}")
    else:
        lines.append("  No obvious issues detected.")
    lines.append("")
    lines.append("Notes: This score is a heuristic using sentence-transformer embeddings and cosine similarity. Tailor truthfully.")
    return "\n".join(lines)
