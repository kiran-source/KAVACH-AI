"""
Submission and Review Packaging Script for KAVACH AI
Creates:
1. KAVACH_AI_Final_Submission.zip
2. KAVACH_AI_Final_Review_Package.zip

Excludes:
- .env files (except .env.example)
- SQLite development databases (kavach.db)
- node_modules
- .venv / venv
- Python cache directories (__pycache__, .pytest_cache)
- Git history (.git)
- Temporary audio uploads
- Temporary logs containing credentials

Includes:
- Full source code (FastAPI backend + React frontend)
- Complete 100-sample multilingual dataset (transcripts, 20 canonical WAVs, splits, metadata)
- All audit, integrity, test, split, and validation reports
- Documentation and environment templates

Verifies zip contents and calculates SHA-256 checksums.
"""

import os
import sys
import json
import zipfile
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "dist_submission"

EXCLUDE_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "__pycache__",
    ".pytest_cache",
    ".vite",
    "scratch",
    "dist_submission",
    ".vscode",
    ".idea",
    "venv",
    ".venv"
}

EXCLUDE_EXTENSIONS = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".db",
    ".sqlite",
    ".sqlite3",
    ".log",
    ".zip"
}

def should_exclude(file_path: Path) -> bool:
    rel_path = file_path.relative_to(PROJECT_ROOT)
    parts = rel_path.parts
    
    # Exclude directories
    for part in parts[:-1]:
        if part in EXCLUDE_DIRS:
            return True
        if part.startswith(".") and part != ".planning":
            return True

    filename = file_path.name
    
    # Exclude all .env files EXCEPT .env.example
    if filename.startswith(".env") and filename != ".env.example":
        return True
    
    # Exclude temporary prompt files or dump files
    if filename.startswith("prompt_") and filename.endswith(".txt"):
        return True
    
    # Exclude database and cache files
    if file_path.suffix.lower() in EXCLUDE_EXTENSIONS:
        return True
    
    if filename == "kavach.db":
        return True

    # Exclude external archive manifests so archives don't contain stale/self-referential hashes
    if filename in {"checksums.sha256", "archive_checksums.json"}:
        return True
        
    # Exclude temporary generated user audio uploads (preserve gitkeeps and default samples)
    if "uploads" in parts and filename != ".gitkeep" and not filename.endswith(".json"):
        return True
        
    return False

def calculate_sha256(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def build_zip(zip_path: Path) -> Tuple[int, int, str]:
    packaged_files = []
    excluded_count = 0
    
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(PROJECT_ROOT):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not (d.startswith(".") and d != ".planning")]
            
            for file in files:
                file_path = Path(root) / file
                if should_exclude(file_path):
                    excluded_count += 1
                    continue
                
                arcname = file_path.relative_to(PROJECT_ROOT)
                zf.write(file_path, arcname)
                packaged_files.append(str(arcname))
                
    sha256_hash = calculate_sha256(zip_path)
    return len(packaged_files), excluded_count, sha256_hash

def verify_archive(zip_path: Path) -> List[str]:
    issues = []
    with zipfile.ZipFile(zip_path, "r") as zf:
        names = zf.namelist()
        for n in names:
            if n == ".env" or n.endswith("/.env") or n.endswith("\\.env"):
                issues.append(f"Forbidden .env file found: {n}")
            if "node_modules" in n:
                issues.append(f"node_modules found: {n}")
            if ".git/" in n or ".git\\" in n:
                issues.append(f"git history found: {n}")
            if n.endswith(".db") or "kavach.db" in n:
                issues.append(f"database file found: {n}")
            if "checksums.sha256" in n or "archive_checksums.json" in n:
                issues.append(f"Forbidden self-referential manifest found inside archive: {n}")
                
        # Check required files
        required_items = [
            "README.md",
            "backend/.env.example",
            "backend/app/main.py",
            "backend/app/ml/artifacts/v1/model.joblib",
            "backend/app/ml/artifacts/v1/vectorizer.joblib",
            "notebooks/KAVACH_AI_Multilingual_Training.ipynb",
            "frontend/package.json",
            "data/kavach_synthetic_v1/metadata/conversations.jsonl",
            "data/kavach_synthetic_v2/metadata/conversations.jsonl",
            "docs/ML_MODEL_CARD.md",
            "docs/DATASET_CARD.md",
            "docs/EVALUATION_REPORT.md",
            "docs/SECURITY_REVIEW.md",
            "docs/KNOWN_LIMITATIONS.md",
            "docs/USER_GUIDE.md"
        ]
        for req in required_items:
            norm_names = [x.replace("\\", "/") for x in names]
            if req.replace("\\", "/") not in norm_names:
                issues.append(f"Missing required artifact: {req}")
                
        # Check audio files count (should be 20)
        audio_files = [x for x in names if "data/kavach_synthetic_v1/audio" in x.replace("\\", "/") and x.endswith(".wav")]
        if len(audio_files) != 20:
            issues.append(f"Expected 20 audio files, found {len(audio_files)}")
            
        # Check transcript files count (should be 100)
        transcript_files = [x for x in names if "data/kavach_synthetic_v1/transcripts" in x.replace("\\", "/") and x.endswith(".txt")]
        if len(transcript_files) != 100:
            issues.append(f"Expected 100 transcript files, found {len(transcript_files)}")
            
    return issues

def package_all():
    import shutil
    print("=" * 75)
    print("KAVACH AI — PACKAGING SUBMISSION AND REVIEW ARCHIVES")
    print("=" * 75)
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR = OUTPUT_DIR / "backups"
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    # Preserve previous archives before generating new ones
    for existing in [
        OUTPUT_DIR / "KAVACH_AI_Final_Submission.zip",
        OUTPUT_DIR / "KAVACH_AI_Final_Review_Package.zip",
        PROJECT_ROOT / "KAVACH_AI_Review_Package.zip"
    ]:
        if existing.exists():
            backup_dest = BACKUP_DIR / f"{existing.stem}_backup{existing.suffix}"
            if not backup_dest.exists():
                shutil.copy2(existing, backup_dest)
                print(f"[BACKUP] Preserved existing archive to: {backup_dest.name}")
    
    # 1. Package KAVACH_AI_Final_Submission.zip
    sub_zip = OUTPUT_DIR / "KAVACH_AI_Final_Submission.zip"
    print(f"\nBuilding {sub_zip.name}...")
    sub_files, sub_excluded, sub_sha = build_zip(sub_zip)
    sub_size_mb = sub_zip.stat().st_size / (1024 * 1024)
    print(f"  [CREATED] {sub_zip.name}")
    print(f"  Size: {sub_size_mb:.2f} MB | Packaged Files: {sub_files} | Excluded: {sub_excluded}")
    print(f"  SHA-256: {sub_sha}")
    
    sub_issues = verify_archive(sub_zip)
    if sub_issues:
        print(f"  [FAIL] Verification issues found: {sub_issues}")
    else:
        print("  [PASS] Archive verification passed: Zero secrets, zero databases, all 100 conversations & 20 WAVs verified.")
        
    # 2. Package KAVACH_AI_Final_Review_Package.zip
    rev_zip = OUTPUT_DIR / "KAVACH_AI_Final_Review_Package.zip"
    print(f"\nBuilding {rev_zip.name}...")
    rev_files, rev_excluded, rev_sha = build_zip(rev_zip)
    rev_size_mb = rev_zip.stat().st_size / (1024 * 1024)
    print(f"  [CREATED] {rev_zip.name}")
    print(f"  Size: {rev_size_mb:.2f} MB | Packaged Files: {rev_files} | Excluded: {rev_excluded}")
    print(f"  SHA-256: {rev_sha}")
    
    rev_issues = verify_archive(rev_zip)
    if rev_issues:
        print(f"  [FAIL] Verification issues found: {rev_issues}")
    else:
        print("  [PASS] Archive verification passed: Zero secrets, zero databases, all 100 conversations & 20 WAVs verified.")

    # 3. Copy review package to root KAVACH_AI_Review_Package.zip
    import shutil
    root_rev_zip = PROJECT_ROOT / "KAVACH_AI_Review_Package.zip"
    shutil.copy2(rev_zip, root_rev_zip)
    root_rev_sha = calculate_sha256(root_rev_zip)
    root_rev_size_mb = root_rev_zip.stat().st_size / (1024 * 1024)
    print(f"\nCopied review package to {root_rev_zip.name}")
    print(f"  Size: {root_rev_size_mb:.2f} MB | SHA-256: {root_rev_sha}")

    # Save manifest of archives
    from datetime import datetime, timezone
    pkg_manifest = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "archives": {
            "submission_archive": {
                "filename": sub_zip.name,
                "path": str(sub_zip),
                "size_mb": round(sub_size_mb, 2),
                "file_count": sub_files,
                "sha256": sub_sha,
                "verification_status": "PASS" if not sub_issues else "FAIL"
            },
            "review_archive": {
                "filename": rev_zip.name,
                "path": str(rev_zip),
                "size_mb": round(rev_size_mb, 2),
                "file_count": rev_files,
                "sha256": rev_sha,
                "verification_status": "PASS" if not rev_issues else "FAIL"
            },
            "root_review_archive": {
                "filename": root_rev_zip.name,
                "path": str(root_rev_zip),
                "size_mb": round(root_rev_size_mb, 2),
                "file_count": rev_files,
                "sha256": root_rev_sha,
                "verification_status": "PASS" if not rev_issues else "FAIL"
            }
        }
    }
    
    with open(OUTPUT_DIR / "archive_checksums.json", "w", encoding="utf-8") as f:
        json.dump(pkg_manifest, f, indent=2)
    print(f"\nWrote checksums manifest to {OUTPUT_DIR / 'archive_checksums.json'}")

    # Write standard .sha256 files
    sha256_lines = [
        f"{sub_sha}  {sub_zip.name}\n",
        f"{rev_sha}  {rev_zip.name}\n",
        f"{root_rev_sha}  {root_rev_zip.name}\n"
    ]
    with open(OUTPUT_DIR / "checksums.sha256", "w", encoding="utf-8") as f:
        f.writelines(sha256_lines)
    print(f"Wrote SHA-256 manifest to {OUTPUT_DIR / 'checksums.sha256'}")

    with open(PROJECT_ROOT / "checksums.sha256", "w", encoding="utf-8") as f:
        f.writelines(sha256_lines)
    print(f"Wrote SHA-256 manifest to {PROJECT_ROOT / 'checksums.sha256'}")

if __name__ == "__main__":
    package_all()
