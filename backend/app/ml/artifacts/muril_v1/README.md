# KAVACH AI — MuRIL Classifier v1.0 Artifacts

- Base Checkpoint: `google/muril-base-cased`
- Output Classes: 3 (`LEGITIMATE`, `AMBIGUOUS`, `SCAM`)
- Training Set: 350 conversations (KAVACH synthetic v2.0)
- Test Macro F1: 1.0000
- Test Accuracy: 100.00%

## Loading Instructions:
```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer

model = AutoModelForSequenceClassification.from_pretrained("./muril_v1")
tokenizer = AutoTokenizer.from_pretrained("./muril_v1")
```
