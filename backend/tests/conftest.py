"""
Pytest Configuration and Fixtures for KAVACH AI
Ensures paths and test environment variables are loaded properly.
Allows tests to run cleanly in clean environments without an active API key.
"""

import os
import sys
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
BACKEND_DIR = TESTS_DIR.parent
PROJECT_ROOT = BACKEND_DIR.parent

# Ensure project root and backend are in sys.path
for p in [str(PROJECT_ROOT), str(BACKEND_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

# Set testing environment flags
os.environ["TESTING"] = "true"
if "DEMO_MODE" not in os.environ:
    os.environ["DEMO_MODE"] = "true"

