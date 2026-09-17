# PBIR Guardrails

- `definition.pbir` is the report pointer and compatibility envelope. Enhanced PBIR requires a version that supports the `definition/` folder; current projects normally use `4.0` or higher.
- `definition/version.json` versions the enhanced report definition itself. Preserve the value emitted by the supported Desktop/schema version. If a project contract fixes it to `2.0.0`, enforce that exact value.
- Do not mix enhanced PBIR `definition/` files with a PBIR-Legacy root `report.json` representation.
- `datasetReference.byPath.path` is relative and uses `/` separators.
- Resource files live under `StaticResources/RegisteredResources`. Resource-package paths in report JSON are bare filenames unless the current schema explicitly states otherwise.
- Page and visual folder names must be unique and stable.
- Validate each layer before adding the next: report shell, resources, page shell, then visual groups.
- When exact visual JSON is uncertain, use a current Desktop-generated example and the matching official schema. Do not invent property shapes.
