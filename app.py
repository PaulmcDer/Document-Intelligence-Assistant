import gradio as gr
import pandas as pd

from document_loader import (
    load_text_file,
    load_pdf_file,
    load_docx_file,
    load_excel_file,
    load_csv_file
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

def load_comparison_file(file):
    
    print(file.name)

    with open(file.name, "rb") as f:
        print(f.read(100))

    if file.name.endswith(".csv"):

        encodings = [
            "utf-8",
            "cp1252",
            "latin1"
        ]

        for enc in encodings:

            try:
                
                with open(file.name, "r", errors="ignore") as f:

                    print("FIRST 5 LINES OF CSV:")

                    for _ in range(5):
                        line = f.readline()

                        if not line:
                            break

                        print(repr(line))

                return pd.read_csv(
                    file.name,
                    encoding=enc,
                    sep=None,
                    engine="python"
                )

            except Exception:
                pass

        raise ValueError(
            "Unable to read CSV file."
        )

    elif file.name.endswith(".xlsx"):

        return pd.read_excel(
            file.name,
            engine="openpyxl"
        )

    else:

        raise ValueError(
            "Only CSV and XLSX files are supported."
        )

        
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
    description="Upload TXT, PDF, DOCX, XLSX or CSV files and search for content"
)

def compare_excel_files(file1, file2):

    df1 = load_comparison_file(file1)
    df2 = load_comparison_file(file2)
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
    description="Upload CSV or XLSX files and compare them."
)

demo = gr.TabbedInterface(
    [search_tab, compare_tab],
    ["Search Documents", "Compare Files"]
)

demo.launch(inbrowser=True)
