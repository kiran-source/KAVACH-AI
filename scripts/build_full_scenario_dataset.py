import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from scripts.dataset_generator import (
    DATASET_ROOT, METADATA_DIR, TRANSCRIPTS_DIR, AUDIO_DIR, SPLITS_DIR, REPORTS_DIR,
    STORAGE_BUDGET_MB, StorageMonitor, ApiUsageLedger, DatasetValidator,
    GnaniTimbreAdapter, GnaniPrismaAdapter, PILOT_CONVERSATIONS
)

# We will build the full 100 conversation catalog in a structured dictionary
print("Building full 100-conversation scenario catalog...")

