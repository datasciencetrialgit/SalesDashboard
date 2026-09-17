# Generic Power BI Project Instructions

This file applies directly to the bundled `SalesDashboard` project. Project-local skills live under `.agents/skills/`, and VS Code/GitHub Copilot custom agents live under `.github/agents/`.

Read `powerbi-project.json` when present; otherwise start from `config/powerbi-project.template.json`. The manifest is the project contract. Do not infer domain tables, measures, pages, visuals, security roles, environments, or branding that the manifest does not define.

## Routing

- End-to-end, status, or “continue” requests: `$powerbi-orchestrator`
- Requirements and architecture: `$powerbi-requirements-planning`
- PBIP topology and file initialization: `$powerbi-project-setup`
- Sources, Power Query, gateway, parameters, or storage mode: `$powerbi-data-connectivity`
- TMDL model objects: `$powerbi-semantic-model`
- Measures or calculation logic: `$powerbi-dax`
- UX, theme, layout, accessibility, mobile: `$powerbi-report-design`
- PBIR report/page/visual JSON: `$powerbi-pbir-authoring`
- RLS, OLS, labels, privacy, governance: `$powerbi-security-governance`
- Performance investigations: `$powerbi-performance`
- Test and release evidence: `$powerbi-testing-validation`
- CI/CD and environment promotion: `$powerbi-deployment-devops`

## Global rules

1. Confirm the selected topology before creating Power BI artifact files.
2. For enhanced PBIR, distinguish `definition.pbir` compatibility version from `definition/version.json` definition-folder version.
3. Do not place secrets, tokens, passwords, tenant IDs, or user-specific credentials in committed files.
4. Local file sources must follow the manifest's portability policy; when an absolute M path is required, resolve the actual saved path.
5. Validate incrementally: model shell, report shell, theme/resources, pages, visual groups, then full round trip.
6. Do not claim Desktop compatibility without open, refresh, save, close, and reopen evidence.
