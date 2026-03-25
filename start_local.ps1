# Start Personal AI Employee - BRONZE TIER (Hackathon 0 Compliant)
# Simple local automation: Filesystem watcher + Claude orchestrator
# 
# Bronze Tier Flow:
#   1. User drops file → obsidian_vault/Inbox/
#   2. Watcher moves it → obsidian_vault/Needs_Action/
#   3. Orchestrator processes → obsidian_vault/Plans/
#   4. Original moved → obsidian_vault/Done/

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Personal AI Employee - BRONZE TIER" -ForegroundColor Cyan
Write-Host "  Hackathon 0 Compliant" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$ProjectDir = $PWD.Path
Set-Location $ProjectDir

# Pre-flight checks
Write-Host "Running pre-flight checks..." -ForegroundColor Yellow
Write-Host ""

# Check .env
if (!(Test-Path ".env")) {
    Write-Host "[✗] .env file missing!" -ForegroundColor Red
    Write-Host "    Create .env with: ANTHROPIC_API_KEY=your_key_here" -ForegroundColor Yellow
    exit 1
}
Write-Host "[✓] .env file found" -ForegroundColor Green

# Check vault
if (!(Test-Path "obsidian_vault")) {
    Write-Host "[✗] Vault directory missing!" -ForegroundColor Red
    exit 1
}
Write-Host "[✓] Vault directory found" -ForegroundColor Green

# Ensure required vault folders exist (Bronze Tier: Inbox, Needs_Action, Plans, Done)
$requiredFolders = @(
    "obsidian_vault\Inbox",
    "obsidian_vault\Needs_Action",
    "obsidian_vault\Plans",
    "obsidian_vault\Done",
    "obsidian_vault\agent_skills",
    "logs"
)

foreach ($folder in $requiredFolders) {
    if (!(Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder -Force | Out-Null
        Write-Host "[✓] Created $folder" -ForegroundColor Green
    } else {
        Write-Host "[✓] $folder exists" -ForegroundColor Green
    }
}

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[✓] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[✗] Python not found!" -ForegroundColor Red
    exit 1
}

# Check required Python packages
Write-Host ""
Write-Host "Checking Python dependencies..." -ForegroundColor Yellow
$requiredPackages = @("anthropic", "watchdog", "python-dotenv")
$missingPackages = @()

foreach ($package in $requiredPackages) {
    python -c "import $($package.Replace('-', '_'))" 2>$null
    if ($LASTEXITCODE -ne 0) {
        $missingPackages += $package
    }
}

if ($missingPackages.Count -gt 0) {
    Write-Host "[!] Missing packages: $($missingPackages -join ', ')" -ForegroundColor Yellow
    Write-Host "    Installing..." -ForegroundColor Yellow
    pip install $($missingPackages -join ' ') | Out-Null
    Write-Host "[✓] Packages installed" -ForegroundColor Green
} else {
    Write-Host "[✓] All required packages installed" -ForegroundColor Green
}

# Check orchestrator script
if (!(Test-Path "orchestrator_claude.py")) {
    Write-Host "[✗] orchestrator_claude.py missing!" -ForegroundColor Red
    exit 1
}
$orchestratorScript = "orchestrator_claude.py"
Write-Host "[✓] Orchestrator script found" -ForegroundColor Green

# Check watcher script
if (!(Test-Path "watcher_filesystem.py")) {
    Write-Host "[✗] watcher_filesystem.py missing!" -ForegroundColor Red
    exit 1
}
$watcherScript = "watcher_filesystem.py"
Write-Host "[✓] Watcher script found" -ForegroundColor Green

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

# Start filesystem watcher in separate background window
Write-Host "Starting filesystem watcher in new window..." -ForegroundColor Yellow
$watcherProcess = Start-Process powershell -ArgumentList "-NoExit","-Command","python $watcherScript" -WindowStyle Normal -PassThru
Write-Host "[✓] Filesystem watcher started (PID: $($watcherProcess.Id))" -ForegroundColor Green

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "Starting orchestrator in THIS window..." -ForegroundColor Yellow
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "BRONZE TIER - System Status:" -ForegroundColor White
Write-Host "  • Orchestrator: Running (this window)" -ForegroundColor White
Write-Host ""
Write-Host "BRONZE TIER FLOW:" -ForegroundColor Yellow
Write-Host "  1. Drop file → obsidian_vault/Inbox/" -ForegroundColor Green
Write-Host "  2. Watcher moves → Needs_Action/" -ForegroundColor Green
Write-Host "  3. Claude processes → Plans/" -ForegroundColor Green
Write-Host "  4. Original → Done/" -ForegroundColor Green
Write-Host ""
Write-Host "FEATURES:" -ForegroundColor Yellow
Write-Host "  ✓ Local filesystem monitoring" -ForegroundColor Green
Write-Host "  ✓ Claude Sonnet 4.5" -ForegroundColor Green
Write-Host "  ✓ Agent Skills (planning + file analysis)" -ForegroundColor Green
Write-Host "  ✓ Obsidian vault knowledge base" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop orchestrator" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Run orchestrator (blocking - stays in this window)
try {
    python $orchestratorScript
} catch {
    Write-Host ""
    Write-Host "Orchestrator stopped" -ForegroundColor Yellow
} finally {
    # Cleanup on exit
    if ($watcherProcess -and -not $watcherProcess.HasExited) {
        Write-Host ""
        Write-Host "Stopping filesystem watcher..." -ForegroundColor Yellow
        Stop-Process -Id $watcherProcess.Id -Force
        Write-Host "[✓] Filesystem watcher stopped" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "Personal AI Employee (Bronze Tier) stopped" -ForegroundColor Gray
}
