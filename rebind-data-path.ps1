$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$CsvPath = (Join-Path $ProjectRoot "data\sales.csv").Replace("\", "/")
$TmdlPath = Join-Path $ProjectRoot "SalesDashboard.SemanticModel\definition\tables\Sales.tmdl"
$ManifestPath = Join-Path $ProjectRoot "powerbi-project.json"

$content = Get-Content -Raw -LiteralPath $TmdlPath
$pattern = 'File\.Contents\("[^"]*sales\.csv"\)'
if (-not [regex]::IsMatch($content, $pattern)) { throw "Could not find the sales.csv File.Contents path in Sales.tmdl" }
$replacement = 'File.Contents("' + $CsvPath + '")'
$updated = [regex]::Replace($content, $pattern, $replacement)
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($TmdlPath, $updated, $utf8NoBom)

$manifest = Get-Content -Raw -LiteralPath $ManifestPath | ConvertFrom-Json
$manifest.connections[0].location = $CsvPath
$manifest.deployment.environments[0].parameters.SalesCsvPath = $CsvPath
$manifestJson = $manifest | ConvertTo-Json -Depth 20
[System.IO.File]::WriteAllText($ManifestPath, $manifestJson + "`n", $utf8NoBom)

Write-Host "Updated CSV path to: $CsvPath"
Write-Host "Run: python .\scripts\validate_salesdashboard.py"
Write-Host "Then open SalesDashboard.pbip in Power BI Desktop."
