"""
SYNTX TEMPORAL API - ZEITBEREICHE & VERLÄUFE
"""

from datetime import datetime
from typing import Optional
import json

class TemporalFieldAnalyzer:
    def __init__(self, log_path="./gpt_generator/logs/gpt_prompts.jsonl"):
        self.log_path = log_path
        self.felder = self._load_temporal_felder()
    
    def _load_temporal_felder(self):
        """Lade Felder mit Zeitstempel-Parsing"""
        felder = []
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
