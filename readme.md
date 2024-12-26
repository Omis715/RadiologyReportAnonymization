# Radiology Report Anonymization

## Overview

This project aims to automatically anonymize radiology reports by identifying and removing Protected Health Information (PHI). The system uses Natural Language Processing (NLP) techniques, specifically Named Entity Recognition (NER), to identify sensitive entities such as patient names, dates, medical record numbers, and other identifiers. The project uses a combination of synthetic data generation, manual annotation with Doccano, and model training with SpaCy to create an NER model capable of accurately anonymizing radiology reports.

## Run the training 
```bash
python -m spacy train config.cfg --output ./models --paths.train data/spacy/train.spacy --paths.dev data/spacy/valid.spacy
```

## Evaluate the model 
```bash
python -m spacy evaluate  ./models/model-last data/spacy/test.spacy --output ./metrics 
```