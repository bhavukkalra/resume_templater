def replace_items_in_project(tex_content, project_title, new_items):
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


# --- Usage Example ---

project_title = "Password Management System"

new_items = [
    "Implemented OAuth 2.0 with Google Sign-In to improve login UX and secure third-party access.",
    "Refactored backend for modularity using Express.js middleware and async services.",
    "Added analytics dashboard using Chart.js and MasdasdasdadongoDB aggregation pipelines."
]

input_file = "resume_template.tex"
output_file = "resume_updated.tex"

# Read file
with open(input_file, "r", encoding="utf-8") as f:
    tex_content = f.read()


