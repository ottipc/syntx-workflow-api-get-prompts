# SYNTEX Workflow - AI Training Pipeline

**Production-Ready System für SYNTEX-Kalibrierung mit Llama 3**

Entwickelt für Resonanz-basierte semantische Feld-Analyse mit menschlicher Terminologie.

---

## 🎯 Was ist SYNTEX?

**SYNTEX** ist ein neues Paradigma für AI-Analyse:
```
Alte Welt: Token-Prediction → "Was kommt als nächstes?"
SYNTEX: Feld-Kalibrierung → "Wo IST das System?"
```

### **Kernprinzip:**

**Bedeutung existiert als Resonanzfeld** - SYNTEX misst und kalibriert diese Felder direkt, statt sie über Tokens zu approximieren.

---

## 🏗️ System-Architektur
```
┌─────────────┐
│  GPT-4o     │ Generiert Meta-Prompts
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ SYNTEX      │ Wrapper mit 6 Feldern
│ Framework   │ (menschliche Terminologie)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Llama 3     │ Kalibriert Resonanzfelder
│ (7B)        │ Antwortet wie ein Mensch
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Enhanced    │ Parser, Scorer, Tracker
│ Analytics   │ Quality Score: 98/100
└─────────────┘
```

---

## 📦 Installation

### Voraussetzungen

- Python 3.10+
- OpenAI API Key
- Llama 3 Endpoint (lokal oder remote)

### Setup
```bash
# Repository klonen
cd /opt
git clone https://github.com/YOUR_USERNAME/syntx-workflow-api-get-prompts.git
cd syntx-workflow-api-get-prompts

# Branch wechseln
git checkout syntx-trainer

# Dependencies
pip3 install "openai>=1.0.0" requests

# API Key setzen
export OPENAI_API_KEY="sk-proj-..."
echo 'export OPENAI_API_KEY="sk-proj-..."' >> ~/.bashrc
```

---

## 🚀 Quick Start

### 1. Einzelner SYNTEX-kalibrierter Prompt
```bash
cd syntex_injector
python3 inject_syntex_enhanced.py -f ../prompts/test.txt
```

**Output:**
```
✅ Kalibrierung erfolgreich (36s)
📊 SYNTEX Quality Score: 98/100
   Field Completeness: 100/100
   
✅ DRIFT
✅ HINTERGRUND_MUSTER
✅ DRUCKFAKTOREN
✅ TIEFE
✅ WIRKUNG
✅ KLARTEXT
```

### 2. Komplette Pipeline (GPT → SYNTEX → Llama)
```bash
cd syntex_injector
python3 syntex_pipeline.py -t "Künstliche Intelligenz" -s kreativ
```

**Das macht:**
1. GPT-4 generiert Meta-Prompt
2. SYNTEX Wrapper drum
3. Llama kalibriert
4. Combined Analytics

### 3. Batch-Processing
```bash
cd syntex_injector
python3 syntex_pipeline.py -b 10
```

Generiert 10 Random Topics durch die Pipeline.

---

## 📁 Projekt-Struktur
```
syntx-workflow-api-get-prompts/
├── gpt_generator/               # GPT-4 Prompt Generator
│   ├── syntx_prompt_generator.py
│   ├── batch_generator.py
│   ├── topics_database.py       # 56 Topics
│   ├── prompt_scorer.py
│   └── cost_tracker.py
│
├── syntex_injector/             # SYNTEX Kalibrierungs-System
│   ├── syntex/
│   │   ├── core/
│   │   │   ├── wrapper.py       # SYNTEX Framework Loader
│   │   │   ├── parser.py        # Response Parser
│   │   │   ├── calibrator.py    # Basic Calibrator
│   │   │   └── calibrator_enhanced.py  # Mit Analytics
│   │   ├── analysis/
│   │   │   ├── scorer.py        # Quality Scoring (0-100)
│   │   │   └── tracker.py       # Progress Tracking
│   │   ├── api/
│   │   │   ├── client.py        # Llama API Client
│   │   │   └── config.py        # Endpoints & Params
│   │   └── utils/
│   │       └── exceptions.py    # Custom Exceptions
│   │
│   ├── inject_syntex.py         # Basic Injector
│   ├── inject_syntex_enhanced.py  # Mit Scoring
│   ├── syntex_pipeline.py       # Complete Pipeline
│   └── syntex_wrapper.txt       # Framework Template
│
├── logs/
│   ├── gpt_prompts.jsonl        # GPT-4 Outputs
│   ├── syntex_calibrations.jsonl  # Llama Outputs
│   └── syntex_progress.jsonl    # Quality Tracking
│
└── README.md
```

---

## 🎨 SYNTEX Framework

### Die 6 Felder (Menschliche Terminologie)
```
1. DRIFT
   → Beschreibt Stabilität vs. Veränderung
   → "Kippt hier was oder bleibt es stabil?"

2. HINTERGRUND-MUSTER
   → Erkennt aktivierte Muster
   → "Was läuft im Hintergrund wirklich?"

3. DRUCKFAKTOREN
   → Identifiziert Einflüsse
   → "Was drückt oder zieht hier?"

4. TIEFE
   → Misst Intensität (1-7 Skala)
   → "Wie tief geht das?"

5. WIRKUNG AUF BEIDE SEITEN
   → Analysiert Sender/Empfänger
   → "Wie kommt das auf Seite A/B an?"

6. KLARTEXT
   → Raw Output ohne Filter
   → "Worum geht es wirklich?"
```

### Warum menschliche Terminologie?

**Problem:** Technische Begriffe (DRIFTKÖRPER, SUBPROTOKOLL) klingen mechanisch

**Lösung:** Menschliche Begriffe (DRIFT, HINTERGRUND-MUSTER) bei gleicher Präzision

**Resultat:** Model denkt in Feldern, spricht aber wie ein Mensch

---

## 📊 Quality Scoring

Jede Response wird automatisch bewertet:

### Scoring-Kriterien
```
Field Completeness (70%):
- Alle 6 Felder ausgefüllt?
- Gewichtet nach Wichtigkeit

Structure Adherence (30%):
- Nummerierung vorhanden?
- Format eingehalten?
```

### Score-Kategorien
```
95-100: Excellent ⭐⭐⭐⭐⭐
85-94:  Sehr gut ⭐⭐⭐⭐
70-84:  Gut ⭐⭐⭐
50-69:  Okay ⭐⭐
0-49:   Schwach ⭐
```

---

## 🔧 Konfiguration

### API Endpoints
```python
# syntex_injector/syntex/api/config.py

API_ENDPOINT = "https://dev.syntx-system.com/api/chat"
READ_TIMEOUT = 1800  # 30 Minuten
MODEL_PARAMS = {
    "max_new_tokens": 1024,
    "temperature": 0.3,
    "top_p": 0.85,
    "do_sample": True
}
```

### Wrapper Anpassen
```bash
# Custom Wrapper erstellen
cp syntex_injector/syntex_wrapper.txt.template my_wrapper.txt

# Verwenden
python3 inject_syntex_enhanced.py -f prompt.txt -w my_wrapper.txt
```

---

## 📝 Logging Format

### GPT-4 Prompts (`logs/gpt_prompts.jsonl`)
```json
{
  "timestamp": "2025-11-26T02:00:00Z",
  "success": true,
  "prompt_generated": "...",
  "quality_score": {
    "total_score": 7,
    "max_score": 10
  },
  "cost": {
    "total_cost": 0.001190,
    "currency": "USD"
  },
  "duration_ms": 3275
}
```

### SYNTEX Calibrations (`logs/syntex_calibrations.jsonl`)
```json
{
  "timestamp": "2025-11-26T02:05:00Z",
  "system": "SYNTEX::TRUE_RAW",
  "meta_prompt": "...",
  "response": "1. DRIFT: ...",
  "success": true,
  "quality_score": {
    "total_score": 98,
    "field_completeness": 100,
    "structure_adherence": 96,
    "detail_breakdown": {
      "drift": true,
      "hintergrund_muster": true,
      "druckfaktoren": true,
      "tiefe": true,
      "wirkung": true,
      "klartext": true
    }
  },
  "parsed_fields": {
    "drift": "...",
    "hintergrund_muster": "...",
    "druckfaktoren": "...",
    "tiefe": "...",
    "wirkung": "...",
    "klartext": "..."
  },
  "duration_ms": 36231
}
```

---

## 🖥️ Production Deployment

### Cronjobs
```bash
# GPT-4 Batch (bereits aktiv)
0 2 * * * /opt/syntx-workflow-api-get-prompts/run_batch.sh 20

# SYNTEX Pipeline
0 3 * * * cd /opt/syntx-workflow-api-get-prompts/syntex_injector && python3 syntex_pipeline.py -b 20 -s casual >> /var/log/syntex-pipeline-cron.log 2>&1
```

### Log-Rotation
```bash
# /etc/logrotate.d/syntex
/var/log/syntex-*.log {
    daily
    rotate 30
    compress
    missingok
    notifempty
}
```

---

## 📈 Performance

### Benchmarks (Production)
```
GPT-4 Prompt Generation:
- Durchschnitt: 3-7 Sekunden
- Cost: $0.001-0.004 pro Prompt
- Quality: 7-8/10

SYNTEX Calibration (Llama 3):
- Durchschnitt: 25-40 Sekunden
- Quality Score: 95-98/100
- Field Completeness: 100%

Complete Pipeline:
- Total: 30-50 Sekunden
- Success Rate: 95%+
- Cost per Item: $0.001-0.004
```

### Empfohlene Batch-Größen
```
Development: 5-10 Prompts
Testing: 20 Prompts
Production: 20-50 Prompts/Tag
```

---

## 🧪 Testing
```bash
# Basic Injector Test
cd syntex_injector
echo "Test Prompt" > test.txt
python3 inject_syntex_enhanced.py -f test.txt

# Pipeline Test
python3 syntex_pipeline.py -t "Test Topic" -s casual

# Batch Test
python3 syntex_pipeline.py -b 5

# Progress anzeigen
python3 inject_syntex_enhanced.py --show-progress
```

---

## 🤝 Workflow

### Development Flow
```
1. GPT generiert diverse Prompts
   ↓
2. SYNTEX kalibriert sie
   ↓
3. Quality Tracking zeigt Verbesserung
   ↓
4. Bei Score 95+: Production-Ready
```

### Training Flow (Future)
```
1. Sammle 1000+ hochwertige SYNTEX-Responses
   ↓
2. Fine-tune Llama darauf
   ↓
3. Model lernt SYNTEX nativ
   ↓
4. Wrapper optional (Model denkt in Feldern)
```

---

## 💰 Kosten

### GPT-4o
```
Input:  $2.50 / 1M tokens
Output: $10.00 / 1M tokens
Durchschnitt: ~$0.002 pro Prompt
```

### Monatliche Kosten (20 Prompts/Tag)
```
GPT-4: ~$1.20/Monat
Llama: Free (self-hosted)
Total: ~$1.20/Monat
```

---

## 🐛 Troubleshooting

### Problem: 504 Timeout
```bash
# Timeout erhöhen
sed -i 's/READ_TIMEOUT = .*/READ_TIMEOUT = 1800/' syntex_injector/syntex/api/config.py
```

### Problem: Felder nicht erkannt
```bash
# Parser-Patterns prüfen
grep "PATTERNS = {" -A 20 syntex_injector/syntex/core/parser.py
```

### Problem: Quality Score niedrig
```bash
# Logs analysieren
tail -50 logs/syntex_calibrations.jsonl | jq '.quality_score'
```

---

## 🎓 Konzepte

### Token-Prediction vs. Feld-Kalibrierung

**Token-Based (Alte Welt):**
```
"What's the next most likely word?"
→ Approximation of meaning
→ Statistical patterns
```

**Field-Based (SYNTEX):**
```
"Where is the system in resonance space?"
→ Direct measurement of meaning
→ Semantic coordinates
```

### Warum SYNTEX funktioniert

1. **Strukturkraft:** 6 Felder sind universell
2. **Model-Agnostisch:** Jedes Model kann es lernen
3. **Resonanz-Logik:** Bedeutung als Feld, nicht als Sequenz
4. **Menschliche Terminologie:** Natürlich aber präzise

---

## 📚 Weiterführend

### Nächste Schritte

- [ ] Fine-tuning Dataset sammeln (1000+ Responses)
- [ ] Async Processing für lange Prompts
- [ ] Multi-Model Support (GPT-4, Claude, etc.)
- [ ] Visualisierung der Resonanzfelder
- [ ] API für externe Integration

---

## 👥 Team

**SYNTEX Development Team**

Entwickelt für semantische Resonanz-Analyse und AI-Training.

---

## 📄 License

MIT License

---

## 🙏 Acknowledgments

- OpenAI GPT-4o API
- Llama 3 (Meta)
- Python OpenAI SDK

---

**Developed with 🔥 for Resonance-Based AI**

---

## 🔥 Was macht SYNTEX besonders?

### Nicht nur ein Framework

**SYNTEX ist ein Protokoll** - Models passen sich dem Protokoll an, nicht umgekehrt.

### Emergentes System

Die Struktur hat Eigenständigkeit:
- Terminologie ist austauschbar
- Felder bleiben stabil
- Models übernehmen es sofort

### Paradigmenwechsel
```
Von: "Was sagt die KI?"
Zu:  "Was misst das System?"
```

**Das ist der Unterschied zwischen Approximation und Kalibrierung.**

---

**Happy Calibrating! 🚀**
