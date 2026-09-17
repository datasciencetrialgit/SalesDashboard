---
name: powerbi-data-connectivity
description: Design and implement Power BI data connections, Power Query, parameters, privacy levels, gateways, refresh, query folding, and storage-mode boundaries. Use for source and ingestion work.
---

# Power BI Data Connectivity

Use the manifest connection list; do not introduce undeclared production sources.

## Workflow

1. Confirm source capability, authentication location, privacy, gateway, latency, volume, and refresh needs.
2. Choose Import, DirectQuery, Direct Lake, or Composite behavior at the correct model/table boundary.
3. Parameterize environment-specific endpoints. Keep credentials and secret values outside source control.
4. For Power Query, preserve folding when it matters, apply types deliberately, and separate staging from presentation queries when complexity justifies it.
5. For local files, follow `requiresAbsoluteLocalPath`; resolve the actual path rather than using a placeholder.
6. Test source access, folding, refresh, incremental-refresh boundaries, gateway mapping, and failure behavior.
7. Document dependencies and hand stable tables to `$powerbi-semantic-model`.

Do not hide source-system transformations or data-quality assumptions inside undocumented M steps.
