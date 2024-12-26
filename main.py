import gradio as gr
import spacy
from PIL import Image
from pdf2image import convert_from_path, convert_from_bytes
import pytesseract
import re
import os
import tempfile

model_path = "models/model-best" 
try:
    nlp = spacy.load(model_path)
except OSError:
    print(f"Error: Could not load the model from {model_path}. "
          f"Please make sure the path is correct and the model is in the specified directory.")
    exit()

# --- Anonymization Function ---
def anonymize_report(text, nlp):
    doc = nlp(text)
    anonymized_text = ""
    last_end = 0
    for ent in doc.ents:
        anonymized_text += text[last_end:ent.start_char] + "[" + ent.label_ + "]"
        last_end = ent.end_char
    anonymized_text += text[last_end:]

    # Add spans for placeholders in the anonymized text
    anonymized_doc = nlp(anonymized_text)
    ents = []
    for match in re.finditer(r"\[(.*?)\]", anonymized_text):  
        s, e = match.span()
        label = match.group(1)
        span = anonymized_doc.char_span(s, e, label=label)
        if span is not None:
            ents.append(span)

    anonymized_doc.ents = ents
    return anonymized_doc, anonymized_text

# --- Function to Convert PDF to Images ---
def convert_pdf_to_images(pdf_path):
    return convert_from_path(pdf_path)

# --- Function to Extract Text from Image ---
def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

# --- Gradio Interface ---
def process_file(file):
    if file is None:
        return "Please upload a file.", ""

    tmp_pdf_path = None

    try:
        file_type = file.name.split(".")[-1]

        if file_type.lower() in ["jpg", "jpeg", "png"]:
            # Process Image
            image = Image.open(file.name)
            original_text = extract_text_from_image(image)

        elif file_type.lower() == "pdf":
            # Process PDF
            images = convert_pdf_to_images(file.name)
            original_text = ""
            for image in images:
                original_text += extract_text_from_image(image)

        else:
            return "Unsupported file type. Please upload an image or PDF.", ""

        anonymized_doc, anonymized_text = anonymize_report(original_text, nlp)
        return original_text, anonymized_text

    except Exception as e:
        return f"An error occurred: {e}", ""

    finally:
        if tmp_pdf_path:
            os.remove(tmp_pdf_path)


iface = gr.Interface(
    fn=process_file,
    inputs=gr.File(label="Upload an image or PDF file"),
    outputs=[
        gr.Textbox(label="Original Report", lines=10),
        gr.Textbox(label="Anonymized Report", lines=10)
    ],
    title="Radiology Report Anonymizer",
    description="Upload a radiology report (image or PDF) and the system will automatically anonymize it by identifying and replacing PHI.",
    allow_flagging="never"
)

if __name__ == "__main__":
    iface.launch()