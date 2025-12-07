"""
SYNTX Performance Analytics
Detailed performance tracking
"""

from fastapi import APIRouter, Query
import sys
sys.path.append('/opt/syntx-workflow-api-get-prompts/api-core')

from utils.log_loader import load_field_flow
from collections import defaultdict
from datetime import datetime, timedelta

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/performance/by-topic")
async def get_performance_by_topic():
    """📊 Performance breakdown by topic"""
    entries = load_field_flow()
    
    by_topic = defaultdict(lambda: {"durations": [], "scores": [], "count": 0})
    
    for e in entries:
        topic = e.get('topic', 'unknown')
        duration = e.get('duration_ms')
        
        qs = e.get('quality_score')
        score = None
        if qs and isinstance(qs, dict):
            score = qs.get('total_score')
        
        by_topic[topic]["count"] += 1
        if duration:
            by_topic[topic]["durations"].append(duration)
        if score is not None:
            by_topic[topic]["scores"].append(score)
    
    results = {}
    for topic, data in by_topic.items():
        durs = data["durations"]
        scores = data["scores"]
        
        results[topic] = {
            "total_jobs": data["count"],
            "avg_duration_ms": round(sum(durs) / len(durs), 2) if durs else 0,
            "avg_score": round(sum(scores) / len(scores), 2) if scores else 0,
            "efficiency_ratio": round((sum(scores) / len(scores)) / (sum(durs) / len(durs)) * 1000, 4) if durs and scores else 0
        }
    
    # Sort by efficiency
    sorted_results = dict(sorted(results.items(), key=lambda x: x[1]['efficiency_ratio'], reverse=True))
    
    return {
        "status": "PERFORMANCE_BY_TOPIC_AKTIV",
        "topics": sorted_results
    }

@router.get("/performance/hourly")
async def get_performance_hourly():
    """⏰ Performance by hour of day"""
    entries = load_field_flow()
    
    by_hour = defaultdict(lambda: {"durations": [], "scores": [], "count": 0})
    
    for e in entries:
        timestamp = e.get('timestamp')
        if not timestamp:
            continue
        
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            hour = dt.hour
        except:
            continue
        
        duration = e.get('duration_ms')
        qs = e.get('quality_score')
        score = None
        if qs and isinstance(qs, dict):
            score = qs.get('total_score')
        
        by_hour[hour]["count"] += 1
        if duration:
            by_hour[hour]["durations"].append(duration)
        if score is not None:
            by_hour[hour]["scores"].append(score)
    
    hourly_data = []
    for hour in range(24):
        if hour in by_hour:
            data = by_hour[hour]
            durs = data["durations"]
            scores = data["scores"]
            
            hourly_data.append({
                "hour": hour,
                "jobs": data["count"],
                "avg_duration_ms": round(sum(durs) / len(durs), 2) if durs else 0,
                "avg_score": round(sum(scores) / len(scores), 2) if scores else 0
            })
    
    return {
        "status": "HOURLY_PERFORMANCE_AKTIV",
        "data": hourly_data
    }
