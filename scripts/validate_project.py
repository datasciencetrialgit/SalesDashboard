#!/usr/bin/env python3
"""Perform topology-aware static validation of a generated Power BI project."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from validate_manifest import load_manifest, validate


SECRET_PATTERNS = [
    re.compile(r"(?i)(password|client[_-]?secret|access[_-]?token)\s*[:=]\s*[^\s,;]+"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"Missing {path}")
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON in {path}: {exc}")
    return {}


def is_absolute_path(value: str) -> bool:
    return value.startswith("/") or bool(re.match(r"^[A-Za-z]:[\\/]", value)) or value.startswith("\\\\")


def scan_for_secrets(root: Path) -> list[str]:
    findings: list[str] = []
    excluded = {".git", ".pbi", "__pycache__"}
    for path in root.rglob("*"):
        if not path.is_file() or excluded.intersection(path.parts):
            continue
        if path.suffix.lower() in {".abf", ".pbix", ".png", ".jpg", ".jpeg", ".gif", ".zip"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                findings.append(str(path.relative_to(root)))
                break
    return findings


def validate_report(report_dir: Path, report: dict, semantic: dict, errors: list[str], warnings: list[str]) -> None:
    definition_pbir = load_json(report_dir / "definition.pbir", errors)
    try:
        if float(str(definition_pbir.get("version", "0"))) < 4.0 and report.get("format") == "PBIR":
            errors.append(f"{report_dir.name}/definition.pbir must support enhanced PBIR")
    except ValueError:
        errors.append(f"{report_dir.name}/definition.pbir version is invalid")

    reference = definition_pbir.get("datasetReference", {})
    if report.get("semanticModel") == "local":
        expected = f"../{semantic['projectName']}.SemanticModel"
        if reference.get("byPath", {}).get("path") != expected:
            errors.append(f"{report_dir.name} must reference {expected}")
    elif report.get("semanticModel") == "remote" and "byConnection" not in reference:
        errors.append(f"{report_dir.name} requires datasetReference.byConnection")

    if report.get("format") == "PBIR":
        definition = report_dir / "definition"
        folder_version = load_json(definition / "version.json", errors)
        if not folder_version.get("version"):
            errors.append(f"{report_dir.name}/definition/version.json requires a version")
        load_json(definition / "report.json", errors)
        load_json(definition / "pages" / "pages.json", errors)
        if (report_dir / "report.json").exists():
            errors.append(f"{report_dir.name} mixes PBIR and PBIR-Legacy report definitions")
    else:
        load_json(report_dir / "report.json", errors)
        if (report_dir / "definition").exists():
            warnings.append(f"{report_dir.name} is PBIR-Legacy but has a definition directory")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--structure-only", action="store_true", help="Validate generated folders before Power BI metadata exists")
    args = parser.parse_args()

    manifest = load_manifest(args.manifest.resolve())
    errors = validate(manifest)
    warnings: list[str] = []
    root = args.root.resolve()
    project_name = manifest.get("project", {}).get("name", "")
    semantic = dict(manifest.get("artifacts", {}).get("semanticModel", {}))
    semantic["projectName"] = project_name

    if not root.is_dir():
        errors.append(f"Project root does not exist: {root}")
    if not (root / "powerbi-project.json").is_file():
        warnings.append("Generated project does not contain its manifest copy")

    if semantic.get("kind") == "local":
        model_dir = root / f"{project_name}.SemanticModel"
        if not model_dir.is_dir():
            errors.append(f"Missing local semantic model folder: {model_dir.name}")
        elif not args.structure_only:
            pbism = load_json(model_dir / "definition.pbism", errors)
            try:
                if float(str(pbism.get("version", "0"))) < 4.0 and semantic.get("format") == "TMDL":
                    errors.append("definition.pbism must be 4.0 or higher for TMDL")
            except ValueError:
                errors.append("definition.pbism version is invalid")
            if semantic.get("format") == "TMDL" and not (model_dir / "definition").is_dir():
                errors.append("TMDL model requires a definition directory")
    elif (root / f"{project_name}.SemanticModel").exists():
        warnings.append("A semantic model folder exists although the manifest does not define a local model")

    for report in manifest.get("artifacts", {}).get("reports", []):
        report_dir = root / f"{report['name']}.Report"
        if not report_dir.is_dir():
            errors.append(f"Missing report folder: {report_dir.name}")
        elif not args.structure_only:
            validate_report(report_dir, report, semantic, errors, warnings)

    if not args.structure_only and manifest.get("artifacts", {}).get("reports"):
        pbip_files = list(root.glob("*.pbip"))
        if not pbip_files:
            warnings.append("No .pbip shortcut exists; reports can still be opened through definition.pbir")
        for pbip in pbip_files:
            load_json(pbip, errors)

    model_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in root.rglob("*.tmdl")
    )
    for connection in manifest.get("connections", []):
        if connection.get("requiresAbsoluteLocalPath"):
            location = str(connection.get("location", ""))
            if not is_absolute_path(location):
                errors.append(f"Connection {connection.get('name')} requires an absolute local path")
            elif not args.structure_only and location not in model_text:
                warnings.append(f"Absolute source path for {connection.get('name')} was not found in TMDL")

    secret_files = scan_for_secrets(root)
    if secret_files:
        errors.append(f"Possible secrets found in: {', '.join(secret_files)}")

    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
    if errors:
        print("Project validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Project validation PASSED")
    if args.structure_only:
        print("- folder topology only; Power BI metadata and Desktop behavior were not tested")
    else:
        print("- static checks only; Desktop open/refresh/save/reopen evidence is still required")
    return 0


if __name__ == "__main__":
    sys.exit(main())
