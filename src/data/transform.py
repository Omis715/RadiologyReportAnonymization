import re
import os
import spacy
from spacy.tokens import DocBin


nlp = spacy.load("en_core_web_sm")

with open('data\\synthetic_radiology_reports.txt', 'r') as file:
    text = file.read()

records = [record.strip() for record in text.split("\n\n") if record.strip()]
records = [records[i]+ "\n" +records[i+1] for i in range(0,len(records),2)]

def extract_data(record):
    data = {
        "Patient Name": None,
        "Date of Birth": None,
        "Medical Record Number": None,
        "Date of Exam": None,
        "Findings": None,
        "Impression": None,
        "Recommendation": None
    }

    # Process each line in the record
    lines = record.split("\n")
    for line in lines:
        line = line.strip()
        if "Patient Name:" in line:
            parts = line.split("Patient Name:")
            if len(parts) > 1:  
                data["Patient Name"] = parts[1].strip()
        elif "Date of Birth:" in line:
            parts = line.split("Date of Birth:")
            if len(parts) > 1:
                data["Date of Birth"] = parts[1].strip()
        elif "Medical Record Number:" in line:
            parts = line.split("Medical Record Number:")
            if len(parts) > 1:
                data["Medical Record Number"] = parts[1].strip()
        elif "Date of Exam:" in line:
            parts = line.split("Date of Exam:")
            if len(parts) > 1:
                data["Date of Exam"] = parts[1].strip()
        elif "FINDINGS:" in line:
            data["Findings"] = line.replace("FINDINGS:", "").strip()
        elif "IMPRESSION:" in line:
            data["Impression"] = line.replace("IMPRESSION:", "").strip()
        elif "Recommend" in line:
            data["Recommendation"] = line.replace("Recommend", "").strip()

    return data

sythetic_reports_data = []
for record in records:
    data = extract_data(record)
    sythetic_reports_data.append(data)


def convert_dict_to_spacy(report_dict, nlp):
    text = f"""
Patient Name: {report_dict['Patient Name']}
Date of Birth: {report_dict['Date of Birth']}
Medical Record Number: {report_dict['Medical Record Number']}
Date of Exam: {report_dict['Date of Exam']}

FINDINGS: {report_dict['Findings']}

IMPRESSION: {report_dict['Impression']}

{report_dict['Recommendation']}"""

    doc = nlp(text)
    ents = []

    entity_mapping = {
        "PERSON": "Patient Name",
        "DATE": ["Date of Birth", "Date of Exam"],
        "MEDICAL_RECORD": "Medical Record Number",
    }
    for ent_type, fields in entity_mapping.items():
      if isinstance(fields, str):
        fields = [fields]
      for field in fields:
        if report_dict[field]:
            value = report_dict[field]
            for match in re.finditer(re.escape(value), doc.text, re.IGNORECASE):
                s, e = match.span()
                span = doc.char_span(s, e, label=ent_type)
                if span is not None:
                    ents.append(span)
                else:
                    print(f"Error creating span for '{value}' in report: {report_dict}")

    doc.ents = ents 
    return doc

def pre_annotate_and_convert_to_spacy(reports_data, spacy_output_path):
    nlp = spacy.blank("en")
    db = DocBin()

    for report_dict in reports_data:
        doc = convert_dict_to_spacy(report_dict, nlp)
        db.add(doc)
    output_dir = os.path.dirname(spacy_output_path)
    os.makedirs(output_dir, exist_ok=True)

    db.to_disk(spacy_output_path)

spacy_output_file = "data/spacy/train.spacy"

pre_annotate_and_convert_to_spacy(sythetic_reports_data, spacy_output_file)

print(f"Converted data to SpaCy format and saved to: {spacy_output_file}")