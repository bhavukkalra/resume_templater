import re

# New items to inject
new_items = [
    ("Built scalable mock API systems",
     "Delivered REST API simulation services that processed 100K+ requests/month using containerized Docker/Kubernetes setups, improving developer experience and debugging efficiency by 40\\%."),

    ("Enhanced platform observability",
     "Instrumented logs and error-handling layers in mock server architecture, reducing operational load by 20\\% and streamlining performance tuning for production replicas."),

    ("Implemented robust testing",
     "Isolated routes and built testable endpoints for 200K+ users, leveraging CI/CD pipelines and API versioning for iterative releases."),

    ("TechStack",
     "node")
]

# Converts the Python list into LaTeX resumeItem block
def format_resume_items(items):
    return '\n'.join(
        f'        \\resumeItem{{{title}}}\n'
        f'          {{{desc}}}' for title, desc in items
    )

# Locate the Hoppscotch block and update only its \resumeItem list
def update_hoppscotch_block(content):
    # Match the block starting with the specific company
    pattern = re.compile(
        r'(\\resumeSubheading\s*\{\{\\faExternalLink\s+Hoppscotch India Pvt\. Ltd\..*?)\\resumeItemListStart(.*?)\\resumeItemListEnd',
        re.DOTALL
    )

    match = pattern.search(content)
    if not match:
        print("❌ Could not find the Hoppscotch block.")
        return content

    before_items = match.group(1)
    new_items_str = format_resume_items(new_items)
    updated_block = f"{before_items}\\resumeItemListStart\n{new_items_str}\n      \\resumeItemListEnd"

    return content[:match.start()] + updated_block + content[match.end():]

# File paths
input_tex_file = "resume_template.tex"
output_tex_file = "resume_updated.tex"

# Read, update, and write
with open(input_tex_file, 'r', encoding='utf-8') as f:
    tex_content = f.read()

updated_tex = update_hoppscotch_block(tex_content)

with open(output_tex_file, 'w', encoding='utf-8') as f:
    f.write(updated_tex)

print("✅ Hoppscotch block updated and written to resume_updated.tex")
