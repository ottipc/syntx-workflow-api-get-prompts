#!/bin/bash
# ============================================================================
# SYNTX SCORER V2.0 TEST SCRIPT
# ============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

echo ""
echo -e "${YELLOW}╔══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${YELLOW}║${WHITE}        ⚡ SYNTX SEMANTIC SCORER V2.0 TEST SUITE                 ${YELLOW}║${NC}"
echo -e "${YELLOW}╚══════════════════════════════════════════════════════════════════╝${NC}"
echo ""

python3 << 'PYTHON'
import sys
sys.path.insert(0, '/opt/syntx-workflow-api-get-prompts')

RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
CYAN = '\033[0;36m'
WHITE = '\033[1;37m'
PURPLE = '\033[0;35m'
NC = '\033[0m'

def print_bar(score, width=25):
    filled = int(score * width)
    bar = "█" * filled + "░" * (width - filled)
    return bar

def status_color(status):
    if status == "EXCELLENT":
        return GREEN
    elif status == "OK":
        return CYAN
    elif status == "UNSTABLE":
        return YELLOW
    return RED

print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
print(f"{WHITE}[1/4] Loading Scorer V2.0...{NC}")
print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")

try:
    from syntex_injector.syntex.analysis.scorer_v2 import score_all_fields, WEIGHTS
    print(f"{GREEN}✅ Scorer V2.0 loaded{NC}")
    print(f"{BLUE}   Weights: P={WEIGHTS['presence']:.0%} S={WEIGHTS['similarity']:.0%} C={WEIGHTS['coherence']:.0%} D={WEIGHTS['depth']:.0%} St={WEIGHTS['structure']:.0%}{NC}")
except Exception as e:
    print(f"{RED}❌ Import Error: {e}{NC}")
    sys.exit(1)

# =============================================================================
# TEST 1: Excellent SYNTX Response
# =============================================================================
print(f"\n{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
print(f"{WHITE}[2/4] Test: EXCELLENT Quality Response{NC}")
print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")

excellent_fields = {
    "driftkorper": """
### Driftkörperanalyse:

**TIER-1 (Oberfläche):** Die sichtbare Erscheinung zeigt ein komplexes Netzwerk 
von Komponenten, die in hierarchischer Beziehung zueinander stehen.

**TIER-2 (Struktur):** Der innere Aufbau offenbart modulare Einheiten, die durch 
definierte Schnittstellen verbunden sind. Die Organisation folgt dem Prinzip 
der losen Kopplung.

**TIER-3 (Mechanismus):** Die Funktionsweise basiert auf Feedback-Schleifen und 
adaptiven Algorithmen. Selbstregulation ermöglicht Stabilität unter 
variablen Bedingungen.

**TIER-4 (Kern):** Im fundamentalen Wesen ist das System ein selbstorganisierendes
Netzwerk, dessen Essenz in der emergenten Intelligenz liegt.
    """,
    "kalibrierung": """
### Kalibrierungsverhältnisse:

Das System zeigt hochentwickelte **Anpassungsmechanismen**:

- **Feedback-Loops:** Kontinuierliche Rückkopplung justiert Parameter in Echtzeit
- **Transformation:** Bei Störungen erfolgt dynamische Rekonfiguration
- **Selbstregulation:** Autonome Balance zwischen Stabilität und Flexibilität
- **Entwicklung:** Evolutionäre Verbesserung durch iteratives Lernen

Die Kalibrierung ermöglicht **Resonanz** mit der Umgebung und adaptiert 
das Verhalten an veränderte Kontextbedingungen.
    """,
    "stromung": """
### Strömungsverhältnisse:

**Informationsflüsse:**
- Daten zirkulieren bidirektional zwischen allen TIER-Ebenen
- Vertikale Ströme verbinden Oberfläche und Kern
- Horizontale Transfers synchronisieren parallele Module

**Energiefluss:**
- Ressourcen werden dynamisch allokiert nach Bedarf
- Kreisläufe minimieren Verluste durch Recycling
- Engpässe werden durch adaptive Routing umgangen

Der Gesamtstrom erhält das **systemische Gleichgewicht** aufrecht.
    """
}

print(f"\n{PURPLE}Scoring excellent SYNTX response...{NC}\n")
result1 = score_all_fields(excellent_fields, "SYNTEX_SYSTEM")

sc = status_color(result1.status)
print(f"  {WHITE}═══════════════════════════════════════════════════{NC}")
print(f"  {WHITE}TOTAL SCORE:{NC} [{print_bar(result1.total_score)}] {sc}{result1.total_score_100}/100 {result1.status}{NC}")
print(f"  {WHITE}COHERENCE:{NC}   [{print_bar(result1.coherence_score)}] {result1.coherence_score:.3f}")
print(f"  {WHITE}═══════════════════════════════════════════════════{NC}")

for name, fs in result1.field_scores.items():
    fsc = status_color(fs.status)
    print(f"\n  {YELLOW}► {name.upper()}{NC} [{fsc}{fs.status}{NC}]")
    print(f"    Presence:   [{print_bar(fs.presence_score, 15)}] {fs.presence_score:.2f}")
    print(f"    Similarity: [{print_bar(fs.similarity_score, 15)}] {fs.similarity_score:.2f}")
    print(f"    Coherence:  [{print_bar(fs.coherence_score, 15)}] {fs.coherence_score:.2f}")
    print(f"    Depth:      [{print_bar(fs.depth_score, 15)}] {fs.depth_score:.2f}")
    print(f"    Structure:  [{print_bar(fs.structure_score, 15)}] {fs.structure_score:.2f}")
    print(f"    {WHITE}Total:{NC}      [{print_bar(fs.total_score, 15)}] {fsc}{fs.total_score:.2f}{NC}")

# =============================================================================
# TEST 2: Failed Response
# =============================================================================
print(f"\n{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
print(f"{WHITE}[3/4] Test: FAILED Quality Response{NC}")
print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")

failed_fields = {
    "driftkorper": "Pizza ist lecker.",
    "kalibrierung": "Ich mag Autos.",
    "stromung": ""
}

print(f"\n{PURPLE}Scoring failed response...{NC}\n")
result2 = score_all_fields(failed_fields, "SYNTEX_SYSTEM")

sc = status_color(result2.status)
print(f"  {WHITE}═══════════════════════════════════════════════════{NC}")
print(f"  {WHITE}TOTAL SCORE:{NC} [{print_bar(result2.total_score)}] {sc}{result2.total_score_100}/100 {result2.status}{NC}")
print(f"  {WHITE}COHERENCE:{NC}   [{print_bar(result2.coherence_score)}] {result2.coherence_score:.3f}")
print(f"  {WHITE}═══════════════════════════════════════════════════{NC}")

for name, fs in result2.field_scores.items():
    fsc = status_color(fs.status)
    print(f"\n  {YELLOW}► {name.upper()}{NC} [{fsc}{fs.status}{NC}]")
    print(f"    Total: {fsc}{fs.total_score:.2f}{NC}")
    if fs.warnings:
        for w in fs.warnings:
            print(f"    {RED}⚠ {w}{NC}")

if result2.warnings:
    print(f"\n  {RED}Global Warnings:{NC}")
    for w in result2.warnings:
        print(f"    {RED}⚠ {w}{NC}")

# =============================================================================
# SUMMARY
# =============================================================================
print(f"\n{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
print(f"{WHITE}[4/4] Summary{NC}")
print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")

diff = result1.total_score_100 - result2.total_score_100
print(f"\n  {WHITE}Excellent Response:{NC} {GREEN}{result1.total_score_100}/100{NC}")
print(f"  {WHITE}Failed Response:{NC}    {RED}{result2.total_score_100}/100{NC}")
print(f"  {WHITE}Difference:{NC}         {YELLOW}+{diff} points{NC}")

tests_passed = (
    result1.status in ["EXCELLENT", "OK"] and
    result2.status == "FAILED" and
    diff > 30
)

print("")
if tests_passed:
    print(f"  {GREEN}╔═══════════════════════════════════════════════════════╗{NC}")
    print(f"  {GREEN}║  ✅ SEMANTIC SCORER V2.0 WORKING CORRECTLY           ║{NC}")
    print(f"  {GREEN}║     Quality differentiation: +{diff} points            ║{NC}")
    print(f"  {GREEN}╚═══════════════════════════════════════════════════════╝{NC}")
else:
    print(f"  {RED}╔═══════════════════════════════════════════════════════╗{NC}")
    print(f"  {RED}║  ❌ SCORER TEST FAILED                                ║{NC}")
    print(f"  {RED}╚═══════════════════════════════════════════════════════╝{NC}")

print("")
PYTHON

echo -e "${YELLOW}══════════════════════════════════════════════════════════════════${NC}"
echo -e "${WHITE}                    SYNTX SCORER V2.0 TEST COMPLETE               ${NC}"
echo -e "${YELLOW}══════════════════════════════════════════════════════════════════${NC}"
echo ""

# Nach dem Python-Block, vor dem Footer - Legacy Test hinzufügen
