# SalesDashboard agent instructions

Read [AGENTS.md](../AGENTS.md) and `powerbi-project.json` before changing Power BI artifacts. Use the project skills under `.agents/skills/` and the custom agents under `.github/agents/`.

Preserve these release-blocking invariants:

- `SalesDashboard.Report/definition/version.json` must remain `2.0.0`.
- The theme resource path in report metadata must remain the bare filename `Signal & Slate.json`.
- The CSV source in TMDL must be an absolute path to this checkout's `data/sales.csv`; run `python rebind-data-path.py` after moving or extracting the repository.
- Static validation does not prove Power BI Desktop compatibility. Record open, refresh, save, close, and reopen evidence separately.

Before completing a change, run the applicable validators and update `docs/QA-RESULTS.md` when evidence changes.
