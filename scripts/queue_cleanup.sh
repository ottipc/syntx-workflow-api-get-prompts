#!/bin/bash
# Queue Cleanup - Stuck Jobs & Errors

echo "🧹 SYNTX Queue Cleanup"
echo "====================="
echo ""

# 1. Stuck Jobs in processing/
STUCK=$(ls queue/processing/*.txt 2>/dev/null | wc -l)
if [ $STUCK -gt 0 ]; then
    echo "⚠️  Found $STUCK stuck jobs in processing/"
    echo "   Moving back to incoming/..."
    mv queue/processing/*.txt queue/incoming/ 2>/dev/null
    mv queue/processing/*.json queue/incoming/ 2>/dev/null
    echo "   ✅ Moved to incoming/"
else
    echo "✅ No stuck jobs in processing/"
fi

echo ""

# 2. Archive old processed jobs (>7 days)
OLD=$(find queue/processed/ -name "*.txt" -mtime +7 2>/dev/null | wc -l)
if [ $OLD -gt 0 ]; then
    echo "📦 Found $OLD old jobs in processed/ (>7 days)"
    echo "   Moving to archive/..."
    find queue/processed/ -name "*.txt" -mtime +7 -exec mv {} queue/archive/ \;
    find queue/processed/ -name "*.json" -mtime +7 -exec mv {} queue/archive/ \;
    echo "   ✅ Archived"
else
    echo "✅ No old jobs to archive"
fi

echo ""
echo "🎯 Cleanup complete!"
