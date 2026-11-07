"""
Preprocessing and normalization utilities for transcript text.
"""

import re
from typing import Optional

def normalize_transcript(text: Optional[str]) -> str:
    """
    Cleans and normalizes transcript text for both rule and ML feature extraction.
    Preserves Indic characters, diacritics, and punctuation relevant to tone.
    """
    if not text:
        return ""
    
    # Strip leading/trailing whitespace
    cleaned = text.strip()
    
    # Normalize multiple whitespace characters to single space
    cleaned = re.sub(r'[\r\n\t]+', ' ', cleaned)
    cleaned = re.sub(r'\s{2,}', ' ', cleaned)
    
    return cleaned

