# CARFAX Project Backup Script (PowerShell)
# Creates a backup of the project with date and time in folder name

param(
    [switch]$Help,
    [string]$Destination = ""
)

function Show-Help {
    Write-Host "🔧 CARFAX Project Backup Tool" -ForegroundColor Cyan
    Write-Host "=" * 30
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\backup.ps1                    # Create backup in parent directory"
    Write-Host "  .\backup.ps1 -Destination C:\Backups  # Create backup in specific location"
    Write-Host "  .\backup.ps1 -Help              # Show this help message"
    Write-Host ""
    Write-Host "Features:" -ForegroundColor Green
    Write-Host "  ✅ Automatic date/time naming"
    Write-Host "  ✅ Excludes unnecessary files (cache, logs, etc.)"
    Write-Host "  ✅ Shows backup size and file count"
    Write-Host "  ✅ Safe and reliable"
    Write-Host ""
}

function Create-Backup {
    param(
        [string]$SourcePath,
        [string]$BackupPath
    )
    
    try {
        # Get current date and time
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $backupFolderName = "backup_$timestamp"
        
        # Create full backup path
        if ($Destination -eq "") {
            $parentDir = Split-Path $SourcePath -Parent
            $fullBackupPath = Join-Path $parentDir $backupFolderName
        } else {
            $fullBackupPath = Join-Path $Destination $backupFolderName
        }
        
        Write-Host "🚀 Creating CARFAX Project Backup..." -ForegroundColor Green
        Write-Host "📁 Source: $SourcePath" -ForegroundColor Yellow
        Write-Host "📁 Backup: $fullBackupPath" -ForegroundColor Yellow
        Write-Host "⏰ Timestamp: $timestamp" -ForegroundColor Cyan
        Write-Host "=" * 50
        
        # Create backup directory if it doesn't exist
        if (!(Test-Path $Destination) -and $Destination -ne "") {
            New-Item -ItemType Directory -Path $Destination -Force | Out-Null
        }
        
        # Copy directory with exclusions
        $excludePatterns = @(
            "__pycache__",
            ".git",
            "*.pyc",
            "*.pyo",
            "*.log",
            "node_modules",
            ".env",
            ".venv",
            "venv",
            "env",
            ".DS_Store",
            "Thumbs.db",
            "*.tmp",
            "*.temp"
        )
        
        # Create robocopy command with exclusions
        $robocopyArgs = @(
            $SourcePath,
            $fullBackupPath,
            "/E",           # Copy subdirectories including empty ones
            "/R:3",         # Retry 3 times on failure
            "/W:1",         # Wait 1 second between retries
            "/MT:4",        # Use 4 threads for faster copying
            "/TEE",         # Output to console and log file
            "/NP",          # No progress bar
            "/NDL"          # No directory list
        )
        
        # Add exclusions
        foreach ($pattern in $excludePatterns) {
            $robocopyArgs += "/XD"
            $robocopyArgs += "*$pattern*"
        }
        
        # Execute robocopy
        $result = & robocopy @robocopyArgs
        
        if ($LASTEXITCODE -le 7) {  # Robocopy success codes are 0-7
            Write-Host "✅ Backup created successfully!" -ForegroundColor Green
            Write-Host "📂 Backup location: $fullBackupPath" -ForegroundColor Cyan
            
            # Calculate backup size
            $backupSize = (Get-ChildItem -Path $fullBackupPath -Recurse -File | Measure-Object -Property Length -Sum).Sum
            $fileCount = (Get-ChildItem -Path $fullBackupPath -Recurse -File).Count
            $sizeMB = [math]::Round($backupSize / 1MB, 2)
            
            Write-Host "📊 Backup size: $sizeMB MB" -ForegroundColor Yellow
            Write-Host "📄 Files backed up: $fileCount" -ForegroundColor Yellow
            
            Write-Host "=" * 50
            Write-Host "🎉 Backup completed successfully!" -ForegroundColor Green
            
            return $true
        } else {
            Write-Host "❌ Backup failed with exit code: $LASTEXITCODE" -ForegroundColor Red
            return $false
        }
        
    } catch {
        Write-Host "❌ Error creating backup: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Main execution
if ($Help) {
    Show-Help
    exit 0
}

# Check if we're in the project directory
$currentDir = Get-Location
$carfaxAppPath = Join-Path $currentDir "carfax-app"

if (!(Test-Path $carfaxAppPath)) {
    Write-Host "❌ Error: Please run this script from the project root directory" -ForegroundColor Red
    Write-Host "   Make sure you're in the folder containing 'carfax-app'" -ForegroundColor Yellow
    exit 1
}

# Create backup
$success = Create-Backup -SourcePath $currentDir

if ($success) {
    Write-Host ""
    Write-Host "💡 Tips:" -ForegroundColor Cyan
    Write-Host "   - Keep your backups in a safe location" -ForegroundColor White
    Write-Host "   - Consider using cloud storage for important backups" -ForegroundColor White
    Write-Host "   - Regular backups help prevent data loss" -ForegroundColor White
} 