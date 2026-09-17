#!/usr/bin/env python3
"""Project-specific static validation for the SalesDashboard PBIP sample."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "SalesDashboard.Report"
MODEL = ROOT / "SalesDashboard.SemanticModel"
THEME_NAME = "Signal & Slate.json"
REQUIRED_COLUMNS = [
    "OrderDate", "OrderID", "Region", "Salesperson", "Category",
    "Product", "Units", "Revenue", "Cost",
]
REQUIRED_MEASURES = {
    "Total Revenue": "SUM(Sales[Revenue])",
    "Gross Profit": "[Total Revenue] - SUM(Sales[Cost])",
    "Gross Margin %": "DIVIDE([Gross Profit], [Total Revenue])",
    "Units Sold": "SUM(Sales[Units])",
    "Orders": "DISTINCTCOUNT(Sales[OrderID])",
    "Average Order Value": "DIVIDE([Total Revenue], [Orders])",
}
REQUIRED_TABLE_FIELDS = {
    "OrderDate", "OrderID", "Region", "Salesperson", "Category",
    "Product", "Units", "Revenue",
}


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"Missing {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}")
    return {}


def is_absolute_path(value: str) -> bool:
    return value.startswith("/") or bool(re.match(r"^[A-Za-z]:[\\/]", value)) or value.startswith("\\\\")


def projected_properties(visual: dict) -> set[str]:
    properties: set[str] = set()
    query_state = visual.get("visual", {}).get("query", {}).get("queryState", {})
    for role in query_state.values():
        for projection in role.get("projections", []):
            field = projection.get("field", {})
            for field_type in ("Column", "Measure", "HierarchyLevel"):
                prop = field.get(field_type, {}).get("Property")
                if prop:
                    properties.add(prop)
    return properties


def validate_csv(errors: list[str]) -> dict[str, float]:
    csv_path = ROOT / "data" / "sales.csv"
    try:
        with csv_path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != REQUIRED_COLUMNS:
                errors.append(f"sales.csv header must be {REQUIRED_COLUMNS}")
                return {}
            rows = list(reader)
    except OSError as exc:
        errors.append(f"Cannot read data/sales.csv: {exc}")
        return {}

    if not rows:
        errors.append("sales.csv has no data rows")
        return {}

    order_ids: set[str] = set()
    revenue = cost = 0.0
    units = 0
    for line_number, row in enumerate(rows, start=2):
        try:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", row["OrderDate"]):
                raise ValueError("OrderDate must use YYYY-MM-DD")
            if not row["OrderID"]:
                raise ValueError("OrderID is blank")
            units += int(row["Units"])
            revenue += float(row["Revenue"])
            cost += float(row["Cost"])
            order_ids.add(row["OrderID"])
        except (ValueError, TypeError) as exc:
            errors.append(f"Invalid CSV row {line_number}: {exc}")

    orders = len(order_ids)
    gross_profit = revenue - cost
    return {
        "rows": float(len(rows)),
        "revenue": revenue,
        "cost": cost,
        "gross_profit": gross_profit,
        "gross_margin": gross_profit / revenue if revenue else 0.0,
        "units": float(units),
        "orders": float(orders),
        "average_order_value": revenue / orders if orders else 0.0,
    }


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    manifest = load_json(ROOT / "powerbi-project.json", errors)
    pbip = load_json(ROOT / "SalesDashboard.pbip", errors)
    pbir = load_json(REPORT / "definition.pbir", errors)
    pbism = load_json(MODEL / "definition.pbism", errors)
    version = load_json(REPORT / "definition" / "version.json", errors)
    report_json = load_json(REPORT / "definition" / "report.json", errors)
    pages_json = load_json(REPORT / "definition" / "pages" / "pages.json", errors)
    theme = load_json(REPORT / "StaticResources" / "RegisteredResources" / THEME_NAME, errors)

    if manifest.get("project", {}).get("name") != "SalesDashboard":
        errors.append("Manifest project name must be SalesDashboard")
    if pbip.get("artifacts", [{}])[0].get("report", {}).get("path") != "SalesDashboard.Report":
        errors.append("SalesDashboard.pbip must point to SalesDashboard.Report")
    try:
        if float(pbir.get("version", "0")) < 4.0:
            errors.append("definition.pbir version must be 4.0 or higher")
    except ValueError:
        errors.append("definition.pbir version is invalid")
    if pbir.get("datasetReference", {}).get("byPath", {}).get("path") != "../SalesDashboard.SemanticModel":
        errors.append("definition.pbir must reference ../SalesDashboard.SemanticModel")
    try:
        if float(pbism.get("version", "0")) < 4.0:
            errors.append("definition.pbism must be 4.0 or higher for TMDL")
    except ValueError:
        errors.append("definition.pbism version is invalid")
    if version.get("version") != "2.0.0":
        errors.append('definition/version.json must contain version "2.0.0"')

    report_text = json.dumps(report_json, ensure_ascii=False)
    custom_theme = report_json.get("themeCollection", {}).get("customTheme", {})
    if custom_theme.get("name") != THEME_NAME:
        errors.append(f"customTheme.name must be {THEME_NAME}")
    registered_items = []
    for package in report_json.get("resourcePackages", []):
        if package.get("type") == "RegisteredResources":
            registered_items.extend(package.get("items", []))
    theme_items = [item for item in registered_items if item.get("type") == "CustomTheme"]
    if len(theme_items) != 1:
        errors.append("Exactly one CustomTheme resource item is required")
    elif theme_items[0].get("name") != THEME_NAME or theme_items[0].get("path") != THEME_NAME:
        errors.append("Custom theme item name and path must be the bare filename")
    if "StaticResources/RegisteredResources" in report_text or "StaticResources\\RegisteredResources" in report_text:
        errors.append("report.json must not prefix the custom theme resource path")

    expected_colors = ["#F26B5B", "#2A9D8F", "#D4A72C", "#607D8B"]
    if theme.get("background") != "#F6F4EF" or theme.get("foreground") != "#1F2A30":
        errors.append("Theme background or foreground does not match the design contract")
    if theme.get("dataColors", [])[:4] != expected_colors:
        errors.append("Theme accent colors do not match coral, teal, gold, and slate")
    if "Segoe UI" not in json.dumps(theme):
        errors.append("Theme must use Segoe UI")

    page_order = pages_json.get("pageOrder", [])
    if len(page_order) != 1:
        errors.append("Exactly one report page is required")
    page_dir = REPORT / "definition" / "pages" / page_order[0] if len(page_order) == 1 else None
    page = load_json(page_dir / "page.json", errors) if page_dir else {}
    if page.get("displayName") != "Executive Overview":
        errors.append("Page displayName must be Executive Overview")
    if (page.get("width"), page.get("height"), page.get("displayOption")) != (1280, 720, "FitToPage"):
        errors.append("Executive Overview must be 1280x720 with FitToPage")

    visuals: list[dict] = []
    if page_dir:
        for visual_file in sorted((page_dir / "visuals").glob("*/visual.json")):
            visuals.append(load_json(visual_file, errors))
    names = [visual.get("name") for visual in visuals]
    if len(names) != len(set(names)):
        errors.append("Visual names must be unique")
    tab_orders = [visual.get("position", {}).get("tabOrder") for visual in visuals]
    if len(tab_orders) != len(set(tab_orders)):
        errors.append("Visual tabOrder values must be unique")

    types = [visual.get("visual", {}).get("visualType") for visual in visuals]
    expected_type_counts = {
        "textbox": 1,
        "cardVisual": 4,
        "lineClusteredColumnComboChart": 1,
        "barChart": 1,
        "donutChart": 1,
        "tableEx": 1,
    }
    for visual_type, count in expected_type_counts.items():
        if types.count(visual_type) != count:
            errors.append(f"Expected {count} {visual_type} visual(s); found {types.count(visual_type)}")

    cards = [visual for visual in visuals if visual.get("visual", {}).get("visualType") == "cardVisual"]
    card_fields = set().union(*(projected_properties(card) for card in cards)) if cards else set()
    if card_fields != {"Total Revenue", "Gross Profit", "Gross Margin %", "Orders"}:
        errors.append(f"KPI card bindings are incorrect: {sorted(card_fields)}")

    table_visuals = [visual for visual in visuals if visual.get("visual", {}).get("visualType") == "tableEx"]
    if table_visuals and projected_properties(table_visuals[0]) != REQUIRED_TABLE_FIELDS:
        errors.append(f"Recent Orders fields are incorrect: {sorted(projected_properties(table_visuals[0]))}")

    tmdl_path = MODEL / "definition" / "tables" / "Sales.tmdl"
    try:
        tmdl = tmdl_path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        errors.append(f"Cannot read Sales.tmdl: {exc}")
        tmdl = ""
    for column in REQUIRED_COLUMNS:
        if not re.search(rf"(?m)^\s*column\s+'?{re.escape(column)}'?\s*$", tmdl):
            errors.append(f"Missing Sales column: {column}")
    for name, expression in REQUIRED_MEASURES.items():
        quoted = f"measure '{name}' = {expression}"
        unquoted = f"measure {name} = {expression}"
        if quoted not in tmdl and unquoted not in tmdl:
            errors.append(f"Missing or incorrect measure: {name}")
    path_matches = re.findall(r'File\.Contents\("([^"]*sales\.csv)"\)', tmdl)
    if len(path_matches) != 1:
        errors.append(f"Expected one sales.csv File.Contents path; found {len(path_matches)}")
    else:
        source_path = path_matches[0]
        if not is_absolute_path(source_path):
            errors.append("The sales.csv M source path must be absolute")
        elif not Path(source_path).is_file():
            errors.append(f"The configured CSV path does not exist on this machine: {source_path}")
        manifest_path = manifest.get("connections", [{}])[0].get("location")
        if manifest_path != source_path:
            errors.append("Manifest and TMDL CSV paths do not match")

    metrics = validate_csv(errors)
    if metrics and int(metrics["orders"]) != int(metrics["rows"]):
        warnings.append("CSV contains duplicate OrderID values; Orders correctly uses DISTINCTCOUNT")

    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
    if errors:
        print("SalesDashboard validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("SalesDashboard static validation PASSED")
    print(f"- {int(metrics['rows'])} sales rows and {int(metrics['orders'])} distinct orders")
    print(f"- Total Revenue: ${metrics['revenue']:,.2f}")
    print(f"- Gross Profit: ${metrics['gross_profit']:,.2f}")
    print(f"- Gross Margin: {metrics['gross_margin']:.1%}")
    print(f"- Units Sold: {int(metrics['units'])}")
    print(f"- Average Order Value: ${metrics['average_order_value']:,.2f}")
    print("- 1 page, 4 KPI cards, 3 charts, 1 table, and 1 title")
    print("- Desktop open/refresh/save/reopen testing is still required")
    return 0


if __name__ == "__main__":
    sys.exit(main())
