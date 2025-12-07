"""
SYNTX PRODUCTION API - FELD-BASIERTE ARCHITEKTUR
Resonanz · Kalibrierung · Ströme · Evolution
"""

from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any
import json
from pathlib import Path as FilePath
from datetime import datetime, timedelta
from collections import defaultdict, Counter

# ═══════════════════════════════════════════════════════════
# SYNTX APP INITIALIZATION
# ═══════════════════════════════════════════════════════════

app = FastAPI(
    title="SYNTX PRODUCTION API",
    description="Feld-basierte API für SYNTX System · Resonanz · Kalibrierung · Evolution",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═══════════════════════════════════════════════════════════
# LOG PATHS - PRODUCTION
# ═══════════════════════════════════════════════════════════

LOGS_DIR = FilePath("/opt/syntx-config/logs")
QUEUE_DIR = FilePath("/opt/syntx-workflow-api-get-prompts/queue")

FIELD_FLOW_LOG = LOGS_DIR / "field_flow.jsonl"
EVOLUTION_LOG = LOGS_DIR / "evolution.jsonl"
WRAPPER_LOG = LOGS_DIR / "wrapper_requests.jsonl"

# ═══════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════

def load_jsonl(path: FilePath, limit: int = None) -> List[Dict]:
    """Load JSONL file"""
    if not path.exists():
        return []
    
    entries = []
    try:
        with open(path, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    entries.append(entry)
                except:
                    continue
    except:
        return []
    
    if limit:
        return entries[-limit:]
    return entries

def count_files(directory: FilePath, pattern: str = "*.txt") -> int:
    """Count files in directory"""
    if not directory.exists():
        return 0
    return len(list(directory.glob(pattern)))

# ═══════════════════════════════════════════════════════════
# FELD EBENE - DRIFT, KALIBRIERUNG, STRÖMUNG
# ═══════════════════════════════════════════════════════════

@app.get("/feld/drift", summary="📦 Drift-Körper Stream")
async def get_drift_stream(
    limit: int = Query(20, description="Anzahl Drift-Körper"),
    topic: Optional[str] = Query(None, description="Filter nach Topic"),
    wrapper: Optional[str] = Query(None, description="Filter nach Wrapper"),
    min_score: Optional[int] = Query(None, description="Minimum Quality Score")
):
    """
    Alle Drift-Körper (Jobs) aus dem System
    Zeigt: Topic, Style, Wrapper, Score, Response
    """
    entries = load_jsonl(FIELD_FLOW_LOG)
    
    # Filter
    if topic:
        entries = [e for e in entries if e.get('topic', '').lower() == topic.lower()]
    if wrapper:
        entries = [e for e in entries if e.get('wrapper', '').lower() == wrapper.lower()]
    if min_score:
        entries = [e for e in entries if e.get('quality_score', {}).get('total_score', 0) >= min_score]
    
    # Limit
    entries = entries[-limit:]
    
    drift_korper = []
    for entry in entries:
        drift_korper.append({
            "id": entry.get('job_id', 'unknown'),
            "topic": entry.get('topic', 'unknown'),
            "style": entry.get('style', 'unknown'),
            "wrapper": entry.get('wrapper', 'unknown'),
            "format": entry.get('format', 'unknown'),
            "kalibrierung_score": entry.get('quality_score', {}).get('total_score'),
            "field_completeness": entry.get('quality_score', {}).get('field_completeness'),
            "felder": entry.get('quality_score', {}).get('fields', {}),
            "response_preview": entry.get('response', '')[:200] if entry.get('response') else None,
            "timestamp": entry.get('timestamp', 'unknown'),
            "resonanz": "KOHÄRENT" if entry.get('quality_score', {}).get('total_score', 0) == 100 else "DRIFT"
        })
    
    return {
        "status": "DRIFT_STROM_AKTIV",
        "count": len(drift_korper),
        "drift_korper": drift_korper
    }

@app.get("/feld/drift/{job_id}", summary="📦 Einzelner Drift-Körper")
async def get_single_drift(job_id: str = Path(..., description="Job ID")):
    """
    Komplette Details eines Drift-Körpers
    """
    entries = load_jsonl(FIELD_FLOW_LOG)
    
    for entry in entries:
        if entry.get('job_id') == job_id:
            return {
                "status": "DRIFT_GEFUNDEN",
                "drift_korper": {
                    "id": entry.get('job_id'),
                    "topic": entry.get('topic'),
                    "style": entry.get('style'),
                    "wrapper": entry.get('wrapper'),
                    "format": entry.get('format'),
                    "prompt": entry.get('prompt'),
                    "response": entry.get('response'),
                    "kalibrierung": {
                        "total_score": entry.get('quality_score', {}).get('total_score'),
                        "field_completeness": entry.get('quality_score', {}).get('field_completeness'),
                        "structure_adherence": entry.get('quality_score', {}).get('structure_adherence'),
                        "fields": entry.get('quality_score', {}).get('fields', {})
                    },
                    "meta": {
                        "session_id": entry.get('session_id'),
                        "duration_ms": entry.get('duration_ms'),
                        "timestamp": entry.get('timestamp')
                    },
                    "resonanz": "KOHÄRENT" if entry.get('quality_score', {}).get('total_score', 0) == 100 else "DRIFT"
                }
            }
    
    raise HTTPException(status_code=404, detail="Drift-Körper nicht gefunden")

@app.get("/feld/kalibrierung", summary="🎯 Kalibrierungs-Übersicht")
async def get_kalibrierung_overview():
    """
    Übersicht aller Kalibrierungen im System
    """
    entries = load_jsonl(FIELD_FLOW_LOG)
    
    total = len(entries)
    scores = [e.get('quality_score', {}).get('total_score', 0) for e in entries if e.get('quality_score')]
    
    perfect = len([s for s in scores if s == 100])
    good = len([s for s in scores if 80 <= s < 100])
    medium = len([s for s in scores if 50 <= s < 80])
    low = len([s for s in scores if s < 50])
    
    return {
        "status": "KALIBRIERUNG_AKTIV",
        "gesamt_kalibrierungen": total,
        "durchschnitt": sum(scores) / len(scores) if scores else 0,
        "verteilung": {
            "perfekt_100": perfect,
            "gut_80_99": good,
            "mittel_50_79": medium,
            "niedrig_0_49": low
        },
        "erfolgsrate": (perfect / total * 100) if total > 0 else 0
    }

@app.get("/feld/stromung", summary="🌊 Strömungs-Verhältnisse")
async def get_stromung():
    """
    Aktuelle Strömungs-Verhältnisse im System
    """
    entries = load_jsonl(FIELD_FLOW_LOG, limit=100)
    
    # Topic flow
    topics = Counter([e.get('topic') for e in entries if e.get('topic')])
    
    # Wrapper flow
    wrappers = Counter([e.get('wrapper') for e in entries if e.get('wrapper')])
    
    # Score flow (last 10)
    recent_scores = [e.get('quality_score', {}).get('total_score', 0) for e in entries[-10:]]
    
    return {
        "status": "STROMUNG_AKTIV",
        "topic_strom": dict(topics.most_common(5)),
        "wrapper_strom": dict(wrappers),
        "score_strom": {
            "recent": recent_scores,
            "trend": "STEIGEND" if len(recent_scores) > 1 and recent_scores[-1] > recent_scores[0] else "STABIL"
        }
    }

# ═══════════════════════════════════════════════════════════
# RESONANZ EBENE - QUEUE, SYSTEM, EVOLUTION
# ═══════════════════════════════════════════════════════════

@app.get("/resonanz/queue", summary="📊 Queue Resonanz")
async def get_queue_resonanz():
    """
    Resonanz-Zustand der Queue
    """
    incoming = count_files(QUEUE_DIR / "incoming")
    processing = count_files(QUEUE_DIR / "processing")
    processed = count_files(QUEUE_DIR / "processed")
    error = count_files(QUEUE_DIR / "error")
    
    total = incoming + processing + processed + error
    
    # Resonanz state
    if processing > 5:
        resonanz = "BLOCKIERT"
    elif incoming > 100:
        resonanz = "ÜBERLASTET"
    elif incoming == 0:
        resonanz = "LEER"
    else:
        resonanz = "KOHÄRENT"
    
    return {
        "status": "QUEUE_RESONANZ_AKTIV",
        "resonanz_zustand": resonanz,
        "felder": {
            "incoming": incoming,
            "processing": processing,
            "processed": processed,
            "error": error
        },
        "gesamt": total,
        "flow_rate": processed / max(total, 1) * 100
    }

@app.get("/resonanz/system", summary="⚡ System Resonanz")
async def get_system_resonanz():
    """
    Gesamt-System Resonanz
    """
    # Queue resonanz
    incoming = count_files(QUEUE_DIR / "incoming")
    processed = count_files(QUEUE_DIR / "processed")
    
    # Field flow resonanz
    entries = load_jsonl(FIELD_FLOW_LOG, limit=100)
    scores = [e.get('quality_score', {}).get('total_score', 0) for e in entries if e.get('quality_score')]
    avg_score = sum(scores) / len(scores) if scores else 0
    
    # Evolution resonanz
    generations = load_jsonl(EVOLUTION_LOG)
    
    # System state
    if avg_score >= 90 and incoming < 50:
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
                "incoming": incoming,
                "processed": processed,
                "resonanz": "KOHÄRENT" if incoming < 50 else "DRIFT"
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

@app.get("/resonanz/evolution", summary="🧬 Evolution Resonanz")
async def get_evolution_resonanz():
    """
    Resonanz des Evolution-Systems
    """
    generations = load_jsonl(EVOLUTION_LOG)
    
    if not generations:
        return {
            "status": "EVOLUTION_INAKTIV",
            "resonanz": "KEINE_DATEN"
        }
    
    latest = generations[-1]
    
    return {
        "status": "EVOLUTION_RESONANZ_AKTIV",
        "aktuelle_generation": latest.get('generation'),
        "resonanz_level": latest.get('learned_from', {}).get('avg_score', 0),
        "sample_count": latest.get('learned_from', {}).get('sample_count', 0),
        "learning_flow": {
            "top_categories": latest.get('learned_from', {}).get('top_categories', []),
            "top_styles": latest.get('learned_from', {}).get('top_styles', [])
        }
    }

# ═══════════════════════════════════════════════════════════
# KALIBRIERUNG EBENE - QUALITÄT, TOPIC, WRAPPER
# ═══════════════════════════════════════════════════════════

@app.get("/kalibrierung/qualitat", summary="📈 Qualitäts-Kalibrierung")
async def get_quality_kalibrierung(
    days: int = Query(7, description="Tage zurück")
):
    """
    Qualitäts-Kalibrierung über Zeit
    """
    entries = load_jsonl(FIELD_FLOW_LOG)
    
    # Filter by days
    cutoff = datetime.now() - timedelta(days=days)
    recent = []
    for e in entries:
        try:
            ts = datetime.fromisoformat(e.get('timestamp', '').replace('Z', '+00:00'))
            if ts >= cutoff:
                recent.append(e)
        except:
            continue
    
    # Daily stats
    by_day = defaultdict(list)
    for e in recent:
        try:
            day = datetime.fromisoformat(e.get('timestamp', '').replace('Z', '+00:00')).strftime('%Y-%m-%d')
            score = e.get('quality_score', {}).get('total_score')
            if score is not None:
                by_day[day].append(score)
        except:
            continue
    
    timeline = []
    for day in sorted(by_day.keys()):
        scores = by_day[day]
        timeline.append({
            "datum": day,
            "durchschnitt": round(sum(scores) / len(scores), 2),
            "anzahl": len(scores),
            "perfekt": len([s for s in scores if s == 100])
        })
    
    return {
        "status": "QUALITAT_KALIBRIERUNG_AKTIV",
        "zeitraum_tage": days,
        "timeline": timeline,
        "gesamt_durchschnitt": round(sum([t['durchschnitt'] for t in timeline]) / len(timeline), 2) if timeline else 0
    }

@app.get("/kalibrierung/topic/{topic}", summary="📚 Topic-Kalibrierung")
async def get_topic_kalibrierung(topic: str = Path(..., description="Topic Name")):
    """
    Kalibrierung für spezifisches Topic
    """
    entries = load_jsonl(FIELD_FLOW_LOG)
    topic_entries = [e for e in entries if e.get('topic', '').lower() == topic.lower()]
    
    if not topic_entries:
        raise HTTPException(status_code=404, detail="Topic nicht gefunden")
    
    scores = [e.get('quality_score', {}).get('total_score', 0) for e in topic_entries if e.get('quality_score')]
    
    return {
        "status": "TOPIC_KALIBRIERUNG_AKTIV",
        "topic": topic,
        "anzahl_jobs": len(topic_entries),
        "durchschnitt": round(sum(scores) / len(scores), 2) if scores else 0,
        "perfekt_rate": len([s for s in scores if s == 100]) / len(scores) * 100 if scores else 0,
        "wrapper_verteilung": dict(Counter([e.get('wrapper') for e in topic_entries]))
    }

@app.get("/kalibrierung/wrapper/{wrapper}", summary="🔧 Wrapper-Kalibrierung")
async def get_wrapper_kalibrierung(wrapper: str = Path(..., description="Wrapper Name")):
    """
    Kalibrierung für spezifischen Wrapper
    """
    entries = load_jsonl(FIELD_FLOW_LOG)
    wrapper_entries = [e for e in entries if e.get('wrapper', '').lower() == wrapper.lower()]
    
    if not wrapper_entries:
        raise HTTPException(status_code=404, detail="Wrapper nicht gefunden")
    
    scores = [e.get('quality_score', {}).get('total_score', 0) for e in wrapper_entries if e.get('quality_score')]
    
    return {
        "status": "WRAPPER_KALIBRIERUNG_AKTIV",
        "wrapper": wrapper,
        "anzahl_jobs": len(wrapper_entries),
        "durchschnitt": round(sum(scores) / len(scores), 2) if scores else 0,
        "perfekt_rate": len([s for s in scores if s == 100]) / len(scores) * 100 if scores else 0,
        "topic_verteilung": dict(Counter([e.get('topic') for e in wrapper_entries]).most_common(10))
    }

# ═══════════════════════════════════════════════════════════
# GENERATION EBENE - EVOLUTION
# ═══════════════════════════════════════════════════════════

@app.get("/generation/alle", summary="🧬 Alle Generationen")
async def get_all_generations():
    """
    Alle Evolution Generationen
    """
    generations = load_jsonl(EVOLUTION_LOG)
    
    return {
        "status": "GENERATION_STROM_AKTIV",
        "anzahl": len(generations),
        "generationen": generations
    }

@app.get("/generation/progress", summary="📈 Evolution Progress")
async def get_evolution_progress():
    """
    Evolution Learning Curve
    """
    generations = load_jsonl(EVOLUTION_LOG)
    
    if not generations:
        return {
            "status": "KEINE_EVOLUTION_DATEN",
            "progress": []
        }
    
    progress = []
    for gen in generations:
        progress.append({
            "generation": gen.get('generation'),
            "timestamp": gen.get('timestamp'),
            "avg_score": gen.get('learned_from', {}).get('avg_score', 0),
            "sample_count": gen.get('learned_from', {}).get('sample_count', 0),
            "prompts_generated": gen.get('prompts_generated', 0)
        })
    
    # Calculate improvement
    if len(progress) > 1:
        first_score = progress[0]['avg_score']
        last_score = progress[-1]['avg_score']
        improvement = last_score - first_score
    else:
        improvement = 0
    
    return {
        "status": "EVOLUTION_PROGRESS_AKTIV",
        "generationen": len(progress),
        "progress": progress,
        "verbesserung": round(improvement, 2),
        "trend": "STEIGEND" if improvement > 0 else "STABIL" if improvement == 0 else "FALLEND"
    }

@app.get("/generation/muster", summary="🔍 Evolution Patterns")
async def get_evolution_patterns():
    """
    Gelernte Patterns aus Evolution
    """
    generations = load_jsonl(EVOLUTION_LOG)
    
    if not generations:
        return {
            "status": "KEINE_MUSTER",
            "patterns": {}
        }
    
    latest = generations[-1]
    
    return {
        "status": "MUSTER_ERKANNT",
        "generation": latest.get('generation'),
        "patterns": {
            "top_categories": latest.get('learned_from', {}).get('top_categories', []),
            "top_styles": latest.get('learned_from', {}).get('top_styles', []),
            "avg_score": latest.get('learned_from', {}).get('avg_score', 0),
            "sample_count": latest.get('learned_from', {}).get('sample_count', 0)
        }
    }

# ═══════════════════════════════════════════════════════════
# STROM EBENE - AKTUELL, VERLAUF
# ═══════════════════════════════════════════════════════════

@app.get("/strom/aktuell", summary="⚡ Aktueller Strom")
async def get_current_strom():
    """
    Aktueller System-Strom
    """
    # Recent activity
    entries = load_jsonl(FIELD_FLOW_LOG, limit=10)
    
    return {
        "status": "STROM_AKTIV",
        "timestamp": datetime.now().isoformat(),
        "recent_activity": [
            {
                "topic": e.get('topic'),
                "score": e.get('quality_score', {}).get('total_score'),
                "timestamp": e.get('timestamp')
            }
            for e in entries
        ]
    }

@app.get("/strom/verlauf", summary="📜 Strom Verlauf")
async def get_strom_verlauf(
    limit: int = Query(50, description="Anzahl Einträge")
):
    """
    Historischer Strom-Verlauf
    """
    entries = load_jsonl(FIELD_FLOW_LOG, limit=limit)
    
    verlauf = []
    for e in entries:
        verlauf.append({
            "job_id": e.get('job_id'),
            "topic": e.get('topic'),
            "wrapper": e.get('wrapper'),
            "score": e.get('quality_score', {}).get('total_score'),
            "timestamp": e.get('timestamp')
        })
    
    return {
        "status": "VERLAUF_STROM_AKTIV",
        "anzahl": len(verlauf),
        "verlauf": verlauf
    }

# ═══════════════════════════════════════════════════════════
# HEALTH & INFO
# ═══════════════════════════════════════════════════════════

@app.get("/health", summary="💚 System Health")
async def health_check():
    """
    System Health Check
    """
    return {
        "status": "SYSTEM_GESUND",
        "api_version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "logs_accessible": FIELD_FLOW_LOG.exists(),
        "queue_accessible": QUEUE_DIR.exists()
    }

@app.get("/", summary="ℹ️ API Info")
async def root():
    """
    API Information
    """
    return {
        "name": "SYNTX Production API",
        "version": "2.0.0",
        "architektur": "Feld-basiert",
        "ebenen": {
            "feld": "/feld/*",
            "resonanz": "/resonanz/*",
            "kalibrierung": "/kalibrierung/*",
            "generation": "/generation/*",
            "strom": "/strom/*"
        },
        "docs": "/docs"
    }

# ═══════════════════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    print("🌊 SYNTX PRODUCTION API STARTET...")
    print("📡 Port: 8020")
    print("📚 Docs: http://localhost:8020/docs")
    uvicorn.run(app, host="0.0.0.0", port=8020)
