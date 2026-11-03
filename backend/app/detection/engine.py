import re
from typing import Dict, Any, List
from app.detection.rules import SCAM_RULES, NEGATIVE_CONTEXT_PATTERNS, RECOMMENDATIONS, SAFETY_WARNINGS
from app.core.logging import logger

def analyze_transcript(transcript_text: str, language_hint: str = "en") -> Dict[str, Any]:
    """
    Performs explainable, multi-factor, multilingual social engineering threat detection.
    Evaluates 8 threat categories, checks negative educational context,
    computes 0-100 risk score, and maps to cybersecurity severity levels.
    """
    if not transcript_text or not transcript_text.strip():
        return {
            "risk_score": 0.0,
            "severity": "Low",
            "threats": [],
            "categories": [],
            "recommendations": RECOMMENDATIONS["default"],
            "engine_version": "1.0.0",
            "context_suppressed": False,
            "explanation": "No speech content provided for threat analysis."
        }

    raw_text = transcript_text.strip()
    text_clean = raw_text.lower()
    
    # 1. Check for negative educational/awareness context
    is_educational = False
    context_note = ""
    for pat in NEGATIVE_CONTEXT_PATTERNS:
        if re.search(pat, text_clean, re.IGNORECASE):
            is_educational = True
            context_note = "Contextual analysis detected security awareness or educational disclaimer."
            logger.info(f"Negative security context detected: {context_note}")
            break

    triggered_threats = []
    total_raw_score = 0.0
    categories_detected = set()

    # 2. Evaluate all 8 threat categories against multilingual patterns
    for rule in SCAM_RULES:
        rule_matched = False
        matched_snippet = ""
        evidence_start = None
        evidence_end = None
        
        for pat in rule.get("patterns", []):
            match = re.search(pat, text_clean, re.IGNORECASE)
            if match:
                rule_matched = True
                matched_snippet = match.group(0)
                evidence_start = match.start()
                evidence_end = match.end()
                break
                
        if rule_matched:
            cat = rule["category"]
            categories_detected.add(cat)
            weight = float(rule["weight"])
            
            # If educational context was detected, suppress or downscale contribution
            if is_educational:
                contribution = round(weight * 0.15, 1) # Reduce significantly
                explanation = f"[Suppressed by security advisory context] {rule['description']}"
            else:
                contribution = weight
                explanation = rule["description"]
                
            total_raw_score += contribution
            triggered_threats.append({
                "rule_id": rule["rule_id"],
                "category": cat,
                "matched_text": matched_snippet,
                "evidence_start": evidence_start,
                "evidence_end": evidence_end,
                "contribution": contribution,
                "explanation": explanation,
                "recommendation": rule.get("recommendation", "")
            })

    # 3. Synergy modifier: Multi-tactic social engineering combinations
    # e.g., Authority Impersonation + Digital Arrest or Credential Theft + Urgency
    synergy_bonus = 0.0
    if not is_educational:
        if len(categories_detected) >= 3:
            synergy_bonus = 15.0
        elif len(categories_detected) == 2:
            synergy_bonus = 8.0
            
    final_score = min(100.0, max(0.0, total_raw_score + synergy_bonus))

    # 4. Severity classification
    if final_score >= 80.0:
        severity = "Critical"
    elif final_score >= 60.0:
        severity = "High"
    elif final_score >= 40.0:
        severity = "Medium"
    elif final_score >= 20.0:
        severity = "Guarded"
    else:
        severity = "Low"

    # 5. Extract targeted recommendations
    recs: List[str] = []
    for cat in categories_detected:
        if cat in RECOMMENDATIONS:
            recs.extend(RECOMMENDATIONS[cat])
    if not recs:
        recs = RECOMMENDATIONS["default"]
    unique_recommendations = list(dict.fromkeys(recs))

    return {
        "risk_score": round(final_score, 1),
        "severity": severity,
        "threats": triggered_threats,
        "categories": sorted(list(categories_detected)),
        "recommendations": unique_recommendations,
        "engine_version": "1.0.0",
        "context_suppressed": is_educational,
        "context_note": context_note
    }

def get_safety_warning_text(language: str = "en", categories: List[str] = None) -> str:
    """Returns official multilingual safety warning message."""
    lang = language.lower()
    if lang not in SAFETY_WARNINGS:
        lang = "en"
        
    warnings_dict = SAFETY_WARNINGS.get(lang, SAFETY_WARNINGS["en"])
    
    if categories:
        for cat in categories:
            if cat in warnings_dict:
                return warnings_dict[cat]
                
    return warnings_dict.get("default", SAFETY_WARNINGS["en"]["default"])
