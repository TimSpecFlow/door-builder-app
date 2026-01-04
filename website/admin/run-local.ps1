param(
  [switch]$StartWrangler
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$siteRoot = Resolve-Path (Join-Path $scriptDir "..")
$port = 8001

Write-Host "Serving site from: $siteRoot"
Write-Host "Admin UI will be available at http://127.0.0.1:$port/admin/"

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
  Write-Warning "Python not found in PATH. Install Python or serve files with another static server."
} else {
  Write-Host "Starting Python static server on port $port..."
  Start-Process -FilePath $python.Path -ArgumentList "-m","http.server","$port","--directory",$siteRoot
  Start-Sleep -Milliseconds 300
  Start-Process "http://127.0.0.1:$port/admin/"
}

if ($StartWrangler) {
  $wrangler = Get-Command wrangler -ErrorAction SilentlyContinue
  if (-not $wrangler) {
    Write-Warning "wrangler not found. Install it with: npm install -g wrangler"
  } else {
    $workerDir = Resolve-Path (Join-Path $scriptDir "..\worker\admin")
    Write-Host "Starting 'wrangler dev' for admin worker in: $workerDir"
    Start-Process -FilePath $wrangler.Path -ArgumentList "dev" -WorkingDirectory $workerDir
  }
}

Write-Host "Run 'Stop-Process -Name python' or close the server process windows to stop the servers." 
