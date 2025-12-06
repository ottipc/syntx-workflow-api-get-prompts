#!/bin/bash
# SYNTX Crontab Installer

echo "🔧 SYNTX Crontab Installation"
echo "=============================="
echo ""

# Get absolute path to repo
REPO_PATH="$(cd "$(dirname "$0")/.." && pwd)"
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

# Add SYNTX entries (replace placeholder with actual path)
echo "" >> "$TMP_CRON"
sed "s|/home/codi/Entwicklung/syntx-workflow-api-get-prompts|$REPO_PATH|g" "$REPO_PATH/crontab/producer.cron" >> "$TMP_CRON"
echo "" >> "$TMP_CRON"
sed "s|/home/codi/Entwicklung/syntx-workflow-api-get-prompts|$REPO_PATH|g" "$REPO_PATH/crontab/consumer.cron" >> "$TMP_CRON"
echo "" >> "$TMP_CRON"
sed "s|/home/codi/Entwicklung/syntx-workflow-api-get-prompts|$REPO_PATH|g" "$REPO_PATH/crontab/monitoring.cron" >> "$TMP_CRON"

# Install new crontab
crontab "$TMP_CRON"
rm "$TMP_CRON"

echo ""
echo "✅ SYNTX crontabs installed!"
echo ""
echo "📋 Installed jobs:"
crontab -l | grep "SYNTX" -A 1

echo ""
echo "🎯 Installation complete!"
