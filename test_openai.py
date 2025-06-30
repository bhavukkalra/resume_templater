import subprocess
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


NON_NEGOTIABLES = ("NON Negotialble - 1. Never include the company name from the job description in the final output"
                   "2. Always maintain the number of input points from the input i.e it shouldn't be never less than the number of points inputed "
                   "either always the same or more")

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
    print("Inside the update jpm block" + "will be replaced by")
    print(new_items)

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
    print("Updating hopp block with ")
    print(new_items_hop)
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
# def update_hopblock(content, new_items_hop):
#     # Match the block starting with the specific company
#     pattern = re.compile(
#         r'(\\resumeSubheading\s*\{\{\\faExternalLink\s+Hoppscotch India Pvt\. Ltd\..*?)\\resumeItemListStart(.*?)\\resumeItemListEnd',
#         re.DOTALL
#     )
#
#     match = pattern.search(content)
#     if not match:
#         print("❌ Could not find the Hoppscotch block.")
#         return content
#
#     before_items = match.group(1)
#     new_items_str = format_resume_items(new_items_hop)
#     updated_block = f"{before_items}\\resumeItemListStart\n{new_items_str}\n      \\resumeItemListEnd"
#
#     return content[:match.start()] + updated_block + content[match.end():]

def replace_items_in_project_pms(tex_content, project_title, new_items):
    # Find the start of the resumeSubItem for the given project
    start_tag = f"\\resumeSubItem{{{{\\faExternalLink {project_title}}}"
    start_index = tex_content.find(start_tag)
    if start_index == -1:
        raise ValueError(f"❌ Project title '{project_title}' not found.")

    # Locate enumerate block inside that project
    enum_start = tex_content.find(r"\begin{enumerate}", start_index)
    enum_end = tex_content.find(r"\end{enumerate}", enum_start)
    if enum_start == -1 or enum_end == -1:
        raise ValueError("❌ 'enumerate' block not found in the specified project.")

    # Keep everything before, replace enumerate content, keep everything after
    before = tex_content[:enum_start]
    after = tex_content[enum_end + len(r"\end{enumerate}"):]  # Include end tag

    # Format the new \item lines
    new_item_block = "\n" + "\n".join([f"    \\item {item}" for item in new_items]) + "\n"

    # Final content
    return before + r"\begin{enumerate}" + new_item_block + r"\end{enumerate}" + after


def clean_and_parse_literal(input_string):
    # Step 1: Strip Markdown-style code fences if present
    input_string = input_string.strip()
    if input_string.startswith("```"):
        parts = input_string.split("```")
        if len(parts) >= 2:
            input_string = parts[1].strip()

    # Step 2: Escape LaTeX-style backslashes that cause issues in literal_eval
    # Only escape if not part of known sequences like \n, \t, \\, etc.
    input_string = re.sub(r'\\(?![\\\'"abfnrtuvxU0-9])', r'\\\\', input_string)

    # Step 3: Safely parse with ast.literal_eval
    try:
        parsed = ast.literal_eval(input_string)
        return parsed
    except Exception as e:
        raise ValueError(f"❌ Failed to parse input as Python literal:\n{e}")


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
 "with tuples and that's a hard requirement for output nothing else will be accepted" + str(new_items) + "\n" + NON_NEGOTIABLES)

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
                                  "with tuples and that's a hard requirement for the output. nothing else will be accepted" + "Here is the original list for reference"  +  "\n"+ str(hopps_list) +
         "it is the most non negotiable to Keep the  of the original list as the same on what was made, Only and just only  add the keywords for the job skills required for the job mentioned in the original list"
         "like include the tech stack required for the role mentioned in the job description" + "Like Built scalable mock API systems and built for 200k + users must and I repeat must be there in the final output"
         + "\n" + NON_NEGOTIABLES)

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

## Pre process the input to add escape characters
import re
rhs = re.sub(r'\\(?![ntr\'"\\])', r'\\\\', rhs)



# STEP 1: Strip Markdown code fences if present
if rhs.strip().startswith("```"):
    rhs = rhs.strip().split("```")[1]  # Take only the content inside the fence

# STEP 2: Use ast.literal_eval to parse safely
try:
    parsed = ast.literal_eval(rhs)
    print("✅ Parsed object:")
    for item in parsed:
        print("-", item)
except Exception as e:
    print("❌ Error parsing input: for Hopp", e)
    exit()


list_obj = parsed
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
print("✅  Updated hopp block")



######### Update projects description based on the input job desc
existing_pms_items = [
    "Enterprise-grade backend: Designed RESTful services in Node.js with JWT and 2FA integration using AWS SES, following security-first design and Terraform-based provisioning.",
    "End-to-end testing and CI/CD: Implemented TDD using Jest and Cypress, with automated deployment via Docker and GitHub Actions for consistent feature delivery.",
    "Role-based access control: Managed CRUD operations on MongoDB with schema validation and session handling, supporting multi-user roles and audit-ready logs."
]

final = (job_description + "\n" + "Given the above description for a job give me bullet points for actions with impact words and "
                                  "percent of impact that matches the job description as closely as possible and give me the output in this format"
                                  "feel free to add or remove the number of list items also change the techstack keywords to exactly match the job description that"
                                  "the job is looking for "
                                  "keywords for skills required for the jobs give me the final out in the form of this input only i.e a list "
                                  "with tuples and that's a hard requirement for the output. nothing else will be accepted" + "Here is the original list" + str(existing_pms_items)
         + "This is the most non negotiable thing that in the final output Maintain the type of project described through the original list, try to add the skill set mentioned in the description of the job description into the original wording of the project "
         "so that it shows the recruiter that I am well versed with the topics asked in the job description. Also keep in mind NOT and I repeat NOT include any impact numbers like "
           "impact: 20 in the final output that was only for demonstration purposes to you. and non negotiable output format is list of strings")

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


# Extract code block using regex
match = re.search(r'```python\n(.*?)```', response, re.DOTALL)
if match:
    code_block = match.group(1)

else:
    print("❌ No Python code block found for project pms")
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
    print(" No list found after equals sign. dEFAULTING TO PREVIOUS FOR project pms")


print("✅ Extracted Python Code for pms :\n")
print(rhs)
rhs = re.sub(r'\\(?![ntr\'"\\])', r'\\\\', rhs)

list_obj = ast.literal_eval(rhs)
print(list_obj)
print(type(list_obj))

new_items = list_obj

project_title = "Password Management System"
# Replace the items
try:
    updated_tex = replace_items_in_project_pms(updated_tex, project_title, new_items)

    # print(f"✅ Successfully updated items for '{project_title}' and saved to '{output_file}'")

except ValueError as e:
    print(str(e))

### Done updating projects

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(updated_tex)

print("✅ Project updated for pms and written to tex")



compile_latex("resume_updated.tex")










    ############ Updating the resume





