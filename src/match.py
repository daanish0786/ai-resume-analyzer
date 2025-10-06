
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

def similarity(a_vec, b_vec) -> float:
    return float(cosine_similarity([a_vec], [b_vec])[0][0])

def tokenize_simple(text: str):
    # lower, strip punctuation-like chars
    text = re.sub(r"[^a-zA-Z0-9+#./-]+", " ", text.lower())
    return [t for t in text.split() if t]

def keyword_gap(jd_text: str, resume_text: str, top_k: int = 25):
    jd_tokens = set(tokenize_simple(jd_text))
    rs_tokens = set(tokenize_simple(resume_text))

    # very common stop-words to ignore (lightweight)
    stop = {
        "and","the","for","with","you","are","will","our","your","from","that","have","this","into",
        "work","team","skills","experience","years","per","week","job","role","requirements","responsibilities",
        "preferred","preferred:","must","about","company","ability","strong","excellent","good"
    }
    tech_like = [w for w in jd_tokens if (w not in rs_tokens and len(w) > 2 and w not in stop)]
    # prioritize tokens that look like tech/skills
    tech_like.sort(key=lambda w: (not any(c.isdigit() for c in w) and w.isalpha(), -len(w)))
    return tech_like[:top_k]
