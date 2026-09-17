---
name: powerbi-project-setup
description: Initialize or inspect a topology-aware PBIP workspace for local models, model-only projects, thin reports, shared models, or multiple reports. Use for folder structure, artifact references, and format selection.
---

# Power BI Project Setup

Read `docs/TOPOLOGIES.md` and validate `powerbi-project.json` first.

## Workflow

1. Confirm local, remote, or absent semantic model and the report list.
2. Run `scripts/new_project.py` only for a new empty workspace; never overwrite an existing project.
3. For existing projects, inventory `.pbip`, `.Report`, `.SemanticModel`, PBIR/TMDL formats, IDs, lineage tags, and unsupported metadata before editing.
4. Create Power BI metadata only from current schemas or a Desktop-generated baseline. The generator intentionally creates directories, not fabricated definitions.
5. Configure each report's local `byPath` or remote `byConnection` reference consistently with the manifest.
6. Run structure validation, then hand source work to `$powerbi-data-connectivity`.

Keep PBIR and PBIR-Legacy mutually exclusive within each report. Keep TMDL and TMSL mutually exclusive within each semantic model.
