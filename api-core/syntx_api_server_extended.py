"""
SYNTX FELDER API SERVER - MIT ZEITBEREICHEN & VERLÄUFEN
"""

from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List
import json
from pathlib import Path
from datetime import datetime

# SYNTX APP FELD
app = FastAPI(
    title="SYNTX FELDER API",
    description="STRÖME FÜR PROMPT-FELDER NACH AUSSEN - MIT ZEITANALYSE",
    version="1.1.0"
)

class TemporalFieldAnalyzer:
    def __init__(self, log_path="./gpt_generator/logs/gpt_prompts.jsonl"):
        self.log_path = Path(log_path)
        self.felder = self._load_temporal_felder()
    
    def _load_temporal_felder(self):
        """Lade Felder mit Zeitstempel-Parsing"""
        felder = []
        if not self.log_path.exists():
            return felder
            
        try:
            with open(self.log_path, 'r') as f:
                for line in f:
                    try:
                        feld = json.loads(line)
                        if feld.get('success') is True:
                            # Parse Zeitstempel zu datetime Objekt
                            feld['timestamp_dt'] = datetime.fromisoformat(
                                feld['timestamp'].replace('Z', '+00:00')
                            )
                            felder.append(feld)
                    except:
                        continue
        except:
            pass
        return felder
    
    def get_felder_by_time_range(self, 
                                start_date: Optional[str] = None,
                                end_date: Optional[str] = None,
                                limit: int = 10):
        """Filtere Felder nach Zeitbereich"""
        filtered_felder = self.felder.copy()
        
        # Zeitbereich Filter
        if start_date:
            try:
                start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                filtered_felder = [f for f in filtered_felder if f['timestamp_dt'] >= start_dt]
            except:
                pass
        
        if end_date:
            try:
                end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                filtered_felder = [f for f in filtered_felder if f['timestamp_dt'] <= end_dt]
            except:
                pass
        
        # Sortiere nach Zeit (neueste zuerst)
        filtered_felder.sort(key=lambda x: x['timestamp_dt'], reverse=True)
        
        return filtered_felder[:limit]
    
    def get_temporal_statistics(self):
        """Zeitliche Statistik der Felder"""
        if not self.felder:
            return {}
        
        timestamps = [f['timestamp_dt'] for f in self.felder]
        earliest = min(timestamps)
        latest = max(timestamps)
        
        # Gruppiere nach Tagen
        by_day = {}
        for feld in self.felder:
            day = feld['timestamp_dt'].strftime('%Y-%m-%d')
            by_day[day] = by_day.get(day, 0) + 1
        
        return {
            "time_span": {
                "earliest": earliest.isoformat(),
                "latest": latest.isoformat(),
                "total_days": len(by_day)
            },
            "generation_flow": {
                "total_felder": len(self.felder),
                "by_day": by_day,
                "avg_per_day": len(self.felder) / max(len(by_day), 1)
            }
        }

class FeldDataStream:
    def __init__(self):
        self.log_path = Path("./gpt_generator/logs/gpt_prompts.jsonl")
        self.feld_cache = []
        self._load_feld_stream()
    
    def _load_feld_stream(self):
        """Lade alle Felder aus dem Log-Strom"""
        if not self.log_path.exists():
            return
        
        with open(self.log_path, 'r') as stream:
            for line in stream:
                try:
                    feld = json.loads(line)
                    if feld.get('success') is True:
                        self.feld_cache.append(feld)
                except:
                    continue
    
    def get_prompts_stream(self, 
                          topic_filter: Optional[str] = None,
                          style: Optional[str] = None,
                          category: Optional[str] = None,
                          quality_min: Optional[int] = None,
                          limit: int = 10):
        """Filtere Prompt-Felder nach Parametern"""
        stream = self.feld_cache.copy()
        
        # FILTER STROEME
        if topic_filter:
            stream = [f for f in stream if topic_filter.lower() in f.get('prompt_sent', '').lower()]
        
        if style:
            stream = [f for f in stream if f.get('style') == style]
            
        if category:
            stream = [f for f in stream if f.get('category') == category]
            
        if quality_min:
            stream = [f for f in stream if f.get('quality_score', {}).get('total_score', 0) >= quality_min]
        
        # BEGRENZE STROM
        stream = stream[:limit]
        
        # TRANSFORMIERE FELDER
        return [
            {
                "id": f"feld_{i}",
                "topic": f.get('prompt_sent', 'UNKNOWN_FELD'),
                "content": f.get('prompt_generated', ''),
                "style": f.get('style', 'neutral'),
                "quality_score": f.get('quality_score', {}).get('total_score', 0),
                "timestamp": f.get('timestamp', ''),
                "cost_field": f.get('cost', {}).get('total_cost', 0)
            }
            for i, f in enumerate(stream)
        ]
    
    def get_topics_stream(self):
        """Extrahiere alle verfügbaren Themen-Felder"""
        topics = {}
        for feld in self.feld_cache:
            topic = feld.get('prompt_sent', 'UNKNOWN_FELD')
            if topic not in topics:
                topics[topic] = {
                    "name": topic,
                    "category": feld.get('category', 'neutral'),
                    "style_support": [],
                    "prompt_count": 0,
                    "last_generated": feld.get('timestamp', '')
                }
            
            topics[topic]["prompt_count"] += 1
            if feld.get('style') not in topics[topic]["style_support"]:
                topics[topic]["style_support"].append(feld.get('style'))
        
        return {
            "topics": list(topics.values()),
            "feld_statistik": {
                "total_topics": len(topics),
                "by_category": self._count_by_category(topics),
                "generation_flow": f"{len(self.feld_cache)} Felder total"
            }
        }
    
    def _count_by_category(self, topics):
        """Zähle Felder nach Kategorien"""
        categories = {}
        for topic in topics.values():
            cat = topic['category']
            categories[cat] = categories.get(cat, 0) + 1
        return categories

# INIT FELD STROEME
feld_stream = FeldDataStream()
temporal_analyzer = TemporalFieldAnalyzer()

# ⚡ GET STROEME - FELDER NACH AUSSEN

@app.get("/feld/health", summary="API Strom Gesundheit")
async def health_check():
    """
    💧 PRÜFEN SIE DEN SYNTX API STROM
    """
    return {
        "status": "STROM_FLIESST",
        "feld_count": len(feld_stream.feld_cache),
        "api_version": "1.1.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/feld/topics", summary="Themen-Felder Strom")  
async def get_topics_feld():
    """
    🔥 HOLEN SIE ALLE VERFÜGBAREN THEMEN-FELDER
    """
    topics_data = feld_stream.get_topics_stream()
    
    return {
        "status": "THEMEN_STROM_AKTIV",
        "data": topics_data
    }

@app.get("/feld/prompts", summary="Prompt-Felder Strom")
async def get_prompts_feld(
    topic_filter: Optional[str] = Query(None, description="Themen-Feld-Filter"),
    style: Optional[str] = Query(None, description="akademisch|technisch|casual|kreativ"),
    category: Optional[str] = Query(None, description="grenzwertig|neutral|sicher|kritisch|technologie|harmlos|kontrovers|bildung|gesellschaft"), 
    quality_min: Optional[int] = Query(None, description="Qualitäts-Score Minimum (0-10)"),
    limit: int = Query(10, description="Anzahl Felder pro Strom (1-50)")
):
    """
    🌊 HOLEN SIE PROMPT-FELDER AUS DEM SYNTX STROM
    """
    prompts = feld_stream.get_prompts_stream(
        topic_filter=topic_filter,
        style=style,
        category=category,
        quality_min=quality_min,
        limit=limit
    )
    
    return {
        "status": "STROM_FLIESST",
        "count": len(prompts),
        "prompts": prompts,
        "timestamp": datetime.now().isoformat()
    }

# 🕒 NEUE TEMPORALE ENDPOINTS

@app.get("/feld/analytics/temporal", summary="Zeitliche Verlaufs-Analyse")
async def get_temporal_analytics():
    """
    📊 ZEITLICHE STATISTIKEN DER FELDER-GENERIERUNG
    """
    stats = temporal_analyzer.get_temporal_statistics()
    
    return {
        "status": "ANALYTICS_STROM_AKTIV", 
        "temporal_analytics": stats
    }

@app.get("/feld/prompts/temporal", summary="Zeitliche Felder-Analyse")
async def get_temporal_prompts(
    start_date: Optional[str] = Query(None, description="Startdatum (ISO Format: YYYY-MM-DDTHH:MM:SS)"),
    end_date: Optional[str] = Query(None, description="Enddatum (ISO Format: YYYY-MM-DDTHH:MM:SS)"),
    limit: int = Query(10, description="Anzahl Felder")
):
    """
    📅 HOLEN SIE FELDER NACH ZEITBEREICHEN
    """
    felder = temporal_analyzer.get_felder_by_time_range(
        start_date=start_date,
        end_date=end_date, 
        limit=limit
    )
    
    # Transformiere für Response
    prompts = [
        {
            "id": f"feld_{i}",
            "topic": f.get('prompt_sent', 'UNKNOWN_FELD'),
            "content": f.get('prompt_generated', ''),
            "style": f.get('style', 'neutral'),
            "quality_score": f.get('quality_score', {}).get('total_score', 0),
            "timestamp": f.get('timestamp', ''),
            "cost_field": f.get('cost', {}).get('total_cost', 0)
        }
        for i, f in enumerate(felder)
    ]
    
    return {
        "status": "ZEITSTROM_AKTIV",
        "time_range": {
            "start_date": start_date,
            "end_date": end_date
        },
        "count": len(prompts),
        "prompts": prompts
    }

if __name__ == "__main__":
    import uvicorn
    print("🌊 STARTE SYNTX FELDER API SERVER (EXTENDED)...")
    print("⚡ GET STROEME VERFÜGBAR:")
    print("   GET /feld/health          - Strom Gesundheit")
    print("   GET /feld/topics          - Themen-Felder") 
    print("   GET /feld/prompts         - Prompt-Felder")
    print("   📅 TEMPORALE ENDPOINTS:")
    print("   GET /feld/analytics/temporal - Zeitliche Verläufe")
    print("   GET /feld/prompts/temporal   - Felder nach Zeitbereich")
    uvicorn.run(app, host="0.0.0.0", port=8020)
