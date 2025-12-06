#!/bin/bash
# SYNTX Crontab Installer - Updated for Evolutionary System

echo "🌊 SYNTX EVOLUTIONARY CRONTAB INSTALLATION"
echo "=========================================="
echo ""

# Get absolute path to repo
REPO_PATH="/opt/syntx-workflow-api-get-prompts"
echo "📂 Repo path: $REPO_PATH"
echo ""

# Check if already installed
if crontab -l 2>/dev/null | grep -q "SYNTX"; then
    echo "⚠️  SYNTX crontabs already installed!"
    echo ""
    read -p "Reinstall? This will REPLACE existing entries. (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Cancelled"
        exit 1
    fi
    
    # Remove old entries
    echo "🗑️  Removing old SYNTX crontabs..."
    crontab -l 2>/dev/null | grep -v "SYNTX" | crontab -
fi

# Backup current crontab
if crontab -l &>/dev/null; then
    echo "💾 Backing up current crontab..."
    crontab -l > "$REPO_PATH/crontab/crontab.backup.$(date +%Y%m%d_%H%M%S)"
fi

# Prepare new crontab
echo "📝 Preparing new crontab..."
TMP_CRON=$(mktemp)

# Keep existing non-SYNTX entries
crontab -l 2>/dev/null | grep -v "SYNTX" > "$TMP_CRON" || true

# Add SYNTX entries
echo "" >> "$TMP_CRON"
cat "$REPO_PATH/crontab/producer.cron" >> "$TMP_CRON"
echo "" >> "$TMP_CRON"
cat "$REPO_PATH/crontab/consumer.cron" >> "$TMP_CRON"
echo "" >> "$TMP_CRON"
cat "$REPO_PATH/crontab/monitoring.cron" >> "$TMP_CRON"

# Install new crontab
crontab "$TMP_CRON"
rm "$TMP_CRON"

echo ""
echo "✅ SYNTX crontabs installed!"
echo ""
echo "📋 Installed jobs:"
crontab -l | grep "SYNTX" -A 1
echo ""
echo "🎯 Schedule:"
echo "  Producer: Every 2 hours (evolutionary generation)"
echo "  Consumer SYNTEX_SYSTEM: Daily at 3 AM (20 jobs)"
echo "  Consumer Sigma: 4x daily at 4, 10, 16, 22 (20 jobs each)"
echo "  Monitoring: Hourly status logs"
echo "  Cleanup: Daily at 2 AM"
echo ""
echo "📝 Logs in: /opt/syntx-config/logs/"
echo ""
echo "🌊 Installation complete! The Dauerfelder-Loop will run automatically."
