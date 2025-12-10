#!/bin/bash

# SYNTX FELD-INSPEKTOR (EXTENDED VERSION)
# Alle Endpoints + Status Summary am Ende

BASE_URL="https://dev.syntx-system.com"

# Array for status tracking
declare -a ENDPOINT_RESULTS

ENDPOINT_PATHS=(
    # === HEALTH & STATUS ===
    "/health"
    
    # === MONITORING (NEW!) ===
    "/monitoring/live-queue"
    
    # === PROMPTS ADVANCED (NEW!) ===
    "/prompts/advanced/fields-missing-analysis"
    "/prompts/advanced/keyword-combinations"
    "/prompts/advanced/templates-by-score?min_score=90"
    "/prompts/advanced/optimal-wrapper-for-topic"
    "/prompts/advanced/evolution-learning-curve"
    
    # === PROMPTS ===
    "/prompts/complete-export?page=1&page_size=2"
    "/prompts/table-view?limit=5"
    "/prompts/all?limit=5"
    "/prompts/best?limit=5"
    "/prompts/fields/breakdown"
    "/prompts/costs/total"
    "/prompts/search?q=tier"
    
    # === ANALYTICS ===
    "/analytics/complete-dashboard"
    "/analytics/overview"
    "/analytics/topics"
    "/analytics/scores/distribution"
    "/analytics/success-rate"
    "/analytics/success-rate/by-wrapper"
    
    # === EVOLUTION ===
    "/evolution/syntx-vs-normal"
    "/evolution/keywords/power"
    "/evolution/topics/resonance"
    
    # === COMPARE ===
    "/compare/wrappers"
    
    # === FELD ===
    "/feld/drift"
    
    # === RESONANZ ===
    "/resonanz/queue"
    "/resonanz/system"
    
    # === GENERATION ===
    "/generation/progress"
)

# Check jq
if ! command -v jq &> /dev/null; then
    echo "⚠️ jq not installed!"
    exit 1
fi

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║          🌊 SYNTX EXTENDED API INSPECTION 🌊                      ║"
echo "║  Base URL: $BASE_URL                              ║"
echo "║  Endpoints: ${#ENDPOINT_PATHS[@]}                                                   ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Test each endpoint
for path in "${ENDPOINT_PATHS[@]}"; do
    URL="${BASE_URL}${path}"
    
    echo "───────────────────────────────────────────────────────────────────"
    echo "🔍 ENDPOINT: $path"
    echo "URL: $URL"
    
    # Execute curl
    HTTP_STATUS=$(curl -s -o /tmp/response.txt -w "%{http_code}" "$URL")
    RESPONSE_BODY=$(cat /tmp/response.txt)
    
    echo "STATUS: $HTTP_STATUS"
    
    # Record result
    if [[ "$HTTP_STATUS" =~ ^2 ]]; then
        ENDPOINT_RESULTS+=("✅ $path → $HTTP_STATUS")
        
        # Try JSON format
        FORMATTED_JSON=$(echo "$RESPONSE_BODY" | jq . 2>/dev/null)
        
        if [ $? -eq 0 ]; then
            echo "RESPONSE (first 30 lines):"
            echo "${FORMATTED_JSON}" | head -n 30
            echo ""
        else
            echo "RESPONSE (not JSON):"
            echo "${RESPONSE_BODY}" | head -n 10
            echo ""
        fi
    elif [ "$HTTP_STATUS" = "404" ]; then
        ENDPOINT_RESULTS+=("❌ $path → 404 NOT FOUND")
        echo "⚠️  NOT FOUND"
        echo ""
    elif [ "$HTTP_STATUS" = "500" ]; then
        ENDPOINT_RESULTS+=("🔴 $path → 500 ERROR")
        echo "🔴 SERVER ERROR"
        echo ""
    else
        ENDPOINT_RESULTS+=("⚠️  $path → $HTTP_STATUS")
        echo "RESPONSE:"
        echo "${RESPONSE_BODY}" | head -n 10
        echo ""
    fi
done

echo ""
echo ""
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                  📋 ENDPOINT STATUS SUMMARY                       ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

for result in "${ENDPOINT_RESULTS[@]}"; do
    echo "$result"
done

echo ""
echo "Total Tested: ${#ENDPOINT_PATHS[@]} endpoints"
echo "Legend: ✅ = 200 OK | ❌ = 404 NOT FOUND | 🔴 = 500 ERROR | ⚠️ = OTHER"
echo ""
echo "✅ INSPECTION COMPLETE"

# Cleanup
rm -f /tmp/response.txt

