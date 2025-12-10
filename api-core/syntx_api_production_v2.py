"""
SYNTX PRODUCTION API v2.1 - PHASE 2
Advanced Analytics, Predictions, Performance
"""
from strom_router import router as strom_router
from feld_router import router as feld_router
from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any
import json
from pathlib import Path as FilePath
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import sys

sys.path.append('/opt/syntx-workflow-api-get-prompts/api-core')

from utils.log_loader import load_field_flow, load_evolution, get_queue_counts, QUEUE_DIR

# Import all routers
from analytics.dashboard import router as analytics_dashboard_router
from analytics.success_rate import router as analytics_success_router
from analytics.advanced import router as analytics_advanced_router
from analytics.performance import router as analytics_performance_router
from compare.wrappers import router as compare_wrappers_router
from compare.topics import router as compare_topics_router
from prompts.prompts_api import router as prompts_router
from prompts.prompts_advanced_api import router as prompts_advanced_router
from monitoring.live_monitor_api import router as monitoring_router
from prompts.evolution_api import router as evolution_router
from prompts.analytics_api import router as analytics_new_router

app = FastAPI(
    title="SYNTX PRODUCTION API",
    description="Feld-basierte API · Analytics · Predictions · Performance · Comparisons",
    version="2.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analytics_dashboard_router)
app.include_router(analytics_success_router)
app.include_router(analytics_advanced_router)
app.include_router(analytics_performance_router)
app.include_router(compare_wrappers_router)
app.include_router(compare_topics_router)
app.include_router(prompts_router)
app.include_router(prompts_advanced_router)
app.include_router(monitoring_router)
app.include_router(strom_router)
app.include_router(feld_router)
app.include_router(evolution_router)
app.include_router(analytics_new_router)

# Original endpoints
@app.get("/feld/drift")
async def get_drift_stream(
    limit: int = Query(20),
    topic: Optional[str] = Query(None),
    wrapper: Optional[str] = Query(None),
    min_score: Optional[int] = Query(None)
):
    """Alle Drift-Körper"""
    entries = load_field_flow()
    
    if topic:
        entries = [e for e in entries if e.get('topic', '').lower() == topic.lower()]
    if wrapper:
        entries = [e for e in entries if e.get('wrapper', '').lower() == wrapper.lower()]
    if min_score:
        qs_filter = []
        for e in entries:
            qs = e.get('quality_score')
            if qs and isinstance(qs, dict) and qs.get('total_score', 0) >= min_score:
                qs_filter.append(e)
        entries = qs_filter
    
    entries = entries[-limit:]
    
    drift_korper = []
    for entry in entries:
        qs = entry.get('quality_score', {})
        total_score = qs.get('total_score') if isinstance(qs, dict) else 0
        
        drift_korper.append({
            "id": entry.get('job_id', 'unknown'),
            "topic": entry.get('topic', 'unknown'),
            "style": entry.get('style', 'unknown'),
            "wrapper": entry.get('wrapper', 'unknown'),
            "kalibrierung_score": total_score,
            "timestamp": entry.get('timestamp', 'unknown'),
            "resonanz": "KOHÄRENT" if total_score == 100 else "DRIFT"
        })
    
    return {
        "status": "DRIFT_STROM_AKTIV",
        "count": len(drift_korper),
        "drift_korper": drift_korper
    }

@app.get("/resonanz/queue")
async def get_queue_resonanz():
    """Queue Resonanz"""
    queue = get_queue_counts()
    total = sum(queue.values())
    
    if queue['processing'] > 5:
        resonanz = "BLOCKIERT"
    elif queue['incoming'] > 100:
        resonanz = "ÜBERLASTET"
    elif queue['incoming'] == 0:
        resonanz = "LEER"
    else:
        resonanz = "KOHÄRENT"
    
    return {
        "status": "QUEUE_RESONANZ_AKTIV",
        "resonanz_zustand": resonanz,
        "felder": queue,
        "gesamt": total,
        "flow_rate": queue['processed'] / max(total, 1) * 100
    }

@app.get("/resonanz/system")
async def get_system_resonanz():
    """System Resonanz"""
    queue = get_queue_counts()
    entries = load_field_flow(limit=100)
    generations = load_evolution()
    
    scores = []
    for e in entries:
        qs = e.get('quality_score')
        if qs and isinstance(qs, dict):
            score = qs.get('total_score')
            if score is not None:
                scores.append(score)
    
    avg_score = sum(scores) / len(scores) if scores else 0
    
    if avg_score >= 90 and queue['incoming'] < 50:
        system_state = "OPTIMAL"
    elif avg_score >= 70:
        system_state = "GUT"
    elif avg_score >= 50:
        system_state = "MARGINAL"
    else:
        system_state = "KRITISCH"
    
    return {
        "status": "SYSTEM_RESONANZ_AKTIV",
        "system_zustand": system_state,
        "resonanz_felder": {
            "queue": {
                "incoming": queue['incoming'],
                "processed": queue['processed'],
                "resonanz": "KOHÄRENT" if queue['incoming'] < 50 else "DRIFT"
            },
            "qualität": {
                "durchschnitt": round(avg_score, 2),
                "resonanz": "KOHÄRENT" if avg_score >= 80 else "DRIFT"
            },
            "evolution": {
                "generationen": len(generations),
                "resonanz": "AKTIV" if len(generations) > 0 else "INAKTIV"
            }
        }
    }

@app.get("/generation/progress")
async def get_evolution_progress():
    """Evolution Progress"""
    generations = load_evolution()
    
    if not generations:
        return {"status": "KEINE_EVOLUTION_DATEN", "progress": []}
    
    progress = []
    for gen in generations:
        progress.append({
            "generation": gen.get('generation'),
            "timestamp": gen.get('timestamp'),
            "avg_score": gen.get('learned_from', {}).get('avg_score', 0),
            "sample_count": gen.get('learned_from', {}).get('sample_count', 0),
            "prompts_generated": gen.get('prompts_generated', 0)
        })
    
    improvement = progress[-1]['avg_score'] - progress[0]['avg_score'] if len(progress) > 1 else 0
    
    return {
        "status": "EVOLUTION_PROGRESS_AKTIV",
        "generationen": len(progress),
        "progress": progress,
        "verbesserung": round(improvement, 2),
        "trend": "STEIGEND" if improvement > 0 else "STABIL" if improvement == 0 else "FALLEND"
    }

@app.get("/health")
async def health_check():
    """System Health"""
    return {
        "status": "SYSTEM_GESUND",
        "api_version": "2.1.0",
        "timestamp": datetime.now().isoformat(),
        "queue_accessible": QUEUE_DIR.exists(),
        "modules": ["analytics", "compare", "feld", "resonanz", "generation", "predictions"]
    }

@app.get("/")
async def root():
    """API Info"""
    return {
        "name": "SYNTX Production API",
        "version": "2.1.0",
        "architektur": "Feld-basiert · Modular · Predictive",
        "phase": "2 - Advanced Analytics",
        "ebenen": {
            "feld": "/feld/*",
            "resonanz": "/resonanz/*",
            "generation": "/generation/*",
            "analytics": "/analytics/* (dashboard, success-rate, trends, performance, correlation, outliers)",
            "compare": "/compare/*"
        },
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    print("🌊 SYNTX PRODUCTION API v2.1 STARTET...")
    print("📡 Port: 8020")
    print("📚 Docs: http://localhost:8020/docs")
    print("🔥 Phase 2: Advanced Analytics, Predictions, Performance")
    uvicorn.run(app, host="0.0.0.0", port=8020)
