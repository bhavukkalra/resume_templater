import re
import subprocess
# New items to replace under "J.P Morgan Chase and Co."
new_items = [
    ("Redesigned cloud architecture",
     "Migrated critical systems from on-prem to AWS, handling 3.6M+ records/day using Databricks and cutting operational costs by \$100K annually."),

    ("Streamlined production efficiency",
     "Tuned Kubernetes and Spark clusters, reducing resource overhead by 35\\% and enhancing pipeline throughput."),

    ("Built REST APIs at scale",
     "Engineered fault-tolerant services using Spring Boot, SQS, and DynamoDB, improving SLA adherence by 40\\%."),

    ("Led mentorship efforts",
     "Guided junior engineers via code reviews and pairing sessions, strengthening code quality and team velocity."),

    ("TechStack",
     "Java, SpringBoot, AWS (DynamoDB, SQS, SNS), Terraform, Kubernetes, Databricks, SQL, Docker")
]

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

# Format into LaTeX-style strings
def format_resume_items(items):
    return '\n'.join(
        f'        \\resumeItem{{{title}}}\n          {{{desc}}}' for title, desc in items
    )

# Update only the "J.P Morgan Chase and Co." block
def update_jpm_block(latex_text, new_items):
    # Pattern to match the specific company heading and its item block
    pattern = re.compile(
        r'(\\resumeSubheading\s*\{\s*J\.P\s+Morgan\s+Chase\s+and\s+Co\.\}\{.*?\}.*?\n\s*\\resumeItemListStart)(.*?)(\\resumeItemListEnd)',
        re.DOTALL
    )

    new_item_block = format_resume_items(new_items)

    def replacer(match):
        return f"{match.group(1)}\n{new_item_block}\n\t\t{match.group(3)}"

    updated = pattern.sub(replacer, latex_text)
    return updated

# --- Example usage with file ---

input_file = "resume_template.tex"
output_file = "resume_updated.tex"

with open(input_file, "r", encoding="utf-8") as f:
    latex_content = f.read()

updated_content = update_jpm_block(latex_content, new_items)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(updated_content)

compile_latex("resume_updated.tex")

print("✅ Updated J.P Morgan Chase and Co. block in resume_updated.tex")
