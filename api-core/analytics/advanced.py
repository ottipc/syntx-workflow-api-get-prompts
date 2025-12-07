"""
SYNTX Advanced Analytics
Predictions, Trends, Outliers
"""

from fastapi import APIRouter, Query
import sys
sys.path.append('/opt/syntx-workflow-api-get-prompts/api-core')

from utils.log_loader import load_field_flow
from utils.algorithms import (
    calculate_moving_average,
    detect_outliers,
    calculate_trend,
    predict_next_value,
    calculate_velocity
)
from collections import defaultdict
from datetime import datetime, timedelta

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/trends")
async def get_trends():
    """📈 Quality Trends with Predictions"""
    entries = load_field_flow()
    
    scores = []
    timestamps = []
    for e in entries:
        qs = e.get('quality_score')
        if qs and isinstance(qs, dict):
            score = qs.get('total_score')
            if score is not None:
                scores.append(score)
                timestamps.append(e.get('timestamp'))
    
    if len(scores) < 5:
        return {"status": "INSUFFICIENT_DATA"}
    
    # Moving average
    ma = calculate_moving_average(scores, window=5)
    
    # Trend
    trend = calculate_trend(scores)
    
    # Velocity (change rate)
    velocity = calculate_velocity(scores)
    
    # Prediction
    prediction = predict_next_value(scores)
    
    # Outliers
    outlier_indices = detect_outliers(scores)
    
    return {
        "status": "TRENDS_AKTIV",
        "current_avg": round(sum(scores[-10:]) / 10, 2) if len(scores) >= 10 else round(sum(scores) / len(scores), 2),
        "trend": trend,
        "velocity": round(velocity, 2),
        "predicted_next": round(prediction, 2),
        "moving_average": [round(v, 2) for v in ma[-20:]],
        "outliers": {
            "count": len(outlier_indices),
            "indices": outlier_indices[-10:]
        },
        "total_samples": len(scores)
    }

@router.get("/performance")
async def get_performance():
    """⚡ Processing Performance Analysis"""
    entries = load_field_flow()
    
    durations = []
    by_wrapper = defaultdict(list)
    
    for e in entries:
        duration = e.get('duration_ms')
        wrapper = e.get('wrapper', 'unknown')
        if duration:
            durations.append(duration)
            by_wrapper[wrapper].append(duration)
    
    if not durations:
        return {"status": "NO_DATA"}
    
    avg_duration = sum(durations) / len(durations)
    
    # Detect slow jobs (outliers)
    outliers = detect_outliers(durations, threshold=2.5)
    
    wrapper_performance = {}
    for wrapper, durs in by_wrapper.items():
        wrapper_performance[wrapper] = {
            "avg_ms": round(sum(durs) / len(durs), 2),
            "min_ms": min(durs),
            "max_ms": max(durs),
            "count": len(durs)
        }
    
    return {
        "status": "PERFORMANCE_AKTIV",
        "gesamt": {
            "avg_duration_ms": round(avg_duration, 2),
            "min_ms": min(durations),
            "max_ms": max(durations),
            "total_jobs": len(durations)
        },
        "by_wrapper": wrapper_performance,
        "bottlenecks": {
            "slow_jobs_detected": len(outliers),
            "threshold_ms": round(avg_duration * 2, 2)
        }
    }

@router.get("/correlation/topic-score")
async def get_topic_score_correlation():
    """🔗 Topic vs Score Correlation"""
    entries = load_field_flow()
    
    by_topic = defaultdict(list)
    
    for e in entries:
        topic = e.get('topic', 'unknown')
        qs = e.get('quality_score')
        if qs and isinstance(qs, dict):
            score = qs.get('total_score')
            if score is not None:
                by_topic[topic].append(score)
    
    correlations = {}
    overall_avg = sum([s for scores in by_topic.values() for s in scores]) / sum([len(scores) for scores in by_topic.values()])
    
    for topic, scores in by_topic.items():
        if len(scores) >= 3:
            topic_avg = sum(scores) / len(scores)
            deviation = topic_avg - overall_avg
            
            correlations[topic] = {
                "avg_score": round(topic_avg, 2),
                "count": len(scores),
                "deviation_from_mean": round(deviation, 2),
                "correlation": "POSITIVE" if deviation > 5 else "NEGATIVE" if deviation < -5 else "NEUTRAL"
            }
    
    # Sort by deviation
    sorted_topics = dict(sorted(correlations.items(), key=lambda x: x[1]['deviation_from_mean'], reverse=True))
    
    return {
        "status": "CORRELATION_AKTIV",
        "overall_avg": round(overall_avg, 2),
        "correlations": sorted_topics
    }

@router.get("/outliers")
async def get_outliers():
    """🎯 Detect Statistical Outliers"""
    entries = load_field_flow()
    
    scores = []
    job_ids = []
    
    for e in entries:
        qs = e.get('quality_score')
        if qs and isinstance(qs, dict):
            score = qs.get('total_score')
            if score is not None:
                scores.append(score)
                job_ids.append(e.get('job_id'))
    
    if len(scores) < 10:
        return {"status": "INSUFFICIENT_DATA"}
    
    outlier_indices = detect_outliers(scores, threshold=2.0)
    
    outlier_jobs = []
    for idx in outlier_indices:
        if idx < len(job_ids):
            outlier_jobs.append({
                "job_id": job_ids[idx],
                "score": scores[idx],
                "index": idx
            })
    
    return {
        "status": "OUTLIERS_DETECTED",
        "total_jobs": len(scores),
        "outliers_found": len(outlier_jobs),
        "outliers": outlier_jobs[-20:],  # Last 20
        "mean_score": round(sum(scores) / len(scores), 2)
    }
