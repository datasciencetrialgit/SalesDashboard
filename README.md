# SalesDashboard PBIP

A sample Power BI Desktop Project using a local CSV, a TMDL semantic model, and enhanced PBIR report metadata.

## Dashboard contents

- One imported `Sales` table sourced from `data/sales.csv`
- Six measures: Total Revenue, Gross Profit, Gross Margin %, Units Sold, Orders, and Average Order Value
- One 1280 × 720 `Executive Overview` page using `FitToPage`
- Four KPI cards, monthly Revenue/Gross Profit combo chart, regional revenue bar chart, category-mix donut, and recent-orders table
- `Signal & Slate.json` theme using warm white, charcoal, coral, teal, gold, slate, and Segoe UI

## Important: bind the CSV path after extraction

Power Query requires an absolute path. The packaged project initially points to its build location. After extracting the ZIP, run one of these commands from the project root:

```powershell
powershell -ExecutionPolicy Bypass -File .\rebind-data-path.ps1
```

or:

```bash
python rebind-data-path.py
```

The script updates both `Sales.tmdl` and `powerbi-project.json` to the extracted location of `data/sales.csv`.

## Validate

```bash
python scripts/validate_salesdashboard.py
python -m unittest discover -s tests -v
```

## Open in Power BI Desktop

1. Enable the Power BI Project and enhanced PBIR preview features if required by your Desktop version.
2. Run the path-rebinding script.
3. Open `SalesDashboard.pbip`.
4. Refresh the model.
5. Verify the Executive Overview page and theme.
6. Save, close Desktop completely, and reopen the PBIP.

## PBIR safeguards

- `definition.pbir` uses version `4.0` and references `../SalesDashboard.SemanticModel`.
- `definition/version.json` uses `2.0.0`, not `1.0.0`.
- The custom theme is stored under `StaticResources/RegisteredResources`.
- The custom-theme name, resource name, and resource path are all `Signal & Slate.json`.
- The resource path is a bare filename.

Static validation passed during packaging. The Windows Power BI Desktop round-trip must be completed after extraction and path rebinding.

## Built-in skills and agents

This repository is self-contained for AI-assisted Power BI development:

- `.agents/skills/` contains 12 portable Agent Skills covering requirements, PBIP setup, data connectivity, semantic modeling, DAX, design, PBIR authoring, security, performance, validation, deployment, and orchestration.
- `.github/agents/` contains matching workspace custom agents for VS Code and GitHub Copilot.
- `AGENTS.md` routes work to the correct skill and defines project-wide safeguards.
- `.github/copilot-instructions.md` applies the SalesDashboard-specific PBIR and CSV-path invariants.
- `config/`, `templates/`, `examples/`, and the generic scripts under `scripts/` provide the reusable scaffold resources referenced by the skills.

Open the extracted `SalesDashboard` folder as the VS Code workspace. Use the **Power BI Orchestrator** custom agent, or start with:

```text
Use $powerbi-orchestrator to inspect this project and execute the next valid phase.
```

To work on one area directly, select its matching custom agent or invoke skills such as `$powerbi-dax`, `$powerbi-pbir-authoring`, or `$powerbi-testing-validation`.
