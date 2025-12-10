"""
SYNTX Live Queue Monitor
Real-time system health tracking
"""

from fastapi import APIRouter
from pathlib import Path
import json
from datetime import datetime, timedelta

router = APIRouter(prefix="/monitoring", tags=["monitoring"])

QUEUE_DIR = Path("/opt/syntx-workflow-api-get-prompts/queue")

@router.get("/live-queue")
def live_queue_monitor():
    """
    🔥 LIVE QUEUE STATUS!
    
    See what's happening RIGHT NOW:
    - Current processing jobs
    - Recent completions
    - Processing speed
    - System health
    """
    
    # Count queue
    incoming = list(QUEUE_DIR.glob("incoming/*.txt"))
    incoming = [f for f in incoming if not f.name.endswith('_response.txt')]
    processing = list(QUEUE_DIR.glob("processing/*.txt"))
    processed_jsons = list(QUEUE_DIR.glob("processed/*.json"))
    errors = list(QUEUE_DIR.glob("error/*.txt"))
    
    # Get processing details
    processing_details = []
    for p in processing:
        stat = p.stat()
        age_seconds = (datetime.now().timestamp() - stat.st_mtime)
        processing_details.append({
            'filename': p.name,
            'age_seconds': round(age_seconds, 1),
            'age_minutes': round(age_seconds / 60, 1),
            'status': '⚠️ STUCK' if age_seconds > 300 else '🔵 PROCESSING'
        })
    
    # Get last 10 completed
    recent_completed = []
    for json_file in sorted(processed_jsons, key=lambda x: x.stat().st_mtime, reverse=True)[:10]:
        try:
            with open(json_file) as f:
                data = json.load(f)
            
            result = data.get('syntex_result', {})
            score_data = result.get('quality_score', {})
            if isinstance(score_data, dict):
                score = score_data.get('total_score', 0)
            else:
                score = 0
            
            stat = json_file.stat()
            completed_at = datetime.fromtimestamp(stat.st_mtime).strftime('%H:%M:%S')
            
            recent_completed.append({
                'filename': data.get('filename', json_file.name),
                'score': score,
                'wrapper': result.get('wrapper', 'unknown'),
                'completed_at': completed_at,
                'rating': '💎' if score >= 95 else '🔥' if score >= 80 else '⚡' if score >= 60 else '💧'
            })
        except:
            continue
    
    # Calculate processing speed (last hour)
    one_hour_ago = datetime.now() - timedelta(hours=1)
    recent_processed = [
        p for p in processed_jsons
        if datetime.fromtimestamp(p.stat().st_mtime) > one_hour_ago
    ]
    jobs_per_hour = len(recent_processed)
    
    # System health
    health = "🟢 HEALTHY"
    if len(processing) > 5:
        health = "🟡 BUSY"
    elif len(processing) > 0 and processing_details[0]['age_seconds'] > 300:
        health = "🔴 STUCK"
    elif len(incoming) < 10:
        health = "🟡 LOW QUEUE"
    
    return {
        "status": "LIVE_QUEUE_MONITOR",
        "timestamp": datetime.now().isoformat(),
        "system_health": health,
        "queue": {
            "incoming": len(incoming),
            "processing": len(processing),
            "processed": len(processed_jsons),
            "errors": len(errors)
        },
        "processing_details": processing_details,
        "recent_completed": recent_completed,
        "performance": {
            "jobs_per_hour": jobs_per_hour,
            "avg_time_estimate": "~45s" if jobs_per_hour > 0 else "unknown",
            "time_to_clear_queue": f"~{round(len(incoming) / (jobs_per_hour or 1), 1)}h" if jobs_per_hour > 0 else "unknown"
        },
        "insights": [
            f"🔥 Processing speed: {jobs_per_hour} jobs/hour",
            f"💎 Last completed: {recent_completed[0]['rating']} {recent_completed[0]['score']}" if recent_completed else "No recent completions",
            f"⏱️ Queue will clear in ~{round(len(incoming) / (jobs_per_hour or 1), 1)}h" if jobs_per_hour > 0 else "⚠️ No processing activity"
        ]
    }

