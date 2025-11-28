#!/bin/bash
# Manual Retry - Move error jobs back to incoming

if [ -z "$1" ]; then
    echo "Usage: ./scripts/manual_retry.sh <filename_pattern>"
    echo ""
    echo "Examples:"
    echo "  ./scripts/manual_retry.sh fotografie  # Retry all fotografie jobs"
    echo "  ./scripts/manual_retry.sh all         # Retry ALL error jobs"
    echo ""
    echo "Current errors:"
    ls queue/error/*.txt 2>/dev/null | sed 's/.*\//  - /'
    exit 1
fi

PATTERN="$1"

if [ "$PATTERN" = "all" ]; then
    COUNT=$(ls queue/error/*.txt 2>/dev/null | wc -l)
    echo "🔄 Retrying ALL $COUNT error jobs..."
    mv queue/error/*.txt queue/incoming/ 2>/dev/null
    mv queue/error/*.json queue/incoming/ 2>/dev/null
    echo "✅ Moved to incoming/"
else
    COUNT=$(ls queue/error/*${PATTERN}*.txt 2>/dev/null | wc -l)
    if [ $COUNT -eq 0 ]; then
        echo "❌ No files matching pattern: $PATTERN"
        exit 1
    fi
    echo "🔄 Retrying $COUNT jobs matching '$PATTERN'..."
    mv queue/error/*${PATTERN}*.txt queue/incoming/ 2>/dev/null
    mv queue/error/*${PATTERN}*.json queue/incoming/ 2>/dev/null
    echo "✅ Moved to incoming/"
fi
