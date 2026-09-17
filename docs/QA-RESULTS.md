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
