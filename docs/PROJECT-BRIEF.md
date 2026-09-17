# Project Brief

## Business outcome

Provide an executive view of sales revenue, gross profit, margin, order volume, regional performance, category mix, monthly movement, and recent transactions.

## Audience and decisions

The sample is designed for a sales or finance leader deciding where revenue and profit are changing, which regions and categories contribute most, and which recent orders require inspection.

## Scope

- Local sample CSV only
- One imported Sales table
- Six explicit measures
- One desktop report page
- No RLS, OLS, service deployment, incremental refresh, or gateway

## Source contract

`data/sales.csv` contains OrderDate, OrderID, Region, Salesperson, Category, Product, Units, Revenue, and Cost. The M expression uses the actual absolute file location and must be rebound after the project is moved.

## Acceptance criteria

- Enhanced PBIR structure loads without the `visualContainers` parsing failure.
- Model refresh succeeds.
- Measures reconcile to the CSV.
- The page is 1280 × 720 with FitToPage.
- Theme, four KPI cards, three charts, and the recent-orders table render correctly.
- Save, close, and reopen succeeds in Power BI Desktop.
