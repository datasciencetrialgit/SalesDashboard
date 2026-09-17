---
name: powerbi-security-governance
description: Design, implement, and verify Power BI security and governance, including RLS, dynamic RLS, OLS, privacy, labels, endorsements, access boundaries, and audit evidence. Use when data visibility or governance matters.
---

# Power BI Security and Governance

Derive security from approved personas, data classifications, and workspace responsibilities.

## Workflow

1. Separate source, model, report, workspace, app, sharing, and tenant controls.
2. Implement RLS/OLS only from explicit rules; document identity mapping and fallback behavior.
3. Test each role with allowed, denied, overlapping, missing, and malformed identity cases.
4. Review relationship propagation, bridge tables, DirectQuery/SSO behavior, Build permission, export, Analyze in Excel, and downstream reuse.
5. Record sensitivity labels, endorsement targets, data owners, retention, audit, and exception processes.
6. Keep principals and environment assignments parameterized or managed outside committed metadata where appropriate.

Never weaken security to make a visual work. Stop for clarification when a role definition or legal/compliance requirement is ambiguous.
