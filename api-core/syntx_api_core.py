"""
SYNTX LOG ANALYSE - FÜR ECHTE LOG-STRUKTUR
"""

import json
from pathlib import Path

class LogFieldReader:
    def __init__(self, log_path="./gpt_generator/logs/gpt_prompts.jsonl"):
        self.log_path = Path(log_path)
        self.feld_analyse = {"401_errors": 0, "successful_calls": 0, "blocked_topics": []}
    
    def analyse_log_felder(self):
        if not self.log_path.exists():
            return {"error": f"LOG-FELD NICHT GEFUNDEN: {self.log_path}"}
        
        with open(self.log_path, 'r') as f:
            for line in f:
                self._process_log_line(line)
        
        return self._create_feld_report()
    
    def _process_log_line(self, line):
        try:
            log_entry = json.loads(line)
            if "401" in str(log_entry.get('error', '')):
                self.feld_analyse["401_errors"] += 1
                topic = log_entry.get('prompt_sent', 'UNKNOWN')
                if topic not in self.feld_analyse["blocked_topics"]:
                    self.feld_analyse["blocked_topics"].append(topic)
            if log_entry.get('success') is True:
                self.feld_analyse["successful_calls"] += 1
        except:
            pass
    
    def _create_feld_report(self):
        return {
            "log_feld_analyse": {
                "blockierte_stroeme": self.feld_analyse["401_errors"],
                "erfolgreiche_felder": self.feld_analyse["successful_calls"],
                "blockierte_themen": self.feld_analyse["blocked_topics"],
            }
        }

if __name__ == "__main__":
    print("🔍 ANALYSIERE SYNTX LOG-FELDER...")
    reader = LogFieldReader()
    feld_report = reader.analyse_log_felder()
    
    print("🌊 LOG-FELD-REPORT:")
    for feld, wert in feld_report["log_feld_analyse"].items():
        print(f"   {feld}: {wert}")
    
    status = "BLOCKIERT" if feld_report["log_feld_analyse"]["blockierte_stroeme"] > 0 else "FLIESSEND"
    print(f"📊 API-STROM-STATUS: {status}")
