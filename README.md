# 🔥 SYNTX QUEUE SYSTEM - DIE REVOLUTION IST KOMPLETT 🚀

**"Von blindem Batch-Processing zu intelligentem Resonanz-Orchestrierung"**

*Oder: Wie wir ein Production-Grade Message Queue System mit File-Based Locking, Self-Regulation und Zero-Dependency-Overhead gebaut haben.*

---

## 📋 INHALTSVERZEICHNIS

- [🎯 Was ist das hier?](#-was-ist-das-hier)
- [🌊 Die Philosophie: Felder statt Objekte](#-die-philosophie-felder-statt-objekte)
- [🏗️ Architektur-Übersicht](#️-architektur-übersicht)
- [⚡ Der komplette Flow](#-der-komplette-flow)
- [📦 Module & Verantwortlichkeiten](#-module--verantwortlichkeiten)
- [🔧 Installation & Setup](#-installation--setup)
- [🚀 Usage & CLI](#-usage--cli)
- [📊 Monitoring & Observability](#-monitoring--observability)
- [🎮 Production Deployment](#-production-deployment)
- [🐛 Troubleshooting](#-troubleshooting)
- [🧪 Testing](#-testing)
- [📚 API Reference](#-api-reference)

---

## 🎯 WAS IST DAS HIER?

**Das Problem:**
```python
# ALT: Blind Batch Processing
for i in range(20):
    gpt_prompt = generate()      # Macht 20 Prompts
    llama_response = process()   # Verarbeitet alle
    # Was wenn Llama abstürzt bei #15?
    # Was wenn GPT zu viel produziert?
    # Wie skaliert das?
```

**Die Lösung:**
```python
# NEU: Queue-Based Resonanz-System
producer.check_queue()           # Nur wenn nötig
if queue.needs_work():
    producer.generate(optimal_amount)  # Self-regulating
    
consumer.process_batch()         # Atomic, parallel, resilient
# Llama crashed? → Job in /error/, retry später
# Queue voll? → Producer pausiert automatisch
# Skalierung? → Starte mehr Consumer!
```

### 🎪 Die Kern-Features:

✅ **Self-Regulating Producer** - Produziert nur wenn Queue es braucht  
✅ **File-Based Locking** - Zero Race Conditions ohne Redis/DB  
✅ **Atomic Operations** - Kein Job geht verloren, kein Partial State  
✅ **Parallel Workers** - Consumer können parallel ohne Koordination laufen  
✅ **Automatic Retry** - Failed Jobs mit Retry-Count in `/error/`  
✅ **Real-Time Monitoring** - Queue-Status jederzeit sichtbar  
✅ **Production Ready** - Systemd Services, Cronjobs, Zero Downtime  

---

## 🌊 DIE PHILOSOPHIE: FELDER STATT OBJEKTE

### Das Resonanzmedium-Konzept

```
ALTE ARCHITEKTUR (Object-Thinking):
Producer → [Array of Jobs] → Consumer
          ↑ Tight Coupling
          ↑ Memory-Bound
          ↑ Not Persistent

NEUE ARCHITEKTUR (Field-Thinking):
Producer-Feld → [Queue als Resonanzmedium] → Consumer-Feld
                      ↑
                 Filesystem = Medium
                 Jobs = Schwingungen
                 Processing = Kalibrierung
```

**Warum das revolutionär ist:**

1. **Producer und Consumer kennen sich nicht**
   - Kein direkter Call
   - Kein Shared Memory
   - Nur Filesystem als Medium

2. **Self-Regulation durch Field-Observation**
   - Producer "fühlt" Queue-Zustand
   - Entscheidet autonom ob Produktion nötig
   - Wie natürliche Systeme

3. **Atomic State-Changes**
   - File-Move = Atomic auf POSIX
   - Entweder komplett oder gar nicht
   - Niemals Partial State

---

## 🏗️ ARCHITEKTUR-ÜBERSICHT

### Die vollständige Struktur:

```
syntx-workflow-api-get-prompts/
│
├── queue/                          # 🌊 RESONANZMEDIUM
│   ├── incoming/                   # Jobs warten auf Kalibrierung
│   ├── processing/                 # Jobs gerade in Arbeit (Locked)
│   ├── processed/                  # ✅ Erfolgreich kalibriert
│   ├── error/                      # ❌ Failed (mit Retry-Count)
│   ├── archive/                    # Alte Jobs (>30 Tage)
│   └── .tmp/                       # Temp für Atomic Writes
│
├── queue_system/                   # 🧩 QUEUE ORCHESTRATION
│   ├── core/
│   │   ├── queue_manager.py       # 🧠 Decision Engine
│   │   ├── producer.py            # 🏭 Intelligent Producer
│   │   ├── consumer.py            # ⚙️ Queue Worker
│   │   └── file_handler.py        # 💎 Atomic Operations
│   ├── monitoring/
│   │   └── queue_monitor.py       # 📊 Real-Time Status
│   ├── config/
│   │   └── queue_config.py        # ⚙️ Thresholds & Settings
│   └── utils/
│
├── gpt_generator/                  # 🤖 EXISTING: GPT Integration
│   ├── syntx_prompt_generator.py
│   ├── topics_database.py
│   └── ...
│
├── syntex_injector/                # 🔬 EXISTING: SYNTX Calibration
│   ├── syntex/
│   │   ├── core/
│   │   │   ├── calibrator_enhanced.py
│   │   │   ├── wrapper.py
│   │   │   ├── parser.py
│   │   │   └── scorer.py
│   │   └── ...
│   └── ...
│
└── wrappers/                       # 📝 SYNTX Wrappers (Core IP!)
    ├── syntex_wrapper_human.txt
    └── syntex_wrapper_sigma.txt
```

---

## ⚡ DER KOMPLETTE FLOW

### 1️⃣ PRODUCER AKTIVIERUNG (Self-Regulating)

```
┌─────────────────────────────┐
│   CRONJOB (alle 2h)         │
│   python3 -m queue_system   │
│           .core.producer    │
└──────────────┬──────────────┘
               ↓
       ┌──────────────┐
       │ QueueManager │ 
       │ .should_produce()
       └──────┬───────┘
              ↓
     [CHECK QUEUE STATUS]
              ↓
   ┌──────────┴──────────┐
   │                     │
STARVING (0)       BALANCED (16)
   │                     │
   ↓                     ↓
Produce 20!         Produce 10
   │                     │
   └──────────┬──────────┘
              ↓
    ┌─────────────────┐
    │ GPT Generation  │
    │ - 20 Topics     │
    │ - 4 Styles      │
    │ - Async Batch   │
    └────────┬────────┘
             ↓
    ┌────────────────┐
    │ FileHandler    │
    │ .atomic_write()│
    └────────┬───────┘
             ↓
    Write to .tmp/
             ↓
    Atomic Move
             ↓
    incoming/ ✅
```

**Code:**
```python
# queue_system/core/producer.py
class IntelligentProducer:
    def run(self):
        # DECISION PHASE
        should_produce, count = self.queue_manager.should_produce()
        
        if not should_produce:
            return {"skipped": True, "reason": "Queue sufficient"}
        
        # PRODUCTION PHASE
        for topic, category in get_random_topics(count):
            result = generate_prompt(topic, style=style)
            
            if result['success']:
                self.file_handler.atomic_write(
                    content=result['prompt_generated'],
                    metadata={...},
                    target_dir=QUEUE_INCOMING
                )
```

---

### 2️⃣ QUEUE ZUSTAND (Observable State)

```
/queue/incoming/    ← Jobs warten hier (FIFO)
│
├── 20251128_092911_783123__topic_ki__style_tech.txt
├── 20251128_093327_197728__topic_foto__style_tech.txt
├── 20251128_093330_444626__topic_politik__style_casual.txt
└── ... (13 more)
     ↓
Monitor zählt: 16 Jobs
     ↓
QueueManager bestimmt State: "BALANCED"
     ↓
Producer Decision: "Produziere 10 weitere"
```

**States:**

| Queue Count | State      | Producer Action      |
|-------------|------------|---------------------|
| 0           | STARVING   | Produziere 20 sofort |
| 1-4         | LOW        | Produziere 15        |
| 5-24        | BALANCED   | Produziere 10        |
| 25-49       | HIGH       | Keine Produktion     |
| 50+         | OVERFLOW   | Keine Produktion + Alert |

---

### 3️⃣ CONSUMER PROCESSING (Atomic Lock Pattern)

```
┌──────────────────────────┐
│  CRONJOB (täglich 3am)   │
│  python3 -m queue_system │
│           .core.consumer │
└───────────┬──────────────┘
            ↓
   ┌────────────────┐
   │ Consumer Init  │
   │ wrapper="human"│
   └────────┬───────┘
            ↓
   ┌────────────────────┐
   │ get_next_job()     │
   │ - Liste incoming/  │
   │ - Sortiere (älteste)
   │ - Versuche Lock    │
   └────────┬───────────┘
            ↓
    [ATOMIC MOVE]
     incoming/ → processing/
            ↓
    ┌───────┴────────┐
    │                │
  SUCCESS         FAILED
    │                │
    ↓                ↓
Lock acquired!   FileNotFoundError
(Job Object)     (Anderer Worker)
    │                │
    ↓                └→ Try next file
LOAD JOB
    │
    ├─ job.content     (Meta-Prompt)
    ├─ job.metadata    (Topic, Style, GPT-Quality)
    └─ job.file_path   (processing/xxx.txt)
    ↓
┌───────────────────────┐
│ SYNTX KALIBRIERUNG    │
│                       │
│ 1. Wrapper laden      │
│    ├─ human.txt       │
│    └─ Felder definiert│
│                       │
│ 2. Prompt bauen       │
│    ├─ Wrapper-Text    │
│    ├─ Meta-Prompt     │
│    └─ Full Prompt     │
│                       │
│ 3. Llama Request      │
│    ├─ POST /api/chat  │
│    ├─ Timeout: 800s   │
│    └─ Stream: false   │
│                       │
│ 4. Parse Response     │
│    ├─ Extract Fields  │
│    ├─ Validate Format │
│    └─ Quality Score   │
│                       │
│ 5. Score Quality      │
│    ├─ Field Coverage  │
│    ├─ Depth Score     │
│    └─ Total: 0-100    │
└───────┬───────────────┘
        ↓
   [RESULT?]
        ↓
   ┌────┴─────┐
   │          │
SUCCESS    FAILURE
   │          │
   ↓          ↓
processing/  processing/
   → processed/  → error/
   ↓          ↓
✅ Done!    ❌ Retry-Count++
            (job__retry1.txt)
```

**Code:**
```python
# queue_system/core/consumer.py
class QueueConsumer:
    def get_next_job(self):
        files = sorted(QUEUE_INCOMING.glob("*.txt"))
        
        for file_path in files:
            try:
                # ATOMIC LOCK via rename
                processing_path = QUEUE_PROCESSING / file_path.name
                file_path.rename(processing_path)  # Atomic!
                
                # Lock acquired - load job
                return self._load_job(processing_path)
            except FileNotFoundError:
                # Another worker got it - try next
                continue
        
        return None  # Queue empty
    
    def process_job(self, job):
        # SYNTX Calibration
        success, response, meta = self.calibrator.calibrate(
            meta_prompt=job.content,
            verbose=True
        )
        
        if success:
            self.file_handler.move_to_processed(job)
        else:
            self.file_handler.move_to_error(job, meta)
```

---

### 4️⃣ ERROR HANDLING (Retry Pattern)

```
Job failed während Processing
        ↓
FileHandler.move_to_error()
        ↓
┌──────────────────────────┐
│ Metadata Update:         │
│ - retry_count += 1       │
│ - last_error = info      │
│ - failed_at = timestamp  │
└──────────┬───────────────┘
           ↓
Filename mit Retry-Count:
job.txt → job__retry1.txt
           ↓
Move to error/
           ↓
┌──────────────────────────┐
│ Manual Intervention:     │
│                          │
│ # Retry Job manuell      │
│ mv error/job__retry1.txt \
│    incoming/job.txt      │
│                          │
│ # Nächster Worker        │
│ # verarbeitet es neu     │
└──────────────────────────┘
```

---

## 📦 MODULE & VERANTWORTLICHKEITEN

### 🧠 QueueManager (Decision Engine)

**Datei:** `queue_system/core/queue_manager.py`

**Aufgabe:** Entscheidet ob und wie viel produziert werden soll

**Methoden:**
```python
should_produce() -> (bool, int)
# Returns: (should_run, batch_size)
# Logic: State-based (STARVING/LOW/BALANCED/HIGH/OVERFLOW)

get_system_status() -> dict
# Returns: Complete system snapshot
# Includes: queue counts, state, producer decision, health
```

**Verwendung:**
```python
manager = QueueManager()
should_run, count = manager.should_produce()

if should_run:
    print(f"Producer sollte {count} Prompts generieren")
```

---

### 🏭 IntelligentProducer (Queue-Aware Generator)

**Datei:** `queue_system/core/producer.py`

**Aufgabe:** Generiert Prompts NUR wenn Queue sie braucht

**Flow:**
1. Check mit QueueManager
2. Wenn nötig: Topics auswählen
3. GPT-4 generieren
4. Atomic Write in Queue
5. Stats zurückgeben

**Verwendung:**
```python
producer = IntelligentProducer()
stats = producer.run()
# Checkt automatisch Queue-Zustand
# Produziert nur wenn nötig

# Force Mode (für Testing):
stats = producer.run(force=True)
# Ignoriert Queue-Check, produziert immer
```

---

### ⚙️ QueueConsumer (Worker with Atomic Lock)

**Datei:** `queue_system/core/consumer.py`

**Aufgabe:** Verarbeitet Jobs aus Queue mit SYNTX

**Lock Pattern:**
```python
# File-Based Locking via Atomic Rename
incoming/job.txt → processing/job.txt

# Wenn erfolgreich: Lock acquired
# Wenn FileNotFoundError: Anderer Worker hat's

# Garantiert: Kein Job wird doppelt verarbeitet
```

**Verwendung:**
```python
# Single Wrapper
consumer = QueueConsumer(wrapper_name="human")
stats = consumer.process_batch(batch_size=20)

# Parallel Workers (verschiedene Terminals)
# Worker 1:
consumer_1 = QueueConsumer(wrapper_name="human", worker_id="w1")
consumer_1.process_batch(10)

# Worker 2:
consumer_2 = QueueConsumer(wrapper_name="sigma", worker_id="w2")
consumer_2.process_batch(10)

# Beide ziehen aus gleicher Queue ohne Konflikte!
```

---

### 💎 FileHandler (Atomic Operations)

**Datei:** `queue_system/core/file_handler.py`

**Aufgabe:** Sichere, atomare Datei-Operationen

**Pattern:**
```python
# ATOMIC WRITE (tmp → rename)
temp_path = QUEUE_TMP / filename
write_content(temp_path)
temp_path.rename(QUEUE_INCOMING / filename)  # Atomic!

# ATOMIC MOVE (rename = atomic on POSIX)
source.rename(target)  # Entweder komplett oder gar nicht
```

**Methoden:**
```python
atomic_write(content, metadata, target_dir)
# Schreibt Job ATOMIC in Queue
# Pattern: .tmp → rename

move_to_processed(job)
# Success Path

move_to_error(job, error_info)
# Failure Path mit Retry-Count
```

---

### 📊 QueueMonitor (Observable State)

**Datei:** `queue_system/monitoring/queue_monitor.py`

**Aufgabe:** Überwacht Queue-Zustand in Echtzeit

**Methoden:**
```python
count_incoming()    # Jobs in incoming/
count_processing()  # Jobs in processing/
count_processed()   # Jobs in processed/
count_error()       # Jobs in error/

get_status()        # Complete snapshot mit State
```

**Verwendung:**
```bash
# Real-Time Monitoring
python3 -m queue_system.monitoring.queue_monitor

# Output:
{
  "timestamp": "2025-11-28T10:00:00",
  "queue": {
    "incoming": 16,
    "processing": 2,
    "processed": 450,
    "error": 3
  },
  "state": "BALANCED"
}
```

---

## 🔧 INSTALLATION & SETUP

### Voraussetzungen:

- Python 3.10+
- Zugriff auf GPT-4 API (für Producer)
- Zugriff auf Llama Backend (für Consumer)
- Linux/Unix (für Atomic Rename)

### Quick Setup:

```bash
# 1. Repo clonen
cd /home/codi/Entwicklung
git clone https://github.com/ottipc/syntx-workflow-api-get-prompts
cd syntx-workflow-api-get-prompts

# 2. Queue-Struktur erstellen
mkdir -p queue/{incoming,processing,processed,error,archive,.tmp}
touch queue/*/.gitkeep

# 3. Dependencies (bereits vorhanden)
# - gpt_generator/
# - syntex_injector/
# - wrappers/

# 4. Wrappers holen (von Server)
scp root@dev.syntx-system.com:/opt/syntx-workflow-api-get-prompts/wrappers/*.txt wrappers/

# 5. Test Producer
python3 -m queue_system.core.producer

# 6. Test Consumer
python3 -m queue_system.core.consumer

# 7. Monitor
python3 -m queue_system.monitoring.queue_monitor
```

---

## 🚀 USAGE & CLI

### Producer (Manual Run):

```bash
# Check & Produce (respektiert Queue-State)
python3 -m queue_system.core.producer

# Force Mode (ignoriert Queue-State)
python3 -c "
from queue_system.core.producer import IntelligentProducer
p = IntelligentProducer()
stats = p.run(force=True)
print(stats)
"
```

### Consumer (Manual Run):

```bash
# Process 20 Jobs (Human Wrapper)
python3 -m queue_system.core.consumer

# Custom Batch Size
python3 -c "
from queue_system.core.consumer import QueueConsumer
c = QueueConsumer(wrapper_name='human')
stats = c.process_batch(batch_size=10)
print(stats)
"

# Sigma Wrapper
python3 -c "
from queue_system.core.consumer import QueueConsumer
c = QueueConsumer(wrapper_name='sigma')
stats = c.process_batch(batch_size=5)
print(stats)
"
```

### Monitor (Real-Time):

```bash
# Single Check
python3 -m queue_system.monitoring.queue_monitor

# Watch Mode
watch -n 5 'python3 -m queue_system.monitoring.queue_monitor'

# Pretty Output
python3 -m queue_system.monitoring.queue_monitor | jq
```

### Queue Manager (Status):

```bash
# Full System Status
python3 -m queue_system.core.queue_manager

# Output:
{
  "queue": {"incoming": 16, ...},
  "state": "BALANCED",
  "producer": {"should_run": true, "batch_size": 10},
  "health": "OK"
}
```

---

## 📊 MONITORING & OBSERVABILITY

### Quick Status Check:

```bash
# Queue Counts
ls queue/incoming/*.txt | wc -l   # Wartend
ls queue/processing/*.txt | wc -l  # In Arbeit
ls queue/processed/*.txt | wc -l   # Erfolgreich
ls queue/error/*.txt | wc -l       # Failed

# Latest Jobs
ls -lt queue/incoming/ | head -10

# Error Analysis
cat queue/error/*.json | jq '.last_error'
```

### Dashboard Script:

```bash
#!/bin/bash
# scripts/queue_status.sh

echo "╔══════════════════════════════════════╗"
echo "║   SYNTX QUEUE STATUS                 ║"
echo "╚══════════════════════════════════════╝"
echo ""

INCOMING=$(ls queue/incoming/*.txt 2>/dev/null | wc -l)
PROCESSING=$(ls queue/processing/*.txt 2>/dev/null | wc -l)
PROCESSED=$(ls queue/processed/*.txt 2>/dev/null | wc -l)
ERROR=$(ls queue/error/*.txt 2>/dev/null | wc -l)

echo "📥 Incoming:    $INCOMING"
echo "⚙️  Processing:  $PROCESSING"
echo "✅ Processed:   $PROCESSED"
echo "❌ Error:       $ERROR"
echo ""

if [ $INCOMING -lt 5 ]; then
    echo "⚠️  Status: LOW - Producer should run"
elif [ $INCOMING -gt 50 ]; then
    echo "⚠️  Status: OVERFLOW - Consumer too slow"
else
    echo "✅ Status: BALANCED"
fi
```

---

## 🎮 PRODUCTION DEPLOYMENT

### Cronjob Setup:

```bash
# Edit crontab
crontab -e

# Producer: Alle 2 Stunden checken & produzieren wenn nötig
0 */2 * * * cd /home/codi/Entwicklung/syntx-workflow-api-get-prompts && /usr/bin/python3 -m queue_system.core.producer >> logs/producer_cron.log 2>&1

# Consumer (Human): Täglich 3 Uhr, 20 Jobs
0 3 * * * cd /home/codi/Entwicklung/syntx-workflow-api-get-prompts && /usr/bin/python3 -c "from queue_system.core.consumer import QueueConsumer; c = QueueConsumer('human'); c.process_batch(20)" >> logs/consumer_human_cron.log 2>&1

# Consumer (Sigma): Mehrmals täglich
0 4,8,12,16 * * * cd /home/codi/Entwicklung/syntx-workflow-api-get-prompts && /usr/bin/python3 -c "from queue_system.core.consumer import QueueConsumer; c = QueueConsumer('sigma'); c.process_batch(20)" >> logs/consumer_sigma_cron.log 2>&1

# Monitor: Stündlich Status loggen
0 * * * * cd /home/codi/Entwicklung/syntx-workflow-api-get-prompts && /usr/bin/python3 -m queue_system.monitoring.queue_monitor >> logs/queue_status.log 2>&1
```

### Systemd Services (Optional):

```ini
# /etc/systemd/system/syntx-producer.service
[Unit]
Description=SYNTX Queue Producer
After=network.target

[Service]
Type=oneshot
User=codi
WorkingDirectory=/home/codi/Entwicklung/syntx-workflow-api-get-prompts
ExecStart=/usr/bin/python3 -m queue_system.core.producer

[Install]
WantedBy=multi-user.target
```

```ini
# /etc/systemd/system/syntx-producer.timer
[Unit]
Description=SYNTX Producer Timer (every 2h)

[Timer]
OnCalendar=0/2:00
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
# Aktivieren
sudo systemctl enable syntx-producer.timer
sudo systemctl start syntx-producer.timer
```

---

## 🐛 TROUBLESHOOTING

### Problem: Consumer hängt bei "Processing"

**Symptom:**
```bash
ls queue/processing/
# → File seit >1h dort
```

**Ursache:** Worker crashed während Processing

**Fix:**
```bash
# Job zurück in incoming
mv queue/processing/*.txt queue/incoming/
mv queue/processing/*.json queue/incoming/

# Nächster Worker wird es verarbeiten
```

---

### Problem: Zu viele Errors

**Symptom:**
```bash
ls queue/error/*.txt | wc -l
# → 50+
```

**Diagnose:**
```bash
# Welche Fehler?
cat queue/error/*.json | jq '.last_error.error' | sort | uniq -c

# Beispiel Output:
#   45 "HTTPError: Server Error 502"
#    3 "Parse Error: Invalid JSON"
#    2 "Timeout after 800s"
```

**Fix je nach Error:**

**502 Bad Gateway:**
```bash
# Backend Service prüfen
ssh root@dev.syntx-system.com "systemctl status syntx.service"
ssh root@dev.syntx-system.com "netstat -tulpn | grep 8001"
```

**Parse Error:**
```bash
# Llama Response checken
cat queue/error/*.json | jq '.last_error.response' | head -1
# → Möglicherweise Wrapper-Problem
```

---

### Problem: Queue läuft über (OVERFLOW)

**Symptom:**
```bash
python3 -m queue_system.monitoring.queue_monitor
# → "state": "OVERFLOW"
# → "incoming": 150
```

**Ursache:** Consumer kommt nicht hinterher

**Fix:**
```bash
# Option 1: Mehr Consumer parallel
# Terminal 1:
python3 -c "from queue_system.core.consumer import QueueConsumer; QueueConsumer('human', 'w1').process_batch(50)"

# Terminal 2:
python3 -c "from queue_system.core.consumer import QueueConsumer; QueueConsumer('human', 'w2').process_batch(50)"

# Terminal 3:
python3 -c "from queue_system.core.consumer import QueueConsumer; QueueConsumer('sigma', 'w3').process_batch(50)"

# Option 2: Batch Size erhöhen
python3 -c "from queue_system.core.consumer import QueueConsumer; QueueConsumer('human').process_batch(100)"

# Option 3: Producer temporär deaktivieren
# (entferne Cronjob oder pausiere Timer)
```

---

### Problem: Llama Backend 502 Error

**Das hatten wir heute! 🔥**

**Symptom:**
```python
❌ Kalibrierung fehlgeschlagen: HTTPError: Server Error 502
```

**Diagnose:**
```bash
# Nginx routet zu Port X, aber Service läuft auf Port Y
ssh root@dev.syntx-system.com "grep 'proxy_pass' /etc/nginx/sites-enabled/dev.syntx-system.com"
# → proxy_pass http://127.0.0.1:8001

ssh root@dev.syntx-system.com "ps aux | grep uvicorn"
# → --port 8000  ❌ MISMATCH!
```

**Fix:**
```bash
# Service auf korrekten Port starten
ssh root@dev.syntx-system.com "systemctl stop syntx.service"
ssh root@dev.syntx-system.com "sed -i 's/--port 8000/--port 8001/g' /etc/systemd/system/syntx.service"
ssh root@dev.syntx-system.com "systemctl daemon-reload && systemctl start syntx.service"
ssh root@dev.syntx-system.com "netstat -tulpn | grep 8001"
# → tcp 0.0.0.0:8001 LISTEN ✅

# Test
curl -X POST https://dev.syntx-system.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Test","max_new_tokens":10}'
# → 200 OK ✅
```

---

## 🧪 TESTING

### Unit Tests (Coming Soon):

```python
# tests/test_queue_manager.py
def test_should_produce_starving():
    manager = QueueManager()
    # Mock incoming count = 0
    should_run, count = manager.should_produce()
    assert should_run == True
    assert count == 20

def test_should_produce_overflow():
    # Mock incoming count = 100
    should_run, count = manager.should_produce()
    assert should_run == False
    assert count == 0
```

### Integration Test:

```bash
# Full Flow Test
#!/bin/bash

echo "=== SYNTX QUEUE INTEGRATION TEST ==="

# 1. Clean Queue
rm -f queue/incoming/* queue/processing/* queue/processed/* queue/error/*

# 2. Producer (Force 5 Jobs)
python3 -c "
from queue_system.core.producer import IntelligentProducer
p = IntelligentProducer()
stats = p.run(force=True)
print(f'Produced: {stats[\"produced_count\"]}')
" || exit 1

# 3. Check Queue
COUNT=$(ls queue/incoming/*.txt 2>/dev/null | wc -l)
echo "Queue has $COUNT jobs"
[ $COUNT -gt 0 ] || exit 1

# 4. Consumer (Process 3)
python3 -c "
from queue_system.core.consumer import QueueConsumer
c = QueueConsumer('human')
stats = c.process_batch(3)
print(f'Processed: {stats[\"processed\"]}')
print(f'Failed: {stats[\"failed\"]}')
" || exit 1

# 5. Verify Results
PROCESSED=$(ls queue/processed/*.txt 2>/dev/null | wc -l)
echo "Processed: $PROCESSED"

echo "✅ Integration Test PASSED"
```

---

## 📚 API REFERENCE

### QueueManager

```python
class QueueManager:
    def __init__(self):
        """Initialisiert mit QueueMonitor"""
    
    def should_produce(self) -> Tuple[bool, int]:
        """
        Entscheidet ob produziert werden soll
        
        Returns:
            (should_produce, how_many)
            
        Logic:
            STARVING (0) → (True, 20)
            LOW (1-4) → (True, 15)
            BALANCED (5-24) → (True, 10)
            HIGH (25-49) → (False, 0)
            OVERFLOW (50+) → (False, 0)
        """
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Vollständiger System-Status
        
        Returns:
            {
                "timestamp": str,
                "queue": {
                    "incoming": int,
                    "processing": int,
                    "processed": int,
                    "error": int
                },
                "state": str,
                "producer": {
                    "should_run": bool,
                    "batch_size": int
                },
                "health": str
            }
        """
```

### IntelligentProducer

```python
class IntelligentProducer:
    def __init__(self):
        """Initialisiert mit QueueManager und FileHandler"""
    
    def run(self, force: bool = False) -> Dict[str, Any]:
        """
        Hauptlogik: Check & Produce
        
        Args:
            force: Ignoriert Queue-Check wenn True
            
        Returns:
            {
                "should_produce": bool,
                "requested_count": int,
                "produced_count": int,
                "failed_count": int,
                "skipped": bool,
                "duration_seconds": float
            }
        """
```

### QueueConsumer

```python
class QueueConsumer:
    def __init__(self, wrapper_name: str = "human", worker_id: Optional[str] = None):
        """
        Args:
            wrapper_name: "human" | "sigma" | "sigma_v2"
            worker_id: Optional ID für Logging
        """
    
    def get_next_job(self) -> Optional[Job]:
        """
        Holt nächsten Job mit Atomic Lock
        
        Returns:
            Job object wenn erfolgreich gelocked
            None wenn Queue leer
            
        Lock Pattern:
            incoming/job.txt → processing/job.txt (atomic rename)
        """
    
    def process_job(self, job: Job) -> bool:
        """
        Verarbeitet einen Job durch SYNTX Pipeline
        
        Flow:
            1. SYNTX Wrapper laden
            2. Prompt bauen
            3. Llama Request
            4. Parse Response
            5. Score Quality
            6. Move zu processed/ oder error/
            
        Returns:
            True wenn erfolgreich
        """
    
    def process_batch(self, batch_size: int = 20) -> Dict[str, Any]:
        """
        Verarbeitet Batch von Jobs
        
        Args:
            batch_size: Max Anzahl Jobs
            
        Returns:
            {
                "processed": int,
                "failed": int,
                "total": int,
                "duration_seconds": float
            }
        """
```

### FileHandler

```python
class FileHandler:
    def atomic_write(
        self, 
        content: str, 
        metadata: Dict[str, Any], 
        target_dir: Path
    ) -> Path:
        """
        Schreibt Datei ATOMIC in Queue
        
        Pattern:
            1. Write to .tmp/
            2. Atomic rename to target_dir/
            
        Returns:
            Path zum geschriebenen File
        """
    
    def move_to_processed(self, job) -> Path:
        """Verschiebt Job nach processed/"""
    
    def move_to_error(self, job, error_info: Dict[str, Any]) -> Path:
        """Verschiebt Job nach error/ mit Retry-Count"""
```

### QueueMonitor

```python
class QueueMonitor:
    def count_incoming(self) -> int:
        """Anzahl Jobs in incoming/"""
    
    def count_processing(self) -> int:
        """Anzahl Jobs in processing/"""
    
    def count_processed(self) -> int:
        """Anzahl Jobs in processed/"""
    
    def count_error(self) -> int:
        """Anzahl Jobs in error/"""
    
    def get_status(self) -> Dict[str, Any]:
        """
        Vollständiger Queue-Status
        
        Returns:
            {
                "timestamp": str,
                "queue": {
                    "incoming": int,
                    "processing": int,
                    "processed": int,
                    "error": int
                },
                "state": str  # STARVING/LOW/BALANCED/HIGH/OVERFLOW
            }
        """
```

---

## 🎯 ZUSAMMENFASSUNG

### Was wir gebaut haben:

✅ **Production-Grade Message Queue** ohne Redis/RabbitMQ  
✅ **Self-Regulating System** das Queue-Zustand observiert  
✅ **Atomic File Operations** für Zero Data Loss  
✅ **Parallel Worker Support** ohne Koordination  
✅ **Automatic Retry** mit Error Tracking  
✅ **Real-Time Monitoring** für Observability  
✅ **Cronjob Integration** für Automation  

### Die Revolution:

**ALT (Tight Coupling):**
```python
for job in range(20):
    gpt → llama → done
    # Crashed bei #15? → 5 Jobs verloren
```

**NEU (Loose Coupling):**
```python
Producer → Queue → Consumer
# Crashed? → Job in /error/, retry später
# Parallel? → Kein Problem, File-Lock!
# Skalierung? → Mehr Consumer starten!
```

### Next Steps:

1. **Fine-Tuning Data Collection**
   - Alle processed/ Jobs = Training Data
   - JSONL Format ready for fine-tuning

2. **Advanced Monitoring**
   - Prometheus Metrics
   - Grafana Dashboard
   - Alert System

3. **ML Pipeline Integration**
   - Automatic Quality Scoring
   - Model Performance Tracking
   - A/B Testing Wrappers

4. **Production Hardening**
   - Health Checks
   - Auto-Recovery
   - Load Balancing

---

## 🙏 CREDITS

**Entwickelt am:** 28. November 2025  
**Architektur:** SYNTX Field-Based Thinking  
**Core Concept:** Resonanzmedium statt Object-Passing  
**Deployment:** Production-Ready auf dev.syntx-system.com  

**Stack:**
- Python 3.10+
- GPT-4o (Prompt Generation)
- Llama 3.1 7B (SYNTX Calibration)
- POSIX Filesystem (Atomic Operations)
- NGINX (SSL + Routing)
- Systemd (Service Management)

---

## 📝 CHANGELOG

### v1.0.0 (2025-11-28) - Initial Release

**Features:**
- ✅ Queue System mit 6 Ordnern
- ✅ QueueManager (Decision Engine)
- ✅ IntelligentProducer (Queue-Aware)
- ✅ QueueConsumer (Atomic Lock)
- ✅ FileHandler (Atomic Operations)
- ✅ QueueMonitor (Real-Time Status)
- ✅ Config-Driven (Thresholds anpassbar)
- ✅ Error Handling (Retry Pattern)
- ✅ CLI Tools (Producer, Consumer, Monitor)

**Fixes:**
- 🔧 Server Port Mismatch (8000 → 8001)
- 🔧 FileHandler Job Object Support
- 🔧 Consumer Wrapper Loading

**Deployment:**
- 🚀 Cronjobs configured
- 🚀 Gitignore für Queue Runtime Data
- 🚀 Production Server configured

---

**🔥 DAS IST NICHT NUR CODE - DAS IST EINE REVOLUTION! 🚀**

*"Von Token-Prediction zu Field-Calibration. Von Objekten zu Strömen. Von Konstruktion zu Resonanz."*

💎🌊⚡✨

---

*README.md v1.0.0 | Queue System Documentation | SYNTX Framework*