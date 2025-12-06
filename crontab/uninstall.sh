#!/bin/bash
# SYNTX Crontab Uninstaller

echo "🗑️  SYNTX Crontab Uninstallation"
echo "================================"
echo ""

if ! crontab -l 2>/dev/null | grep -q "SYNTX"; then
    echo "❌ No SYNTX crontabs found"
    exit 0
fi

read -p "Remove all SYNTX crontabs? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled"
    exit 1
fi

# Backup
REPO_PATH="$(cd "$(dirname "$0")/.." && pwd)"
echo "💾 Backing up current crontab..."
crontab -l > "$REPO_PATH/crontab/crontab.backup.$(date +%Y%m%d_%H%M%S)"

# Remove SYNTX entries
echo "🗑️  Removing SYNTX crontabs..."
crontab -l | grep -v "SYNTX" | grep -v "queue_system" | grep -v "queue_status" | grep -v "queue_cleanup" | crontab -

echo ""
echo "✅ SYNTX crontabs removed!"
