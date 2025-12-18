#!/bin/bash
# ============================================================================
# SYNTX LIVE SCORING TEST - Teste V2 mit echten Queue-Daten
# ============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo ""
echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║${WHITE}        🔴 SYNTX LIVE SCORING TEST - Echte Queue-Daten           ${PURPLE}║${NC}"
echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════════╝${NC}"
echo ""

python3 << 'PYTHON'
import sys
import json
from pathlib import Path
sys.path.insert(0, '/opt/syntx-workflow-api-get-prompts')

RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
CYAN = '\033[0;36m'
WHITE = '\033[1;37m'
PURPLE = '\033[0;35m'
NC = '\033[0m'

def print_bar(score, width=20):
    filled = int(score * width)
    return "█" * filled + "░" * (width - filled)

print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
print(f"{WHITE}[1/3] Loading processed responses...{NC}")
print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")

# Finde Response-Dateien
processed_dir = Path("/opt/syntx-workflow-api-get-prompts/queue/processed")
response_files = list(processed_dir.glob("*_response.txt"))[:5]  # Erste 5

print(f"\n  Found {len(response_files)} response files")

from syntex_injector.syntex.analysis.scorer_v2 import score_all_fields
from syntex_injector.syntex.core.parser import SyntexParser

parser = SyntexParser()

print(f"\n{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
print(f"{WHITE}[2/3] Scoring responses with V2...{NC}")
print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")

results = []

for i, resp_file in enumerate(response_files, 1):
    print(f"\n{YELLOW}═══ Response {i}: {resp_file.name[:50]}...{NC}")
    
    # Lade Response
    response_text = resp_file.read_text()
    
    # Lade JSON für alte Score
    json_file = resp_file.parent / resp_file.name.replace("_response.txt", ".json")
    old_score = 0
    if json_file.exists():
        with open(json_file) as f:
            meta = json.load(f)
            old_score = meta.get("syntex_result", {}).get("quality_score", {}).get("total_score", 0)
    
    # Parse Fields
    try:
        fields = parser.parse(response_text)
        format_type = fields.get_format()
        fields_dict = {k: v for k, v in fields.to_dict().items() if v}
        
        # V2 Score
        v2_result = score_all_fields(fields_dict, format_type)
        
        print(f"  {WHITE}Format:{NC} {format_type}")
        print(f"  {WHITE}Old Score (v1):{NC} {old_score}/100")
        print(f"  {WHITE}New Score (v2):{NC} {v2_result.total_score_100}/100 ({v2_result.status})")
        print(f"  {WHITE}Coherence:{NC} {v2_result.coherence_score:.3f}")
        
        diff = v2_result.total_score_100 - old_score
        diff_color = GREEN if diff >= 0 else RED
        print(f"  {WHITE}Difference:{NC} {diff_color}{diff:+d}{NC}")
        
        results.append({
            "file": resp_file.name,
            "old": old_score,
            "new": v2_result.total_score_100,
            "diff": diff,
            "status": v2_result.status
        })
        
    except Exception as e:
        print(f"  {RED}Error: {e}{NC}")

print(f"\n{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
print(f"{WHITE}[3/3] Summary{NC}")
print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")

if results:
    avg_old = sum(r["old"] for r in results) / len(results)
    avg_new = sum(r["new"] for r in results) / len(results)
    avg_diff = avg_new - avg_old
    
    print(f"\n  {WHITE}Responses Scored:{NC} {len(results)}")
    print(f"  {WHITE}Average V1 Score:{NC} {avg_old:.1f}/100")
    print(f"  {WHITE}Average V2 Score:{NC} {avg_new:.1f}/100")
    print(f"  {WHITE}Average Difference:{NC} {avg_diff:+.1f}")
    
    print(f"\n  {WHITE}Status Distribution:{NC}")
    for status in ["EXCELLENT", "OK", "UNSTABLE", "FAILED"]:
        count = sum(1 for r in results if r["status"] == status)
        if count > 0:
            print(f"    {status}: {count}")

print(f"\n  {GREEN}╔═══════════════════════════════════════════════════════╗{NC}")
print(f"  {GREEN}║  ✅ LIVE SCORING TEST COMPLETE                        ║{NC}")
print(f"  {GREEN}╚═══════════════════════════════════════════════════════╝{NC}")
print("")
PYTHON

echo -e "${PURPLE}══════════════════════════════════════════════════════════════════${NC}"
echo -e "${WHITE}                    LIVE SCORING TEST COMPLETE                     ${NC}"
echo -e "${PURPLE}══════════════════════════════════════════════════════════════════${NC}"
echo ""
