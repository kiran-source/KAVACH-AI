# KAVACH AI — Head-to-Head 6-Configuration Benchmark Report

## 1. Executive Summary

This empirical evaluation provides a controlled, fair head-to-head comparison across six architectural configurations on the held-out test partition of Dataset v3:
- **Test Corpus**: `data/kavach_synthetic_v3/splits/test.jsonl`
- **Total Records Evaluated**: **450** (135 LEGITIMATE, 135 AMBIGUOUS, 180 SCAM)
- **Language Coverage**: 90 English (`en`), 90 Hindi (`hi`), 90 Telugu (`te`), 90 Hinglish (`hi-en`), 90 Tenglish (`te-en`)
- **Evaluation Discipline**: Strict offline evaluation without label leakage; identical evaluation pipeline across all configurations.

> [!IMPORTANT]
> **Dataset Limitation Disclosure**: All 450 test records originate from synthetic generation scripts with annotation status `pending_review`. The high classification scores reflect model capacity on synthesized semantic and lexical patterns and must not be conflated with real-world wild telephony audio performance.

---

## 2. Comprehensive 6-Configuration Benchmark Results

| Metric | Config A: TF-IDF v3 Only | Config B: MuRIL v1 Only | Config C: Hybrid Selective (Recommended) | Config D: Hybrid Always | Config E: Rule Shield Only | Config F: Full Hybrid (Shield + Selective) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Accuracy** | 100.00% | 100.00% | **100.00%** | 100.00% | 58.67% | **100.00%** |
| **Macro Precision** | 1.0000 | 1.0000 | **1.0000** | 1.0000 | 0.6185 | **1.0000** |
| **Macro Recall** | 1.0000 | 1.0000 | **1.0000** | 1.0000 | 0.5753 | **1.0000** |
| **Macro F1-Score** | 1.0000 | 1.0000 | **1.0000** | 1.0000 | 0.5844 | **1.0000** |
| **Weighted F1-Score** | 1.0000 | 1.0000 | **1.0000** | 1.0000 | 0.6075 | **1.0000** |
| **SCAM False Negatives** | **0** | **0** | **0** | **0** | 56 | **0** |
| **Mean Latency (ms)** | **4.29 ms** | 1,543.21 ms | **498.12 ms** | 1,547.50 ms | **0.85 ms** | **498.97 ms** |
| **Median (P50) Latency**| 4.22 ms | 1,454.09 ms | **4.29 ms** | 1,458.31 ms | 0.72 ms | **5.01 ms** |
| **95th Percentile (P95)**| 5.74 ms | 2,289.55 ms | 1,547.50 ms | 2,295.29 ms | 1.45 ms | 1,548.95 ms |
| **Throughput (inf/sec)**| 233.1 | 0.65 | **2.01** | 0.65 | 1,176.5 | **2.00** |
| **MuRIL Invocation %** | 0.0% | 100.0% | **32.0%** | 100.0% | 0.0% | **32.0%** |

---

## 3. Per-Class Breakdown & Confusion Matrices

### Configurations A, B, C, D, and F (100% Macro Performance on Synthetic Test Split)

Confusion Matrix ($N=450$):
$$\begin{pmatrix} 135 & 0 & 0 \\ 0 & 135 & 0 \\ 0 & 0 & 180 \end{pmatrix}$$
- **LEGITIMATE** ($N=135$): Precision 1.0000, Recall 1.0000, F1 1.0000
- **AMBIGUOUS** ($N=135$): Precision 1.0000, Recall 1.0000, F1 1.0000
- **SCAM** ($N=180$): Precision 1.0000, Recall 1.0000, F1 1.0000

### Configuration E: Rule-Priority Shield Alone

Confusion Matrix ($N=450$):
$$\begin{pmatrix} 59 & 76 & 0 \\ 54 & 81 & 0 \\ 45 & 11 & 124 \end{pmatrix}$$
- **LEGITIMATE** ($N=135$): Precision 0.3734, Recall 0.4370, F1 0.4027
- **AMBIGUOUS** ($N=135$): Precision 0.4821, Recall 0.6000, F1 0.5347
- **SCAM** ($N=180$): Precision 1.0000, Recall 0.6889, F1 0.8158
- **Critical Failure**: Missed 56 scam records (predicted as Legitimate or Ambiguous) because rule keywords did not capture nuanced social engineering without explicit blacklist triggers. However, its Precision on SCAM was 100%, proving that when a rule triggers, it is virtually always an active scam.

---

## 4. Per-Language Performance Analysis

Across all five language splits ($N=90$ each), Configurations A, B, C, D, and F maintained 100% classification accuracy on the synthetic benchmark:

| Language Partition | Samples | Config A (TF-IDF) | Config B (MuRIL) | Config C (Selective) | Config E (Rules) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **English (`en`)** | 90 | 100.0% | 100.0% | 100.0% | 42.22% |
| **Hindi (`hi`)** | 90 | 100.0% | 100.0% | 100.0% | 60.00% |
| **Telugu (`te`)** | 90 | 100.0% | 100.0% | 100.0% | 65.56% |
| **Hinglish (`hi-en`)**| 90 | 100.0% | 100.0% | 100.0% | 60.00% |
| **Tenglish (`te-en`)**| 90 | 100.0% | 100.0% | 100.0% | 65.56% |

---

## 5. Architectural Trade-off Analysis & Recommendation

1. **Why Config C / Config F (Hybrid Selective) is the Optimal Production Target**:
   - **Compute Reduction**: Cuts expensive transformer invocations from 100% down to **32.0%**, delivering a **68% compute reduction**.
   - **Median Latency Preservation**: Median (P50) latency remains **4.29 ms** (matching TF-IDF fast path) because 68% of standard incoming calls are handled without touching the transformer.
   - **Zero Safety Compromise**: The Rule-Priority Shield guarantees immediate intervention for known critical scams, while selective escalation routes complex or borderline calls to MuRIL.
2. **Operational Verdict**:
   - **READY FOR HYBRID EXPERIMENTATION** in controlled staging environments.

