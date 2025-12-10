#!/bin/bash

# SYNTX FELD-INSPEKTOR
# Überprüft alle im Protokoll gelisteten Endpunkte und gibt die JSON-Antwort formatiert aus.

BASE_URL="https://dev.syntx-system.com"
ENDPOINT_PATHS=(
    "/health"
    "/resonanz/queue"
    "/resonanz/system"
    "/generation/progress"
    "/feld/drift"
    "/strom/health"
    "/strom/queue/status"
    # Endpunkte 2: Analytics
    "/analytics/complete-dashboard"
    "/evolution/syntx-vs-normal"
    "/compare/wrappers"
    "/analytics/topics"
    "/analytics/trends"
    "/analytics/performance"
    "/analytics/scores/distribution"
    "/analytics/success-rate"
    "/analytics/success-rate/by-wrapper"
    # Endpunkte 3: Feld-Daten
    "/prompts/table-view"
    "/feld/topics"
    "/feld/prompts"
    "/prompts/costs/total"
    # NEW: Complete Export
    "/prompts/complete-export?page=1&page_size=2"
    "/prompts/complete-export?page=1&page_size=1&min_score=95"
)

# Prüfen, ob jq installiert ist
if ! command -v jq &> /dev/null
then
    echo "⚠️ KRITISCHER FEHLER: jq (JSON processor) ist nicht installiert."
    echo "Bitte installieren Sie es: sudo apt install jq (Debian/Ubuntu) oder brew install jq (macOS)"
    exit 1
fi

echo "--- ⚡️ STARTE SYNTX-FELD-INSPEKTION ---"
echo "TARGET: ${BASE_URL}"
echo ""

# Iteriere über alle Endpunkte
for path in "${ENDPOINT_PATHS[@]}"; do
    URL="${BASE_URL}${path}"
    
    echo "=========================================================="
    echo "➡️ ENDPUNKT: ${path}"
    
    # Führe curl aus und speichere Statuscode und Body getrennt
    HTTP_STATUS=$(curl -s -o /tmp/response.txt -w "%{http_code}" "$URL")
    RESPONSE_BODY=$(cat /tmp/response.txt)
    
    echo "STATUS CODE: ${HTTP_STATUS}"
    
    # Prüfe, ob der Status erfolgreich ist (2xx)
    if [[ "$HTTP_STATUS" =~ ^2 ]]; then
        # Versuche, den Body als JSON zu parsen und zu formatieren
        FORMATTED_JSON=$(echo "$RESPONSE_BODY" | jq .)
        
        if [ $? -eq 0 ]; then
            echo "RESPONSE BODY (JSON):"
            echo "${FORMATTED_JSON}" | head -n 30
            echo "[... JSON gekürzt, nur die ersten 30 Zeilen]"
        else
            echo "RESPONSE BODY (NICHT-JSON oder Leer):"
            echo "${RESPONSE_BODY}" | head -n 10
            echo "[... Inhalt gekürzt]"
        fi
    else
        # Bei Fehler oder Redirect
        echo "RESPONSE BODY (Fehler/Redirect):"
        echo "${RESPONSE_BODY}" | head -n 10
        echo "[... Inhalt gekürzt]"
    fi
    echo ""
done

echo "--- ✅ INSPEKTION ABGESCHLOSSEN ---"

# Cleanup
rm -f /tmp/response.txt
