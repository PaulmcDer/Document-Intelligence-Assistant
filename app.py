import gradio as gr
import pandas as pd

from document_loader import (
    load_text_file,
    load_pdf_file,
    load_docx_file,
    load_excel_file
)


def analyze_document(file, search_term):

    if file.name.endswith(".txt"):
        content = load_text_file(file)

    elif file.name.endswith(".pdf"):
        content = load_pdf_file(file)

    elif file.name.endswith(".docx"):
        content = load_docx_file(file)
        
    elif file.name.endswith(".xlsx"):
        content = load_excel_file(file)
        
    elif file.name.endswith(".csv"):
        content = load_csv_file(file)

    else:
        return "Unsupported file type."

    words = len(content.split())

    if not search_term:

        return f"""
Words: {words}

Preview:

{content[:1000]}
"""

    lines = content.splitlines()

    matches = []

    for i, line in enumerate(lines):

    	if search_term.lower() in line.lower():

        	start = max(0, i - 2)
        	end = min(len(lines), i + 3)

        	context = "\n".join(lines[start:end])

       		matches.append(context)

    count = len(matches)

    preview_matches = "\n\n-------------------\n\n".join(matches[:5])

    return f"""
Search Term: {search_term}

Occurrences Found: {count}

First Matches:

{preview_matches}
"""
def compare_excel_files(file1, file2):

    df1 = pd.read_excel(file1.name)
    df2 = pd.read_excel(file2.name)
    if list(df1.columns) != list(df2.columns):
        return "Files have different column structures."

    differences = df1.compare(df2)

    if differences.empty:
        return "No differences found."

    return differences.to_string()



search_tab = gr.Interface(
    fn=analyze_document,
    inputs=[
        gr.File(label="Upload File"),
        gr.Textbox(label="Search Term")
    ],
    outputs=gr.Textbox(
        label="Analysis",
        lines=20
    ),
    title="Document Intelligence Assistant",
    description="Upload TXT, PDF or DOCX files and search for content."
)

def compare_excel_files(file1, file2):

    df1 = pd.read_excel(file1.name)
    df2 = pd.read_excel(file2.name)
    if list(df1.columns) != list(df2.columns):
        return "Files have different column structures."

    differences = []

    rows_to_check = min(len(df1), len(df2))

    for row in range(rows_to_check):

        for column in df1.columns:

            value1 = str(df1.loc[row, column])
            value2 = str(df2.loc[row, column])

            if value1 != value2:

                differences.append(
                    f"""
Row {row + 1}

Column: {column}

File A: {value1}
File B: {value2}

--------------------
"""
                )

    if not differences:
        return "No differences found."

    return (
        f"Differences Found: {len(differences)}\n\n"
        + "\n".join(differences)
    )

compare_tab = gr.Interface(
    fn=compare_excel_files,
    inputs=[
        gr.File(label="File A"),
        gr.File(label="File B")
    ],
    outputs=gr.Textbox(
        label="Differences",
        lines=20
    ),
    title="Compare Files",
    description="Upload two Excel files and compare them."
)

demo = gr.TabbedInterface(
    [search_tab, compare_tab],
    ["Search Documents", "Compare Files"]
)

demo.launch(inbrowser=True)
