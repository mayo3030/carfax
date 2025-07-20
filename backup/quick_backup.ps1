# Quick Backup Script - From backup folder
# Usage: .\quick_backup.ps1

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupName = "backup_$timestamp"
$currentDir = Get-Location
$parentDir = Split-Path $currentDir -Parent
$backupPath = Join-Path $parentDir $backupName

Write-Host "Creating CARFAX Project Backup..." -ForegroundColor Green
Write-Host "Source: $parentDir" -ForegroundColor Yellow
Write-Host "Backup: $backupPath" -ForegroundColor Yellow
Write-Host "Timestamp: $timestamp" -ForegroundColor Cyan

# Check if we're in the backup directory
if (!(Test-Path "backup_script.py")) {
    Write-Host "Error: Please run this script from the backup folder" -ForegroundColor Red
    exit 1
}

# Create backup using robocopy
robocopy $parentDir $backupPath /E /R:3 /W:1 /MT:4 /NP /NDL /XD "__pycache__" ".git" "node_modules" ".venv" "venv" "env" "backup"

if ($LASTEXITCODE -le 7) {
    Write-Host "Backup created successfully!" -ForegroundColor Green
    Write-Host "Backup location: $backupPath" -ForegroundColor Cyan
    
    # Calculate backup size
    $backupSize = (Get-ChildItem -Path $backupPath -Recurse -File | Measure-Object -Property Length -Sum).Sum
    $fileCount = (Get-ChildItem -Path $backupPath -Recurse -File).Count
    $sizeMB = [math]::Round($backupSize / 1MB, 2)
    
    Write-Host "Backup size: $sizeMB MB" -ForegroundColor Yellow
    Write-Host "Files backed up: $fileCount" -ForegroundColor Yellow
    Write-Host "Backup completed successfully!" -ForegroundColor Green
} else {
    Write-Host "Backup failed with exit code: $LASTEXITCODE" -ForegroundColor Red
} 