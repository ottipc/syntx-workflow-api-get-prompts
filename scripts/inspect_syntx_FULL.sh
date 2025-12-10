#!/bin/bash

# SYNTX API ULTIMATE COMPREHENSIVE TEST
# FULL PAYLOADS, ALL METRICS, COMPLETE SYSTEM STATE
# Save output to file: ./scripts/inspect_syntx_FULL.sh > system_report.json 2>&1

BASE_URL="https://dev.syntx-system.com"

echo "{"
echo "  \"test_timestamp\": \"$(date -Iseconds)\","
echo "  \"test_description\": \"Complete SYNTX system analysis - all endpoints, full payloads\","
echo "  \"endpoints\": {"

# === 1. HEALTH ===
echo "    \"health\": $(curl -s "$BASE_URL/health"),"

# === 2. LIVE QUEUE MONITOR ===
echo "    \"monitoring_live_queue\": $(curl -s "$BASE_URL/monitoring/live-queue"),"

# === 3. PREDICT SCORE ===
echo "    \"predict_score_test\": $(curl -s -X POST "$BASE_URL/prompts/advanced/predict-score" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt_text": "**Meta-Prompt mit TIER-1 und TIER-2 Analyse** Beschreibe den Driftkörper in allen Facetten. Analysiere die Kalibrierung des Systems. Zeige die Strömung der Resonanzfelder. Erkläre die Struktur und den Mechanismus.",
    "topic": "technologie",
    "style": "kreativ"
  }'),"

# === 4. FIELD MISSING ANALYSIS ===
echo "    \"field_missing_analysis\": $(curl -s "$BASE_URL/prompts/advanced/fields-missing-analysis"),"

# === 5. KEYWORD COMBINATIONS ===
echo "    \"keyword_combinations\": $(curl -s "$BASE_URL/prompts/advanced/keyword-combinations"),"

# === 6. TEMPLATES BY SCORE ===
echo "    \"templates_score_90\": $(curl -s "$BASE_URL/prompts/advanced/templates-by-score?min_score=90"),"
echo "    \"templates_score_95\": $(curl -s "$BASE_URL/prompts/advanced/templates-by-score?min_score=95"),"

# === 7. OPTIMAL WRAPPER ===
echo "    \"optimal_wrapper_per_topic\": $(curl -s "$BASE_URL/prompts/advanced/optimal-wrapper-for-topic"),"

# === 8. EVOLUTION LEARNING CURVE ===
echo "    \"evolution_learning_curve\": $(curl -s "$BASE_URL/prompts/advanced/evolution-learning-curve"),"

# === 9. COMPLETE EXPORT (samples) ===
echo "    \"complete_export_page1\": $(curl -s "$BASE_URL/prompts/complete-export?page=1&page_size=3"),"
echo "    \"complete_export_high_scores\": $(curl -s "$BASE_URL/prompts/complete-export?min_score=95&page_size=5"),"

# === 10. TABLE VIEW ===
echo "    \"table_view_top10\": $(curl -s "$BASE_URL/prompts/table-view?limit=10"),"

# === 11. PROMPTS ALL ===
echo "    \"prompts_all_sample\": $(curl -s "$BASE_URL/prompts/all?limit=5"),"

# === 12. PROMPTS BEST ===
echo "    \"prompts_best\": $(curl -s "$BASE_URL/prompts/best?limit=10"),"

# === 13. FIELD BREAKDOWN ===
echo "    \"prompts_field_breakdown\": $(curl -s "$BASE_URL/prompts/fields/breakdown"),"

# === 14. COSTS TOTAL ===
echo "    \"prompts_costs_total\": $(curl -s "$BASE_URL/prompts/costs/total"),"

# === 15. SEARCH ===
echo "    \"prompts_search_tier\": $(curl -s "$BASE_URL/prompts/search?q=tier"),"
echo "    \"prompts_search_drift\": $(curl -s "$BASE_URL/prompts/search?q=drift"),"

# === 16. ANALYTICS DASHBOARD ===
echo "    \"analytics_complete_dashboard\": $(curl -s "$BASE_URL/analytics/complete-dashboard"),"

# === 17. ANALYTICS OVERVIEW ===
echo "    \"analytics_overview\": $(curl -s "$BASE_URL/analytics/overview"),"

# === 18. ANALYTICS TOPICS ===
echo "    \"analytics_topics\": $(curl -s "$BASE_URL/analytics/topics"),"

# === 19. ANALYTICS SCORES DISTRIBUTION ===
echo "    \"analytics_scores_distribution\": $(curl -s "$BASE_URL/analytics/scores/distribution"),"

# === 20. ANALYTICS SUCCESS RATE ===
echo "    \"analytics_success_rate\": $(curl -s "$BASE_URL/analytics/success-rate"),"
echo "    \"analytics_success_rate_by_wrapper\": $(curl -s "$BASE_URL/analytics/success-rate/by-wrapper"),"

# === 21. EVOLUTION SYNTX VS NORMAL ===
echo "    \"evolution_syntx_vs_normal\": $(curl -s "$BASE_URL/evolution/syntx-vs-normal"),"

# === 22. EVOLUTION KEYWORDS POWER ===
echo "    \"evolution_keywords_power\": $(curl -s "$BASE_URL/evolution/keywords/power"),"

# === 23. EVOLUTION TOPICS RESONANCE ===
echo "    \"evolution_topics_resonance\": $(curl -s "$BASE_URL/evolution/topics/resonance"),"

# === 24. COMPARE WRAPPERS ===
echo "    \"compare_wrappers\": $(curl -s "$BASE_URL/compare/wrappers"),"

# === 25. FELD DRIFT ===
echo "    \"feld_drift\": $(curl -s "$BASE_URL/feld/drift"),"

# === 26. RESONANZ QUEUE ===
echo "    \"resonanz_queue\": $(curl -s "$BASE_URL/resonanz/queue"),"

# === 27. RESONANZ SYSTEM ===
echo "    \"resonanz_system\": $(curl -s "$BASE_URL/resonanz/system"),"

# === 28. GENERATION PROGRESS ===
echo "    \"generation_progress\": $(curl -s "$BASE_URL/generation/progress")"

echo "  },"

# === SYSTEM STATE ===
echo "  \"system_state\": {"
echo "    \"queue_incoming_count\": $(ls /opt/syntx-workflow-api-get-prompts/queue/incoming/*.txt 2>/dev/null | grep -v response | wc -l),"
echo "    \"queue_processing_count\": $(ls /opt/syntx-workflow-api-get-prompts/queue/processing/*.txt 2>/dev/null | wc -l),"
echo "    \"queue_processed_count\": $(ls /opt/syntx-workflow-api-get-prompts/queue/processed/*.json 2>/dev/null | wc -l),"
echo "    \"queue_error_count\": $(ls /opt/syntx-workflow-api-get-prompts/queue/error/*.txt 2>/dev/null | wc -l),"
echo "    \"disk_usage\": \"$(du -sh /opt/syntx-workflow-api-get-prompts | cut -f1)\","
echo "    \"api_process_running\": $(pgrep -f 'syntx_api_production' > /dev/null && echo 'true' || echo 'false'),"
echo "    \"crontab_jobs\": $(crontab -l | grep syntx | wc -l)"
echo "  },"

# === GIT STATE ===
echo "  \"git_state\": {"
echo "    \"current_branch\": \"$(cd /opt/syntx-workflow-api-get-prompts && git branch --show-current)\","
echo "    \"last_commit\": \"$(cd /opt/syntx-workflow-api-get-prompts && git log -1 --oneline)\","
echo "    \"uncommitted_changes\": $(cd /opt/syntx-workflow-api-get-prompts && git status --short | wc -l),"
echo "    \"total_commits\": $(cd /opt/syntx-workflow-api-get-prompts && git rev-list --count HEAD)"
echo "  },"

# === LOG STATS ===
echo "  \"logs_state\": {"
echo "    \"costs_log_lines\": $(wc -l < /opt/syntx-workflow-api-get-prompts/logs/costs.jsonl 2>/dev/null || echo 0),"
echo "    \"gpt_prompts_log_lines\": $(wc -l < /opt/syntx-workflow-api-get-prompts/logs/gpt_prompts.jsonl 2>/dev/null || echo 0),"
echo "    \"syntex_calibrations_log_lines\": $(wc -l < /opt/syntx-workflow-api-get-prompts/logs/syntex_calibrations.jsonl 2>/dev/null || echo 0),"
echo "    \"syntex_progress_log_lines\": $(wc -l < /opt/syntx-workflow-api-get-prompts/logs/syntex_progress.jsonl 2>/dev/null || echo 0)"
echo "  }"

echo "}"

