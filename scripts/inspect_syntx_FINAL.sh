#!/bin/bash

# SYNTX FELD-INSPEKTOR (FINAL VERSION)
# Alle Endpoints inkl. POST

BASE_URL="https://dev.syntx-system.com"

# Array for status tracking
declare -a ENDPOINT_RESULTS

# GET endpoints
ENDPOINT_PATHS=(
    "/health"
    "/monitoring/live-queue"
    "/prompts/advanced/fields-missing-analysis"
    "/prompts/advanced/keyword-combinations"
    "/prompts/advanced/templates-by-score?min_score=90"
    "/prompts/advanced/optimal-wrapper-for-topic"
    "/prompts/advanced/evolution-learning-curve"
    "/prompts/complete-export?page=1&page_size=2"
    "/prompts/table-view?limit=5"
    "/prompts/all?limit=5"
    "/prompts/best?limit=5"
    "/prompts/fields/breakdown"
    "/prompts/costs/total"
    "/prompts/search?q=tier"
    "/analytics/complete-dashboard"
    "/analytics/overview"
    "/analytics/topics"
    "/analytics/scores/distribution"
    "/analytics/success-rate"
    "/analytics/success-rate/by-wrapper"
    "/evolution/syntx-vs-normal"
    "/evolution/keywords/power"
    "/evolution/topics/resonance"
    "/compare/wrappers"
    "/feld/drift"
    "/resonanz/queue"
    "/resonanz/system"
    "/generation/progress"
)

# Check jq
if ! command -v jq &> /dev/null; then
    echo "⚠️ jq not installed!"
    exit 1
fi

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║          🌊 SYNTX FINAL API INSPECTION 🌊                         ║"
echo "║  Base URL: $BASE_URL                              ║"
echo "║  GET Endpoints: ${#ENDPOINT_PATHS[@]}                                               ║"
echo "║  POST Endpoints: 1                                                ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Test GET endpoints
for path in "${ENDPOINT_PATHS[@]}"; do
    URL="${BASE_URL}${path}"
    
    echo "───────────────────────────────────────────────────────────────────"
    echo "🔍 ENDPOINT: $path"
    echo "URL: $URL"
    
    HTTP_STATUS=$(curl -s -o /tmp/response.txt -w "%{http_code}" "$URL")
    RESPONSE_BODY=$(cat /tmp/response.txt)
    
    echo "STATUS: $HTTP_STATUS"
    
    if [[ "$HTTP_STATUS" =~ ^2 ]]; then
        ENDPOINT_RESULTS+=("✅ GET $path → $HTTP_STATUS")
        
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
        ENDPOINT_RESULTS+=("❌ GET $path → 404 NOT FOUND")
        echo "⚠️  NOT FOUND"
        echo ""
    elif [ "$HTTP_STATUS" = "500" ]; then
        ENDPOINT_RESULTS+=("🔴 GET $path → 500 ERROR")
        echo "🔴 SERVER ERROR"
        echo ""
    else
        ENDPOINT_RESULTS+=("⚠️  GET $path → $HTTP_STATUS")
        echo "RESPONSE:"
        echo "${RESPONSE_BODY}" | head -n 10
        echo ""
    fi
done

# Test POST endpoint
echo "───────────────────────────────────────────────────────────────────"
echo "🔍 ENDPOINT (POST): /prompts/advanced/predict-score"
echo "URL: ${BASE_URL}/prompts/advanced/predict-score"
echo "PAYLOAD: {prompt_text with TIER-1 TIER-2 keywords}"

HTTP_STATUS=$(curl -s -o /tmp/response.txt -w "%{http_code}" \
    -X POST "${BASE_URL}/prompts/advanced/predict-score" \
    -H "Content-Type: application/json" \
    -d '{
        "prompt_text": "**TIER-1 TIER-2 TIER-3 TIER-4** Beschreibe den Driftkörper in allen Facetten. Analysiere die Kalibrierung des Systems präzise. Zeige die Strömung der Resonanzfelder detailliert. Erkläre die fundamentalen Mechanismen.",
        "topic": "technologie",
        "style": "kreativ"
    }')

RESPONSE_BODY=$(cat /tmp/response.txt)

echo "STATUS: $HTTP_STATUS"

if [[ "$HTTP_STATUS" =~ ^2 ]]; then
    ENDPOINT_RESULTS+=("✅ POST /prompts/advanced/predict-score → $HTTP_STATUS")
    
    FORMATTED_JSON=$(echo "$RESPONSE_BODY" | jq . 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        echo "RESPONSE:"
        echo "${FORMATTED_JSON}"
        echo ""
    else
        echo "RESPONSE (not JSON):"
        echo "${RESPONSE_BODY}"
        echo ""
    fi
elif [ "$HTTP_STATUS" = "404" ]; then
    ENDPOINT_RESULTS+=("❌ POST /prompts/advanced/predict-score → 404 NOT FOUND")
    echo "⚠️  NOT FOUND"
    echo ""
else
    ENDPOINT_RESULTS+=("⚠️  POST /prompts/advanced/predict-score → $HTTP_STATUS")
    echo "RESPONSE:"
    echo "${RESPONSE_BODY}"
    echo ""
fi

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
echo "Total Tested: $((${#ENDPOINT_PATHS[@]} + 1)) endpoints (28 GET + 1 POST)"
echo "Legend: ✅ = 200 OK | ❌ = 404 NOT FOUND | 🔴 = 500 ERROR | ⚠️ = OTHER"
echo ""
echo "✅ INSPECTION COMPLETE"

# Cleanup
rm -f /tmp/response.txt

