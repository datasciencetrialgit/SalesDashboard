#!/usr/bin/env python3
"""Create a safe folder scaffold from a validated Power BI project manifest."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from validate_manifest import load_manifest, validate


ROOT = Path(__file__).resolve().parents[1]


def copy_template(name: str, destination: Path) -> None:
    shutil.copyfile(ROOT / "templates" / name, destination)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    manifest = load_manifest(args.manifest.resolve())
    errors = validate(manifest)
    if errors:
        print("Project generation blocked by manifest errors:")
        for error in errors:
            print(f"- {error}")
        return 1

    project_name = manifest["project"]["name"]
    target = args.output.resolve() / project_name
    if target.exists() and any(target.iterdir()):
        print(f"Refusing to overwrite non-empty directory: {target}")
        return 1

    target.mkdir(parents=True, exist_ok=True)
    (target / "docs").mkdir()
    (target / "tests").mkdir()
    (target / "data").mkdir()
    (target / "tests" / ".gitkeep").write_text("", encoding="utf-8")
    (target / "data" / ".gitkeep").write_text("", encoding="utf-8")
    (target / ".gitignore").write_text((ROOT / ".gitignore").read_text(encoding="utf-8"), encoding="utf-8")
    (target / "powerbi-project.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    copy_template("PROJECT-BRIEF.md", target / "docs" / "PROJECT-BRIEF.md")
    copy_template("ARCHITECTURE-DECISIONS.md", target / "docs" / "ARCHITECTURE-DECISIONS.md")
    copy_template("QA-RESULTS.md", target / "docs" / "QA-RESULTS.md")

    semantic = manifest["artifacts"]["semanticModel"]
    if semantic["kind"] == "local":
        model_dir = target / f"{project_name}.SemanticModel"
        model_dir.mkdir()
        (model_dir / ".gitkeep").write_text("", encoding="utf-8")

    for report in manifest["artifacts"]["reports"]:
        report_dir = target / f"{report['name']}.Report"
        report_dir.mkdir()
        (report_dir / ".gitkeep").write_text("", encoding="utf-8")

    readme = f"""# {manifest['project']['displayName']}

{manifest['project']['description']}

This folder was generated from `powerbi-project.json`. Power BI metadata files are intentionally not fabricated by the generator. Use `$powerbi-orchestrator` to author each valid layer and validate it before continuing.
"""
    (target / "README.md").write_text(readme, encoding="utf-8")
    print(f"Created project scaffold: {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
