#!/usr/bin/env python3
"""Validate the generic Power BI project manifest using only the Python standard library."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{1,63}$")
REQUIRED_TOP_LEVEL = {
    "schemaVersion", "project", "artifacts", "connections", "model",
    "report", "security", "deployment", "quality",
}
STORAGE_MODES = {"Import", "DirectQuery", "DirectLake", "Composite", "LiveConnection", "none"}


def load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(manifest: dict[str, Any], allow_placeholders: bool = False) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_TOP_LEVEL - manifest.keys()
    if missing:
        errors.append(f"Missing top-level keys: {', '.join(sorted(missing))}")

    if manifest.get("schemaVersion") != "1.0":
        errors.append("schemaVersion must be 1.0")

    project = manifest.get("project", {})
    name = project.get("name", "")
    if not isinstance(name, str) or not NAME_RE.fullmatch(name):
        errors.append("project.name must start with a letter and use only letters, digits, _ or -")
    for field in ("displayName", "description"):
        if not isinstance(project.get(field), str) or not project.get(field, "").strip():
            errors.append(f"project.{field} must be a non-empty string")

    if not allow_placeholders:
        serialized = json.dumps(manifest).lower()
        for marker in ("replaceme", "replace-me"):
            if marker in serialized:
                errors.append(f"Manifest still contains template marker: {marker}")

    artifacts = manifest.get("artifacts", {})
    semantic = artifacts.get("semanticModel", {})
    kind = semantic.get("kind")
    model_format = semantic.get("format")
    storage_mode = semantic.get("storageMode")
    if kind not in {"local", "remote", "none"}:
        errors.append("semanticModel.kind must be local, remote, or none")
    if storage_mode not in STORAGE_MODES:
        errors.append(f"Unsupported semanticModel.storageMode: {storage_mode}")
    if kind == "local":
        if model_format not in {"TMDL", "TMSL"}:
            errors.append("A local semantic model requires TMDL or TMSL format")
        if storage_mode in {"LiveConnection", "none"}:
            errors.append("A local semantic model cannot use LiveConnection or none storage mode")
    if kind == "remote":
        if model_format != "none" or storage_mode != "LiveConnection":
            errors.append("A remote semantic model requires format none and LiveConnection")
        if not semantic.get("remoteConnection") and not allow_placeholders:
            errors.append("A remote semantic model requires remoteConnection metadata")
    if kind == "none" and model_format != "none":
        errors.append("semanticModel.kind none requires format none")

    reports = artifacts.get("reports", [])
    if not isinstance(reports, list):
        errors.append("artifacts.reports must be an array")
        reports = []
    report_names: set[str] = set()
    for index, report in enumerate(reports):
        report_name = report.get("name", "")
        if not NAME_RE.fullmatch(report_name):
            errors.append(f"reports[{index}].name is invalid")
        if report_name in report_names:
            errors.append(f"Duplicate report name: {report_name}")
        report_names.add(report_name)
        if report.get("format") not in {"PBIR", "PBIR-Legacy"}:
            errors.append(f"reports[{index}].format must be PBIR or PBIR-Legacy")
        reference = report.get("semanticModel")
        if reference == "local" and kind != "local":
            errors.append(f"Report {report_name} references a local model that is not configured")
        if reference == "remote" and kind != "remote":
            errors.append(f"Report {report_name} references a remote model that is not configured")

    connections = manifest.get("connections", [])
    if not isinstance(connections, list):
        errors.append("connections must be an array")
    else:
        names: set[str] = set()
        for index, connection in enumerate(connections):
            connection_name = connection.get("name")
            if not connection_name:
                errors.append(f"connections[{index}].name is required")
            elif connection_name in names:
                errors.append(f"Duplicate connection name: {connection_name}")
            names.add(connection_name)
            forbidden = {key.lower() for key in connection} & {"password", "token", "secret", "clientsecret", "accesstoken"}
            if forbidden:
                errors.append(f"Connection {connection_name} contains forbidden secret fields: {', '.join(sorted(forbidden))}")

    quality = manifest.get("quality", {})
    for field in ("maxVisualsPerPage", "targetVisualRenderMs"):
        value = quality.get(field)
        if not isinstance(value, int) or value <= 0:
            errors.append(f"quality.{field} must be a positive integer")

    environments = manifest.get("deployment", {}).get("environments", [])
    environment_names = [item.get("name") for item in environments]
    if len(environment_names) != len(set(environment_names)):
        errors.append("Deployment environment names must be unique")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--allow-template-placeholders", action="store_true")
    args = parser.parse_args()
    try:
        manifest = load_manifest(args.manifest)
    except Exception as exc:  # noqa: BLE001
        print(f"Manifest validation FAILED\n- {exc}")
        return 1

    errors = validate(manifest, args.allow_template_placeholders)
    if errors:
        print("Manifest validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Manifest validation PASSED")
    print(f"- project: {manifest['project']['name']}")
    print(f"- reports: {len(manifest['artifacts']['reports'])}")
    print(f"- model topology: {manifest['artifacts']['semanticModel']['kind']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
