import spacy
from spacy.tokens import DocBin
from spacy import displacy

nlp = spacy.load("models/model-last")  

db = DocBin().from_disk("data/spacy/test.spacy")
docs = list(db.get_docs(nlp.vocab))

doc_to_visualize = docs[0]
displacy.serve(doc_to_visualize, style="ent")