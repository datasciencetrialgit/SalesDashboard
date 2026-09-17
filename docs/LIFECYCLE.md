# Power BI Development Lifecycle

The orchestrator advances through these phases. A project may skip a phase only when its manifest makes that phase irrelevant.

| Phase | Outcome | Primary skill | Exit evidence |
| --- | --- | --- | --- |
| 0. Discover | Business questions, users, decisions, constraints | requirements-planning | Approved brief and manifest |
| 1. Architect | Artifact topology, storage mode, source and environment choices | project-setup | Architecture decision record |
| 2. Connect | Source queries, parameters, privacy, credentials and gateway plan | data-connectivity | Source refresh/query evidence |
| 3. Model | Tables, relationships, metadata, calculation groups | semantic-model | Model validation |
| 4. Calculate | Measures, formats, test cases | dax | Reconciled measure tests |
| 5. Design | Page purpose, layout, theme, accessibility, interactions | report-design | Reviewed report plan |
| 6. Author | PBIR pages, visuals, filters, bookmarks and resources | pbir-authoring | Static PBIR validation |
| 7. Secure | RLS/OLS, privacy, labels and governance | security-governance | Security test matrix |
| 8. Optimize | Model, query, refresh, DAX and render performance | performance | Performance baseline |
| 9. Validate | Functional, visual, accessibility and round-trip QA | testing-validation | Signed QA results |
| 10. Release | CI/CD, parameterization, promotion and rollback | deployment-devops | Release record |

## Gate principle

Do not author downstream artifacts against an unstable upstream contract. Changes to grain, keys, storage mode, security rules, or deployment topology require re-evaluating affected later phases.
