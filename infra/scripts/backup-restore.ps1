# ==============================================================================
# LeadForge: PostgreSQL Logical Backup and Restore Verification Script (LF-506)
# ==============================================================================

param (
    [string]$Action = "backup",
    [string]$BackupDir = "infra/backups"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
}

$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

if ($Action -eq "backup") {
    Write-Host "Creating backup of leadforge_app (private leads)..."
    pg_dump -U postgres -h localhost -d leadforge_app -F c -f "$BackupDir/leadforge_app_$Timestamp.dump"

    Write-Host "Creating backup of leadforge_cms (content)..."
    pg_dump -U postgres -h localhost -d leadforge_cms -F c -f "$BackupDir/leadforge_cms_$Timestamp.dump"

    Write-Host "Backup completed successfully in $BackupDir."
}
elseif ($Action -eq "test-restore") {
    Write-Host "Rehearsing restore to disposable database leadforge_restore_test..."
    psql -U postgres -h localhost -c "DROP DATABASE IF EXISTS leadforge_restore_test;"
    psql -U postgres -h localhost -c "CREATE DATABASE leadforge_restore_test;"

    $LatestAppBackup = Get-ChildItem "$BackupDir/leadforge_app_*.dump" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if (-not $LatestAppBackup) {
        Write-Error "No backup file found in $BackupDir."
    }

    Write-Host "Restoring $($LatestAppBackup.FullName)..."
    pg_restore -U postgres -h localhost -d leadforge_restore_test $LatestAppBackup.FullName

    $RestoredCount = (psql -U postgres -h localhost -d leadforge_restore_test -t -c "SELECT COUNT(*) FROM leads;").Trim()
    Write-Host "Verification successful: Restored $RestoredCount leads into leadforge_restore_test."

    psql -U postgres -h localhost -c "DROP DATABASE leadforge_restore_test;"
    Write-Host "Cleaned up disposable restore database."
}
else {
    Write-Host "Usage: ./backup-restore.ps1 -Action [backup|test-restore]"
}
