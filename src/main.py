import spacy
from spacy.tokens import DocBin

def get_entities_by_label(spacy_filepath, label):
    """
    Loads a .spacy file, gets all Doc objects, and extracts entities of a specific label.

    Args:
        spacy_filepath: Path to the .spacy file.
        label: The entity label to extract (e.g., "PERSON").

    Returns:
        A list of entity texts for the specified label.
    """
    nlp = spacy.blank("en")  # Use the same language model as during conversion
    db = DocBin().from_disk(spacy_filepath)
    docs = list(db.get_docs(nlp.vocab))

    entities = []
    for doc in docs:
        for ent in doc.ents:
            if ent.label_ == label:
                entities.append(ent.text)
    return entities

# Example Usage:
spacy_filepath = "data/spacy/train.spacy"  # Replace with your file path
person_entities = get_entities_by_label(spacy_filepath, "PERSON")

print(f"Found PERSON entities: {person_entities}")