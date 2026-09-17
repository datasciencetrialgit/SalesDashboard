# Project Topologies

## Local model and report

Use `semanticModel.kind = local`. Generate `<name>.SemanticModel` plus one or more `<report>.Report` folders. Each local report uses `datasetReference.byPath`.

## Semantic-model-only

Use a local model and an empty `reports` array. Build and deploy the TMDL model without a PBIR report.

## Thin report

Use `semanticModel.kind = remote`, `storageMode = LiveConnection`, and provide `remoteConnection`. Report `semanticModel` values should be `remote`. Do not generate a local model folder.

## Multiple reports, shared model

Define several report entries and one local or remote semantic model. Keep report-specific measures only when a live-connection design explicitly requires them.

## Composite model

Use `storageMode = Composite`. Document storage mode per table, source-group boundaries, relationship behavior, and security propagation before authoring.

## Direct Lake

Use `storageMode = DirectLake`. Confirm Fabric capacity, supported source artifacts, fallback behavior, security semantics, and deployment constraints before implementation.

## Existing project or migration

Point the work at an existing PBIP root. Inventory current artifacts before mutation. Preserve stable IDs, lineage tags, unsupported metadata, and user changes. Treat SSAS/AAS, Tableau, or legacy PBIX conversion as a migration stream with explicit parity tests.

## Extensions

Use the manifest `extensions` array for work outside standard PBIP authoring, such as `paginated-report`, `embedded`, `custom-visual`, `streaming`, `fabric-notebook`, or `deployment-pipeline`. Each extension needs its own tools and acceptance criteria.
