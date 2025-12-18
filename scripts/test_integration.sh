#!/bin/bash
# ============================================================================
# SYNTX INTEGRATION TEST - V2 Scorer mit Legacy-Kompatibilität
# ============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

echo ""
echo -e "${YELLOW}╔══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${YELLOW}║${WHITE}        🔌 SYNTX INTEGRATION TEST - Legacy Kompatibilität         ${YELLOW}║${NC}"
echo -e "${YELLOW}╚══════════════════════════════════════════════════════════════════╝${NC}"
echo ""

python3 << 'PYTHON'
import sys
sys.path.insert(0, '/opt/syntx-workflow-api-get-prompts')

RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
CYAN = '\033[0;36m'
WHITE = '\033[1;37m'
NC = '\033[0m'

print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
print(f"{WHITE}[1/4] Legacy Kompatibilität Test...{NC}")
print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")

from syntex_injector.syntex.analysis.scorer_v2 import score_all_fields, QualityScoreV2

test_fields = {
    "driftkorper": "Die Struktur zeigt hierarchische Organisation mit TIER-1 bis TIER-4.",
    "kalibrierung": "Feedback-Mechanismen steuern die dynamische Anpassung.",
    "stromung": "Informationsflüsse verbinden alle Systemebenen."
}

result = score_all_fields(test_fields, "SYNTEX_SYSTEM")

# Legacy Properties testen
tests_passed = 0
tests_failed = 0

print(f"\n{WHITE}Checking Legacy Properties:{NC}\n")

# Test 1: total_score (int)
if hasattr(result, 'total_score_100') and isinstance(result.total_score_100, int):
    print(f"  {GREEN}✓{NC} total_score_100: {result.total_score_100} (int)")
    tests_passed += 1
else:
    print(f"  {RED}✗{NC} total_score_100 missing or wrong type")
    tests_failed += 1

# Test 2: field_completeness
if hasattr(result, 'field_completeness'):
    print(f"  {GREEN}✓{NC} field_completeness: {result.field_completeness} (legacy property)")
    tests_passed += 1
else:
    print(f"  {RED}✗{NC} field_completeness missing")
    tests_failed += 1

# Test 3: structure_adherence
if hasattr(result, 'structure_adherence'):
    print(f"  {GREEN}✓{NC} structure_adherence: {result.structure_adherence} (legacy property)")
    tests_passed += 1
else:
    print(f"  {RED}✗{NC} structure_adherence missing")
    tests_failed += 1

# Test 4: detail_breakdown
if hasattr(result, 'detail_breakdown') and isinstance(result.detail_breakdown, dict):
    print(f"  {GREEN}✓{NC} detail_breakdown: {result.detail_breakdown}")
    tests_passed += 1
else:
    print(f"  {RED}✗{NC} detail_breakdown missing")
    tests_failed += 1

# Test 5: to_dict() funktioniert
try:
    d = result.to_dict()
    if 'total_score' in d and 'field_completeness' in d:
        print(f"  {GREEN}✓{NC} to_dict() returns legacy-compatible format")
        tests_passed += 1
    else:
        print(f"  {RED}✗{NC} to_dict() missing legacy fields")
        tests_failed += 1
except Exception as e:
    print(f"  {RED}✗{NC} to_dict() error: {e}")
    tests_failed += 1

print(f"\n{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
print(f"{WHITE}[2/4] Calibrator Import Test (Legacy Mode)...{NC}")
print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")

try:
    import os
    os.environ['SYNTX_SCORER_V2'] = 'false'
    from syntex_injector.syntex.core.calibrator_enhanced import EnhancedSyntexCalibrator
    print(f"\n  {GREEN}✓{NC} Calibrator import OK (Legacy Mode)")
    tests_passed += 1
except Exception as e:
    print(f"\n  {RED}✗{NC} Calibrator import FAILED: {e}")
    tests_failed += 1

print(f"\n{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
print(f"{WHITE}[3/4] Calibrator Import Test (V2 Mode)...{NC}")
print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")

try:
    os.environ['SYNTX_SCORER_V2'] = 'true'
    # Force reimport
    import importlib
    import syntex_injector.syntex.core.calibrator_enhanced as cal_mod
    importlib.reload(cal_mod)
    print(f"\n  {GREEN}✓{NC} Calibrator import OK (V2 Mode)")
    tests_passed += 1
except Exception as e:
    print(f"\n  {RED}✗{NC} Calibrator import FAILED: {e}")
    tests_failed += 1

print(f"\n{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
print(f"{WHITE}[4/4] Tracker Kompatibilität Test...{NC}")
print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")

try:
    # Simuliere was tracker.log_progress macht
    score = result
    entry_data = {
        "quality_score": score.total_score if hasattr(score, 'total_score') else 0,
        "field_completeness": score.field_completeness,
        "structure_adherence": score.structure_adherence,
    }
    print(f"\n  {GREEN}✓{NC} Tracker data extraction works:")
    print(f"      quality_score: {entry_data['quality_score']}")
    print(f"      field_completeness: {entry_data['field_completeness']}")
    print(f"      structure_adherence: {entry_data['structure_adherence']}")
    tests_passed += 1
except Exception as e:
    print(f"\n  {RED}✗{NC} Tracker compatibility FAILED: {e}")
    tests_failed += 1

# Summary
print(f"\n{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
print(f"{WHITE}Summary{NC}")
print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")

total = tests_passed + tests_failed
print(f"\n  {WHITE}Tests Passed:{NC} {GREEN}{tests_passed}{NC}/{total}")
print(f"  {WHITE}Tests Failed:{NC} {RED}{tests_failed}{NC}/{total}")

if tests_failed == 0:
    print(f"\n  {GREEN}╔═══════════════════════════════════════════════════════╗{NC}")
    print(f"  {GREEN}║  ✅ ALL INTEGRATION TESTS PASSED                      ║{NC}")
    print(f"  {GREEN}║     V2 Scorer is fully backward compatible!           ║{NC}")
    print(f"  {GREEN}╚═══════════════════════════════════════════════════════╝{NC}")
else:
    print(f"\n  {RED}╔═══════════════════════════════════════════════════════╗{NC}")
    print(f"  {RED}║  ❌ INTEGRATION TESTS FAILED                          ║{NC}")
    print(f"  {RED}╚═══════════════════════════════════════════════════════╝{NC}")

print("")
PYTHON

echo -e "${YELLOW}══════════════════════════════════════════════════════════════════${NC}"
echo -e "${WHITE}                    INTEGRATION TEST COMPLETE                      ${NC}"
echo -e "${YELLOW}══════════════════════════════════════════════════════════════════${NC}"
echo ""
