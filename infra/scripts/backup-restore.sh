#!/bin/sh
set -e

ACTION=${1:-backup}
BACKUP_DIR="infra/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

if [ "$ACTION" = "backup" ]; then
    echo "Creating logical database backups..."
    pg_dump -U postgres -h localhost -d leadforge_app -F c -f "$BACKUP_DIR/leadforge_app_$TIMESTAMP.dump"
    pg_dump -U postgres -h localhost -d leadforge_cms -F c -f "$BACKUP_DIR/leadforge_cms_$TIMESTAMP.dump"
    echo "Backups completed in $BACKUP_DIR."
elif [ "$ACTION" = "test-restore" ]; then
    echo "Rehearsing restore to disposable database leadforge_restore_test..."
    psql -U postgres -h localhost -c "DROP DATABASE IF EXISTS leadforge_restore_test;"
    psql -U postgres -h localhost -c "CREATE DATABASE leadforge_restore_test;"

    LATEST=$(ls -t "$BACKUP_DIR"/leadforge_app_*.dump | head -n 1)
    echo "Restoring from $LATEST..."
    pg_restore -U postgres -h localhost -d leadforge_restore_test "$LATEST"
    
    COUNT=$(psql -U postgres -h localhost -d leadforge_restore_test -t -c "SELECT COUNT(*) FROM leads;")
    echo "Verified: Restored $COUNT records successfully."

    psql -U postgres -h localhost -c "DROP DATABASE leadforge_restore_test;"
    echo "Restore test database cleaned up."
fi
