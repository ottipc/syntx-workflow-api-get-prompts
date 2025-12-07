"""
SYNTX Compare Topics
"""

from fastapi import APIRouter
import sys
sys.path.append('/opt/syntx-workflow-api-get-prompts/api-core')

from utils.log_loader import load_field_flow

router = APIRouter(prefix="/compare", tags=["compare"])

@router.get("/topics/{topic1}/{topic2}")
async def compare_two_topics(topic1: str, topic2: str):
    """Compare two topics"""
    entries = load_field_flow()
    
    t1_data = {"scores": [], "wrappers": []}
    t2_data = {"scores": [], "wrappers": []}
    
    for e in entries:
        topic = e.get('topic', '').lower()
        score = e.get('quality_score', {}).get('total_score')
        wrapper = e.get('wrapper')
        
        if topic == topic1.lower() and score is not None:
            t1_data["scores"].append(score)
            if wrapper:
                t1_data["wrappers"].append(wrapper)
        elif topic == topic2.lower() and score is not None:
            t2_data["scores"].append(score)
            if wrapper:
                t2_data["wrappers"].append(wrapper)
    
    if not t1_data["scores"] or not t2_data["scores"]:
        return {"status": "INSUFFICIENT_DATA"}
    
    t1_avg = sum(t1_data["scores"]) / len(t1_data["scores"])
    t2_avg = sum(t2_data["scores"]) / len(t2_data["scores"])
    
    from collections import Counter
    
    return {
        "status": "TOPIC_COMPARISON_AKTIV",
        "comparison": {
            topic1: {
                "avg_score": round(t1_avg, 2),
                "total_jobs": len(t1_data["scores"]),
                "wrapper_distribution": dict(Counter(t1_data["wrappers"]))
            },
            topic2: {
                "avg_score": round(t2_avg, 2),
                "total_jobs": len(t2_data["scores"]),
                "wrapper_distribution": dict(Counter(t2_data["wrappers"]))
            },
            "better_topic": topic1 if t1_avg > t2_avg else topic2,
            "score_difference": round(abs(t1_avg - t2_avg), 2)
        }
    }
