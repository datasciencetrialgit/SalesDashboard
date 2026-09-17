#!/usr/bin/env python3
"""Rebind the local CSV source after moving or extracting the PBIP project."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CSV_PATH = (ROOT / "data" / "sales.csv").resolve()
TMDL_PATH = ROOT / "SalesDashboard.SemanticModel" / "definition" / "tables" / "Sales.tmdl"
MANIFEST_PATH = ROOT / "powerbi-project.json"

text = TMDL_PATH.read_text(encoding="utf-8-sig")
replacement = f'File.Contents("{CSV_PATH.as_posix()}")'
updated, count = re.subn(r'File\.Contents\("[^"]*sales\.csv"\)', replacement, text)
if count != 1:
    raise SystemExit(f"Expected one sales.csv File.Contents expression; found {count}")
TMDL_PATH.write_text(updated, encoding="utf-8", newline="\n")

manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
manifest["connections"][0]["location"] = CSV_PATH.as_posix()
manifest["deployment"]["environments"][0]["parameters"]["SalesCsvPath"] = CSV_PATH.as_posix()
MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

print(f"Updated CSV path to: {CSV_PATH}")
print("Run: python scripts/validate_salesdashboard.py")
