---
name: powerbi-deployment-devops
description: Configure source control, CI checks, environment parameterization, Fabric/Power BI deployment, promotion, ownership, refresh, release evidence, and rollback. Use after artifacts pass development validation.
---

# Power BI Deployment and DevOps

Use the manifest environment list and deployment strategy.

## Workflow

1. Keep authoring files in source control and local caches, secrets, and environment state out of it.
2. Run manifest, structural, schema, test, security, and policy checks before packaging or deployment.
3. Parameterize connections, workspace references, gateway mappings, and environment settings without committing credentials.
4. Choose supported promotion tooling: Fabric Git integration, deployment pipelines, REST APIs, or Desktop publish, according to the project contract.
5. Validate permissions, ownership, refresh schedules, credentials, app audiences, subscriptions, endorsements, and labels after deployment.
6. Smoke-test critical reports and model queries in the target environment.
7. Record artifact versions, approvers, changes, verification, and rollback steps.

Do not deploy from an uncommitted or unvalidated state. Require explicit authorization before mutating shared or production workspaces.
