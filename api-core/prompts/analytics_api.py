"""
SYNTX Analytics API
Deep insights into system performance
"""
from fastapi import APIRouter, Query
from pathlib import Path
import json
from typing import Optional, Dict, List
from collections import defaultdict, Counter
from datetime import datetime

router = APIRouter(prefix="/analytics", tags=["analytics"])

QUEUE_DIR = Path("/opt/syntx-workflow-api-get-prompts/queue")
LOGS_DIR = Path("/opt/syntx-workflow-api-get-prompts/logs")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def load_all_processed() -> List[Dict]:
    """Load all processed prompts - SAFE VERSION"""
    processed = []
    processed_dir = QUEUE_DIR / "processed"
    
    if not processed_dir.exists():
        return processed
    
    for file in processed_dir.glob("*.json"):
        try:
            with open(file) as f:
                data = json.load(f)
                if data is not None and isinstance(data, dict):  # SAFE CHECK
                    processed.append(data)
        except Exception as e:
            print(f"⚠️ Error loading {file}: {e}")
            continue
    
    return processed

def safe_get_score(prompt: Dict) -> float:
    """Safely extract score from prompt"""
    try:
        return prompt.get('syntex_result', {}).get('quality_score', {}).get('total_score', 0) or 0
    except:
        return 0

# ============================================================================
# OVERVIEW
# ============================================================================

@router.get("/overview")
async def analytics_overview():
    """Complete system overview"""
    processed = load_all_processed()
    
    if not processed:
        return {"status": "NO_DATA", "message": "Keine verarbeiteten Prompts gefunden"}
    
    scores = [safe_get_score(p) for p in processed]
    avg_score = sum(scores) / len(scores) if scores else 0
    perfect_scores = sum(1 for s in scores if s >= 98)
    topics = Counter(p.get('topic', 'unknown') for p in processed)
    languages = Counter(p.get('language', 'de') for p in processed)
    
    return {
        "status": "OVERVIEW_READY",
        "total_prompts": len(processed),
        "quality": {
            "average_score": round(avg_score, 2),
            "perfect_scores": perfect_scores,
            "perfect_rate": round(perfect_scores / len(processed) * 100, 2)
        },
        "topics": dict(topics.most_common(10)),
        "languages": dict(languages),
        "timestamp": datetime.now().isoformat()
    }

# ============================================================================
# TOPICS
# ============================================================================

@router.get("/topics")
async def analytics_topics():
    """Topic performance breakdown"""
    processed = load_all_processed()
    if not processed:
        return {"status": "NO_DATA"}
    
    topic_data = defaultdict(lambda: {"scores": [], "count": 0})
    for p in processed:
        topic = p.get('topic', 'unknown')
        score = safe_get_score(p)
        topic_data[topic]["scores"].append(score)
        topic_data[topic]["count"] += 1
    
    results = {}
    for topic, data in topic_data.items():
        scores = data["scores"]
        results[topic] = {
            "count": data["count"],
            "avg_score": round(sum(scores) / len(scores), 2),
            "perfect_count": sum(1 for s in scores if s >= 98),
            "min_score": min(scores),
            "max_score": max(scores)
        }
    
    sorted_results = dict(sorted(results.items(), key=lambda x: x[1]["avg_score"], reverse=True))
    
    return {
        "status": "TOPICS_ANALYZED",
        "total_topics": len(results),
        "topics": sorted_results
    }

@router.get("/topics/{topic_name}")
async def analytics_topic_detail(topic_name: str):
    """Detailed analysis for specific topic"""
    processed = load_all_processed()
    topic_prompts = [p for p in processed if p.get('topic') == topic_name]
    
    if not topic_prompts:
        return {"status": "TOPIC_NOT_FOUND", "topic": topic_name}
    
    scores = [safe_get_score(p) for p in topic_prompts]
    
    return {
        "status": "TOPIC_DETAIL",
        "topic": topic_name,
        "total_prompts": len(topic_prompts),
        "scores": {
            "average": round(sum(scores) / len(scores), 2),
            "min": min(scores),
            "max": max(scores),
            "perfect_count": sum(1 for s in scores if s >= 98)
        },
        "recent_prompts": topic_prompts[-5:]
    }

# ============================================================================
# SCORES
# ============================================================================

@router.get("/scores/distribution")
async def score_distribution():
    """Score distribution analysis"""
    processed = load_all_processed()
    if not processed:
        return {"status": "NO_DATA"}
    
    scores = [safe_get_score(p) for p in processed]
    
    buckets = {
        "0-20": 0, "20-40": 0, "40-60": 0, "60-80": 0,
        "80-90": 0, "90-95": 0, "95-98": 0, "98-100": 0
    }
    
    for score in scores:
        if score < 20: buckets["0-20"] += 1
        elif score < 40: buckets["20-40"] += 1
        elif score < 60: buckets["40-60"] += 1
        elif score < 80: buckets["60-80"] += 1
        elif score < 90: buckets["80-90"] += 1
        elif score < 95: buckets["90-95"] += 1
        elif score < 98: buckets["95-98"] += 1
        else: buckets["98-100"] += 1
    
    return {
        "status": "DISTRIBUTION_READY",
        "total_scores": len(scores),
        "distribution": buckets,
        "statistics": {
            "mean": round(sum(scores) / len(scores), 2),
            "median": sorted(scores)[len(scores) // 2],
            "mode": Counter(scores).most_common(1)[0][0] if scores else 0
        }
    }

@router.get("/scores/trends")
async def score_trends():
    """Score trends over time"""
    processed = load_all_processed()
    if not processed:
        return {"status": "NO_DATA"}
    
    sorted_prompts = sorted(processed, key=lambda x: x.get('timestamp', ''))
    daily_scores = defaultdict(list)
    
    for p in sorted_prompts:
        timestamp = p.get('timestamp', '')
        if timestamp:
            date = timestamp.split('T')[0]
            daily_scores[date].append(safe_get_score(p))
    
    trends = {}
    for date, scores in daily_scores.items():
        trends[date] = {
            "avg_score": round(sum(scores) / len(scores), 2),
            "count": len(scores),
            "perfect_count": sum(1 for s in scores if s >= 98)
        }
    
    return {
        "status": "TRENDS_READY",
        "total_days": len(trends),
        "daily_trends": dict(sorted(trends.items()))
    }

# ============================================================================
# COMPLETE DASHBOARD - ALLES AUF EINEN BLICK
# ============================================================================

@router.get("/complete-dashboard")
async def complete_dashboard():
    """
    🔥 COMPLETE SYNTX DASHBOARD
    Alles aggregiert: System Health, Quality, Keywords, Topics, Success Stories
    """
    processed = load_all_processed()
    
    if not processed:
        return {"status": "NO_DATA"}
    
    # SAFE: Filter None values
    processed = [p for p in processed if p is not None and isinstance(p, dict)]
    
    if not processed:
        return {"status": "NO_DATA_AFTER_FILTER"}
    
    total = len(processed)
    scores = [safe_get_score(p) for p in processed]
    avg_score = sum(scores) / len(scores) if scores else 0
    perfect_scores = sum(1 for s in scores if s >= 98)
    
    # Success stories (score >= 95)
    success_stories = []
    for p in processed:
        score = safe_get_score(p)
        if score >= 95:
            success_stories.append({
                'topic': p.get('topic', 'unknown'),
                'score': score,
                'style': p.get('style', 'unknown'),
                'timestamp': p.get('processed_at', '')
            })
    success_stories = sorted(success_stories, key=lambda x: x['score'], reverse=True)[:20]
    
    # Topics
    topic_data = defaultdict(lambda: {'scores': [], 'count': 0})
    for p in processed:
        topic = p.get('topic', 'unknown')
        score = safe_get_score(p)
        topic_data[topic]['scores'].append(score)
        topic_data[topic]['count'] += 1
    
    top_topics = {}
    for topic, data in topic_data.items():
        scores_list = data['scores']
        top_topics[topic] = {
            'count': data['count'],
            'avg_score': round(sum(scores_list) / len(scores_list), 2),
            'perfect_count': sum(1 for s in scores_list if s >= 98)
        }
    top_topics = dict(sorted(top_topics.items(), key=lambda x: x[1]['avg_score'], reverse=True)[:10])
    
    # Failures
    failures = [p for p in processed if safe_get_score(p) == 0]
    failure_topics = Counter(p.get('topic', 'unknown') for p in failures)
    
    return {
        "status": "COMPLETE_DASHBOARD",
        "timestamp": datetime.now().isoformat(),
        "system_health": {
            "total_prompts": total,
            "avg_score": round(avg_score, 2),
            "perfect_scores": perfect_scores,
            "perfect_rate": round(perfect_scores / total * 100, 2) if total > 0 else 0,
            "success_rate": round(len(success_stories) / total * 100, 2) if total > 0 else 0
        },
        "success_stories": {
            "count": len(success_stories),
            "examples": success_stories[:10]
        },
        "topics": {
            "top_performers": top_topics,
            "total_topics": len(topic_data)
        },
        "failures": {
            "count": len(failures),
            "failure_rate": round(len(failures) / total * 100, 2) if total > 0 else 0,
            "top_failing_topics": dict(failure_topics.most_common(5))
        }
    }
