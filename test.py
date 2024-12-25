import spacy
from spacy.tokens import DocBin

# Load the .spacy file
filepath = "data/spacy/train.spacy"  # Replace with the actual path to your file
db = DocBin().from_disk(filepath)

# Load a blank English language model (or any suitable model)
nlp = spacy.blank("en")

# Get the Doc objects from the DocBin
docs = list(db.get_docs(nlp.vocab))

# Now you can iterate through the Doc objects and access their content:
for doc in docs:
    print("Text:", doc.text)  # Print the text of the document
    print("Entities:")
    for ent in doc.ents:
        print(f"  - {ent.text} ({ent.label_}): {ent.start_char}, {ent.end_char}")  # Print entity details
    print("---")