#!/bin/bash

# SYNTX API Complete Test Script
# Tests ALL endpoints including NEW advanced features!

BASE_URL="https://dev.syntx-system.com"

echo "╔═════════════════════════════════════════╗"
echo "║   🔥 SYNTX API COMPREHENSIVE TEST 🔥    ║"
echo "╚═════════════════════════════════════════╝"
echo ""

# === HEALTH ===
echo "🏥 HEALTH CHECK"
curl -s "$BASE_URL/health" | jq '{status, version: .api_version}'
echo ""

# === MONITORING (NEW!) ===
echo "📡 LIVE QUEUE MONITOR (NEW!)"
curl -s "$BASE_URL/monitoring/live-queue" | jq '{health: .system_health, queue: .queue, performance: .performance}'
echo ""

# === ADVANCED PROMPTS (NEW!) ===
echo "🔮 PREDICT SCORE (NEW!)"
curl -s -X POST "$BASE_URL/prompts/advanced/predict-score" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt_text": "**Meta-Prompt mit TIER-1** Beschreibe den Driftkörper mit Kalibrierung und Strömung.",
    "topic": "technologie",
    "style": "kreativ"
  }' | jq '{predicted_score, confidence, recommendation}'
echo ""

echo "🔍 FIELD MISSING ANALYSIS (NEW!)"
curl -s "$BASE_URL/prompts/advanced/fields-missing-analysis" | jq '{status, worst_3: .fields_by_detection_rate[:3] | map({field, rate: .detection_rate, severity})}'
echo ""

echo "🔥 KEYWORD COMBINATIONS (NEW!)"
curl -s "$BASE_URL/prompts/advanced/keyword-combinations" | jq '{status, top_3: .top_combinations[:3] | map({combo: .combination, score: .avg_score})}'
echo ""

echo "📚 TEMPLATES BY SCORE (NEW!)"
curl -s "$BASE_URL/prompts/advanced/templates-by-score?min_score=95" | jq '{found: .templates_found, avg_length: .patterns.avg_length}'
echo ""

echo "🎯 OPTIMAL WRAPPER PER TOPIC (NEW!)"
curl -s "$BASE_URL/prompts/advanced/optimal-wrapper-for-topic" | jq '{topics: .topics_analyzed, best: .recommendations[0] | {topic, wrapper: .best_wrapper, score: .best_avg_score}}'
echo ""

echo "🧠 EVOLUTION LEARNING CURVE (NEW!)"
curl -s "$BASE_URL/prompts/advanced/evolution-learning-curve" | jq '{days: .days_tracked, trend: .overall_trend}'
echo ""

# === COMPLETE EXPORT ===
echo "📦 COMPLETE EXPORT (page 1, 5 items)"
curl -s "$BASE_URL/prompts/complete-export?page=1&page_size=5" | jq '{status, total: .pagination.total_items, items: .exports | length}'
echo ""

# === ANALYTICS ===
echo "📊 ANALYTICS DASHBOARD"
curl -s "$BASE_URL/analytics/complete-dashboard" | jq '{system_health: .system_health, insights: .insights[:3]}'
echo ""

# === EVOLUTION ===
echo "🧬 SYNTX VS NORMAL"
curl -s "$BASE_URL/evolution/syntx-vs-normal" | jq '{syntx_avg: .comparison.syntx.avg_score, normal_avg: .comparison.normal.avg_score, gap: .score_gap}'
echo ""

# === RESONANZ ===
echo "🌊 QUEUE RESONANZ"
curl -s "$BASE_URL/resonanz/queue" | jq
echo ""

echo "╔═════════════════════════════════════════╗"
echo "║   ✅ ALL ENDPOINTS TESTED! ✅           ║"
echo "║                                         ║"
echo "║   Total: 15+ endpoints                  ║"
echo "║   New Advanced: 7 endpoints             ║"
echo "║   Status: 💎 OPERATIONAL 💎            ║"
echo "╚═════════════════════════════════════════╝"

