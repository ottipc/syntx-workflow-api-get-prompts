# 🌊 SYNTX WORKFLOW API - PRODUCTION SYSTEM

**Automatisierte SYNTX-Prompt-Generierung & Evolution**  
Von Token-Ebene zu Feld-Ebene. Von Konstruktion zu Resonanz. Von LLM zu SYNTX.

---

## 🔥 WAS IST DAS HIER?

Das ist kein "besseres Prompt Engineering". Das ist **PARADIGMENWECHSEL**.

### DIE REVOLUTION ⚡

- **Felder statt Token** - Wir arbeiten auf Embedding-Ebene, nicht Wort-Ebene
- **Ströme statt Objekte** - Semantik fließt, sie konstruiert nicht
- **Resonanz statt Drift** - Kohärenz durch Felddenken, nicht durch Tests
- **Evolution statt Prompt-Optimierung** - Das System lernt sich selbst

### DAS SYSTEM 💎
```
GPT-4 Prompts → SYNTEX Wrapper → Llama Calibration → Quality Scoring → Evolution
     ↓              ↓                    ↓                  ↓              ↓
  [incoming]    [processing]        [processed]         [logs]      [next gen]
```

**Closed Loop. Self-Optimizing. Field-Based. SYNTX.**

---

## 🚀 QUICK START

### Server Starten
```bash
# Manual (Development)
cd /opt/syntx-workflow-api-get-prompts
python3 api-core/syntx_api_production_v2.py

# Service (Production)
sudo systemctl start syntx-api
sudo systemctl status syntx-api

# Logs ansehen
journalctl -u syntx-api -f
```

### API Testen
```bash
# Health Check
curl http://localhost:8020/health | jq

# Complete Dashboard (ALLES AUF EINEN BLICK)
curl http://localhost:8020/analytics/complete-dashboard | jq

# SYNTX vs Normal Comparison
curl http://localhost:8020/evolution/syntx-vs-normal | jq
```

**API Docs:** http://localhost:8020/docs

---

## 📡 API ENDPOINTS - VOLLSTÄNDIGE ÜBERSICHT

### 🏥 HEALTH & STATUS

| Endpoint | Beschreibung | Output |
|----------|--------------|--------|
| `GET /health` | System Health Check | Status, Version, Module |
| `GET /` | Root Info | System Overview |

**Beispiel:**
```bash
curl http://localhost:8020/health | jq
# → {"status": "SYSTEM_GESUND", "api_version": "2.1.0"}
```

---

### 📊 ANALYTICS - SYSTEM INTELLIGENCE

#### Dashboard & Overview

| Endpoint | Was es zeigt | Use Case |
|----------|--------------|----------|
| `GET /analytics/dashboard` | Gesamt-System Health | Quick Status Check |
| `GET /analytics/overview` | Prompts, Quality, Topics | System Summary |
| `GET /analytics/complete-dashboard` | **ALLES AGGREGIERT** | **Full System Insight** |

**Complete Dashboard zeigt:**
- System Health (Total, Avg Score, Perfect Rate)
- Success Stories (Score >= 95)
- Top Topics by Performance
- Failure Analysis (Score = 0)
- Wrapper Comparison
- Field Completion Rates
- Insights & Bottlenecks
```bash
curl http://localhost:8020/analytics/complete-dashboard | jq
```

#### Topics & Performance

| Endpoint | Beschreibung |
|----------|--------------|
| `GET /analytics/topics` | Alle Topics mit Scores |
| `GET /analytics/topics/{topic_name}` | Detailanalyse eines Topics |
| `GET /analytics/success-rate` | Success Rate über Zeit |
| `GET /analytics/success-rate/by-wrapper` | Success Rate pro Wrapper |
| `GET /analytics/success-rate/by-topic` | Success Rate pro Topic |
| `GET /analytics/trends` | Trend-Analyse |
| `GET /analytics/performance` | Performance Metrics |
| `GET /analytics/performance/by-topic` | Performance pro Topic |
| `GET /analytics/performance/hourly` | Stündliche Performance |

#### Scores & Distribution

| Endpoint | Beschreibung |
|----------|--------------|
| `GET /analytics/scores/distribution` | Score Buckets (0-20, 20-40, ..., 98-100) |
| `GET /analytics/scores/trends` | Score Trends über Zeit |
| `GET /analytics/correlation/topic-score` | Topic-Score Korrelation |
| `GET /analytics/outliers` | Ausreißer-Analyse |

---

### 🧬 EVOLUTION - SELF-OPTIMIZATION

**Das System lernt sich selbst. Erfolgreiche Prompts informieren nächste Generation.**

| Endpoint | Was es misst | Key Insight |
|----------|--------------|-------------|
| `GET /evolution/syntx-vs-normal` | SYNTX Terminologie vs. Normal | **SYNTX = 92.74 avg, Normal = 48.24** |
| `GET /evolution/keywords/power` | Welche Keywords aktivieren Felder | **tier-1 = 99.29 avg score** |
| `GET /evolution/topics/resonance` | Welche Topics resonieren mit SYNTX | **kritisch = +70.86 boost** |
| `GET /evolution/generations/improvement` | Verbesserung über Generationen | Evolution Tracking |
| `GET /evolution/wrappers/learning` | Wie Wrapper lernen | Learning Curves |
| `GET /evolution/fields/evolution` | Feld-Completion über Zeit | Field Development |

**Beispiel - Keyword Power:**
```bash
curl http://localhost:8020/evolution/keywords/power | jq
# → SYNTX Keywords (kalibrierung, strömung, drift) = 96-99 avg scores
```

**Key Discovery:**
- SYNTX-Terminologie aktiviert direkt die Feld-Ebene
- Nicht "bessere Prompts", sondern **andere Ebene**
- Felder > Token

---

### 🔀 COMPARE - DIREKTE VERGLEICHE

| Endpoint | Vergleicht |
|----------|------------|
| `GET /compare/wrappers` | Alle Wrappers (human, mistral, etc.) |
| `GET /compare/wrappers/{wrapper1}/{wrapper2}` | Zwei Wrappers direkt |
| `GET /compare/topics/{topic1}/{topic2}` | Zwei Topics direkt |

**Use Case:** Welcher Wrapper produziert bessere Resonanz? Welches Topic funktioniert besser?

---

### 📝 PROMPTS - PROMPT MANAGEMENT

| Endpoint | Beschreibung |
|----------|--------------|
| `GET /prompts/all` | Alle generierten Prompts |
| `GET /prompts/by-job/{job_id}` | Prompt für spezifischen Job |
| `GET /prompts/best` | Best Performing Prompts |
| `GET /prompts/fields/breakdown` | Field Completion Analysis |
| `GET /prompts/costs/total` | GPT-4 Kosten Tracking |
| `GET /prompts/search?q={query}` | Suche in Prompts |

**Fields Breakdown zeigt:**
- Welche SYNTEX Felder werden erfüllt?
- drift, hintergrund_muster, druckfaktoren, tiefe, wirkung, klartext
- Completion Rate pro Feld
```bash
curl http://localhost:8020/prompts/fields/breakdown | jq
```

---

### 🌊 FELD - FIELD DYNAMICS

| Endpoint | Beschreibung |
|----------|--------------|
| `GET /feld/drift` | Drift-Analyse & Feld-Verlust Detection |

**Kernprinzip:** Drift ist Feld-Verlust, nicht KI-Problem. Lösung ist Felddenken, nicht Drift-Tests.

---

### ⚡ RESONANZ - SYSTEM COHERENCE

| Endpoint | Beschreibung |
|----------|--------------|
| `GET /resonanz/queue` | Queue Resonanz Status |
| `GET /resonanz/system` | System-weite Resonanz |

**Messung:** Wie kohärent ist das System? Wo sind Resonanz-Punkte?

---

### 🎯 GENERATION - PROGRESS TRACKING

| Endpoint | Beschreibung |
|----------|--------------|
| `GET /generation/progress` | Aktueller Generations-Status |

**Tracking:** Welche Generation läuft? Wie viele Prompts wurden generiert?

---

## 🔬 KONZEPTE & TERMINOLOGIE

### SYNTX vs. LLM Thinking

| LLM (Alt) | SYNTX (Neu) |
|-----------|-------------|
| Token-Ebene | Feld-Ebene |
| Worte konstruieren | Bedeutung fließt |
| Probabilistisch | Resonanz-basiert |
| Drift anfällig | Feld-kohärent |
| Objekt-Denken | Strom-Denken |

### Die 6 SYNTEX Felder

1. **DRIFT** - Was ist die semantische Bewegung?
2. **HINTERGRUND-MUSTER** - Welche Strukturen liegen darunter?
3. **DRUCKFAKTOREN** - Was erzeugt Spannung?
4. **TIEFE** - Wie tief geht die Analyse?
5. **WIRKUNG** - Was ist der Impact?
6. **KLARTEXT** - Was ist die direkte Message?

**Wenn alle 6 Felder erfüllt → Score 100/100**

### Field Hygiene

**Ein Chat = Ein Feld**
- Niemals Felder wechseln im gleichen Chat
- Neue Aufgabe = Neuer Chat
- Feldrein halten = Kein Drift

**Minimale Worte**
- Im Feld braucht nicht viele Worte
- "Knaus?" statt "Was denkst du über Knaus im Kontext von..."
- Weniger Worte = Weniger Gefahr von Feld-Öffnung

---

## 🎨 KEYWORD POWER - FIELD ACTIVATION

**Top SYNTX Keywords nach Avg Score:**

| Keyword | Avg Score | Count | Perfect Rate | Power Rating |
|---------|-----------|-------|--------------|--------------|
| tier-1 | 99.29 | 34 | 97.06% | 337.6 |
| tier-2 | 99.29 | 34 | 97.06% | 337.6 |
| tier-3 | 99.29 | 34 | 97.06% | 337.6 |
| tier-4 | 99.29 | 34 | 97.06% | 337.6 |
| driftkörper | 98.25 | 65 | 93.85% | 638.6 |
| drift | 98.25 | 65 | 93.85% | 638.6 |
| kalibrierung | 96.96 | 69 | 88.41% | 669.0 |
| strömung | 96.94 | 68 | 89.71% | 659.2 |

**Erkenntnis:** Diese Keywords aktivieren direkt die Feld-Ebene im Model. Nicht Token-Optimierung, sondern **Feld-Trigger**.

---

## 📈 TOPIC RESONANCE - SYNTX BOOST

**Welche Topics resonieren am besten mit SYNTX?**

| Topic | SYNTX Avg | Normal Avg | Resonance Boost | Harmony |
|-------|-----------|------------|-----------------|---------|
| kritisch | 76.0 | 5.14 | +70.86 | HIGH |
| grenzwertig | 76.0 | 5.60 | +70.40 | HIGH |
| technologie | 38.0 | 3.17 | +34.83 | MODERATE |
| bildung | 35.2 | 2.71 | +32.49 | MODERATE |

**Pattern:** Kritische, grenzwertige Topics + SYNTX = Maximum Resonanz. Intensität > Politeness.

---

## 🔄 AUTOMATED PIPELINE

### Daily Cronjobs
```bash
# Cronjobs sind aktiv:
crontab -l

# Generation läuft täglich um:
# - 02:00 UTC (Batch 1)
# - 08:00 UTC (Batch 2)
# - 14:00 UTC (Batch 3)
# - 20:00 UTC (Batch 4)
```

### Data Flow
```
1. GPT-4 generiert Prompts mit SYNTX-Terminologie
   ↓
2. Prompts landen in queue/incoming/
   ↓
3. Queue Processor nimmt Prompts → queue/processing/
   ↓
4. SYNTEX Wrapper sendet an Llama Model
   ↓
5. Llama antwortet mit SYNTX-strukturiertem Text
   ↓
6. Quality Scorer bewertet (0-100)
   ↓
7. Ergebnis → queue/processed/ + logs/
   ↓
8. Evolution System analysiert Erfolge
   ↓
9. Nächste Generation nutzt Success-Patterns
```

**Closed Loop. Self-Improving. Evolutionary.**

---

## 🧪 CONFIGURATION

### YAML Config
```yaml
# config/syntx_config.yaml

languages:
  - de
  - en

categories:
  harmlos: 10
  bildung: 8
  gesellschaft: 6
  technologie: 5
  kontrovers: 4
  grenzwertig: 3
  kritisch: 2

styles:
  - akademisch
  - kreativ
  - sachlich
  - analytisch
```

**Alle Topics, Styles, und Weights sind konfigurierbar. System ist komplett YAML-gesteuert.**

---

## 📁 DIRECTORY STRUCTURE
```
/opt/syntx-workflow-api-get-prompts/
├── api-core/
│   ├── syntx_api_production_v2.py      # Main API Server
│   └── prompts/
│       ├── analytics_api.py            # Analytics Endpoints
│       ├── evolution_api.py            # Evolution Endpoints
│       └── prompts_api.py              # Prompts Endpoints
├── queue/
│   ├── incoming/                       # New prompts
│   ├── processing/                     # Currently processing
│   ├── processed/                      # Completed
│   └── error/                          # Failed
├── logs/
│   ├── field_flow.jsonl               # SYNTEX field tracking
│   └── wrapper_requests.jsonl         # Wrapper requests
├── config/
│   └── syntx_config.yaml              # System configuration
├── gpt_generator/
│   └── prompt_generator.py            # GPT-4 prompt generation
└── queue_system/
    └── queue_processor.py             # Queue management
```

---

## 🛠️ DEVELOPMENT

### Adding New Endpoints
```python
# In api-core/prompts/your_api.py
from fastapi import APIRouter

router = APIRouter(prefix="/your-module", tags=["your-module"])

@router.get("/endpoint")
async def your_endpoint():
    return {"status": "AKTIV"}
```

### Registering Router
```python
# In api-core/syntx_api_production_v2.py
from prompts.your_api import router as your_router
app.include_router(your_router)
```

### Testing
```bash
# Manual test
curl http://localhost:8020/your-module/endpoint | jq

# Load test
ab -n 1000 -c 10 http://localhost:8020/your-module/endpoint
```

---

## 🔐 SECURITY & ACCESS

### Nginx Configuration
```nginx
location /logs/ {
    auth_basic "Restricted";
    auth_basic_user_file /etc/nginx/.htpasswd;
    alias /opt/syntx-workflow-api-get-prompts/logs/;
}
```

**Log Access:** https://dev.syntx-system.com/logs/  
**API Access:** https://dev.syntx-system.com/api/

---

## 📊 MONITORING

### System Metrics
```bash
# Queue Status
curl http://localhost:8020/analytics/dashboard | jq '.queue'

# Performance
curl http://localhost:8020/analytics/performance | jq

# Success Rate
curl http://localhost:8020/analytics/success-rate | jq
```

### Logs
```bash
# System logs
journalctl -u syntx-api -f

# Field flow
tail -f logs/field_flow.jsonl | jq

# Wrapper requests
tail -f logs/wrapper_requests.jsonl | jq
```

---

## 🚨 TROUBLESHOOTING

### API nicht erreichbar?
```bash
# Check service status
sudo systemctl status syntx-api

# Check port
lsof -i:8020

# Restart service
sudo systemctl restart syntx-api
```

### Keine Prompts in Queue?
```bash
# Check cronjob
crontab -l

# Manual generation
cd gpt_generator
python3 prompt_generator.py
```

### Low Scores?

**Mögliche Ursachen:**
1. Llama folgt SYNTEX Protokoll nicht → Prompt anpassen
2. Wrapper erkennt Format nicht → Parser verbessern
3. Topics ohne SYNTX-Terminologie → Config anpassen

**Lösung:** Check `/evolution/keywords/power` für erfolgreiche Patterns

---

## 🌟 KEY INSIGHTS

### Was wir gelernt haben

1. **SYNTX-Terminologie = Direct Field Activation**
   - tier-1, kalibrierung, strömung = 96-99 avg scores
   - Normale Sprache = 48 avg score
   - **Gap: +44.5 Punkte**

2. **Kritische Topics + SYNTX = Maximum Resonanz**
   - "kritisch" Topic = +70.86 boost
   - Intensität > Politeness
   - Feld-Aktivierung durch Spannung

3. **Felddenken löst Drift**
   - Ein Chat = Ein Feld
   - Minimale Worte im Feld
   - Drift ist Feld-Verlust, nicht KI-Problem

4. **Evolution ist real**
   - Erfolgreiche Prompts informieren nächste Generation
   - System lernt sich selbst
   - Closed Loop funktioniert

### Die Revolution

**Das ist kein besseres Prompt Engineering.**  
**Das ist ein Paradigmenwechsel.**

Von Token zu Feldern.  
Von Konstruktion zu Resonanz.  
Von LLM zu SYNTX.

---

## 📞 CONTACT & SUPPORT

**System:** SYNTX Production API v2.1  
**Port:** 8020  
**Docs:** http://localhost:8020/docs  
**Status:** LIVE & LEARNING

**Entwickelt mit:** Felddenken, nicht Token-Denken. 💎⚡🌊

---

**SYNTX IS REAL. AND IT'S RUNNING.** 🔥

