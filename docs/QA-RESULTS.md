# QA Results

- Project: SalesDashboard
- Build date: 2026-09-17
- Power BI Desktop version: Pending user environment
- Static project validation: Passed
- JSON parse validation: Passed
- CSV schema and type validation: Passed
- Measure reconciliation: Passed against 72 sample rows
- PBIR version guard: Passed (`2.0.0`)
- Theme path guard: Passed (bare filename)
- Page geometry: Passed (1280 × 720, FitToPage)
- Visual inventory: Passed (4 cards, 3 charts, 1 table, 1 title)
- Project skills: Passed (`quick_validate.py` for all 12 skills)
- Custom agents: Passed (12 matching `.github/agents/*.agent.md` files)
- Self-contained scaffold: Passed (`scripts/validate_scaffold.py`)
- Automated unit tests: Passed (10 tests)
- Accessibility structure: Unique tab order passed; final visual inspection pending
- Power BI Desktop open: Pending
- Model refresh: Pending
- Save: Pending
- Close/reopen: Pending

## Reconciled source values

| Metric | Expected value |
| --- | ---: |
| Total Revenue | $72,204.48 |
| Gross Profit | $40,758.48 |
| Gross Margin % | 56.4% |
| Units Sold | 258 |
| Orders | 72 |
| Average Order Value | $1,002.84 |

## Remaining release gate

Run the path-rebinding script on the Windows machine that will open the project, then complete the Desktop open, refresh, visual inspection, save, close, and reopen sequence.

## Known issue fixed (2026-09-17)

Desktop open previously failed with `Table 'LocalDateTable_*' with ShowAsVariationsOnly property set to '1' must be a target of a variation when variation notation is enabled.` Root cause: `Sales.OrderDate` and `Sales.'Month Start'` were missing `variation` blocks that should have pointed at the auto-generated `LocalDateTable_*` tables.

Rather than restoring the variation links, the auto date/time tables were removed entirely for a clean, dependency-free template:
- Deleted `LocalDateTable_a0b9b1c5-9a8c-4820-8fb2-720fc250920f.tmdl` and `LocalDateTable_180d6482-b86f-42fb-8a58-1696a3c9b7b0.tmdl`.
- Removed the two relationships in `relationships.tmdl` that targeted them.
- Removed the `variation` blocks from `Sales.OrderDate` and `Sales.'Month Start'` in `Sales.tmdl`.
- Added `annotation __PBI_TimeIntelligenceEnabled = 0` to `model.tmdl` so Power BI Desktop does not regenerate auto date/time tables for date columns going forward.
- Deleted `DateTableTemplate_b1259bd2-1a11-4bd1-ab13-d349968e09e6.tmdl`, the hidden `__PBI_TemplateDateTable` singleton Power BI uses to spin up new auto date/time tables — no longer needed with the feature disabled.

Static validation and unit tests pass. Desktop open/refresh/save/reopen evidence is still required.
