import re

def extract_company_block(tex, company_name):
    pattern = re.compile(
        rf'(\\resumeSubheading\s*{{{re.escape(company_name)}}}.*?)\\resumeItemListEnd',
        re.DOTALL
    )
    return pattern.search(tex)

def update_resume_items(block, new_items):
    item_block = '\n'.join(
        f'        \\resumeItem{{{title}}}{{{desc}}}' for title, desc in new_items
    )
    updated = re.sub(
        r'\\resumeItemListStart.*?\\resumeItemListEnd',
        f'\\resumeItemListStart\n{item_block}\n\t\t\\resumeItemListEnd',
        block,
        flags=re.DOTALL
    )
    return updated

def replace_block(tex, old_block, new_block):
    return tex.replace(old_block, new_block)

# ----------- USAGE -----------
file_path = 'resume_template.tex'
output_path = 'resume_updated.tex'
company_name = 'J.P Morgan Chase and Co.'

# Step 1: Read LaTeX content
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Step 2: Extract company block
match = extract_company_block(content, company_name)
if not match:
    print(f"❌ Couldn't find the block for: {company_name}")
    exit()

old_block = match.group(0)

# Step 3: Define new \resumeItem entries
new_items = [
    ("Led the cloud migration of on-prem",
     "infrastructure to AWS, enabling scalable processing of 3.6M+ records/day across 54 data pipelines; boosted data ingestion efficiency by 40\\% using Databricks workflows."),

    ("Optimized compute resource usage",
     "across multiple production workloads, cutting DBU consumption by 35\\% and delivering \\$100K+ annual cost savings."),

    # Removed "Handling Large Scale Data"

    ("Introduced Auto Scaling",
     "Implemented Kubernetes HPA, reducing manual intervention and improving fault tolerance."),

    ("TechStack",
     "Java, SpringBoot, SpringWeb, Microservices, AWS, Kubernetes")
]

# Step 4: Replace items and write output
new_block = update_resume_items(old_block, new_items)
updated_content = replace_block(content, old_block, new_block)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(updated_content)

print(f"\n✅ Updated {company_name} block in: {output_path}")
