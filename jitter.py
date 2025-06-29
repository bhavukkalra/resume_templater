import re
import subprocess
from collections import Counter
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import string
import os

def extract_keywords(text, top_n=30):
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    words = [word for word in text.split() if word not in ENGLISH_STOP_WORDS]
    common = Counter(words).most_common(top_n)
    return [word for word, _ in common]

def insert_keywords_into_resume(tex_path, output_tex_path, keywords):
    with open(tex_path, 'r', encoding='utf-8') as f:
        content = f.read()

    keyword_items = '\n'.join([f'\\item {kw}' for kw in keywords])
    print("Extracted keywords")
    print("keyword_items")


    # Replace placeholder with keywords
    updated_content = content.replace('%KEYWORDS_PLACEHOLDER', keyword_items)

    with open(output_tex_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"Updated LaTeX written to {output_tex_path}")

def compile_latex(tex_file_path, output_dir="."):
    print("Compiling LaTeX to PDF...")
    try:
        subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-output-directory', output_dir, tex_file_path],
            check=True
        )
        print("PDF generated successfully!")
    except subprocess.CalledProcessError as e:
        print("LaTeX compilation failed:", e)

# --------- CONFIG ---------
job_description = """
We are looking for a backend software engineer experienced in Java, Spring Boot, and AWS services. 
Candidates should have a deep understanding of REST APIs, distributed systems, and CI/CD pipelines. 
Knowledge of Kubernetes, Docker, and Terraform is a plus. Experience with financial platforms and 
data modeling is highly desirable.
"""

# Ensure you have this file with %KEYWORDS_PLACEHOLDER in your Skills section
base_tex_file = "resume_template.tex"
modified_tex_file = "resume_fusion.tex"
output_pdf_file = "resume_fusion.pdf"

# --------- RUN SCRIPT ---------
keywords = extract_keywords(job_description)
insert_keywords_into_resume(base_tex_file, modified_tex_file, keywords)
compile_latex(modified_tex_file)
