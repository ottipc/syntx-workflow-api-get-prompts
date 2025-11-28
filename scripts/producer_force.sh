#!/bin/bash
# Force Producer Run - Ignoriert Queue-Status

echo "🏭 SYNTX Force Producer Run"
echo "============================"
echo ""

# Aktueller Status
INCOMING=$(ls queue/incoming/*.txt 2>/dev/null | wc -l)
echo "Current queue: $INCOMING jobs"
echo ""

# Confirmation
read -p "Force produce 20 new prompts? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled"
    exit 1
fi

echo "🔧 Starting force production..."
echo ""

# Run producer in force mode
python3 -c "
from queue_system.core.producer import IntelligentProducer
p = IntelligentProducer()
stats = p.run(force=True)
print(f\"✅ Produced: {stats['produced_count']}/{stats['requested_count']}\")
print(f\"⏱️  Duration: {stats['duration_seconds']:.1f}s\")
"

echo ""
echo "🎯 Force production complete!"
