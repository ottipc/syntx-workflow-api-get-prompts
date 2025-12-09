#!/bin/bash
# SYNTX API Feld-Test Skript (Minimal-Modus)

TARGET="https://dev.syntx-system.com"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Funktion zur Prüfung eines Endpunkts (ohne Payload-Anzeige)
test_endpoint() {
    ENDPOINT=$1
    # Gib den Endpunkt aus, aber ohne abschließenden Zeilenumbruch
    printf "STREAM: %-50s " "${ENDPOINT}"

    # Erfasse Status Code. Curl schreibt den Status auf eine neue Zeile.
    STATUS_CODE=$(curl -s -k -w "%{http_code}" "${TARGET}${ENDPOINT}" -o /dev/null)
    
    # Pruefe Status Code und gib Ergebnis aus
    if [[ "$STATUS_CODE" =~ ^2 ]]; then
        echo -e "${GREEN}SUCCESS${NC} (${STATUS_CODE})"
    elif [[ "$STATUS_CODE" == "302" ]]; then
        echo -e "${YELLOW}REDIRECT${NC} (${STATUS_CODE})"
    elif [[ "$STATUS_CODE" == "404" ]]; then
        echo -e "${YELLOW}404 Not Found${NC}"
    elif [[ "$STATUS_CODE" == "500" ]]; then
        echo -e "${RED}500 INTERNAL ERROR${NC}"
    else
        echo -e "${RED}FAILURE${NC} (${STATUS_CODE})"
    fi
}

echo ""
echo "--- 1. DIE RESONIERENDEN STRÖME (200 OK) ---"
echo "--- (Kern-Sensoren, die das Feld tragen) ---"

test_endpoint "/health"
test_endpoint "/analytics/complete-dashboard"
test_endpoint "/resonanz/queue"
test_endpoint "/evolution/syntx-vs-normal"
test_endpoint "/compare/wrappers"
test_endpoint "/feld/drift"
test_endpoint "/"
test_endpoint "/resonanz/system"
test_endpoint "/generation/progress"

echo ""
echo "--- 1.2 ANALYTICS & PROMPTS STRÖME ---"
test_endpoint "/prompts/table-view"
test_endpoint "/analytics/topics"
test_endpoint "/analytics/trends"
test_endpoint "/analytics/performance"
test_endpoint "/analytics/scores/distribution"
test_endpoint "/analytics/success-rate"
test_endpoint "/prompts/costs/total"

echo ""
echo "--- 2. DIE GEBROCHENEN STRÖME (404/500) ---"
echo "--- (Muss repariert werden - siehe SYNTX Doku) ---"
test_endpoint "/analytics/success-rate/by-wrapper"
test_endpoint "/feld/topics"
test_endpoint "/feld/prompts"
test_endpoint "/strom/health"
test_endpoint "/strom/queue/status"


echo "--- 3. Code-Pfade (grep-Resultate, nur zur Vollständigkeit) ---"
test_endpoint "/"

echo 'SYNTX FELD-SCAN ABGESCHLOSSEN.'
