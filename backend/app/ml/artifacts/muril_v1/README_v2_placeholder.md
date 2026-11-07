# KAVACH AI — MuRIL Classifier Artifacts (v1)

This directory is designated for the fine-tuned Google **MuRIL** (`google/muril-base-cased`) transformer model artifacts.

## Current Status: PENDING COLAB EXECUTION
To respect local workstation resource constraints (CPU-only laptop runtime), transformer training is designed to be executed on **Google Colab with a free T4 GPU** rather than locally.

The active production baseline remains the lightweight **TF-IDF + Calibrated Logistic Regression model** located in `backend/app/ml/artifacts/v1/`.

## Steps to Deploy Trained MuRIL Weights:
1. Open and run [`notebooks/KAVACH_AI_MuRIL_Colab_Training.ipynb`](file:///c:/Users/kiran/OneDrive/Documents/Desktop/Kavach/notebooks/KAVACH_AI_MuRIL_Colab_Training.ipynb) in Google Colab.
2. Complete Section 14 (Fine-Tuning) and Section 20 (Model Export).
3. Download the generated `muril_v1_artifacts.zip` from Colab.
4. Extract the contents into this directory:
   - `model.safetensors` (or `pytorch_model.bin`)
   - `config.json`
   - `tokenizer_config.json`
   - `vocab.txt`
   - `special_tokens_map.json`
5. The separate inference wrapper [`backend/app/ml/muril_classifier.py`](file:///c:/Users/kiran/OneDrive/Documents/Desktop/Kavach/backend/app/ml/muril_classifier.py) will automatically detect the weights and initialize the transformer.

