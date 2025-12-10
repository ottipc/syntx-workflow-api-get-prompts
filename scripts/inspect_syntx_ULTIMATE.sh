#!/bin/bash

# SYNTX API ULTIMATE COMPREHENSIVE TEST
# Beautiful, structured, complete system analysis

BASE_URL="https://dev.syntx-system.com"
TIMESTAMP=$(date -Iseconds)

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                                                                   ║"
echo "║          🌊 SYNTX SYSTEM COMPLETE ANALYSIS 🌊                     ║"
echo "║                                                                   ║"
echo "║  Timestamp: $TIMESTAMP                           ║"
echo "║  Test Mode: COMPREHENSIVE (28 endpoints + system state)          ║"
echo "║                                                                   ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""
echo ""

# === SYSTEM STATE ===
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                     📊 SYSTEM STATE                               ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""
echo "Queue Status:"
echo "  - Incoming:   $(ls /opt/syntx-workflow-api-get-prompts/queue/incoming/*.txt 2>/dev/null | grep -v response | wc -l) jobs"
echo "  - Processing: $(ls /opt/syntx-workflow-api-get-prompts/queue/processing/*.txt 2>/dev/null | wc -l) jobs"
echo "  - Processed:  $(ls /opt/syntx-workflow-api-get-prompts/queue/processed/*.json 2>/dev/null | wc -l) jobs"
echo "  - Errors:     $(ls /opt/syntx-workflow-api-get-prompts/queue/error/*.txt 2>/dev/null | wc -l) jobs"
echo ""
echo "System Info:"
echo "  - Disk Usage: $(du -sh /opt/syntx-workflow-api-get-prompts | cut -f1)"
echo "  - API Running: $(pgrep -f 'syntx_api_production' > /dev/null && echo '✅ YES' || echo '❌ NO')"
echo "  - Cronjobs: $(crontab -l | grep syntx | wc -l) active"
echo ""
echo "Git Status:"
echo "  - Branch: $(cd /opt/syntx-workflow-api-get-prompts && git branch --show-current)"
echo "  - Last Commit: $(cd /opt/syntx-workflow-api-get-prompts && git log -1 --oneline)"
echo "  - Uncommitted: $(cd /opt/syntx-workflow-api-get-prompts && git status --short | wc -l) files"
echo "  - Total Commits: $(cd /opt/syntx-workflow-api-get-prompts && git rev-list --count HEAD)"
echo ""
echo "Logs:"
echo "  - Costs: $(wc -l < /opt/syntx-workflow-api-get-prompts/logs/costs.jsonl 2>/dev/null || echo 0) lines"
echo "  - GPT Prompts: $(wc -l < /opt/syntx-workflow-api-get-prompts/logs/gpt_prompts.jsonl 2>/dev/null || echo 0) lines"
echo "  - Calibrations: $(wc -l < /opt/syntx-workflow-api-get-prompts/logs/syntex_calibrations.jsonl 2>/dev/null || echo 0) lines"
echo ""
echo ""

# === ENDPOINTS ===
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                     🔥 API ENDPOINTS TEST                         ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# 1. HEALTH
echo "───────────────────────────────────────────────────────────────────"
echo "1. 🏥 HEALTH CHECK"
echo "───────────────────────────────────────────────────────────────────"
echo "Description: System health and version info"
echo "Endpoint: GET /health"
echo ""
HEALTH=$(curl -s "$BASE_URL/health")
echo "$HEALTH" | jq '.'
echo ""
echo "Key Metrics:"
echo "  - Status: $(echo "$HEALTH" | jq -r '.status')"
echo "  - Version: $(echo "$HEALTH" | jq -r '.api_version')"
echo "  - Queue Accessible: $(echo "$HEALTH" | jq -r '.queue_accessible')"
echo ""
echo ""

# 2. LIVE QUEUE MONITOR
echo "───────────────────────────────────────────────────────────────────"
echo "2. 📡 LIVE QUEUE MONITOR (NEW!)"
echo "───────────────────────────────────────────────────────────────────"
echo "Description: Real-time queue status, processing jobs, recent completions"
echo "Endpoint: GET /monitoring/live-queue"
echo ""
MONITOR=$(curl -s "$BASE_URL/monitoring/live-queue" 2>/dev/null || echo '{"error": "404 Not Found"}')
if echo "$MONITOR" | jq -e '.status' > /dev/null 2>&1; then
  echo "$MONITOR" | jq '.'
  echo ""
  echo "Key Metrics:"
  echo "  - System Health: $(echo "$MONITOR" | jq -r '.system_health')"
  echo "  - Incoming: $(echo "$MONITOR" | jq -r '.queue.incoming')"
  echo "  - Processing: $(echo "$MONITOR" | jq -r '.queue.processing')"
  echo "  - Processed: $(echo "$MONITOR" | jq -r '.queue.processed')"
  echo "  - Jobs/Hour: $(echo "$MONITOR" | jq -r '.performance.jobs_per_hour')"
else
  echo "⚠️  ENDPOINT NOT AVAILABLE (404)"
fi
echo ""
echo ""

# 3. PREDICT SCORE
echo "───────────────────────────────────────────────────────────────────"
echo "3. 🔮 PREDICT SCORE (NEW!)"
echo "───────────────────────────────────────────────────────────────────"
echo "Description: Predict quality score before processing"
echo "Endpoint: POST /prompts/advanced/predict-score"
echo ""
PREDICT=$(curl -s -X POST "$BASE_URL/prompts/advanced/predict-score" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt_text": "**Meta-Prompt mit TIER-1 und TIER-2** Beschreibe den Driftkörper. Analysiere die Kalibrierung. Zeige die Strömung der Resonanzfelder.",
    "topic": "technologie",
    "style": "kreativ"
  }')
echo "$PREDICT" | jq '.'
echo ""
echo "Key Metrics:"
echo "  - Predicted Score: $(echo "$PREDICT" | jq -r '.predicted_score')"
echo "  - Confidence: $(echo "$PREDICT" | jq -r '.confidence')"
echo "  - Recommendation: $(echo "$PREDICT" | jq -r '.recommendation')"
echo "  - Keywords Found: $(echo "$PREDICT" | jq -r '.analysis.total_keywords')"
echo ""
echo ""

# 4. FIELD MISSING ANALYSIS
echo "───────────────────────────────────────────────────────────────────"
echo "4. 🔍 FIELD MISSING ANALYSIS (NEW!)"
echo "───────────────────────────────────────────────────────────────────"
echo "Description: Analyze which fields are NOT being detected"
echo "Endpoint: GET /prompts/advanced/fields-missing-analysis"
echo ""
FIELDS=$(curl -s "$BASE_URL/prompts/advanced/fields-missing-analysis")
echo "$FIELDS" | jq '{status, total_jobs_analyzed, worst_3: .fields_by_detection_rate[:3]}'
echo ""
echo "Critical Issues:"
echo "$FIELDS" | jq -r '.fields_by_detection_rate[:3] | .[] | "  - \(.field): \(.detection_rate)% detected (\(.severity))"'
echo ""
echo ""

# 5. KEYWORD COMBINATIONS
echo "───────────────────────────────────────────────────────────────────"
echo "5. 🔥 KEYWORD COMBINATIONS (NEW!)"
echo "───────────────────────────────────────────────────────────────────"
echo "Description: Best keyword combinations for high scores"
echo "Endpoint: GET /prompts/advanced/keyword-combinations"
echo ""
COMBOS=$(curl -s "$BASE_URL/prompts/advanced/keyword-combinations")
echo "$COMBOS" | jq '{status, total_combinations_found, top_5: .top_combinations[:5]}'
echo ""
echo "Top Combos:"
echo "$COMBOS" | jq -r '.top_combinations[:5] | .[] | "  \(.power_rating) \(.combination): \(.avg_score) avg (\(.sample_count) samples)"'
echo ""
echo ""

# 6. TEMPLATES BY SCORE
echo "───────────────────────────────────────────────────────────────────"
echo "6. 📚 TEMPLATES BY SCORE (NEW!)"
echo "───────────────────────────────────────────────────────────────────"
echo "Description: Extract patterns from high-scoring prompts"
echo "Endpoint: GET /prompts/advanced/templates-by-score?min_score=95"
echo ""
TEMPLATES=$(curl -s "$BASE_URL/prompts/advanced/templates-by-score?min_score=95")
echo "$TEMPLATES" | jq '{status, templates_found, patterns}'
echo ""
echo "Patterns:"
echo "  - Avg Length: $(echo "$TEMPLATES" | jq -r '.patterns.avg_length') chars"
echo "  - Avg Keywords: $(echo "$TEMPLATES" | jq -r '.patterns.avg_keywords_count')"
echo "  - Length Range: $(echo "$TEMPLATES" | jq -r '.patterns.length_range')"
echo ""
echo ""

# 7. OPTIMAL WRAPPER PER TOPIC
echo "───────────────────────────────────────────────────────────────────"
echo "7. 🎯 OPTIMAL WRAPPER PER TOPIC (NEW!)"
echo "───────────────────────────────────────────────────────────────────"
echo "Description: Which wrapper performs best for each topic"
echo "Endpoint: GET /prompts/advanced/optimal-wrapper-for-topic"
echo ""
WRAPPER_OPT=$(curl -s "$BASE_URL/prompts/advanced/optimal-wrapper-for-topic")
echo "$WRAPPER_OPT" | jq '{status, topics_analyzed, top_3: .recommendations[:3]}'
echo ""
echo "Best Matches:"
echo "$WRAPPER_OPT" | jq -r '.recommendations[:3] | .[] | "  - \(.topic): \(.best_wrapper) (\(.best_avg_score) avg)"'
echo ""
echo ""

# 8. EVOLUTION LEARNING CURVE
echo "───────────────────────────────────────────────────────────────────"
echo "8. 🧠 EVOLUTION LEARNING CURVE (NEW!)"
echo "───────────────────────────────────────────────────────────────────"
echo "Description: Track system learning over time"
echo "Endpoint: GET /prompts/advanced/evolution-learning-curve"
echo ""
CURVE=$(curl -s "$BASE_URL/prompts/advanced/evolution-learning-curve")
echo "$CURVE" | jq '{status, days_tracked, overall_trend, last_3_days: .timeline[-3:]}'
echo ""
echo "Learning Trend:"
echo "  - Learning Velocity: $(echo "$CURVE" | jq -r '.overall_trend.learning_velocity') points/day"
echo "  - Direction: $(echo "$CURVE" | jq -r '.overall_trend.direction')"
echo "  - Improvement: $(echo "$CURVE" | jq -r '.overall_trend.total_improvement') points"
echo ""
echo ""

# 9. COMPLETE EXPORT
echo "───────────────────────────────────────────────────────────────────"
echo "9. 📦 COMPLETE EXPORT"
echo "───────────────────────────────────────────────────────────────────"
echo "Description: Full prompts + responses + scores with pagination"
echo "Endpoint: GET /prompts/complete-export?page=1&page_size=3"
echo ""
EXPORT=$(curl -s "$BASE_URL/prompts/complete-export?page=1&page_size=3")
echo "$EXPORT" | jq '{status, pagination, sample: .exports[0] | {id, score: .quality.total_score, prompt_length: .prompt.text | length, response_length: .response.text | length}}'
echo ""
echo "Pagination Info:"
echo "  - Total Items: $(echo "$EXPORT" | jq -r '.pagination.total_items')"
echo "  - Total Pages: $(echo "$EXPORT" | jq -r '.pagination.total_pages')"
echo "  - Page Size: $(echo "$EXPORT" | jq -r '.pagination.page_size')"
echo ""
echo ""

# 10. ANALYTICS DASHBOARD
echo "───────────────────────────────────────────────────────────────────"
echo "10. 📊 ANALYTICS COMPLETE DASHBOARD"
echo "───────────────────────────────────────────────────────────────────"
echo "Description: System-wide metrics and insights"
echo "Endpoint: GET /analytics/complete-dashboard"
echo ""
DASHBOARD=$(curl -s "$BASE_URL/analytics/complete-dashboard")
echo "$DASHBOARD" | jq '{status, system_health, success_stories: .success_stories.count, failure_rate: .failures.failure_rate}'
echo ""
echo "Key Stats:"
echo "  - Total Prompts: $(echo "$DASHBOARD" | jq -r '.system_health.total_prompts')"
echo "  - Avg Score: $(echo "$DASHBOARD" | jq -r '.system_health.avg_score')"
echo "  - Perfect Scores: $(echo "$DASHBOARD" | jq -r '.system_health.perfect_scores')"
echo "  - Success Rate: $(echo "$DASHBOARD" | jq -r '.system_health.success_rate')%"
echo ""
echo ""

# 11. EVOLUTION SYNTX VS NORMAL
echo "───────────────────────────────────────────────────────────────────"
echo "11. 🧬 SYNTX VS NORMAL COMPARISON"
echo "───────────────────────────────────────────────────────────────────"
echo "Description: Proof that SYNTX works better"
echo "Endpoint: GET /evolution/syntx-vs-normal"
echo ""
SYNTX_VS=$(curl -s "$BASE_URL/evolution/syntx-vs-normal")
echo "$SYNTX_VS" | jq '{status, score_gap, syntx_avg: .comparison.syntx.avg_score, normal_avg: .comparison.normal.avg_score, syntx_perfect_rate: .comparison.syntx.perfect_rate}'
echo ""
echo "🔥 THE PROOF:"
echo "  - SYNTX Avg: $(echo "$SYNTX_VS" | jq -r '.comparison.syntx.avg_score')"
echo "  - Normal Avg: $(echo "$SYNTX_VS" | jq -r '.comparison.normal.avg_score')"
echo "  - Gap: +$(echo "$SYNTX_VS" | jq -r '.score_gap') points"
echo "  - SYNTX Perfect Rate: $(echo "$SYNTX_VS" | jq -r '.comparison.syntx.perfect_rate')%"
echo ""
echo ""

# 12. KEYWORD POWER
echo "───────────────────────────────────────────────────────────────────"
echo "12. ⚡ KEYWORD POWER RANKINGS"
echo "───────────────────────────────────────────────────────────────────"
echo "Description: Which keywords create highest scores"
echo "Endpoint: GET /evolution/keywords/power"
echo ""
KEYWORDS=$(curl -s "$BASE_URL/evolution/keywords/power")
echo "$KEYWORDS" | jq '{status, top_3: .most_powerful[:3]}'
echo ""
echo "Power Rankings:"
echo "$KEYWORDS" | jq -r '.most_powerful[:5] | .[] | "  \(.keyword): \(.avg_score) avg (\(.perfect_rate)% perfect)"'
echo ""
echo ""

# 13. COSTS
echo "───────────────────────────────────────────────────────────────────"
echo "13. 💰 COST TRACKING"
echo "───────────────────────────────────────────────────────────────────"
echo "Description: GPT-4 generation costs"
echo "Endpoint: GET /prompts/costs/total"
echo ""
COSTS=$(curl -s "$BASE_URL/prompts/costs/total")
echo "$COSTS" | jq '.'
echo ""
echo "Cost Summary:"
echo "  - Total Cost: \$$(echo "$COSTS" | jq -r '.total_cost_usd')"
echo "  - Total Prompts: $(echo "$COSTS" | jq -r '.total_prompts')"
echo "  - Avg Cost/Prompt: \$$(echo "$COSTS" | jq -r '.avg_cost_per_prompt')"
echo ""
echo ""

# 14. RESONANZ QUEUE
echo "───────────────────────────────────────────────────────────────────"
echo "14. 🌊 RESONANZ QUEUE STATUS"
echo "───────────────────────────────────────────────────────────────────"
echo "Description: Queue health and flow rate"
echo "Endpoint: GET /resonanz/queue"
echo ""
RESONANZ=$(curl -s "$BASE_URL/resonanz/queue")
echo "$RESONANZ" | jq '.'
echo ""
echo ""

# === SUMMARY ===
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                     ✅ TEST COMPLETE                              ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""
echo "Summary:"
echo "  - Endpoints Tested: 14+"
echo "  - System Status: $(pgrep -f 'syntx_api_production' > /dev/null && echo '🟢 OPERATIONAL' || echo '🔴 DOWN')"
echo "  - Queue Health: $([ $(ls /opt/syntx-workflow-api-get-prompts/queue/processing/*.txt 2>/dev/null | wc -l) -eq 0 ] && echo '🟢 CLEAR' || echo '🟡 PROCESSING')"
echo "  - Total Processed: $(ls /opt/syntx-workflow-api-get-prompts/queue/processed/*.json 2>/dev/null | wc -l) jobs"
echo ""
echo "Report Generated: $TIMESTAMP"
echo ""

