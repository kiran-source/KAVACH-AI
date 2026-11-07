# KAVACH AI — Google Colab MuRIL Fine-Tuning Execution Guide

This document provides complete, reproducible, step-by-step instructions for fine-tuning **Google's MuRIL** (`google/muril-base-cased`) transformer model on Google Colab for multilingual voice scam, vishing, and social-engineering fraud text classification across **Telugu, Hindi, English, and Code-Mixed** Indian languages.

---

## 1. Why MuRIL for Indian Telephony Scam Detection?

**MuRIL** (*Multilingual Representations for Indian Languages*) was developed by Google specifically for the linguistic landscape of India:
- Pre-trained on **17 Indian languages** plus English.
- Pre-trained on **monolingual**, **parallel translated**, and crucially **Latin-transliterated text** (e.g. Hinglish and Tenglish).
- Highly resilient to the colloquial spelling variations, phonetic transliterations, and code-switching commonly encountered in Indian cybercrime conversations.

---

## 2. Hardware & Runtime Requirements

- **Environment**: Google Colab (Standard Free Tier or Colab Pro)
- **Hardware Accelerator**: **NVIDIA T4 GPU** (15 GB VRAM) or higher (V100, A100)
- **Local Workstation Impact**: **Zero.** Training executes entirely in the cloud. No heavy transformer weights are downloaded to your local workstation.
- **Estimated Wall-Clock Time**: ~6 to 10 minutes on a standard Colab T4 GPU for 3 epochs on 350 training samples.

---

## 3. Step-by-Step Google Colab Execution

### Step 1: Open the Notebook in Google Colab
1. Navigate to [Google Colab](https://colab.research.google.com/).
2. Click **Upload** and select [`notebooks/KAVACH_AI_MuRIL_Colab_Training.ipynb`](file:///c:/Users/kiran/OneDrive/Documents/Desktop/Kavach/notebooks/KAVACH_AI_MuRIL_Colab_Training.ipynb) (or [`KAVACH_AI_MuRIL_Colab_Training.ipynb`](file:///c:/Users/kiran/OneDrive/Documents/Desktop/Kavach/KAVACH_AI_MuRIL_Colab_Training.ipynb)).

### Step 2: Set the GPU Accelerator
1. In the Colab top menu, go to **Runtime** → **Change runtime type**.
2. Under **Hardware accelerator**, select **T4 GPU**.
3. Click **Save**.

### Step 3: Run Section 1 to 4 (Environment & Dependencies)
1. Run **Cell 1**: Initializes the master `CONFIG` dictionary:
   - Base Checkpoint: `google/muril-base-cased`
   - Target Classes: `LEGITIMATE: 0`, `AMBIGUOUS: 1`, `SCAM: 2`
   - Max Sequence Length: `256`
   - Batch Size: `8`
   - Learning Rate: `2e-5`
   - Epochs: `3` (with early stopping)
   - Seed: `42`
2. Run **Cell 2**: Verifies CUDA availability and detects your assigned GPU.
3. Run **Cell 3**: Installs `transformers`, `datasets`, `accelerate`, `evaluate`, `scikit-learn`, and `sentencepiece`.
4. Run **Cell 4** *(Optional)*: Mount Google Drive if you plan to persist checkpoints across sessions.

### Step 4: Load the Dataset (Section 5 to 7)
1. Run **Cell 5**: Discovers the dataset.
   - If you cloned the repository in Colab (`!git clone ...`), it auto-locates `data/kavach_synthetic_v2/splits/`.
   - If running standalone, it prompts an interactive file upload widget for `train.jsonl`, `validation.jsonl`, and `test.jsonl`.
2. Run **Cell 6**: Inspects record schema, verifies class distribution, and confirms the `review_status: "pending_review"` annotation status.
3. Run **Cell 7**: Executes the zero-leakage audit, asserting that zero Conversation IDs, zero scenario families, and zero exact dialogue text hashes cross between train, validation, and test splits.

### Step 5: Tokenization & Model Initialization (Section 8 to 13)
1. Run **Cell 8**: Extracts dialogue transcripts and assigns integer class labels.
2. Run **Cell 9**: Downloads and initializes the official `google/muril-base-cased` tokenizer (~3.1 MB).
3. Run **Cell 10 & 11**: Encodes text to `max_length=256` with attention masks and creates Hugging Face `Dataset` objects.
4. Run **Cell 12**: Instantiates `AutoModelForSequenceClassification` with 3 target classes and transfers it to GPU VRAM (~430 MB).
5. Run **Cell 13**: Configures `TrainingArguments` with FP16 mixed precision, `eval_strategy="epoch"`, `metric_for_best_model="macro_f1"`, and an `EarlyStoppingCallback(early_stopping_patience=2)`.

### Step 6: Execute Fine-Tuning (Section 14 & 15)
1. Run **Cell 14**: Launches GPU training via Hugging Face `Trainer`.
   - Includes automatic checkpoint recovery: if interrupted, re-running Cell 14 automatically resumes from the last saved epoch checkpoint.
2. Run **Cell 15**: Evaluates the best checkpoint on the validation split.

### Step 7: Evaluate on Held-Out Test Split (Section 16 to 18)
1. Run **Cell 16**: Generates predictions on the isolated 75-sample test set. Computes accuracy, macro precision, macro recall, and macro F1.
2. Run **Cell 17**: Displays the full Scikit-Learn `classification_report` and plots the 2D confusion matrix.
3. Run **Cell 18**: Computes disaggregated accuracy and macro F1 per language category (Telugu, Hindi, English, Hinglish, Tenglish).

### Step 8: Live Scenario Inference (Section 19)
1. Run **Cell 19**: Runs live inference across 5 representative Indian cybercrime and benign scenario archetypes:
   - CBI Digital Arrest (English)
   - Delhi Police Narcotics Contraband (Hindi)
   - Bank KYC Phishing (Telugu Code-Mixed)
   - Public Bank Security Awareness Broadcast (English, Benign)
   - E-Commerce Delivery Address Clarification (Telugu, Ambiguous)

### Step 9: Export Artifacts (Section 20 & 21)
1. Run **Cell 20**: Exports the fine-tuned model weights, tokenizer, label mapping, training configuration, evaluation metrics, and metadata to `./muril_v1/`.
2. Run **Cell 21**: Packages `./muril_v1/` into `muril_v1_artifacts.zip` and triggers an automatic browser download (or copies to Google Drive).

### Step 10: Compare Baseline & Review Summary (Section 22)
1. Run **Cell 22**: Displays a side-by-side benchmark table comparing the fine-tuned MuRIL transformer with KAVACH AI's production TF-IDF + Logistic Regression baseline.

---

## 4. Deploying Trained Weights to KAVACH AI

Once you download `muril_v1_artifacts.zip`:
1. Extract the contents into your local project directory:
   ```
   backend/app/ml/artifacts/muril_v1/
   ```
   The directory should contain:
   - `model.safetensors` (or `pytorch_model.bin`)
   - `config.json`
   - `tokenizer_config.json`
   - `vocab.txt`
   - `special_tokens_map.json`
   - `label_mapping.json`
   - `metadata.json`
   - `training_config.json`
   - `evaluation_metrics.json`
2. Run the comparative evaluation script locally:
   ```bash
   python scripts/evaluate_muril_vs_baseline.py
   ```
3. Use the separate inference wrapper:
   ```python
   from app.ml.muril_classifier import get_muril_classifier

   classifier = get_muril_classifier()
   result = classifier.predict("This is CBI Mumbai calling regarding illegal hawala transfer.")
   print(result.predicted_class, result.confidence, result.probabilities)
   ```

---

## 5. Architectural & Operational Comparison

| Metric / Property | Production Baseline (TF-IDF) | MuRIL Transformer (`google/muril-base-cased`) |
| :--- | :--- | :--- |
| **Model Type** | Sublinear TF-IDF + Calibrated Logistic Regression | Bidirectional Transformer Encoder |
| **Parameter Count** | 2,607 linear features | ~110 Million parameters |
| **Artifact Footprint** | **553.5 KB** | **~430 MB** |
| **Inference Hardware** | **Host CPU Native** (Zero GPU required) | **NVIDIA GPU Recommended** (T4 / V100) |
| **Host CPU Latency** | **Mean: 11.68 ms, P50: 10.27 ms, P95: 23.06 ms** | ~350 - 500 ms (CPU) / ~40 - 60 ms (GPU) |
| **Memory Requirement** | < 50 MB RAM | ~1.2 GB RAM (CPU) / ~2.5 GB VRAM (GPU) |
| **Operational Role** | **Active Production Default** | **Advanced Secondary Arbiter & Research Pathway** |

---

## 6. Critical Safety Guarantees

In KAVACH AI, machine learning models serve strictly as **advisory inputs** within a defense-in-depth architecture:
1. **Rule-Priority Shield**: Deterministic critical scam rules (OTP demands, Digital Arrest coercion, AnyDesk APK remote control) retain absolute precedence. A machine learning prediction—whether from TF-IDF or MuRIL—can **never downgrade a critical deterministic rule violation**.
2. **Synthetic Data Boundaries**: High performance on domain-curated synthetic test sets does **not** establish wild telephony scam detection accuracy. Real telephony introduces non-standard codecs (AMR-NB 8 kHz), acoustic reverberation, packet loss, and emergent regional slang.
3. **No Automatic Replacement**: The production TF-IDF model remains the active default to preserve 100% reliable execution on 16GB consumer laptops without external GPU dependencies.
