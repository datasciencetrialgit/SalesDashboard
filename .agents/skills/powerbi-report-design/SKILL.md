---
name: powerbi-report-design
description: Plan Power BI report UX, page purpose, layout, chart selection, theme, interactions, drill paths, accessibility, and mobile behavior. Use before or during visual authoring, without fabricating model fields.
---

# Power BI Report Design

Design each page around an audience decision, not around available chart types.

## Workflow

1. Define the page question, audience, action, primary comparison, and required detail.
2. Map only manifest/model fields and measures to visuals.
3. Establish canvas size, grid, hierarchy, whitespace, titles, units, number formats, colors, and interaction rules.
4. Choose charts based on comparison, trend, composition, distribution, relationship, or detail needs.
5. Plan tooltips, drillthrough, bookmarks, navigation, slicers, and mobile layouts only when they improve a defined workflow.
6. Meet contrast, alt-text, tab-order, keyboard, color-independence, and readable-label requirements.
7. Keep visual density within the manifest threshold and document exceptions.

Produce a page plan that `$powerbi-pbir-authoring` can implement. Do not encode visual JSON in the design phase unless the user asks for combined work.
