#!/bin/bash
echo "╔══════════════════════════════════════╗"
echo "║   SYNTX QUEUE STATUS                 ║"
echo "╚══════════════════════════════════════╝"
echo ""

INCOMING=$(ls queue/incoming/*.txt 2>/dev/null | wc -l)
PROCESSING=$(ls queue/processing/*.txt 2>/dev/null | wc -l)
PROCESSED=$(ls queue/processed/*.txt 2>/dev/null | wc -l)
ERROR=$(ls queue/error/*.txt 2>/dev/null | wc -l)

echo "📥 Incoming:    $INCOMING"
echo "⚙️  Processing:  $PROCESSING"
echo "✅ Processed:   $PROCESSED"
echo "❌ Error:       $ERROR"
echo ""

if [ $INCOMING -lt 5 ]; then
    echo "⚠️  Status: LOW - Producer should run"
elif [ $INCOMING -gt 50 ]; then
    echo "⚠️  Status: OVERFLOW - Consumer too slow"
else
    echo "✅ Status: BALANCED"
fi
