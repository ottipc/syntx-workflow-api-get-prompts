"""
SYNTX Compare Wrappers - FIXED
"""

from fastapi import APIRouter
import sys
sys.path.append('/opt/syntx-workflow-api-get-prompts/api-core')

from utils.log_loader import load_field_flow
from collections import Counter

router = APIRouter(prefix="/compare", tags=["compare"])

@router.get("/wrappers")
async def compare_all_wrappers():
    """Compare all wrappers"""
    entries = load_field_flow()
    
    by_wrapper = {}
    for e in entries:
        wrapper = e.get('wrapper', 'unknown')
        if wrapper not in by_wrapper:
            by_wrapper[wrapper] = {
                "scores": [],
                "topics": [],
                "durations": []
            }
        
        # Handle None quality_score
        qs = e.get('quality_score')
        if qs and isinstance(qs, dict):
            score = qs.get('total_score')
            if score is not None:
                by_wrapper[wrapper]["scores"].append(score)
        
        topic = e.get('topic')
        if topic:
            by_wrapper[wrapper]["topics"].append(topic)
        
        duration = e.get('duration_ms')
        if duration:
            by_wrapper[wrapper]["durations"].append(duration)
    
    comparison = {}
    for wrapper, data in by_wrapper.items():
        scores = data["scores"]
        durations = data["durations"]
        
        comparison[wrapper] = {
            "total_jobs": len(scores) if scores else 0,
            "avg_score": round(sum(scores) / len(scores), 2) if scores else 0,
            "success_rate": round(len([s for s in scores if s == 100]) / len(scores) * 100, 2) if scores else 0,
            "avg_duration_ms": round(sum(durations) / len(durations), 2) if durations else 0,
            "top_topics": dict(Counter(data["topics"]).most_common(5))
        }
    
    return {
        "status": "WRAPPER_COMPARISON_AKTIV",
        "wrappers": comparison
    }

@router.get("/wrappers/{wrapper1}/{wrapper2}")
async def compare_two_wrappers(wrapper1: str, wrapper2: str):
    """Compare two wrappers"""
    entries = load_field_flow()
    
    w1_data = {"scores": [], "durations": []}
    w2_data = {"scores": [], "durations": []}
    
    for e in entries:
        wrapper = e.get('wrapper', '').lower()
        
        # Handle None quality_score
        qs = e.get('quality_score')
        score = None
        if qs and isinstance(qs, dict):
            score = qs.get('total_score')
        
        duration = e.get('duration_ms')
        
        if wrapper == wrapper1.lower() and score is not None:
            w1_data["scores"].append(score)
            if duration:
                w1_data["durations"].append(duration)
        elif wrapper == wrapper2.lower() and score is not None:
            w2_data["scores"].append(score)
            if duration:
                w2_data["durations"].append(duration)
    
    if not w1_data["scores"] or not w2_data["scores"]:
        return {"status": "INSUFFICIENT_DATA"}
    
    w1_avg = sum(w1_data["scores"]) / len(w1_data["scores"])
    w2_avg = sum(w2_data["scores"]) / len(w2_data["scores"])
    
    return {
        "status": "WRAPPER_COMPARISON_AKTIV",
        "comparison": {
            wrapper1: {
                "avg_score": round(w1_avg, 2),
                "total_jobs": len(w1_data["scores"]),
                "avg_duration_ms": round(sum(w1_data["durations"]) / len(w1_data["durations"]), 2) if w1_data["durations"] else 0
            },
            wrapper2: {
                "avg_score": round(w2_avg, 2),
                "total_jobs": len(w2_data["scores"]),
                "avg_duration_ms": round(sum(w2_data["durations"]) / len(w2_data["durations"]), 2) if w2_data["durations"] else 0
            },
            "winner": wrapper1 if w1_avg > w2_avg else wrapper2,
            "difference": round(abs(w1_avg - w2_avg), 2)
        }
    }
