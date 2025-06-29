import subprocess
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Print or use the key
if api_key:
    print("✅ API key loaded:", api_key[:5] + "..." + api_key[-4:])  # Print masked key
else:
    print("❌ API key not found. Please check your .env file.")
    exit()


def extract_company_block(tex, company_name):
    pattern = re.compile(
        rf'(\\resumeSubheading\s*{{{re.escape(company_name)}}}.*?)\\resumeItemListEnd',
        re.DOTALL
    )
    return pattern.search(tex)

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

def replace_block(tex, old_block, new_block):
    return tex.replace(old_block, new_block)




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



# Converts the Python list into LaTeX resumeItem block
def format_resume_items(items):
    return '\n'.join(
        f'        \\resumeItem{{{title}}}\n'
        f'          {{{desc}}}' for title, desc in items
    )

# Locate the Hoppscotch block and update only its \resumeItem list
def update_hoppscotch_block(content, new_items_hop):
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
    new_items_str = format_resume_items(new_items_hop)
    updated_block = f"{before_items}\\resumeItemListStart\n{new_items_str}\n      \\resumeItemListEnd"

    return content[:match.start()] + updated_block + content[match.end():]

# Locate the Hoppscotch block and update only its \resumeItem list
def update_jpm_block(content, new_items_hop):
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
    new_items_str = format_resume_items(new_items_hop)
    updated_block = f"{before_items}\\resumeItemListStart\n{new_items_str}\n      \\resumeItemListEnd"

    return content[:match.start()] + updated_block + content[match.end():]






from openai import OpenAI
import ast
job_description = None
with open('job_description.txt', 'r', encoding='utf-8') as f:
    job_description = f.read()



client = OpenAI(
    api_key=api_key
)

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

final = (job_description + "\n" + "Given the above description for a job give me bullet points for actions with impact words and "
 "percent of impact that matches the job description as closely as possible and give me the output in this format"
 "feel free to add or remove the number of list items also change the techstack keywords to exactly match the job description that"
         "the job is looking for "
 "keywords for skills required for the jobs give me the final out in the form of this input only i.e a list "
 "with tuples and that's a hard requirement for output nothing else will be accepted" + str(new_items))

final_input_for_ai =final


completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
        {"role": "user", "content": final_input_for_ai}
    ]
)


response = completion.choices[0].message
response = str(response.content)
## Extract usefull stuff from the response

import re

# Extract code block using regex
match = re.search(r'```python\n(.*?)```', response, re.DOTALL)
if match:
    code_block = match.group(1)

else:
    print(f"❌ No Python code block found. for jpm")
    code_block = response

# Optional: decode escaped characters like \\% and \\$
cleaned_code_block = code_block.encode().decode('unicode_escape')

print("✅ Extracted Python Code: for JP\n")
print(cleaned_code_block)


## more cleaning

# Extract the content after the '=' sign
match = re.search(r'=\s*(\[.*\])', cleaned_code_block, re.DOTALL)
if match:
    rhs = match.group(1).strip()
    print(f'"{rhs}"')  # Output with double quotes
else:
    rhs = cleaned_code_block
    print(" No list found after equals sign. dEFAULTING TO PREVIOUS FOR HOPP")


list_obj = ast.literal_eval(rhs)
print(list_obj)
print(type(list_obj))

######## updating the resume


# ----------- USAGE -----------
file_path = 'resume_template.tex'
output_path = 'resume_updated.tex'
company_name = 'J.P Morgan Chase and Co.'

# Step 1: Read LaTeX content
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# # Step 2: Extract company block
# match = extract_company_block(content, company_name)
# if not match:
#     print(f"❌ Couldn't find the block for: {company_name}")
#     exit()
#
# old_block = match.group(0)

# Step 3: Define new \resumeItem entries
new_items = list_obj
# new_items = [
#     ("Led the cloud migration of on-prem",
#      "infrastructure to AWS, enabling scalable processing of 3.6M+ records/day across 54 data pipelines; boosted data ingestion efficiency by 40\\% using Databricks workflows."),
#
#     ("Optimized compute resource usage",
#      "across multiple production workloads, cutting DBU consumption by 35\\% and delivering \\$100K+ annual cost savings."),
#
#     # Removed "Handling Large Scale Data"
#
#     ("Introduced Auto Scaling",
#      "Implemented Kubernetes HPA, reducing manual intervention and improving fault tolerance."),
#
#     ("TechStack",
#      "Java, SpringBoot, SpringWeb, Microservices, AWS, Kubernetes")
# ]

# Step 4: Replace items and write output
updated_content = update_jpm_block(content, new_items)
# updated_content = replace_block(content, old_block, new_block)

### Pass updated content into hopps block

# with open(output_path, 'w', encoding='utf-8') as f:
#     f.write(updated_content)

print(f"\n✅ Updated  block in: JPM Chase")










    ############ Updating the resume















"""
Hoppscotch Section
"""

hopps_list = [
    ("Built scalable mock API systems",
     "Delivered REST API simulation services that processed 100K+ requests/month using containerized Docker/Kubernetes setups, improving developer experience and debugging efficiency by 40\\%."),

    ("Enhanced platform observability",
     "Instrumented logs and error-handling layers in mock server architecture, reducing operational load by 20\\% and streamlining performance tuning for production replicas."),

    ("Implemented robust testing",
     "Isolated routes and built testable endpoints for 200K+ users, leveraging CI/CD pipelines and API versioning for iterative releases."),

    ("TechStack",
     "Node.js, GraphQL, NuxtJS, PostgreSQL, Docker, Kubernetes, React")
]

final = (job_description + "\n" + "Given the above description for a job give me bullet points for actions with impact words and "
                                  "percent of impact that matches the job description as closely as possible and give me the output in this format"
                                  "feel free to add or remove the number of list items also change the techstack keywords to exactly match the job description that"
                                  "the job is looking for "
                                  "keywords for skills required for the jobs give me the final out in the form of this input only i.e a list "
                                  "with tuples and that's a hard requirement for the output. nothing else will be accepted" + str(hopps_list))

final_input_for_ai =final


completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
        {"role": "user", "content": final_input_for_ai}
    ]
)


response = completion.choices[0].message
response = str(response.content)
## Extract usefull stuff from the response



# Extract code block using regex
match = re.search(r'```python\n(.*?)```', response, re.DOTALL)
if match:
    code_block = match.group(1)

else:
    print("❌ No Python code block found for Hopps")
    code_block = response

# Optional: decode escaped characters like \\% and \\$
cleaned_code_block = code_block.encode().decode('unicode_escape')

# Extract the content after the '=' sign
match = re.search(r'=\s*(\[.*\])', cleaned_code_block, re.DOTALL)
if match:
    rhs = match.group(1).strip()
    print(f'"{rhs}"')  # Output with double quotes
else:
    rhs = cleaned_code_block
    print(" No list found after equals sign. dEFAULTING TO PREVIOUS FOR HOPP")


print("✅ Extracted Python Code for Hopp :\n")
print(rhs)
list_obj = ast.literal_eval(rhs)
print(list_obj)
print(type(list_obj))



######## updating the resume


# ----------- USAGE -----------
# file_path = 'resume_template.tex'
# output_path = 'resume_updated.tex'
# company_name = 'Hoppscotch India Pvt. Ltd.'

# Step 1: Read LaTeX content
# with open(file_path, 'r', encoding='utf-8') as f:
#     content = f.read()

# Step 2: Extract company block
# print("updated_content")
# print(updated_content)

match = extract_company_block(updated_content, company_name)
if not match:
    print(f"❌ Couldn't find the block for: {company_name}")
    exit()

old_block = match.group(0)

# Step 3: Define new \resumeItem entries
new_items = list_obj


    # Read, update, and write
# with open(input_tex_file, 'r', encoding='utf-8') as f:
#     tex_content = f.read()

updated_tex = update_hoppscotch_block(updated_content, new_items)



######### Update projects description based on the input job desc



with open(output_path, 'w', encoding='utf-8') as f:
    f.write(updated_tex)

print("✅ Hoppscotch block updated and written to resume_updated.tex")



compile_latex("resume_updated.tex")










    ############ Updating the resume





