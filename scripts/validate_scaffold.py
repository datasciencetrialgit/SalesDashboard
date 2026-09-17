#!/usr/bin/env python3
"""Validate this reusable scaffold and its project-scoped skills."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = {
    "powerbi-orchestrator", "powerbi-requirements-planning", "powerbi-project-setup",
    "powerbi-data-connectivity", "powerbi-semantic-model", "powerbi-dax",
    "powerbi-report-design", "powerbi-pbir-authoring", "powerbi-security-governance",
    "powerbi-performance", "powerbi-testing-validation", "powerbi-deployment-devops",
}
EXPECTED_AGENTS = EXPECTED_SKILLS


def main() -> int:
    errors: list[str] = []
    required_files = [
        "README.md", "AGENTS.md", "config/powerbi-project.template.json",
        "config/powerbi-project.schema.json", "docs/LIFECYCLE.md", "docs/TOPOLOGIES.md",
        "scripts/new_project.py", "scripts/validate_manifest.py", "scripts/validate_project.py",
        ".github/copilot-instructions.md",
    ]
    for relative in required_files:
        if not (ROOT / relative).is_file():
            errors.append(f"Missing {relative}")

    skills_root = ROOT / ".agents" / "skills"
    actual = {path.name for path in skills_root.iterdir() if path.is_dir()}
    if EXPECTED_SKILLS - actual:
        errors.append(f"Missing skills: {', '.join(sorted(EXPECTED_SKILLS - actual))}")
    for name in sorted(EXPECTED_SKILLS):
        skill = skills_root / name / "SKILL.md"
        metadata = skills_root / name / "agents" / "openai.yaml"
        if not skill.is_file() or f"name: {name}" not in skill.read_text(encoding="utf-8"):
            errors.append(f"Invalid skill: {name}")
        elif "TODO" in skill.read_text(encoding="utf-8"):
            errors.append(f"Unfinished TODO in {name}")
        if not metadata.is_file() or f"${name}" not in metadata.read_text(encoding="utf-8"):
            errors.append(f"Invalid skill metadata: {name}")

    agents_root = ROOT / ".github" / "agents"
    actual_agents = {
        path.name.removesuffix(".agent.md")
        for path in agents_root.glob("*.agent.md")
    }
    if EXPECTED_AGENTS - actual_agents:
        errors.append(f"Missing custom agents: {', '.join(sorted(EXPECTED_AGENTS - actual_agents))}")
    for name in sorted(EXPECTED_AGENTS):
        agent = agents_root / f"{name}.agent.md"
        text = agent.read_text(encoding="utf-8") if agent.is_file() else ""
        if not text.startswith("---\n") or f".agents/skills/{name}/SKILL.md" not in text:
            errors.append(f"Invalid custom agent: {name}")

    for path in list((ROOT / "config").glob("*.json")) + list((ROOT / "examples").glob("*.json")) + list((ROOT / "templates").glob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}")

    if errors:
        print("Scaffold validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Scaffold validation PASSED")
    print(f"- {len(EXPECTED_SKILLS)} reusable Power BI skills")
    print(f"- {len(EXPECTED_AGENTS)} Power BI custom agents")
    print("- generic manifest, topology guidance, templates, and examples")
    return 0


if __name__ == "__main__":
    sys.exit(main())
