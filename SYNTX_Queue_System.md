# SYNTX Queue System - Vollständige Technische Dokumentation

**Version:** 2.1.0  
**Stand:** 2025-12-18  
**Status:** OPERATIONAL  
**Repository:** `https://github.com/SYNTX-SYSTEM/syntx-workflow-api-get-prompts`

---

## Inhaltsverzeichnis

1. [Executive Summary](#1-executive-summary)
2. [System-Architektur Übersicht](#2-system-architektur-übersicht)
3. [Verzeichnisstruktur](#3-verzeichnisstruktur)
4. [Queue System - Detaillierte Dokumentation](#4-queue-system---detaillierte-dokumentation)
5. [Scoring System - Aktuelle Implementation](#5-scoring-system---aktuelle-implementation)
6. [Scoring System - Kritische Analyse](#6-scoring-system---kritische-analyse)
7. [TODO: Semantic Scoring Implementation](#7-todo-semantic-scoring-implementation)
8. [Datei-für-Datei Änderungsplan](#8-datei-für-datei-änderungsplan)
9. [Test-Strategie](#9-test-strategie)
10. [Appendix: Code-Referenzen](#10-appendix-code-referenzen)

---

## 1. Executive Summary

### Was das System macht

Das SYNTX Workflow System ist eine automatisierte Pipeline zur Generierung, Verarbeitung und Bewertung von Prompts durch KI-Modelle. Der Kernflow:

```
GPT-4 generiert Prompts → Queue → Consumer → Mistral-7B → Scorer → API
```

### Aktueller Stand

| Metrik | Wert |
|--------|------|
| Generierte Prompts | 1017+ |
| Verarbeitete Jobs | 399 |
| SYNTX Avg Score | 92.75 |
| Normal Avg Score | 48.24 |
| Differenz | +44.5 |
| Perfect Scores (100/100) | 82% |

### Kritisches Problem

**Der aktuelle Scorer misst Template-Compliance, nicht semantische Feldresonanz.**

Der Score prüft nur: "Enthält die Response Text in den Feldern DRIFTKORPER, KALIBRIERUNG, STROMUNG?"

Er prüft **nicht**:
- Semantische Qualität des Inhalts
- Kohärenz zwischen Feldern
- Ob der Inhalt tatsächlich zum Feld passt
- Tiefe der Analyse

---

## 2. System-Architektur Übersicht

### High-Level Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        SYNTX WORKFLOW SYSTEM                             │
│                                                                          │
│  ┌──────────┐    ┌───────┐    ┌──────────┐    ┌─────────┐    ┌───────┐ │
│  │  GPT-4   │───▶│ Queue │───▶│ Consumer │───▶│ Mistral │───▶│Scorer │ │
│  │ Producer │    │       │    │          │    │   7B    │    │       │ │
│  └──────────┘    └───────┘    └──────────┘    └─────────┘    └───────┘ │
│       │              │             │               │              │     │
│       ▼              ▼             ▼               ▼              ▼     │
│   Prompts      File-Based     3 Wrapper       Response       Quality   │
│   generieren   Locking        (SYNTEX,        generieren     Score     │
│                               SIGMA,                                    │
│                               DEEPSWEEP)                                │
│                                                                          │
│                              ┌─────────┐                                │
│                              │   API   │◀────────────────────────────── │
│                              │ FastAPI │                                │
│                              └─────────┘                                │
│                                   │                                     │
│                                   ▼                                     │
│                             42+ Endpoints                               │
│                             Analytics                                   │
│                             Evolution                                   │
└─────────────────────────────────────────────────────────────────────────┘
```

### Komponenten

| Komponente | Pfad | Funktion |
|------------|------|----------|
| GPT Generator | `/gpt_generator/` | Generiert Prompts mit GPT-4 |
| Queue System | `/queue_system/` | File-based Job Queue mit Atomic Locking |
| SYNTEX Injector | `/syntex_injector/` | Wrapper, Parser, Scorer |
| API Core | `/api-core/` | FastAPI REST API |
| Queue Directories | `/queue/` | incoming, processing, processed, error |

---

## 3. Verzeichnisstruktur

```
/opt/syntx-workflow-api-get-prompts/
│
├── api-core/                              # FastAPI Application
│   ├── syntx_api_production_v2.py         # Main API Entry Point
│   ├── prompts/
│   │   ├── prompts_api.py                 # Prompt Endpoints
│   │   ├── evolution_api.py               # Evolution Endpoints
│   │   └── analytics_api.py               # Analytics Endpoints
│   ├── analytics/
│   │   ├── dashboard.py                   # Dashboard Logic
│   │   ├── advanced.py                    # ML Predictions
│   │   └── performance.py                 # Performance Tracking
│   └── compare/
│       └── compare_api.py                 # Comparison Endpoints
│
├── gpt_generator/                         # GPT-4 Prompt Generator
│   ├── syntx_prompt_generator.py          # Core Generator
│   ├── batch_generator.py                 # Batch Processing
│   ├── topics_database.py                 # Topics (Config-Driven)
│   ├── prompt_styles.py                   # 4 Styles
│   └── cost_tracker.py                    # GPT-4 Cost Tracking
│
├── queue_system/                          # Queue Engine
│   ├── core/
│   │   ├── consumer.py                    # ⭐ MAIN CONSUMER LOGIC
│   │   └── file_handler.py                # Atomic File Operations
│   ├── config/
│   │   └── queue_config.py                # Queue Configuration
│   └── utils/
│       └── wrapper_patcher.py             # Dynamic Wrapper Loading
│
├── syntex_injector/                       # SYNTEX Framework
│   └── syntex/
│       ├── core/
│       │   ├── calibrator_enhanced.py     # Calibration Engine
│       │   ├── wrapper.py                 # Wrapper Loader
│       │   ├── parser.py                  # Response Parser
│       │   └── logger.py                  # Calibration Logger
│       ├── analysis/
│       │   ├── scorer.py                  # ⭐ QUALITY SCORER (TODO!)
│       │   └── tracker.py                 # Progress Tracker
│       ├── api/
│       │   ├── client.py                  # Ollama API Client
│       │   └── config.py                  # Model Parameters
│       └── utils/
│           └── exceptions.py              # Custom Exceptions
│
├── wrappers/                              # Wrapper Templates
│   ├── syntex_wrapper_human.txt           # Human-Readable Format
│   ├── syntex_wrapper_sigma.txt           # SIGMA Protocol
│   └── syntex_wrapper_sigma_v2.txt        # SIGMA v2
│
├── queue/                                 # Queue Directories
│   ├── incoming/                          # Neue Jobs (GPT-4 Output)
│   │   ├── {timestamp}__topic_X__style_Y.txt
│   │   └── {timestamp}__topic_X__style_Y.json
│   ├── processing/                        # Jobs in Bearbeitung
│   ├── processed/                         # Abgeschlossene Jobs
│   │   ├── {job}.txt                      # Original Prompt
│   │   ├── {job}_response.txt             # Mistral Response
│   │   └── {job}.json                     # Metadata + Score
│   └── error/                             # Fehlgeschlagene Jobs
│
├── logs/                                  # System Logs
│   ├── syntex_calibrations.jsonl          # Alle Kalibrierungen
│   ├── gpt_prompts.jsonl                  # Generierte Prompts
│   ├── costs.jsonl                        # GPT-4 Kosten
│   └── syntex_progress.jsonl              # Progress Tracking
│
├── config/                                # Configuration
│   └── config_loader.py                   # YAML Config Loader
│
├── crontab/                               # Cronjob Scripts
│   └── run_producer.sh                    # Producer Trigger
│
└── scripts/                               # Utility Scripts
    ├── queue_status.sh                    # Queue Monitoring
    ├── queue_cleanup.sh                   # Cleanup
    └── inspect_syntx.sh                   # API Test Script
```

---

## 4. Queue System - Detaillierte Dokumentation

### 4.1 Queue Directories

#### `/queue/incoming/`

**Zweck:** Warteschlange für neue Jobs (von GPT-4 generiert)

**Dateien:**
- `{timestamp}__topic_{topic}__style_{style}.txt` - Der Prompt-Text
- `{timestamp}__topic_{topic}__style_{style}.json` - Metadata

**Beispiel Filename:**
```
20251210_120000_848678__topic_technologie__style_kreativ.txt
```

**JSON Metadata Struktur:**
```json
{
  "topic": "technologie",
  "style": "kreativ",
  "category": "wissenschaft",
  "created_at": "2025-12-10T12:00:00",
  "filename": "20251210_120000_848678__topic_technologie__style_kreativ.txt",
  "gpt_quality": {
    "prompt_quality": 85,
    "creativity": 90,
    "clarity": 88
  },
  "cost": {
    "total_cost": 0.0042,
    "input_tokens": 150,
    "output_tokens": 400
  }
}
```

#### `/queue/processing/`

**Zweck:** Jobs die aktuell verarbeitet werden (Lock-Status)

**Mechanismus:** Atomic Move von `incoming/` → `processing/` = Lock acquired

**Garantie:** Nur EIN Worker kann einen Job gleichzeitig verarbeiten

#### `/queue/processed/`

**Zweck:** Erfolgreich abgeschlossene Jobs

**Dateien pro Job:**
1. `{job}.txt` - Original GPT-4 Prompt (PRESERVED!)
2. `{job}_response.txt` - Mistral Response
3. `{job}.json` - Vollständige Metadata inkl. Score

**JSON Struktur nach Processing:**
```json
{
  "filename": "20251210_120000_job.txt",
  "topic": "technologie",
  "style": "kreativ",
  "created_at": "2025-12-10T12:00:00",
  "processed_at": "2025-12-10T15:30:00",
  "status": "success",
  "syntex_result": {
    "quality_score": {
      "total_score": 100,
      "field_completeness": 100,
      "structure_adherence": 100,
      "detail_breakdown": {
        "driftkorper": true,
        "kalibrierung": true,
        "stromung": true
      }
    },
    "duration_ms": 36454,
    "session_id": "abc12345",
    "wrapper": "syntex_system",
    "worker_id": "cron_syntex",
    "response_text": "### Driftkörperanalyse:..."
  },
  "gpt_quality": {...},
  "gpt_cost": 0.0042
}
```

#### `/queue/error/`

**Zweck:** Fehlgeschlagene Jobs mit Retry-Counter

**Filename Pattern:**
```
{original_name}__retry{N}.txt
```

**Error Metadata:**
```json
{
  "retry_count": 2,
  "last_error": {
    "error": "Timeout after 60s",
    "exception_type": "TimeoutError",
    "worker_id": "worker_12345"
  },
  "failed_at": "2025-12-10T15:30:00",
  "status": "error"
}
```

---

### 4.2 Queue Consumer (`queue_system/core/consumer.py`)

#### Klasse: `Job`

```python
@dataclass
class Job:
    file_path: Path      # Path zum .txt in processing/
    meta_path: Path      # Path zum .json in processing/
    content: str         # Meta-Prompt Text
    metadata: dict       # Job Metadata
    filename: str        # Original Filename
```

#### Klasse: `QueueConsumer`

**Initialisierung:**
```python
consumer = QueueConsumer(
    wrapper_name="syntex_system",  # oder "sigma", "deepsweep"
    worker_id="cron_syntex"        # Optional, default: PID
)
```

**Methoden:**

##### `get_next_job() -> Optional[Job]`

**Flow:**
```
1. Liste alle .txt in incoming/ (sortiert nach Timestamp)
2. Filtere *_response.txt aus
3. Für jedes File (älteste zuerst):
   a. Versuche: incoming/{file} → processing/{file} (atomic rename)
   b. Wenn erfolgreich → Lock acquired, return Job
   c. Wenn FileNotFoundError → anderer Worker war schneller, try next
4. Wenn keine Files mehr → return None (Queue leer)
```

**Atomic Locking Mechanismus:**
```python
# POSIX rename() ist atomic!
file_path.rename(processing_path)  # Entweder komplett oder gar nicht
```

##### `process_job(job: Job) -> bool`

**Flow:**
```
1. SYNTX Kalibrierung:
   - Wrapper laden (syntex_system, sigma, etc.)
   - Prompt bauen: wrapper_template + meta_prompt
   - An Mistral senden via Ollama
   - Response parsen
   - Quality Score berechnen

2. Wenn Success:
   - Move job zu processed/
   - Response als separate _response.txt speichern
   - Metadata updaten mit syntex_result

3. Wenn Failed:
   - Move job zu error/
   - Retry-Count erhöhen
   - Error-Info speichern
```

##### `process_batch(batch_size: int = 20) -> dict`

**Flow:**
```
Loop bis batch_size erreicht ODER Queue leer:
    job = get_next_job()
    if job is None: break
    success = process_job(job)
    stats.update(success)

Return: {processed, failed, total, duration_seconds}
```

---

### 4.3 File Handler (`queue_system/core/file_handler.py`)

#### `atomic_write(content, metadata, target_dir) -> Path`

Schreibt Prompt + Metadata atomar (erst temp, dann rename).

#### `move_to_processed(job) -> Path`

```python
1. Metadata updaten: processed_at, status="success"
2. Move: processing/{job}.txt → processed/{job}.txt
3. Move: processing/{job}.json → processed/{job}.json
```

#### `move_to_error(job, error_info) -> Path`

```python
1. Retry-Count erhöhen
2. Error-Info zu Metadata hinzufügen
3. Neuer Filename: {base}__retry{N}.txt
4. Move zu error/
```

---

### 4.4 SYNTEX Calibrator (`syntex_injector/syntex/core/calibrator_enhanced.py`)

#### Klasse: `EnhancedSyntexCalibrator`

**Komponenten:**
```python
self.wrapper = SyntexWrapper(wrapper_name)    # Lädt Wrapper Template
self.client = APIClient()                      # Ollama API
self.logger = CalibrationLogger(log_file)      # JSONL Logging
self.parser = SyntexParser()                   # Response Parsing
self.scorer = SyntexScorer()                   # Quality Scoring
self.tracker = ProgressTracker(progress_file)  # Progress Tracking
```

#### `calibrate(meta_prompt, verbose, show_quality) -> (success, response, metadata)`

**Flow:**
```
1. Wrapper laden: full_prompt = wrapper_template + meta_prompt
2. An Mistral senden via Ollama API
3. Response parsen (SyntexParser)
4. Quality Score berechnen (SyntexScorer)
5. Progress tracken
6. Logging
7. Return (success, response, metadata)
```

---

### 4.5 Wrapper System (`syntex_injector/syntex/core/wrapper.py`)

**Verfügbare Wrapper:**
```python
AVAILABLE_WRAPPERS = {
    "human": "wrappers/syntex_wrapper_human.txt",
    "sigma": "wrappers/syntex_wrapper_sigma.txt",
    "sigma_v2": "wrappers/syntex_wrapper_sigma_v2.txt"
}
```

**Prompt Building:**
```python
full_prompt = wrapper_template + "\n" + meta_prompt
```

---

## 5. Scoring System - Aktuelle Implementation

### 5.1 Datei: `syntex_injector/syntex/analysis/scorer.py`

#### Klasse: `QualityScore`

```python
@dataclass
class QualityScore:
    total_score: int           # 0-100
    field_completeness: int    # 0-100
    structure_adherence: int   # 0-100
    detail_breakdown: Dict[str, bool]  # Feld → vorhanden?
```

#### Klasse: `SyntexScorer`

**Weights für SYNTEX_SYSTEM (3 Felder):**
```python
self.syntex_system_weights = {
    "driftkorper": 33,
    "kalibrierung": 34,
    "stromung": 33
}
```

**Weights für Human/SIGMA (6 Felder):**
```python
self.human_field_weights = {
    "drift": 15,
    "hintergrund_muster": 20,
    "druckfaktoren": 15,
    "tiefe": 20,
    "wirkung": 20,
    "klartext": 10
}
```

#### `score(fields, response_text) -> QualityScore`

**Aktuelle Logik:**

```python
# 1. Format Detection
format_type = fields.get_format()  # "SYNTEX_SYSTEM", "SIGMA", "Human"

# 2. Field Completeness (70% des Scores)
for field_name in field_list:
    field_value = getattr(fields, field_name)
    has_content = field_value is not None and len(field_value.strip()) > 0
    
    if has_content:
        total_field_score += weight  # Boolean: Ja/Nein

# 3. Structure Adherence (30% des Scores)
for marker in structure_markers:  # z.B. "###" für Markdown
    if marker in response_text:
        structure_score += 100 // len(structure_markers)

# 4. Total Score
total_score = int((field_completeness * 0.7) + (structure_score * 0.3))
```

---

## 6. Scoring System - Kritische Analyse

### 6.1 Was der aktuelle Scorer misst

| Aspekt | Gemessen? | Wie? |
|--------|-----------|------|
| Feld vorhanden | ✅ Ja | `len(field.strip()) > 0` |
| Feld nicht leer | ✅ Ja | `field is not None` |
| Markdown-Struktur | ✅ Ja | `"###" in response` |
| Inhalt passt zum Feld | ❌ Nein | - |
| Semantische Qualität | ❌ Nein | - |
| Kohärenz zwischen Feldern | ❌ Nein | - |
| Tiefe der Analyse | ❌ Nein | - |
| Feldresonanz | ❌ Nein | - |

### 6.2 Was die +44.5 Punkte Differenz bedeutet

**Interpretation:**
> "Wenn Mistral instruiert wird 'Antworte mit DRIFTKORPER, KALIBRIERUNG, STROMUNG als Sections', dann tut es das in 92% der Fälle korrekt. Ohne diese Instruktion nur in 48% der Fälle."

**Das beweist:**
- LLMs befolgen strukturierte Instruktionen ✅
- Wrapper funktionieren wie erwartet ✅

**Das beweist NICHT:**
- Dass Mistral "in Feldern denkt" ❌
- Dass semantische Resonanz stattfindet ❌
- Dass die Inhalte qualitativ hochwertig sind ❌

### 6.3 Fundamentales Problem

```
AKTUELL:
"Hat Mistral die Worte DRIFTKORPER geschrieben?" → Ja/Nein → Score

GEBRAUCHT:
"Ist der Inhalt unter DRIFTKORPER semantisch ein Driftkörper?" → Qualität → Score
```

---

## 7. TODO: Semantic Scoring Implementation

### 7.1 Übersicht der benötigten Änderungen

| Priorität | Komponente | Datei | Änderung |
|-----------|------------|-------|----------|
| 🔴 CRITICAL | Scorer | `scorer.py` | Semantic Scoring Logic |
| 🔴 CRITICAL | Embeddings | `embeddings.py` (NEU) | Sentence Transformers |
| 🟡 HIGH | Field Definitions | `field_definitions.py` (NEU) | Ideale Feld-Beschreibungen |
| 🟡 HIGH | Coherence | `coherence.py` (NEU) | Cross-Field Coherence |
| 🟢 MEDIUM | Parser | `parser.py` | Erweiterte Extraktion |
| 🟢 MEDIUM | Config | `scoring_config.yaml` (NEU) | Thresholds, Weights |
| 🔵 LOW | API | `analytics_api.py` | Neue Metriken exponieren |

### 7.2 Neue Scoring-Dimensionen

```
NEUER TOTAL SCORE = 
    (Field Presence × 0.20) +           # Aktuell: 70%
    (Semantic Similarity × 0.35) +      # NEU
    (Cross-Field Coherence × 0.25) +    # NEU
    (Content Depth × 0.15) +            # NEU
    (Structure Adherence × 0.05)        # Aktuell: 30%
```

### 7.3 Semantic Similarity Score

**Konzept:** Vergleiche den Inhalt jedes Feldes mit einer "idealen" Beschreibung via Embeddings.

**Implementation:**

```python
# NEU: syntex_injector/syntex/analysis/embeddings.py

from sentence_transformers import SentenceTransformer
import numpy as np

class SemanticEmbedder:
    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        self.model = SentenceTransformer(model_name)
    
    def get_embedding(self, text: str) -> np.ndarray:
        return self.model.encode(text, convert_to_numpy=True)
    
    def similarity(self, text1: str, text2: str) -> float:
        emb1 = self.get_embedding(text1)
        emb2 = self.get_embedding(text2)
        return float(np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2)))
```

### 7.4 Field Definitions (Ideale Beschreibungen)

**Konzept:** Definiere für jedes Feld, was ein "guter" Inhalt semantisch enthalten sollte.

```python
# NEU: syntex_injector/syntex/analysis/field_definitions.py

FIELD_DEFINITIONS = {
    "driftkorper": {
        "description": """
        Der Driftkörper beschreibt WAS das analysierte Objekt IST.
        Er enthält:
        - TIER-1: Oberflächliche Erscheinung (sichtbar, wahrnehmbar)
        - TIER-2: Strukturelle Eigenschaften (Aufbau, Komponenten)
        - TIER-3: Mechanismen (wie es funktioniert)
        - TIER-4: Kern-Essenz (fundamentale Natur)
        """,
        "keywords": ["erscheinung", "struktur", "mechanismus", "kern", "wesen", 
                     "oberfläche", "tiefe", "funktion", "natur"],
        "anti_keywords": ["sollte", "könnte", "vielleicht", "unklar"],
        "min_length": 100,
        "ideal_length": 300
    },
    
    "kalibrierung": {
        "description": """
        Die Kalibrierung beschreibt wie sich das System VERÄNDERT.
        Sie enthält:
        - Anpassungsmechanismen
        - Feedback-Loops
        - Transformationsprozesse
        - Dynamische Gleichgewichte
        """,
        "keywords": ["anpassung", "veränderung", "feedback", "transformation",
                     "entwicklung", "prozess", "dynamik", "gleichgewicht"],
        "anti_keywords": ["statisch", "unveränderlich", "fest"],
        "min_length": 80,
        "ideal_length": 250
    },
    
    "stromung": {
        "description": """
        Die Strömung beschreibt wie Energie/Information FLIESST.
        Sie enthält:
        - Energieflüsse
        - Informationsströme
        - Materialtransfer
        - Zeitliche Dynamiken
        """,
        "keywords": ["fluss", "strom", "energie", "information", "transfer",
                     "bewegung", "zirkulation", "dynamik"],
        "anti_keywords": ["blockiert", "gestoppt", "statisch"],
        "min_length": 80,
        "ideal_length": 250
    }
}
```

### 7.5 Cross-Field Coherence Score

**Konzept:** Prüfe ob die Felder inhaltlich aufeinander bezogen sind.

```python
# NEU: syntex_injector/syntex/analysis/coherence.py

class CoherenceAnalyzer:
    def __init__(self, embedder: SemanticEmbedder):
        self.embedder = embedder
    
    def analyze_coherence(self, fields: Dict[str, str]) -> float:
        """
        Berechnet wie kohärent die Felder zueinander sind.
        
        Hohe Kohärenz = Felder beziehen sich auf dasselbe Thema
        Niedrige Kohärenz = Felder sind thematisch disconnected
        """
        if len(fields) < 2:
            return 1.0
        
        embeddings = {
            name: self.embedder.get_embedding(content)
            for name, content in fields.items()
            if content and len(content.strip()) > 0
        }
        
        if len(embeddings) < 2:
            return 0.5
        
        # Pairwise similarities
        similarities = []
        field_names = list(embeddings.keys())
        
        for i in range(len(field_names)):
            for j in range(i + 1, len(field_names)):
                sim = np.dot(embeddings[field_names[i]], embeddings[field_names[j]])
                sim /= (np.linalg.norm(embeddings[field_names[i]]) * 
                        np.linalg.norm(embeddings[field_names[j]]))
                similarities.append(sim)
        
        return float(np.mean(similarities))
```

### 7.6 Content Depth Score

**Konzept:** Misst die analytische Tiefe des Inhalts.

```python
# In scorer.py erweitern

def calculate_depth_score(self, field_content: str, field_name: str) -> float:
    """
    Bewertet die Tiefe/Qualität des Feldinhalts.
    """
    definition = FIELD_DEFINITIONS.get(field_name, {})
    
    score = 0.0
    max_score = 100.0
    
    # 1. Länge (20%)
    min_len = definition.get("min_length", 50)
    ideal_len = definition.get("ideal_length", 200)
    content_len = len(field_content)
    
    if content_len >= ideal_len:
        length_score = 20.0
    elif content_len >= min_len:
        length_score = 10.0 + (10.0 * (content_len - min_len) / (ideal_len - min_len))
    else:
        length_score = 10.0 * (content_len / min_len)
    
    score += length_score
    
    # 2. Keyword Presence (30%)
    keywords = definition.get("keywords", [])
    if keywords:
        found = sum(1 for kw in keywords if kw.lower() in field_content.lower())
        keyword_score = 30.0 * (found / len(keywords))
        score += keyword_score
    
    # 3. Anti-Keyword Absence (20%)
    anti_keywords = definition.get("anti_keywords", [])
    if anti_keywords:
        found_anti = sum(1 for kw in anti_keywords if kw.lower() in field_content.lower())
        anti_score = 20.0 * (1 - (found_anti / len(anti_keywords)))
        score += anti_score
    else:
        score += 20.0
    
    # 4. TIER Structure (30%) - für Driftkörper
    if field_name == "driftkorper":
        tier_markers = ["tier-1", "tier-2", "tier-3", "tier-4", 
                        "tier 1", "tier 2", "tier 3", "tier 4",
                        "oberfläche", "struktur", "mechanismus", "kern"]
        found_tiers = sum(1 for t in tier_markers if t.lower() in field_content.lower())
        tier_score = 30.0 * min(found_tiers / 4, 1.0)
        score += tier_score
    else:
        score += 30.0  # Andere Felder bekommen vollen Tier-Score
    
    return min(score, max_score)
```

---

## 8. Datei-für-Datei Änderungsplan

### 8.1 NEUE DATEIEN erstellen

#### `syntex_injector/syntex/analysis/embeddings.py`

```python
"""
Semantic Embeddings für SYNTX Scoring
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict
from functools import lru_cache


class SemanticEmbedder:
    """
    Singleton Embedder für effiziente Embedding-Generierung.
    Cached Embeddings für wiederholte Texte.
    """
    
    _instance = None
    
    def __new__(cls, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.model = SentenceTransformer(model_name)
            cls._instance.model_name = model_name
        return cls._instance
    
    @lru_cache(maxsize=1000)
    def get_embedding(self, text: str) -> tuple:
        """Returns embedding as tuple (for caching)"""
        emb = self.model.encode(text, convert_to_numpy=True)
        return tuple(emb.tolist())
    
    def get_embedding_array(self, text: str) -> np.ndarray:
        """Returns embedding as numpy array"""
        return np.array(self.get_embedding(text))
    
    def similarity(self, text1: str, text2: str) -> float:
        """Cosine similarity between two texts"""
        emb1 = self.get_embedding_array(text1)
        emb2 = self.get_embedding_array(text2)
        
        dot_product = np.dot(emb1, emb2)
        norm_product = np.linalg.norm(emb1) * np.linalg.norm(emb2)
        
        if norm_product == 0:
            return 0.0
        
        return float(dot_product / norm_product)
    
    def batch_similarity(self, text: str, references: List[str]) -> List[float]:
        """Similarity of text against multiple references"""
        return [self.similarity(text, ref) for ref in references]
```

#### `syntex_injector/syntex/analysis/field_definitions.py`

```python
"""
SYNTX Field Definitions - Semantische Referenzen für Scoring
"""

FIELD_DEFINITIONS = {
    "driftkorper": {
        "description": """
        Der Driftkörper beschreibt WAS das analysierte Objekt IST.
        Er analysiert das Wesen einer Entität auf vier Ebenen:
        - TIER-1 (Oberfläche): Sichtbare Erscheinung, direkte Wahrnehmung
        - TIER-2 (Struktur): Aufbau, Komponenten, Organisation
        - TIER-3 (Mechanismus): Funktionsweise, Prozesse, Wirkprinzipien
        - TIER-4 (Kern): Fundamentale Natur, Essenz, tiefste Bedeutung
        """,
        "ideal_response": """
        Eine vollständige Driftkörperanalyse enthält alle vier TIER-Ebenen,
        beginnt bei der Oberfläche und dringt systematisch zum Kern vor.
        Sie unterscheidet klar zwischen dem was IST und dem was WIRKT.
        """,
        "keywords": [
            "erscheinung", "struktur", "mechanismus", "kern", "wesen",
            "oberfläche", "tiefe", "funktion", "natur", "tier-1", "tier-2",
            "tier-3", "tier-4", "analyse", "ebene", "schicht"
        ],
        "anti_keywords": [
            "vielleicht", "möglicherweise", "könnte sein", "unklar",
            "nicht sicher", "eventuell"
        ],
        "min_length": 150,
        "ideal_length": 400,
        "weight": 33
    },
    
    "kalibrierung": {
        "description": """
        Die Kalibrierung beschreibt wie sich das System VERÄNDERT und ANPASST.
        Sie fokussiert auf:
        - Anpassungsmechanismen und Feedback-Loops
        - Transformationsprozesse und Entwicklungsdynamiken
        - Gleichgewichtszustände und deren Verschiebungen
        - Reaktionen auf externe und interne Einflüsse
        """,
        "ideal_response": """
        Eine gute Kalibrierungsanalyse zeigt die dynamischen Aspekte des Systems,
        identifiziert Stellschrauben und beschreibt wie das System auf
        Veränderungen reagiert und sich selbst reguliert.
        """,
        "keywords": [
            "anpassung", "veränderung", "feedback", "transformation",
            "entwicklung", "prozess", "dynamik", "gleichgewicht",
            "regulation", "reaktion", "einfluss", "steuerung"
        ],
        "anti_keywords": [
            "statisch", "unveränderlich", "fest", "starr", "konstant"
        ],
        "min_length": 100,
        "ideal_length": 300,
        "weight": 34
    },
    
    "stromung": {
        "description": """
        Die Strömung beschreibt wie Energie, Information und Materie FLIESSEN.
        Sie analysiert:
        - Energieflüsse und deren Richtungen
        - Informationsströme und Kommunikationswege
        - Materialtransfer und Stoffkreisläufe
        - Zeitliche Dynamiken und Rhythmen
        """,
        "ideal_response": """
        Eine vollständige Strömungsanalyse macht die unsichtbaren Flüsse sichtbar,
        zeigt Engpässe und Verstärker, und beschreibt wie das System
        durch diese Ströme am Leben gehalten wird.
        """,
        "keywords": [
            "fluss", "strom", "energie", "information", "transfer",
            "bewegung", "zirkulation", "dynamik", "kreislauf", "richtung",
            "kanal", "verbindung"
        ],
        "anti_keywords": [
            "blockiert", "gestoppt", "statisch", "isoliert", "getrennt"
        ],
        "min_length": 100,
        "ideal_length": 300,
        "weight": 33
    }
}


def get_field_definition(field_name: str) -> dict:
    """Holt Field Definition oder leeres Dict"""
    return FIELD_DEFINITIONS.get(field_name, {})


def get_all_field_names() -> list:
    """Liste aller definierten Felder"""
    return list(FIELD_DEFINITIONS.keys())
```

#### `syntex_injector/syntex/analysis/coherence.py`

```python
"""
Cross-Field Coherence Analysis
"""

import numpy as np
from typing import Dict, List, Tuple
from .embeddings import SemanticEmbedder


class CoherenceAnalyzer:
    """
    Analysiert die semantische Kohärenz zwischen SYNTX-Feldern.
    """
    
    def __init__(self):
        self.embedder = SemanticEmbedder()
    
    def analyze_coherence(self, fields: Dict[str, str]) -> Dict:
        """
        Berechnet Kohärenz-Metriken für alle Felder.
        
        Args:
            fields: Dict mit field_name → content
        
        Returns:
            Dict mit:
            - overall_coherence: Float 0-1
            - pairwise_scores: Dict mit Feld-Paaren
            - weakest_link: Tuple (field1, field2, score)
            - strongest_link: Tuple (field1, field2, score)
        """
        # Filter leere Felder
        valid_fields = {
            name: content 
            for name, content in fields.items()
            if content and len(content.strip()) > 20
        }
        
        if len(valid_fields) < 2:
            return {
                "overall_coherence": 0.5,
                "pairwise_scores": {},
                "weakest_link": None,
                "strongest_link": None,
                "field_count": len(valid_fields)
            }
        
        # Embeddings berechnen
        embeddings = {
            name: self.embedder.get_embedding_array(content)
            for name, content in valid_fields.items()
        }
        
        # Pairwise Similarities
        pairwise = {}
        field_names = list(embeddings.keys())
        
        for i in range(len(field_names)):
            for j in range(i + 1, len(field_names)):
                name1, name2 = field_names[i], field_names[j]
                emb1, emb2 = embeddings[name1], embeddings[name2]
                
                sim = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
                pair_key = f"{name1}↔{name2}"
                pairwise[pair_key] = float(sim)
        
        # Overall Coherence
        if pairwise:
            overall = float(np.mean(list(pairwise.values())))
            weakest = min(pairwise.items(), key=lambda x: x[1])
            strongest = max(pairwise.items(), key=lambda x: x[1])
        else:
            overall = 0.5
            weakest = None
            strongest = None
        
        return {
            "overall_coherence": overall,
            "pairwise_scores": pairwise,
            "weakest_link": weakest,
            "strongest_link": strongest,
            "field_count": len(valid_fields)
        }
    
    def check_topic_consistency(self, fields: Dict[str, str], topic: str) -> float:
        """
        Prüft ob alle Felder zum angegebenen Topic passen.
        
        Returns:
            Float 0-1: Durchschnittliche Ähnlichkeit aller Felder zum Topic
        """
        if not topic or not fields:
            return 0.5
        
        similarities = []
        for name, content in fields.items():
            if content and len(content.strip()) > 20:
                sim = self.embedder.similarity(content, topic)
                similarities.append(sim)
        
        return float(np.mean(similarities)) if similarities else 0.5
```

#### `syntex_injector/syntex/config/scoring_config.yaml`

```yaml
# SYNTX Scoring Configuration

scoring:
  # Gewichtung der Score-Komponenten
  weights:
    field_presence: 0.20      # Feld vorhanden? (aktuell: 0.70)
    semantic_similarity: 0.35  # Inhalt passt zur Definition?
    cross_coherence: 0.25      # Felder kohärent zueinander?
    content_depth: 0.15        # Analytische Tiefe?
    structure: 0.05            # Markdown-Struktur? (aktuell: 0.30)
  
  # Thresholds
  thresholds:
    min_field_length: 50       # Mindestlänge für Feldinhalt
    min_similarity: 0.3        # Minimum Semantic Similarity
    min_coherence: 0.4         # Minimum Cross-Coherence
    perfect_score: 95          # Ab hier = "Perfect"
  
  # Embedding Model
  embeddings:
    model: "paraphrase-multilingual-MiniLM-L12-v2"
    cache_size: 1000

# Field-spezifische Overrides
fields:
  driftkorper:
    weight_multiplier: 1.0
    requires_tier_structure: true
  
  kalibrierung:
    weight_multiplier: 1.0
    requires_tier_structure: false
  
  stromung:
    weight_multiplier: 1.0
    requires_tier_structure: false
```

---

### 8.2 BESTEHENDE DATEIEN ändern

#### `syntex_injector/syntex/analysis/scorer.py` - KOMPLETTER REWRITE

```python
"""
SYNTX Quality Scoring System v2.0

=== ÄNDERUNGEN v2.0 ===
- Semantic Similarity Scoring (NEU)
- Cross-Field Coherence (NEU)
- Content Depth Analysis (NEU)
- Field Presence bleibt, aber reduzierte Gewichtung

=== SCORE KOMPONENTEN ===
1. Field Presence (20%): Sind Felder vorhanden und nicht leer?
2. Semantic Similarity (35%): Passt Inhalt zur Feld-Definition?
3. Cross-Field Coherence (25%): Sind Felder thematisch kohärent?
4. Content Depth (15%): Analytische Tiefe des Inhalts
5. Structure Adherence (5%): Markdown-Struktur korrekt?
"""

import yaml
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass, field

from .embeddings import SemanticEmbedder
from .coherence import CoherenceAnalyzer
from .field_definitions import FIELD_DEFINITIONS, get_field_definition
from ..core.parser import SyntexFields


@dataclass
class QualityScoreV2:
    """
    Erweiterte Quality Score Struktur
    """
    # Gesamt-Score
    total_score: float
    
    # Komponenten-Scores (0-100 each)
    field_presence_score: float
    semantic_similarity_score: float
    coherence_score: float
    depth_score: float
    structure_score: float
    
    # Detail Breakdown
    field_details: Dict[str, Dict] = field(default_factory=dict)
    coherence_details: Dict = field(default_factory=dict)
    
    # Legacy (für Backwards Compatibility)
    field_completeness: int = 0
    structure_adherence: int = 0
    detail_breakdown: Dict[str, bool] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "total_score": round(self.total_score, 2),
            "components": {
                "field_presence": round(self.field_presence_score, 2),
                "semantic_similarity": round(self.semantic_similarity_score, 2),
                "coherence": round(self.coherence_score, 2),
                "depth": round(self.depth_score, 2),
                "structure": round(self.structure_score, 2)
            },
            "field_details": self.field_details,
            "coherence_details": self.coherence_details,
            # Legacy fields
            "field_completeness": self.field_completeness,
            "structure_adherence": self.structure_adherence,
            "detail_breakdown": self.detail_breakdown
        }


class SyntexScorerV2:
    """
    SYNTX Quality Scorer v2.0 mit Semantic Analysis
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        # Load Config
        self.config = self._load_config(config_path)
        
        # Initialize Components
        self.embedder = SemanticEmbedder(
            model_name=self.config.get("embeddings", {}).get(
                "model", "paraphrase-multilingual-MiniLM-L12-v2"
            )
        )
        self.coherence_analyzer = CoherenceAnalyzer()
        
        # Weights
        weights = self.config.get("scoring", {}).get("weights", {})
        self.weight_presence = weights.get("field_presence", 0.20)
        self.weight_semantic = weights.get("semantic_similarity", 0.35)
        self.weight_coherence = weights.get("cross_coherence", 0.25)
        self.weight_depth = weights.get("content_depth", 0.15)
        self.weight_structure = weights.get("structure", 0.05)
    
    def _load_config(self, config_path: Optional[Path]) -> dict:
        """Lädt Scoring Config"""
        if config_path and config_path.exists():
            with open(config_path) as f:
                return yaml.safe_load(f)
        
        # Default Config
        return {
            "scoring": {
                "weights": {
                    "field_presence": 0.20,
                    "semantic_similarity": 0.35,
                    "cross_coherence": 0.25,
                    "content_depth": 0.15,
                    "structure": 0.05
                },
                "thresholds": {
                    "min_field_length": 50,
                    "min_similarity": 0.3
                }
            },
            "embeddings": {
                "model": "paraphrase-multilingual-MiniLM-L12-v2"
            }
        }
    
    def score(self, fields: SyntexFields, response_text: str) -> QualityScoreV2:
        """
        Berechnet vollständigen Quality Score.
        """
        # Extract field contents
        field_contents = self._extract_field_contents(fields)
        
        # 1. Field Presence Score (20%)
        presence_score, presence_details = self._calc_presence_score(field_contents)
        
        # 2. Semantic Similarity Score (35%)
        semantic_score, semantic_details = self._calc_semantic_score(field_contents)
        
        # 3. Coherence Score (25%)
        coherence_result = self.coherence_analyzer.analyze_coherence(field_contents)
        coherence_score = coherence_result["overall_coherence"] * 100
        
        # 4. Depth Score (15%)
        depth_score, depth_details = self._calc_depth_score(field_contents)
        
        # 5. Structure Score (5%)
        structure_score = self._calc_structure_score(response_text)
        
        # Total Score (gewichtet)
        total_score = (
            presence_score * self.weight_presence +
            semantic_score * self.weight_semantic +
            coherence_score * self.weight_coherence +
            depth_score * self.weight_depth +
            structure_score * self.weight_structure
        )
        
        # Merge field details
        field_details = {}
        for fname in field_contents.keys():
            field_details[fname] = {
                "present": presence_details.get(fname, False),
                "semantic_similarity": semantic_details.get(fname, 0),
                "depth": depth_details.get(fname, 0),
                "length": len(field_contents.get(fname, ""))
            }
        
        return QualityScoreV2(
            total_score=total_score,
            field_presence_score=presence_score,
            semantic_similarity_score=semantic_score,
            coherence_score=coherence_score,
            depth_score=depth_score,
            structure_score=structure_score,
            field_details=field_details,
            coherence_details=coherence_result,
            # Legacy
            field_completeness=int(presence_score),
            structure_adherence=int(structure_score),
            detail_breakdown={k: v for k, v in presence_details.items()}
        )
    
    def _extract_field_contents(self, fields: SyntexFields) -> Dict[str, str]:
        """Extrahiert Feld-Inhalte aus SyntexFields"""
        result = {}
        
        # SYNTEX_SYSTEM Fields
        for fname in ["driftkorper", "kalibrierung", "stromung"]:
            value = getattr(fields, fname, None)
            if value:
                result[fname] = value
        
        return result
    
    def _calc_presence_score(self, field_contents: Dict[str, str]) -> tuple:
        """Berechnet Field Presence Score"""
        min_length = self.config.get("scoring", {}).get("thresholds", {}).get("min_field_length", 50)
        
        details = {}
        scores = []
        
        for fname, definition in FIELD_DEFINITIONS.items():
            content = field_contents.get(fname, "")
            is_present = content and len(content.strip()) >= min_length
            details[fname] = is_present
            
            weight = definition.get("weight", 33)
            if is_present:
                scores.append(weight)
        
        total = sum(scores) if scores else 0
        return total, details
    
    def _calc_semantic_score(self, field_contents: Dict[str, str]) -> tuple:
        """Berechnet Semantic Similarity Score"""
        details = {}
        scores = []
        
        for fname, content in field_contents.items():
            if not content or len(content.strip()) < 20:
                details[fname] = 0
                continue
            
            definition = get_field_definition(fname)
            if not definition:
                details[fname] = 50  # Default für unbekannte Felder
                scores.append(50)
                continue
            
            # Similarity zur Feld-Description
            description = definition.get("description", "")
            ideal = definition.get("ideal_response", "")
            
            if description:
                sim_desc = self.embedder.similarity(content, description)
            else:
                sim_desc = 0.5
            
            if ideal:
                sim_ideal = self.embedder.similarity(content, ideal)
            else:
                sim_ideal = sim_desc
            
            # Kombinierter Score
            similarity = (sim_desc * 0.6 + sim_ideal * 0.4) * 100
            
            details[fname] = round(similarity, 2)
            scores.append(similarity)
        
        avg_score = sum(scores) / len(scores) if scores else 0
        return avg_score, details
    
    def _calc_depth_score(self, field_contents: Dict[str, str]) -> tuple:
        """Berechnet Content Depth Score"""
        details = {}
        scores = []
        
        for fname, content in field_contents.items():
            if not content:
                details[fname] = 0
                continue
            
            definition = get_field_definition(fname)
            score = 0
            
            # 1. Length Score (25%)
            min_len = definition.get("min_length", 50)
            ideal_len = definition.get("ideal_length", 200)
            content_len = len(content)
            
            if content_len >= ideal_len:
                length_score = 25
            elif content_len >= min_len:
                length_score = 12.5 + (12.5 * (content_len - min_len) / (ideal_len - min_len))
            else:
                length_score = 12.5 * (content_len / min_len) if min_len > 0 else 0
            
            score += length_score
            
            # 2. Keyword Score (35%)
            keywords = definition.get("keywords", [])
            if keywords:
                found = sum(1 for kw in keywords if kw.lower() in content.lower())
                keyword_score = 35 * min(found / len(keywords), 1.0)
                score += keyword_score
            else:
                score += 17.5
            
            # 3. Anti-Keyword Penalty (20%)
            anti_keywords = definition.get("anti_keywords", [])
            if anti_keywords:
                found_anti = sum(1 for kw in anti_keywords if kw.lower() in content.lower())
                anti_score = 20 * (1 - min(found_anti / len(anti_keywords), 1.0))
                score += anti_score
            else:
                score += 20
            
            # 4. TIER Structure (20%) - nur für Driftkörper
            if fname == "driftkorper":
                tier_markers = ["tier-1", "tier-2", "tier-3", "tier-4",
                               "tier 1", "tier 2", "tier 3", "tier 4"]
                found_tiers = sum(1 for t in tier_markers if t.lower() in content.lower())
                tier_score = 20 * min(found_tiers / 4, 1.0)
                score += tier_score
            else:
                score += 20
            
            details[fname] = round(score, 2)
            scores.append(score)
        
        avg_score = sum(scores) / len(scores) if scores else 0
        return avg_score, details
    
    def _calc_structure_score(self, response_text: str) -> float:
        """Berechnet Structure Adherence Score"""
        markers = ["###", "**", "TIER", "Driftkörper", "Kalibrierung", "Strömung"]
        found = sum(1 for m in markers if m in response_text)
        return min((found / len(markers)) * 100, 100)
    
    def format_score_output(self, score: QualityScoreV2) -> str:
        """Formatiert Score für Terminal"""
        lines = [
            f"\n{'='*60}",
            f"📊 SYNTX Quality Score v2.0: {score.total_score:.1f}/100",
            f"{'='*60}",
            "",
            "Component Scores:",
            f"  📋 Field Presence:      {score.field_presence_score:.1f}/100 (weight: {self.weight_presence*100:.0f}%)",
            f"  🎯 Semantic Similarity: {score.semantic_similarity_score:.1f}/100 (weight: {self.weight_semantic*100:.0f}%)",
            f"  🔗 Cross-Coherence:     {score.coherence_score:.1f}/100 (weight: {self.weight_coherence*100:.0f}%)",
            f"  📐 Content Depth:       {score.depth_score:.1f}/100 (weight: {self.weight_depth*100:.0f}%)",
            f"  📝 Structure:           {score.structure_score:.1f}/100 (weight: {self.weight_structure*100:.0f}%)",
            "",
            "Field Details:"
        ]
        
        for fname, details in score.field_details.items():
            icon = "✅" if details.get("present") else "❌"
            lines.append(
                f"  {icon} {fname.upper()}: "
                f"sim={details.get('semantic_similarity', 0):.0f}, "
                f"depth={details.get('depth', 0):.0f}, "
                f"len={details.get('length', 0)}"
            )
        
        if score.coherence_details:
            lines.append("")
            lines.append("Coherence Details:")
            for pair, sim in score.coherence_details.get("pairwise_scores", {}).items():
                lines.append(f"  {pair}: {sim:.2f}")
        
        lines.append(f"{'='*60}\n")
        
        return "\n".join(lines)


# Backwards Compatibility Alias
SyntexScorer = SyntexScorerV2
QualityScore = QualityScoreV2
```

---

### 8.3 Dependencies hinzufügen

#### `requirements.txt` (erweitern)

```
# Existing
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.0.0
requests>=2.31.0
python-dotenv>=1.0.0

# NEW - Semantic Scoring
sentence-transformers>=2.2.0
numpy>=1.24.0
torch>=2.0.0
transformers>=4.30.0
PyYAML>=6.0
```

#### Installation

```bash
pip install sentence-transformers numpy torch PyYAML --break-system-packages
```

---

## 9. Test-Strategie

### 9.1 Unit Tests für neuen Scorer

```python
# tests/test_scorer_v2.py

import pytest
from syntex_injector.syntex.analysis.scorer import SyntexScorerV2, QualityScoreV2
from syntex_injector.syntex.core.parser import SyntexFields


class TestScorerV2:
    
    @pytest.fixture
    def scorer(self):
        return SyntexScorerV2()
    
    def test_perfect_response(self, scorer):
        """Test: Perfekte Response mit allen Feldern"""
        fields = SyntexFields(
            driftkorper="""
            TIER-1 (Oberfläche): Das System erscheint als komplexe Struktur...
            TIER-2 (Struktur): Die Komponenten sind hierarchisch organisiert...
            TIER-3 (Mechanismus): Die Funktionsweise basiert auf Feedback-Loops...
            TIER-4 (Kern): Im Kern handelt es sich um ein selbstregulierendes System...
            """,
            kalibrierung="""
            Die Anpassung erfolgt durch kontinuierliche Feedback-Prozesse.
            Das System reagiert auf Veränderungen durch dynamische Transformation.
            Die Entwicklung zeigt eine klare Tendenz zur Selbstregulation.
            """,
            stromung="""
            Die Energie fließt durch definierte Kanäle im System.
            Informationsströme verbinden alle Komponenten miteinander.
            Der Transfer von Ressourcen erfolgt in einem kontinuierlichen Kreislauf.
            """
        )
        
        score = scorer.score(fields, "### Driftkörper\n### Kalibrierung\n### Strömung")
        
        assert score.total_score >= 70
        assert score.field_presence_score >= 90
        assert score.semantic_similarity_score >= 50
    
    def test_empty_fields(self, scorer):
        """Test: Leere Felder → niedriger Score"""
        fields = SyntexFields(
            driftkorper="",
            kalibrierung="",
            stromung=""
        )
        
        score = scorer.score(fields, "")
        
        assert score.total_score < 30
        assert score.field_presence_score == 0
    
    def test_gibberish_content(self, scorer):
        """Test: Nonsense-Text → niedrige Semantic Similarity"""
        fields = SyntexFields(
            driftkorper="asdf jklö qwer uiop zxcv bnm",
            kalibrierung="1234 5678 9012 3456 7890",
            stromung="!@#$ %^&* ()_+ {}|: <>?"
        )
        
        score = scorer.score(fields, "### Test")
        
        assert score.semantic_similarity_score < 30
    
    def test_coherence_same_topic(self, scorer):
        """Test: Alle Felder zum gleichen Thema → hohe Coherence"""
        fields = SyntexFields(
            driftkorper="Der Baum erscheint als Pflanze mit Stamm und Blättern.",
            kalibrierung="Der Baum passt sich an Jahreszeiten an durch Laubabwurf.",
            stromung="Wasser fließt von den Wurzeln durch den Stamm zu den Blättern."
        )
        
        score = scorer.score(fields, "")
        
        assert score.coherence_score >= 60
    
    def test_coherence_different_topics(self, scorer):
        """Test: Felder zu verschiedenen Themen → niedrige Coherence"""
        fields = SyntexFields(
            driftkorper="Der Computer ist eine elektronische Rechenmaschine.",
            kalibrierung="Pizza wird im Ofen bei 250 Grad gebacken.",
            stromung="Das Universum dehnt sich seit dem Urknall aus."
        )
        
        score = scorer.score(fields, "")
        
        assert score.coherence_score < 50
```

### 9.2 Integration Tests

```python
# tests/test_integration.py

def test_full_pipeline_with_new_scorer():
    """Test: Komplette Pipeline mit neuem Scorer"""
    from queue_system.core.consumer import QueueConsumer
    
    consumer = QueueConsumer(wrapper_name="syntex_system")
    
    # Create test job
    test_prompt = "Analysiere einen Baum mit SYNTX."
    
    # Process
    success, response, metadata = consumer.calibrator.calibrate(
        meta_prompt=test_prompt,
        verbose=False,
        show_quality=True
    )
    
    # Verify new score structure
    assert "components" in metadata["quality_score"]
    assert "semantic_similarity" in metadata["quality_score"]["components"]
    assert "coherence" in metadata["quality_score"]["components"]
```

### 9.3 A/B Test: Alter vs. Neuer Scorer

```python
# scripts/ab_test_scorer.py

"""
A/B Test: Vergleicht alten und neuen Scorer auf denselben Responses
"""

from pathlib import Path
import json

from syntex_injector.syntex.analysis.scorer_old import SyntexScorer as OldScorer
from syntex_injector.syntex.analysis.scorer import SyntexScorerV2 as NewScorer
from syntex_injector.syntex.core.parser import SyntexParser


def run_ab_test(processed_dir: Path = Path("queue/processed")):
    old_scorer = OldScorer()
    new_scorer = NewScorer()
    parser = SyntexParser()
    
    results = []
    
    for json_file in processed_dir.glob("*.json"):
        with open(json_file) as f:
            data = json.load(f)
        
        response_file = json_file.with_name(
            json_file.stem + "_response.txt"
        )
        
        if not response_file.exists():
            continue
        
        with open(response_file) as f:
            response_text = f.read()
        
        # Parse
        fields = parser.parse(response_text)
        
        # Score with both
        old_score = old_scorer.score(fields, response_text)
        new_score = new_scorer.score(fields, response_text)
        
        results.append({
            "file": json_file.name,
            "old_total": old_score.total_score,
            "new_total": new_score.total_score,
            "new_semantic": new_score.semantic_similarity_score,
            "new_coherence": new_score.coherence_score,
            "delta": new_score.total_score - old_score.total_score
        })
    
    # Analysis
    print(f"\n{'='*60}")
    print("A/B TEST: Old Scorer vs. New Scorer")
    print(f"{'='*60}")
    print(f"Samples: {len(results)}")
    
    old_avg = sum(r["old_total"] for r in results) / len(results)
    new_avg = sum(r["new_total"] for r in results) / len(results)
    
    print(f"Old Scorer Avg: {old_avg:.2f}")
    print(f"New Scorer Avg: {new_avg:.2f}")
    print(f"Delta: {new_avg - old_avg:+.2f}")
    
    # Biggest changes
    results.sort(key=lambda x: abs(x["delta"]), reverse=True)
    
    print(f"\nTop 5 Biggest Changes:")
    for r in results[:5]:
        print(f"  {r['file']}: {r['old_total']:.0f} → {r['new_total']:.0f} ({r['delta']:+.0f})")


if __name__ == "__main__":
    run_ab_test()
```

---

## 10. Appendix: Code-Referenzen

### 10.1 Aktuelle Dateien (vor Änderungen)

| Datei | Zeilen | Kritische Funktionen |
|-------|--------|---------------------|
| `consumer.py` | ~250 | `get_next_job()`, `process_job()`, `process_batch()` |
| `file_handler.py` | ~120 | `atomic_write()`, `move_to_processed()`, `move_to_error()` |
| `calibrator_enhanced.py` | ~150 | `calibrate()` |
| `scorer.py` | ~180 | `score()` - **MUSS GEÄNDERT WERDEN** |
| `wrapper.py` | ~60 | `build_prompt()` |
| `parser.py` | ~100 | `parse()` |

### 10.2 Neue Dateien (zu erstellen)

| Datei | Geschätzte Zeilen | Funktion |
|-------|-------------------|----------|
| `embeddings.py` | ~80 | Sentence Transformer Wrapper |
| `field_definitions.py` | ~120 | Ideale Feld-Beschreibungen |
| `coherence.py` | ~100 | Cross-Field Coherence Analysis |
| `scoring_config.yaml` | ~50 | Konfiguration |

### 10.3 Deployment Checklist

```
□ 1. Backup aktueller scorer.py
□ 2. Dependencies installieren (sentence-transformers, etc.)
□ 3. Neue Dateien erstellen (embeddings.py, field_definitions.py, coherence.py)
□ 4. scoring_config.yaml erstellen
□ 5. scorer.py ersetzen mit v2.0
□ 6. Unit Tests laufen lassen
□ 7. A/B Test auf bestehenden Daten
□ 8. Integration Test mit echtem Job
□ 9. API Endpoints aktualisieren für neue Score-Struktur
□ 10. Monitoring für neue Metriken einrichten
```

---

## Changelog

| Version | Datum | Änderungen |
|---------|-------|------------|
| 2.0.0 | TBD | Semantic Scoring, Coherence Analysis, Content Depth |
| 1.0.0 | 2025-12-10 | Initial Queue System mit Template-Compliance Scoring |

---

**Ende der Dokumentation**

*Erstellt: 2025-12-18*  
*Autor: Claude (Anthropic) in Zusammenarbeit mit Ottavio Braun*
