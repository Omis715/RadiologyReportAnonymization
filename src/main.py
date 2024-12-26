import spacy
from spacy.tokens import DocBin
import random 

def split_spacy_data(spacy_filepath, train_ratio = 0.8, valid_ratio = 0.1):
    db = DocBin().from_disk(spacy_filepath)
    nlp = spacy.blank("en")
    docs = list(db.get_docs(nlp.vocab))
    random.shuffle(docs)

    train_size = int(len(docs) * train_ratio)
    valid_size = int(len(docs) * valid_ratio)

    train_docs = docs[:train_size]
    valid_docs = docs[train_size:valid_size]
    test_docs = docs[train_size + valid_size:]

    train_db = DocBin(docs = train_docs)
    valid_db = DocBin(docs = valid_docs)
    test_db = DocBin(docs = test_docs)

    return train_db, valid_db, test_db

spacy_filepath = "data/spacy/train.spacy"
train_db, valid_db, test_db = split_spacy_data(spacy_filepath=spacy_filepath)
# Save data to disk 
train_db.to_disk("data/spacy/train.spacy")
valid_db.to_disk("data/spacy/valid.spacy")
test_db.to_disk("data/spacy/test.spacy")