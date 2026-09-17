---
name: Power BI Data Connectivity
description: Build and validate Power Query, source, parameter, and refresh behavior.
argument-hint: Describe the source or refresh change
user-invocable: true
---

Read [the data connectivity skill](../../.agents/skills/powerbi-data-connectivity/SKILL.md) and the connection contract in `powerbi-project.json`. Implement source access, explicit types, storage mode, parameters, privacy, and gateway assumptions without committing credentials. For the local CSV, run `python rebind-data-path.py` so TMDL contains the actual absolute path.
