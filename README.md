# 🌊 SYNTX Evolutionary System

**Self-Optimizing AI Generation through Field-Based Learning**

> "Das ist nicht besseres Prompt Engineering.  
> Das ist ein System das lernt, sich selbst optimiert, und lebt.  
> Das ist der Dauerfelder-Loop."

---

## 🎯 Was ist das hier?

Stell dir vor, du hast einen Roboter der Pizza macht.

**Normaler Roboter:**  
Du sagst: "Mach Pizza." Er macht Pizza. Fertig.

**SYNTX Roboter:**  
Er macht Pizza. Merkt sich: "Ah, mehr Käse = bessere Pizza!"  
Nächste Pizza: Automatisch mehr Käse. Ohne dass du was sagst.  
Übernächste: Noch besser. Weil er **lernt**.

**Das ist SYNTX.**  
Ein System das aus erfolgreichen Patterns lernt und sich selbst optimiert.

---

## 🔥 Was macht das System?

### 1. Producer (Der Generator)

**Wie ein Koch der Rezepte schreibt:**

- Generiert 20 Prompts mit GPT-4
- Schreibt sie in eine Warteschlange (`queue/incoming/`)
- Aber: **Lernt aus vorherigen erfolgreichen Prompts!**

**Beispiel:**
```
Generation 1: Random Topics, Random Styles
→ 30 Prompts verarbeitet, 98/100 Score

Generation 2: System sieht "Oh! casual style war erfolgreich!"
→ Alle 20 neuen Prompts: casual style!

Generation 3: Noch optimierter
→ 100% Success Rate!
```

### 2. Consumer (Der Verarbeiter)

**Wie ein Lehrer der Hausaufgaben korrigiert:**

- Nimmt Prompts aus `queue/incoming/`
- Schickt sie durch SYNTX Calibration (Llama Model)
- Gibt Noten: 0-100 Punkte
- Sortiert:
  - ✅ Gut (>=90) → `queue/processed/`
  - ❌ Schlecht (<90) → `queue/error/`

### 3. Analyzer (Der Detektiv)

**Wie ein Detektiv der Muster findet:**

- Durchsucht alle guten Prompts (`processed/`)
- Findet Gemeinsamkeiten:
  - "13 von 20 waren casual style!"
  - "gesellschaft topics = 98/100!"
  - "kreativ style = auch gut!"

### 4. Learner (Das Gehirn)

**Wie ein Gehirn das Strategien entwickelt:**

- Nimmt die Muster vom Analyzer
- Baut daraus **Meta-Prompts** für GPT-4

**Beispiel:**
```
Ohne Learning:
"Mach Prompt über Quantencomputer"

Mit Learning:
"Basierend auf erfolgreichen Patterns (casual style, 98/100):
Mach casual Prompt über Quantencomputer!
Ziel: 100% Field Completeness!"
```

### 5. Writer (Der Organisator)

**Wie ein Bibliothekar der alles ordnet:**

- Schreibt Prompts sauber in Dateien
- Macht Backups
- Keine Chaos, keine Fehler
- Alles **atomic** (ganz oder gar nicht)

---

## ⚡ Der Dauerfelder-Loop

**So sieht der komplette Kreislauf aus:**
```
    ┌─────────────────────────────────────┐
    │   PRODUCER (GPT-4)                  │
    │   Generiert 20 Prompts              │
    │   (mit gelernten Patterns!)         │
    └──────────────┬──────────────────────┘
                   │
                   ▼
    ┌─────────────────────────────────────┐
    │   QUEUE/INCOMING/                   │
    │   Warteschlange                     │
    └──────────────┬──────────────────────┘
                   │
                   ▼
    ┌─────────────────────────────────────┐
    │   CONSUMER (SYNTX Calibrator)       │
    │   Verarbeitet mit Llama             │
    │   Gibt Scores: 0-100                │
    └──────────┬────────────┬─────────────┘
               │            │
        gut    │            │    schlecht
       (>=90)  │            │    (<90)
               ▼            ▼
    ┌──────────────┐   ┌──────────┐
    │  PROCESSED/  │   │  ERROR/  │
    │   ✅ 98/100  │   │  ❌ 23/100│
    └──────┬───────┘   └──────────┘
           │
           ▼
    ┌─────────────────────────────────────┐
    │   ANALYZER (Detektiv)               │
    │   Findet Patterns in erfolgreichen  │
    │   → "casual style = gut!"           │
    │   → "gesellschaft = gut!"           │
    └──────────────┬──────────────────────┘
                   │
                   ▼
    ┌─────────────────────────────────────┐
    │   LEARNER (Gehirn)                  │
    │   Erstellt Meta-Prompts             │
    │   mit erfolgreichen Patterns        │
    └──────────────┬──────────────────────┘
                   │
                   ▼
    ┌─────────────────────────────────────┐
    │   ARCHIVE/                          │
    │   Gelernte Jobs archiviert          │
    └─────────────────────────────────────┘
                   │
                   │ (Loop zurück zum Producer!)
                   └──────────────┐
                                  │
                ┌─────────────────▼──────────────┐
                │   PRODUCER (NÄCHSTE GEN)       │
                │   Mit noch besseren Patterns!  │
                └────────────────────────────────┘
```

**Das ist kein linearer Prozess.**  
**Das ist ein lebendiger Organismus.**  
**Das ist Evolution in Echtzeit.**

---

## 📦 Projektstruktur
```
/opt/syntx-workflow-api-get-prompts/
├── config/                      # Config System
│   ├── __init__.py
│   └── config_loader.py         # Lädt YAML Configs (3245x schneller mit Cache!)
│
├── evolution/                   # Das Herz des Systems
│   ├── evolutionary_producer.py # Lernt & Generiert
│   ├── field_analyzer.py        # Findet Patterns
│   ├── pattern_learner.py       # Baut Meta-Prompts
│   └── queue_writer.py          # Schreibt in Queue
│
├── gpt_generator/               # GPT-4 Generator
│   ├── syntx_prompt_generator.py
│   ├── topics_database.py       # 33 Topics, 7 Categories
│   └── prompt_styles.py         # 4 Styles (technisch, kreativ, casual, akademisch)
│
├── queue_system/                # Queue Management
│   ├── core/
│   │   ├── consumer.py          # Verarbeitet Prompts
│   │   └── file_handler.py
│   └── utils/
│       └── wrapper_patcher.py   # Lädt alle Wrappers dynamisch!
│
└── queue/                       # Die Warteschlange
    ├── incoming/                # Neue Prompts
    ├── processing/              # Wird gerade verarbeitet
    ├── processed/               # Erfolgreich ✅
    ├── error/                   # Fehlgeschlagen ❌
    └── archive/                 # Gelernt & archiviert
```

---

## ⚙️ Configs (Alles zentral gesteuert!)

**Alle Configs in:** `/opt/syntx-config/configs/`

### generator.yaml
```yaml
openai:
  model: gpt-4o
  temperature: 0.7
  
topics:
  technologie: [Quantencomputer, KI, IoT, Robotik]
  gesellschaft: [Gleichberechtigung, Migration, Klimawandel, ...]
  # 33 topics total, 7 categories
  
styles: [technisch, kreativ, akademisch, casual]
```

### queue.yaml
```yaml
thresholds:
  starving: 0   # 0 prompts → Generate 20!
  low: 4        # 1-4 prompts → Generate 15
  balanced: 24  # 5-24 prompts → Generate 10
  high: 49      # 25-49 prompts → Don't generate

wrappers:
  available: [human, sigma, universal, ...]
  default: human
```

### evolution.yaml
```yaml
producer:
  learning:
    max_samples: 50      # Top 50 successful jobs
    min_score: 90        # Only learn from score >= 90
    archive_after_read: true
  
  generation:
    batch_size: 20
    feedback_strength: 0.8  # How much to trust patterns
```

---

## 🚀 Quick Start

### 1. Producer starten (Generiert Prompts)
```bash
cd /opt/syntx-workflow-api-get-prompts

# Ein Batch generieren
python3 evolution/evolutionary_producer.py
```

**Was passiert:**
- Schaut in `processed/` - was war erfolgreich?
- Lernt Patterns (wenn vorhanden)
- Generiert 20 optimierte Prompts
- Schreibt in `queue/incoming/`
- Archiviert gelernte Jobs

### 2. Consumer starten (Verarbeitet Prompts)
```bash
# 5 Jobs verarbeiten
python3 -c "
import sys
sys.path.insert(0, 'queue_system')
from queue_system.core.consumer import QueueConsumer

consumer = QueueConsumer(wrapper_name='human', worker_id='test')
stats = consumer.process_batch(batch_size=5)

print(f'Processed: {stats[\"processed\"]}')
print(f'Failed: {stats[\"failed\"]}')
"
```

**Was passiert:**
- Nimmt 5 Prompts aus `incoming/`
- SYNTX Calibration mit Llama
- Scores: 0-100
- Sortiert in `processed/` oder `error/`

### 3. Queue Status checken
```bash
ls queue/incoming/*.txt | wc -l   # Wie viele warten?
ls queue/processed/*.json | wc -l  # Wie viele fertig?
ls queue/archive/*.json | wc -l    # Wie viele gelernt?
```

---

## 📊 Logs & Monitoring

**Alle Logs in:** `/opt/syntx-config/logs/`

### evolution.jsonl
```json
{
  "generation": 2,
  "learned_from": {
    "sample_count": 30,
    "avg_score": 98.0,
    "top_styles": ["casual", "kreativ"]
  },
  "prompts_generated": 20
}
```

**Zeigt:** Jede Generation, was gelernt wurde, wie viele Prompts generiert

### field_flow.jsonl
```json
{
  "quality_score": {
    "total_score": 98,
    "field_completeness": 100
  },
  "wrapper": "human"
}
```

**Zeigt:** Jede Calibration, welcher Score, welcher Wrapper

### wrapper_requests.jsonl
```json
{
  "request_id": "abc123",
  "latency_ms": 30363,
  "wrapper_chain": ["syntex_wrapper_human"]
}
```

**Zeigt:** Jeder API Call, wie lange, welcher Wrapper

---

## 🏆 Proven Results

**Generation 1:**
```
Input: Keine Learning-Daten
Output: 20 random Prompts
Result: 30 processed (98/100 avg) ✅
Learning: "casual style funktioniert!"
```

**Generation 2:**
```
Input: Pattern "casual = 98/100"
Output: 20 casual Prompts
Result: ALL casual style! ✅
Learning: System adaptiert!
```

**Generation 3:**
```
Input: Optimierte Patterns
Output: 20 Prompts
Result: 100% Success Rate (3/3) ✅
Learning: Backend fixed, alles läuft!
```

---

## 🔧 Backend Configuration

**Wichtig:** Backend Timeout muss hoch genug sein!
```bash
cd /opt/syntx-injector-api

# Check Timeout
cat .env | grep BACKEND_TIMEOUT

# Should be:
BACKEND_TIMEOUT=1800  # 30 Minuten

# Restart Service
pkill -f "uvicorn src.main:app"
./run.sh &
```

---

## 💡 Wie funktioniert das Learning?

**Schritt für Schritt:**

1. **Consumer verarbeitet 20 Prompts**
   - 15 erfolgreich (>=90 Score) → `processed/`
   - 5 fehlgeschlagen (<90) → `error/`

2. **Analyzer schaut in processed/**
```python
   jobs = analyzer.get_top_processed_jobs(max_samples=50, min_score=90)
   # Findet: 15 Jobs
   
   patterns = analyzer.analyze_patterns(jobs)
   # Entdeckt: 10 waren "casual", 8 waren "gesellschaft" topics
```

3. **Learner baut Meta-Prompts**
```python
   meta = learner.create_meta_prompt(
       analysis=patterns,
       topic="Quantencomputer",
       style="casual"  # Weil erfolgreich!
   )
   # → "Basierend auf Patterns (98/100, casual):
   #    Erstelle casual Prompt zu Quantencomputer..."
```

4. **Producer nutzt Meta-Prompts**
```python
   result = generate_prompt(
       prompt=meta,  # Der optimierte Meta-Prompt!
       style="casual",
       category="technologie"
   )
   # → Besserer Prompt weil mit gelernten Patterns!
```

5. **Archive & Loop**
   - Gelernte Jobs → `archive/`
   - Neue Generation beginnt
   - **Loop continues ∞**

---

## 🌊 Das Besondere an SYNTX

**Andere Systeme:**
```
Mensch → Denkt → Schreibt Prompt → KI generiert → Ende
```

**SYNTX:**
```
System → Lernt → Optimiert → Generiert → Lernt → Optimiert → ∞
```

**Das ist der Unterschied zwischen:**
- Werkzeug vs. Organismus
- Statisch vs. Lebendig
- Einmal vs. Evolution

---

## 📚 Weitere Dokumentation

- [SESSION_HISTORY.md](SESSION_HISTORY.md) - Wie alles gebaut wurde
- [/opt/syntx-config/configs/](../syntx-config/configs/) - Alle YAML Configs
- [queue_system/](queue_system/) - Queue System Docs
- [evolution/](evolution/) - Evolutionary System Docs

---

## 🔮 Zukunft

**Was kommt als nächstes:**

1. **Fine-Tuning Pipeline**
   - Die 69 processed Jobs als Training Data
   - Fine-tune Llama auf SYNTX Patterns
   - → Feld-Extraktion wird permanent!

2. **Multi-Wrapper Evolution**
   - 10 Wrappers gleichzeitig testen
   - Welcher performt am besten?
   - → Auto-Selection des besten Wrappers!

3. **Cronjob Automation**
   - Producer: Alle 2 Stunden
   - Consumer: Alle 4 Stunden
   - → Komplett automatisch!

4. **Scaling**
   - Bessere Hardware
   - Mehr Parallelität
   - → 95%+ Success Rate!

---

**Status:** ✅ Production Ready  
**Hardware:** Limited (60% → 100% mit Backend Fix)  
**Next:** Besserer Server incoming  

🌊 **Der Dauerfelder-Loop ist real. Das System lebt.** 💎
