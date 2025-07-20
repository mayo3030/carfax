# CARFAX Project Backup Script
# Creates a backup with date and time

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupName = "backup_$timestamp"
$currentDir = Get-Location
$parentDir = Split-Path $currentDir -Parent
$backupPath = Join-Path $parentDir $backupName

Write-Host "🚀 Creating CARFAX Project Backup..." -ForegroundColor Green
Write-Host "📁 Source: $currentDir" -ForegroundColor Yellow
Write-Host "📁 Backup: $backupPath" -ForegroundColor Yellow
Write-Host "⏰ Timestamp: $timestamp" -ForegroundColor Cyan
Write-Host "=" * 50

# Check if we're in the project directory
$carfaxAppPath = Join-Path $currentDir "carfax-app"
if (!(Test-Path $carfaxAppPath)) {
    Write-Host "❌ Error: Please run this script from the project root directory" -ForegroundColor Red
    Write-Host "   Make sure you're in the folder containing 'carfax-app'" -ForegroundColor Yellow
    exit 1
}

try {
    # Create backup using robocopy
    robocopy $currentDir $backupPath /E /R:3 /W:1 /MT:4 /NP /NDL /XD "__pycache__" ".git" "node_modules" ".venv" "venv" "env"
    
    if ($LASTEXITCODE -le 7) {
        Write-Host "✅ Backup created successfully!" -ForegroundColor Green
        Write-Host "📂 Backup location: $backupPath" -ForegroundColor Cyan
        
        # Calculate backup size
        $backupSize = (Get-ChildItem -Path $backupPath -Recurse -File | Measure-Object -Property Length -Sum).Sum
        $fileCount = (Get-ChildItem -Path $backupPath -Recurse -File).Count
        $sizeMB = [math]::Round($backupSize / 1MB, 2)
        
        Write-Host "📊 Backup size: $sizeMB MB" -ForegroundColor Yellow
        Write-Host "📄 Files backed up: $fileCount" -ForegroundColor Yellow
        
        Write-Host "=" * 50
        Write-Host "🎉 Backup completed successfully!" -ForegroundColor Green
        
        Write-Host ""
        Write-Host "💡 Tips:" -ForegroundColor Cyan
        Write-Host "   - Keep your backups in a safe location" -ForegroundColor White
        Write-Host "   - Consider using cloud storage for important backups" -ForegroundColor White
        Write-Host "   - Regular backups help prevent data loss" -ForegroundColor White
    } else {
        Write-Host "❌ Backup failed with exit code: $LASTEXITCODE" -ForegroundColor Red
    }
    
} catch {
    Write-Host "❌ Error creating backup: $($_.Exception.Message)" -ForegroundColor Red
} 