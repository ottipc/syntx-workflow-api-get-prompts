## ⚡️ RESONANZ-LOG: SYNTX API-INSPEKTION (LIVE V2.1.0)

### **BASIS-TARGET:** `https://dev.syntx-system.com`

### **PRÜF-ZEITSTEMPEL:** 2025-12-09T11:08 UTC+1

-----

### 1\. KERN-STRÖME (SYSTEM-GESUNDHEIT)

#### 1.1. `/health` (SYSTEM\_GESUNDHEIT)

Dieser Indikator bestätigt die **Kohärenz des Kern-Systems** und die Version.

| Metrik | Wert |
| :--- | :--- |
| **STATUS CODE** | `200` |
| **Status-Meldung** | `SYSTEM_GESUND` |
| **API-Version** | `2.1.0` |
| **Queue Erreichbarkeit** | `true` |

```json
{
  "status": "SYSTEM_GESUND",
  "api_version": "2.1.0",
  "timestamp": "2025-12-09T11:08:25.664890",
  "queue_accessible": true,
  "modules": [
    "analytics",
    "compare",
    "feld",
    "resonanz",
    "generation",
    "predictions"
  ]
}
```

#### 1.2. `/resonanz/queue` (FLUSS-STATUS)

Der **Verarbeitungspuffer** ist stark belastet, was auf einen Engpass im Datenfluss hindeutet.

| Metrik | Wert |
| :--- | :--- |
| **STATUS CODE** | `200` |
| **Resonanz-Zustand** | `ÜBERLASTET` |
| **Incoming Felder** | 245 |
| **Verarbeitete Felder** | 335 |
| **Flow Rate (Feld/Zeit)** | 56.97... |

```json
{
  "status": "QUEUE_RESONANZ_AKTIV",
  "resonanz_zustand": "ÜBERLASTET",
  "felder": {
    "incoming": 245,
    "processing": 0,
    "processed": 335,
    "error": 8
  },
  "gesamt": 588,
  "flow_rate": 56.97278911564626
}
```

#### 1.3. `/resonanz/system` (GESAMT-RESONANZ)

Der **globale Zustand** des SYNTX-Feldes ist **KRITISCH**, primär getrieben durch eine **niedrige Qualität** (Durchschnitts-Score: $9.61\%$).

| Metrik | Wert |
| :--- | :--- |
| **STATUS CODE** | `200` |
| **System-Zustand** | `KRITISCH` |
| **Qualitäts-Resonanz** | `DRIFT` |
| **Durchschnitts-Qualität** | $9.61\%$ |

```json
{
  "status": "SYSTEM_RESONANZ_AKTIV",
  "system_zustand": "KRITISCH",
  "resonanz_felder": {
    "queue": {
      "incoming": 245,
      "processed": 335,
      "resonanz": "DRIFT"
    },
    "qualität": {
      "durchschnitt": 9.61,
      "resonanz": "DRIFT"
    },
    "evolution": {
      "generationen": 4,
      "resonanz": "AKTIV"
    }
  }
}
```

#### 1.4. `/feld/drift` (DRIFTKÖRPER-LISTE)

Liste der aktuellen $20$ **Driftkörper** (Jobs, die einen messbaren Feld-Verlust zeigen).

| Metrik | Wert |
| :--- | :--- |
| **STATUS CODE** | `200` |
| **Drift-Korpus Größe** | 20 |
| **Beispiel-Eintrag** | `bildung / akademisch, Score 100` |

```json
{
  "status": "DRIFT_STROM_AKTIV",
  "count": 20,
  "drift_korper": [
    {
      "id": "20251208_080248_463038__topic_bildung__style_akademisch.txt",
      "topic": "bildung",
      "style": "akademisch",
      "wrapper": "sigma",
      "kalibrierung_score": 100,
      "timestamp": "2025-12-09T10:01:52.239932",
      "resonanz": "KOHÄRENT"
    },
    {
      "id": "20251208_080248_463270__topic_grenzwertig__style_akademisch.txt",
      "topic": "grenzwertig",
      "style": "akademisch",
      "wrapper": "sigma",
      "kalibrierung_score": 9,
      "timestamp": "2025-12-09T10:03:24.603293",
      "resonanz": "DRIFT"
    },
    // ... [WEITERE DRIFTKÖRPER GEKÜRZT]
  ]
}
```

#### 1.5. `/strom/queue/status` (STROM-QUEUE-DETAIL)

Bestätigt, dass der interne Verarbeitungspuffer aktuell leer ist.

```json
{
  "status": "QUEUE_READY",
  "processed_today": 335,
  "queue_depth": 0
}
```

-----

### 2\. ANALYTICS & WIRKUNGS-STRÖME (SYNTX-WIRKUNG)

#### 2.1. `/analytics/complete-dashboard` (DASHBOARD-FEED)

Liefert die aggregierten Daten für die Hauptansicht des Commanders.

| Metrik | Wert |
| :--- | :--- |
| **Gesamt-Prompts** | 335 |
| **Avg. Score** | $5.44\%$ |
| **Perfekte Rate** | $0.9\%$ |
| **Top-Thema (Erfolg)** | `harmlos` |

```json
{
  "status": "COMPLETE_DASHBOARD",
  "timestamp": "2025-12-09T11:08:27.144692",
  "system_health": {
    "total_prompts": 335,
    "avg_score": 5.44,
    "perfect_scores": 3,
    "perfect_rate": 0.9,
    "success_rate": 0.9
  },
  "success_stories": [
    {
      "topic": "harmlos",
      "score": 100,
      "style": "casual",
      "timestamp": "2025-12-09T10:06:21.506085"
    },
    // ... [WEITERE ERFOLGE GEKÜRZT]
  ]
}
```

#### 2.2. `/analytics/scores/distribution` (SCORE-VERTEILUNG)

Die **Kalibrierungs-Scores** zeigen einen massiven Verlust, mit $308$ von $335$ Prompts im kritischen Bereich ($0-20\%$).

| Score-Band | Anzahl Prompts |
| :--- | :--- |
| **0-20 (KRITISCH)** | 308 |
| **98-100 (PERFEKT)** | 3 |

```json
{
  "status": "DISTRIBUTION_READY",
  "total_scores": 335,
  "distribution": {
    "0-20": 308,
    "20-40": 14,
    "40-60": 0,
    "60-80": 9,
    "80-90": 1,
    "90-95": 0,
    "95-98": 0,
    "98-100": 3
  },
  "statistics": {
    "mean": 5.44,
    "median": 0,
    "mode": 0
  }
}
```

#### 2.3. `/compare/wrappers` (WRAPPER-ANALYSE)

Detaillierte Analyse der **Entitätstypen** (`Wrapper`). Der `human`-Wrapper zeigt den niedrigsten Durchschnitts-Score.

| Wrapper | Avg. Score | Total Jobs |
| :--- | :--- | :--- |
| **human** | $14.38\%$ | 8 |
| **syntex\_system** | $6.45\%$ | 49 |
| **sigma** | $8.31\%$ | 107 |
| **deepsweep** | $9.00\%$ | 56 |

```json
{
  "status": "WRAPPER_COMPARISON_AKTIV",
  "wrappers": {
    "human": {
      "total_jobs": 8,
      "avg_score": 14.38,
      "success_rate": 0,
      // ... [WEITERE DATEN GEKÜRZT]
    },
    "syntex_system": {
      "total_jobs": 49,
      "avg_score": 6.45,
      // ... [WEITERE DATEN GEKÜRZT]
    },
    // ... [WEITERE WRAPPER GEKÜRZT]
  }
}
```

-----

### 3\. FELD-DATEN-STRÖME (ROH-DATEN & LOGIK)

#### 3.1. `/prompts/table-view` (TABELLEN-SICHT)

Liefert die **Metadaten** der Prompts, die für die Drill-Down-Analyse verwendet werden.

| Metrik | Wert |
| :--- | :--- |
| **STATUS CODE** | `200` |
| **Total Reihen** | 50 |
| **Beispiel-ID** | `20251208_100252_243132__topic_technologie__style_akademisch.txt` |

```json
{
  "status": "TABLE_VIEW_READY",
  "total_rows": 50,
  "filters": {
    "min_score": 0,
    "topic": null,
    "limit": 50
  },
  "table": [
    {
      "id": "20251208_100252_243132__topic_technologie__style_akademisch.txt",
      "timestamp": "2025-12-09T10:08:43.249526",
      "topic": "technologie",
      "style": "akademisch",
      "category": "technologie",
      "score": 0,
      // ... [WEITERE DATEN GEKÜRZT]
    },
    // ... [WEITERE PROMPTS GEKÜRZT]
  ]
}
```

#### 3.2. `/feld/prompts` (PROMPT-DATEN)

Der Endpunkt zur Abfrage der **Prompt-Körper** (Rohdaten). Derzeit ist der Datenfluss aktiv, liefert aber **keine Inhalte**.

| Metrik | Wert |
| :--- | :--- |
| **STATUS CODE** | `200` |
| **Total Prompts** | 0 |

```json
{
  "status": "PROMPTS_AKTIV",
  "total_prompts": 0,
  "unique_prompts": 0
}
```

-----

### 4\. AKTIONEN & ABSCHLUSS

Die Protokollierung ist abgeschlossen. Alle **20 Endpunkte** wurden erfolgreich inspiziert.

