"""
SYNTX Analytics Dashboard
"""

from fastapi import APIRouter
import sys
sys.path.append('/opt/syntx-workflow-api-get-prompts/api-core')

from utils.log_loader import load_field_flow, load_evolution, get_queue_counts
from utils.algorithms import calculate_health_score, calculate_trend
from collections import Counter

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/dashboard")
async def get_dashboard():
    """📊 Dashboard Summary"""
    entries = load_field_flow(limit=100)
    generations = load_evolution()
    queue = get_queue_counts()
    
    scores = [e.get('quality_score', {}).get('total_score', 0) for e in entries if e.get('quality_score')]
    avg_score = sum(scores) / len(scores) if scores else 0
    
    perfect = len([s for s in scores if s == 100])
    success_rate = (perfect / len(scores) * 100) if scores else 0
    
    topics = Counter([e.get('topic') for e in entries if e.get('topic')])
    wrappers = Counter([e.get('wrapper') for e in entries if e.get('wrapper')])
    
    recent_scores = scores[-10:] if len(scores) > 10 else scores
    trend = calculate_trend(recent_scores)
    
    metrics = {
        "queue_health": 100 - (queue['incoming'] / 200 * 100),
        "quality": avg_score,
        "success_rate": success_rate,
        "evolution": len(generations) * 10
    }
    weights = {"queue_health": 0.2, "quality": 0.4, "success_rate": 0.3, "evolution": 0.1}
    health = calculate_health_score(metrics, weights)
    
    return {
        "status": "DASHBOARD_AKTIV",
        "gesamt_health": round(health, 2),
        "queue": queue,
        "qualität": {
            "durchschnitt": round(avg_score, 2),
            "success_rate": round(success_rate, 2),
            "trend": trend
        },
        "aktivität": {
            "total_jobs": len(entries),
            "generationen": len(generations),
            "top_topics": dict(topics.most_common(5)),
            "wrappers": dict(wrappers)
        }
    }
