import gradio as gr

def analyze_text(file, question):

    with open(file.name, "r", encoding="utf-8") as f:
        content = f.read()

    words = len(content.split())

    return f"""
Question:
{question}

Words:
{words}

Document Preview:

{content[:500]}
"""


demo = gr.Interface(
    fn=analyze_text,
    inputs=[
        gr.File(label="Upload TXT File"),
        gr.Textbox(label="Question")
    ],
    outputs="text",
    title="Document Intelligence Assistant"
)

demo.launch(inbrowser=True)