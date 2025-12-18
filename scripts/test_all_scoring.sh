#!/bin/bash
# SYNTX SCORING SUITE - RUN ALL TESTS 🚀

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         🚀 SYNTX SCORING V2.0 - FULL TEST SUITE               ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

cd /opt/syntx-workflow-api-get-prompts

echo "[1/4] EMBEDDINGS TEST"
echo "────────────────────────────────────────"
./scripts/test_embeddings.sh
echo ""

echo "[2/4] COHERENCE TEST"
echo "────────────────────────────────────────"
./scripts/test_coherence.sh
echo ""

echo "[3/4] SCORER V2.0 TEST"
echo "────────────────────────────────────────"
./scripts/test_scorer_v2.sh
echo ""

echo "[4/4] INTEGRATION TEST"
echo "────────────────────────────────────────"
./scripts/test_integration.sh
echo ""

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         ✅ ALL TESTS COMPLETE                                  ║"
echo "╚════════════════════════════════════════════════════════════════╝"
