# Architecture Decisions

| ID | Decision | Rationale | Consequence |
| --- | --- | --- | --- |
| ADR-001 | Local semantic model using TMDL | Keeps model metadata source-control friendly | Requires supported Power BI Desktop version |
| ADR-002 | Import mode from local CSV | Matches sample scope and provides fast visuals | Absolute CSV path must be rebound after moving the project |
| ADR-003 | Single Sales table | Required by the sample specification | No relationships or separate date table |
| ADR-004 | Hidden-in-practice Month Start calculated column | Provides chronological monthly grouping without adding a second table | The model has one derived column beyond the CSV schema |
| ADR-005 | Enhanced PBIR | Enables page- and visual-level source control | Exact schemas and definition version must remain valid |
| ADR-006 | PBIR definition version 2.0.0 | Prevents the known stale-version parsing failure | Release validation blocks 1.0.0 |
| ADR-007 | Bare theme resource filename | Matches registered-resource conventions | Folder-prefixed resource paths are rejected |
| ADR-008 | No row-level security | Sample data contains no restricted identities | Security testing is not applicable |
