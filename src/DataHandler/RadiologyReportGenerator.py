from faker import Faker
import random

class RadiologyReportGenerator:
    def __init__(self):
        self.fake = Faker()
        self.anatomical_locations = [
            "left upper lobe", "right upper lobe", "left lower lobe", "right lower lobe",
            "right middle lobe", "mediastinum", "pleural space", "left hilum", "right hilum",
            "cardiac silhouette", "aortic arch", "thoracic spine", "diaphragm"
        ]
        self.findings = [
            "nodule", "mass", "opacity", "consolidation", "effusion", "pneumothorax",
            "atelectasis", "scarring", "calcification", "lesion", "infiltrate"
        ]
        self.descriptors = [
            "small", "large", "well-defined", "poorly-defined", "calcified", "non-calcified",
            "round", "oval", "irregular", "spiculated", "lobulated"
        ]
        self.diseases = [
            "pneumonia", "atelectasis", "pulmonary edema", "lung cancer", "tuberculosis",
            "bronchitis", "pleural effusion", "pulmonary embolism"
        ]
        self.recommendations = [
            "Recommend follow-up CT scan", "Clinical correlation suggested",
            "Recommend biopsy", "No further imaging recommended at this time",
            "Correlation with prior studies suggested"
        ]
        self.findings_templates = [
                "A {descriptor} {finding} is present in the {location}.",
                "The {location} demonstrates a {descriptor} {finding}.",
                "There is evidence of a {finding} measuring approximately {size} cm in the {location}.",
                "{finding} noted in the {location}, {descriptor} in appearance.",
                "No significant {finding} identified."
        ]
        self.impression_templates = [
                "IMPRESSION: {disease}.",
                "IMPRESSION: Findings suggestive of {disease}.",
                "IMPRESSION: {descriptor} {finding} in the {location}, concerning for {disease}.",
                "IMPRESSION: No acute cardiopulmonary process.",
                "IMPRESSION: Stable appearance compared to prior examination."
        ]

    def generate_phi(self):
        return {
            "patient_name": self.fake.name(),
            "dob": self.fake.date_of_birth(minimum_age=20, maximum_age=90).strftime("%m/%d/%Y"),
            "mrn": self.fake.numerify(text="#######"),
            "exam_date": self.fake.date_this_year(before_today=True, after_today=False).strftime("%Y-%m-%d")
        }

    def generate_findings(self):
        num_findings = random.randint(0, 3)
        if num_findings == 0:
            return "No acute cardiopulmonary findings."
        findings_text = []
        for _ in range(num_findings):
          template = random.choice(self.findings_templates)
          finding = random.choice(self.findings)
          location = random.choice(self.anatomical_locations)
          descriptor = random.choice(self.descriptors)
          size = random.randint(1, 5)
          if random.random() < 0.2:
            if "No significant" in template:
                finding_text = template.format(finding=finding)
            else:
                finding_text = "No evidence of " + finding + " in the " + location + "."
          elif random.random() < 0.1:
            finding_text = template.format(
                descriptor=descriptor, finding="possible " + finding, location=location, size=size
            )
          else:
           finding_text = template.format(
                descriptor=descriptor, finding=finding, location=location, size=size
            )
          findings_text.append(finding_text)
        return " ".join(findings_text)

    def generate_impression(self):
        template = random.choice(self.impression_templates)
        if "disease" in template:
          disease = random.choice(self.diseases)
          location = random.choice(self.anatomical_locations)
          descriptor = random.choice(self.descriptors)
          finding = random.choice(self.findings)
          return template.format(disease=disease, location=location, finding=finding, descriptor=descriptor)
        else:
          return template
    
    def generate_recommendation_section(self):
       if random.random() < 0.7:
         return random.choice(self.recommendations)
       else:
         return ""
    def generate_report(self):
        phi = self.generate_phi()
        findings = self.generate_findings()
        impression = self.generate_impression()
        # Combine everything into a report
        return f"""Patient Name: {phi['patient_name']} 
Date of Birth: {phi['dob']}
Medical Record Number: {phi['mrn']}
Date of Exam: {phi['exam_date']}


FINDINGS: {findings} 
        
{impression}
        
{self.generate_recommendation_section()}
        """
# Usage
generator = RadiologyReportGenerator()
synthetic_reports = []
for _ in range(500):
    synthetic_reports.append(generator.generate_report())

# Print or save the reports
for i, report in enumerate(synthetic_reports):
    print(f"--- Report {i+1} ---\n{report}\n")

# Save the reports to a file
try:
    with open("synthetic_radiology_reports.txt", "w") as f:
        for report in synthetic_reports:
            f.write(report + "\n\n")
except Exception as e:
    print(f"An error occurred while saving the reports: {e}")