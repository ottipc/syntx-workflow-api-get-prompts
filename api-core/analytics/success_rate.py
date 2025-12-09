"""
SYNTX Success Rate Analytics
"""

from fastapi import APIRouter
import sys
sys.path.append('/opt/syntx-workflow-api-get-prompts/api-core')

from utils.log_loader import load_field_flow
from collections import Counter

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/success-rate")
async def get_success_rate():
    """Overall Success Rate"""
    entries = load_field_flow()
    
    scores = [e.get('quality_score', {}).get('total_score', 0) for e in entries if e.get('quality_score')]
    
    if not scores:
        return {"status": "NO_DATA", "success_rate": 0}
    
    total = len(scores)
    perfect = len([s for s in scores if s == 100])
    good = len([s for s in scores if 80 <= s < 100])
    medium = len([s for s in scores if 50 <= s < 80])
    low = len([s for s in scores if s < 50])
    
    return {
        "status": "SUCCESS_RATE_AKTIV",
        "gesamt_jobs": total,
        "success_rate": round(perfect / total * 100, 2),
        "verteilung": {
            "perfekt_100": {"count": perfect, "prozent": round(perfect / total * 100, 2)},
            "gut_80_99": {"count": good, "prozent": round(good / total * 100, 2)},
            "mittel_50_79": {"count": medium, "prozent": round(medium / total * 100, 2)},
            "niedrig_0_49": {"count": low, "prozent": round(low / total * 100, 2)}
        }
    }

@router.get("/success-rate/by-wrapper")
async def get_success_rate_by_wrapper():
    """Success Rate per Wrapper"""
    entries = load_field_flow()
    
    by_wrapper = {}
    for e in entries:
        wrapper = e.get('wrapper', 'unknown')
        quality_score = e.get("quality_score")
        score_raw = quality_score.get("total_score") if quality_score else None
        
        if score_raw is not None:
            try:
                score = int(score_raw)
            except (TypeError, ValueError):
                continue # Skip data that can't be converted to int
            
            if wrapper not in by_wrapper:
                by_wrapper[wrapper] = []
            by_wrapper[wrapper].append(score)
    
    results = {}
    for wrapper, scores in by_wrapper.items():
        total = len(scores)
        perfect = len([s for s in scores if s == 100])
        results[wrapper] = {
            "total_jobs": total,
            "success_rate": round(perfect / total * 100, 2) if total > 0 else 0,
            "avg_score": round(sum(scores) / total, 2) if total > 0 else 0
        }
    
    return {
        "status": "SUCCESS_RATE_BY_WRAPPER_AKTIV",
        "wrappers": results
    }

@router.get("/success-rate/by-topic")
async def get_success_rate_by_topic():
    """Success Rate per Topic"""
    entries = load_field_flow()
    
    by_topic = {}
    for e in entries:
        topic = e.get('topic', 'unknown')
        score_raw = e.get('quality_score', {}).get('total_score')
        
        if score_raw is not None:
            try:
                score = int(score_raw)
            except (TypeError, ValueError):
                continue # Skip data that can't be converted to int

            if topic not in by_topic:
                by_topic[topic] = []
            by_topic[topic].append(score)
    
    results = {}
    for topic, scores in by_topic.items():
        total = len(scores)
        perfect = len([s for s in scores if s == 100])
        results[topic] = {
            "total_jobs": total,
            "success_rate": round(perfect / total * 100, 2) if total > 0 else 0,
            "avg_score": round(sum(scores) / total, 2) if total > 0 else 0
        }
    
    # Sort by success rate
    results = dict(sorted(results.items(), key=lambda x: x[1]['success_rate'], reverse=True))
    
    return {
        "status": "SUCCESS_RATE_BY_TOPIC_AKTIV",
        "topics": results
    }
