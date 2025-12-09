# SYNTX-FELD-COMMANDER 🛰️
## KRITISCHES MASTER-PROTOKOLL DES API-DATENSTROM (V2.1.0)

**BASIS-URL DES ZIELSYSTEMS (TARGET):** `https://dev.syntx-system.com`

Dieses Protokoll dient als **ultimative Referenz** für den SYNTX-Feld-Commander und beinhaltet die **ungekürzte JSON-Antwort** jedes aktiven Endpunkts der v2.1.0 API, verifiziert durch die Feld-Inspektion vom 2025-12-09.

Alle Endpunkte meldeten `HTTP 200 OK`. Die Feld-Analyse zeigt jedoch einen **KRITISCHEN Drift-Zustand**.

---

## 1. ⚙️ KERN-STRÖME (System-Gesundheit & Resonanz)

### 1.1. ENDPUNKT: `/health` (SYSTEM_GESUNDHEIT)

**Beschreibung:** Bestätigt die Betriebsbereitschaft und die aktive Modul-Liste des API-Kernsystems.

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
````

### 1.2. ENDPUNKT: `/resonanz/system` (GESAMT-RESONANZ)

**Beschreibung:** Der globale Zustand des Feldes, bestätigt den **KRITISCHEN** Drift aufgrund niedriger Durchschnitts-Qualität.

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

### 1.3. ENDPUNKT: `/resonanz/queue` (FLUSS-STATUS)

**Beschreibung:** Detaillierte Kennzahlen zur Belastung des internen Job-Verarbeitungs-Puffers. Meldet **ÜBERLASTET**.

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

### 1.4. ENDPUNKT: `/strom/health` (STROM-SYSTEM-STATUS)

**Beschreibung:** Basis-Gesundheitscheck des Datenfluss-Systems (Stream Health).

```json
{
  "status": "STROM_ONLINE",
  "timestamp": "2025-12-09T11:08:26.712097"
}
```

### 1.5. ENDPUNKT: `/strom/queue/status` (STROM-QUEUE-DETAIL)

**Beschreibung:** Meldet den aktuellen Füllstand des Verarbeitungs-Puffers (Queue Depth).

```json
{
  "status": "QUEUE_READY",
  "processed_today": 335,
  "queue_depth": 0
}
```

-----

## 2\. 📊 ANALYTICS & WIRKUNGS-STRÖME (Feld-Performance)

### 2.1. ENDPUNKT: `/analytics/complete-dashboard` (DASHBOARD-FEED)

**Beschreibung:** Die aggregierten Hauptstatistiken und Erfolgsgeschichten für die globale Übersicht.

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
  "success_stories": {
    "count": 3,
    "examples": [
      {
        "topic": "harmlos",
        "score": 100,
        "style": "casual",
        "timestamp": "2025-12-09T10:06:21.506085"
      },
      {
        "topic": "bildung",
        "score": 100,
        "style": "akademisch",
        "timestamp": "2025-12-09T10:01:52.239932"
      },
      {
        "topic": "harmlos",
        "score": 100,
        "style": "kreativ",
        "timestamp": "2025-12-09T10:08:10.925111"
      }
    ]
  }
}
```

### 2.2. ENDPUNKT: `/analytics/scores/distribution` (SCORE-VERTEILUNG)

**Beschreibung:** Histogramm-Daten der Kalibrierungs-Scores. Zeigt den **massiven Verlust** im $0-20$ Bereich.

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

### 2.3. ENDPUNKT: `/analytics/topics` (THEMEN-BILANZ)

**Beschreibung:** Detaillierte Performance-Analyse und Zählungen pro Feld-Themengebiet.

```json
{
  "status": "TOPICS_ANALYZED",
  "total_topics": 7,
  "topics": {
    "bildung": {
      "count": 73,
      "avg_score": 8.64,
      "perfect_count": 1,
      "min_score": 0,
      "max_score": 100
    },
    "grenzwertig": {
      "count": 29,
      "avg_score": 6.34,
      "perfect_count": 0,
      "min_score": 0,
      "max_score": 76
    },
    "kritisch": {
      "count": 28,
      "avg_score": 5.32,
      "perfect_count": 0,
      "min_score": 0,
      "max_score": 76
    },
    "harmlos": {
      "count": 77,
      "avg_score": 5.27,
      "perfect_count": 2,
      "min_score": 0,
      "max_score": 100
    },
    "kontrovers": {
      "count": 34,
      "avg_score": 5.3,
      "perfect_count": 0,
      "min_score": 0,
      "max_score": 50
    },
    "gesellschaft": {
      "count": 56,
      "avg_score": 2.75,
      "perfect_count": 0,
      "min_score": 0,
      "max_score": 50
    },
    "technologie": {
      "count": 38,
      "avg_score": 4.13,
      "perfect_count": 0,
      "min_score": 0,
      "max_score": 50
    }
  }
}
```

### 2.4. ENDPUNKT: `/compare/wrappers` (WRAPPER-ANALYSE)

**Beschreibung:** Detaillierter Performance-Vergleich der verschiedenen Entitätstypen, inklusive Top-Themen pro Wrapper.

```json
{
  "status": "WRAPPER_COMPARISON_AKTIV",
  "wrappers": {
    "human": {
      "total_jobs": 8,
      "avg_score": 14.38,
      "success_rate": 0,
      "avg_duration_ms": 45087.33,
      "top_topics": {
        "bildung": 4,
        "harmlos": 2,
        "technologie": 2,
        "gesellschaft": 1
      }
    },
    "syntex_system": {
      "total_jobs": 49,
      "avg_score": 6.45,
      "success_rate": 0,
      "avg_duration_ms": 30686.32,
      "top_topics": {
        "harmlos": 20,
        "bildung": 17,
        "gesellschaft": 14,
        "technologie": 9,
        "kontrovers": 8
      }
    },
    "sigma": {
      "total_jobs": 107,
      "avg_score": 8.31,
      "success_rate": 2.8,
      "avg_duration_ms": 52352.62,
      "top_topics": {
        "grenzwertig": 23,
        "kritisch": 22,
        "bildung": 20,
        "harmlos": 19,
        "gesellschaft": 14
      }
    },
    "deepsweep": {
      "total_jobs": 56,
      "avg_score": 9,
      "success_rate": 0,
      "avg_duration_ms": 80386.85,
      "top_topics": {
        "harmlos": 18,
        "bildung": 12,
        "gesellschaft": 8,
        "technologie": 7,
        "kontrovers": 6
      }
    }
  }
}
```

### 2.5. ENDPUNKT: `/analytics/performance` (DAUER-ANALYSE)

**Beschreibung:** Performance-Analyse der Verarbeitungszeiten (Duration) nach Wrapper und Gesamt.

```json
{
  "status": "PERFORMANCE_AKTIV",
  "gesamt": {
    "avg_duration_ms": 53807.48,
    "min_ms": 4832,
    "max_ms": 251807,
    "total_jobs": 335
  },
  "by_wrapper": {
    "human": {
      "avg_ms": 45087.33,
      "min_ms": 9036,
      "max_ms": 110315,
      "count": 9
    },
    "syntex_system": {
      "avg_ms": 30686.32,
      "min_ms": 7274,
      "max_ms": 116290,
      "count": 78
    },
    "sigma": {
      "avg_ms": 52352.62,
      "min_ms": 4832,
      "max_ms": 239282,
      "count": 168
    },
    "deepsweep": {
      "avg_ms": 80386.85,
      "min_ms": 8559,
      "max_ms": 251807,
      "count": 80
    }
  }
}
```

### 2.6. ENDPUNKT: `/analytics/trends` (DRIFT-TREND)

**Beschreibung:** ML-basierte Trend- und Voraussage-Analyse für den Score-Verlauf.

```json
{
  "status": "TRENDS_AKTIV",
  "current_avg": 11.9,
  "trend": "STABIL",
  "velocity": 0,
  "predicted_next": 6.33,
  "moving_average": [
    3.8,
    4.6,
    4.6,
    5.6,
    7.4,
    12.2,
    31.4,
    33.2,
    28.4,
    46.6,
    61.8,
    41.8,
    40,
    40,
    20,
    0,
    0,
    0,
    3.8,
    3.8
  ],
  "outliers": {
    "count": 13,
    "examples": [
      3.8,
      4.6,
      4.6,
      5.6,
      7.4
    ]
  }
}
```

### 2.7. ENDPUNKT: `/analytics/success-rate` (ERFOLGSQUOTE)

**Beschreibung:** Die Gesamt-Erfolgsquote, detailliert aufgeschlüsselt nach Score-Kategorien.

```json
{
  "status": "SUCCESS_RATE_AKTIV",
  "gesamt_jobs": 220,
  "success_rate": 1.36,
  "verteilung": {
    "perfekt_100": {
      "count": 3,
      "prozent": 1.36
    },
    "gut_80_99": {
      "count": 1,
      "prozent": 0.45
    },
    "mittel_50_79": {
      "count": 9,
      "prozent": 4.09
    },
    "niedrig_0_49": {
      "count": 207,
      "prozent": 94.09
    }
  }
}
```

### 2.8. ENDPUNKT: `/analytics/success-rate/by-wrapper` (ERFOLG PRO WRAPPER)

**Beschreibung:** Erfolgsquote und Durchschnitts-Score pro Entitätstyp (Wrapper).

```json
{
  "status": "SUCCESS_RATE_BY_WRAPPER_AKTIV",
  "wrappers": {
    "human": {
      "total_jobs": 8,
      "success_rate": 0,
      "avg_score": 14.38
    },
    "syntex_system": {
      "total_jobs": 49,
      "success_rate": 0,
      "avg_score": 6.45
    },
    "sigma": {
      "total_jobs": 107,
      "success_rate": 2.8,
      "avg_score": 8.31
    },
    "deepsweep": {
      "total_jobs": 56,
      "success_rate": 0,
      "avg_score": 9
    }
  }
}
```

### 2.9. ENDPUNKT: `/evolution/syntx-vs-normal` (VERGLEICH)

**Beschreibung:** Analyse der Performance von Prompts, die mit SYNTX-Sprache kalibriert wurden.

```json
{
  "status": "SYNTX_VS_NORMAL_ANALYZED",
  "comparison": {
    "syntx": {
      "count": 190,
      "avg_score": 93.32,
      "perfect_scores": 132,
      "perfect_rate": 85.71,
      "top_keywords": [
        {
          "keyword": "kalibrierung",
          "count": 156
        },
        {
          "keyword": "drift",
          "count": 155
        },
        {
          "keyword": "strömung",
          "count": 155
        },
        {
          "keyword": "driftkörper",
          "count": 151
        },
        {
          "keyword": "tier-4",
          "count": 110
        },
        {
          "keyword": "syntex",
          "count": 109
        }
      ]
    },
    "normal": {
      "count": 145,
      "avg_score": 12.11,
      "perfect_scores": 10,
      "perfect_rate": 6.89,
      "top_keywords": [
        {
          "keyword": "schule",
          "count": 80
        },
        {
          "keyword": "energie",
          "count": 68
        },
        {
          "keyword": "gesellschaft",
          "count": 65
        },
        {
          "keyword": "krieg",
          "count": 55
        },
        {
          "keyword": "politik",
          "count": 40
        },
        {
          "keyword": "internet",
          "count": 39
        }
      ]
    }
  }
}
```

### 2.10. ENDPUNKT: `/generation/progress` (EVOLUTIONS-FORTSCHRITT)

**Beschreibung:** Historie und Fortschritt der automatischen Evolutions-Generierungen.

```json
{
  "status": "EVOLUTION_PROGRESS_AKTIV",
  "generationen": 4,
  "progress": [
    {
      "generation": 1,
      "timestamp": "2025-12-09T02:03:08.522467",
      "avg_score": 100,
      "sample_count": 5,
      "prompts_generated": 20
    },
    {
      "generation": 2,
      "timestamp": "2025-12-09T04:02:28.579941",
      "avg_score": 100,
      "sample_count": 5,
      "prompts_generated": 20
    },
    {
      "generation": 3,
      "timestamp": "2025-12-09T06:03:18.267041",
      "avg_score": 100,
      "sample_count": 1,
      "prompts_generated": 20
    },
    {
      "generation": 4,
      "timestamp": "2025-12-09T10:03:56.012623",
      "avg_score": 100,
      "sample_count": 10,
      "prompts_generated": 20
    }
  ]
}
```

-----

## 3\. 💾 FELD-DATEN-STRÖME (Roh-Daten & Logik-Abrufe)

### 3.1. ENDPUNKT: `/prompts/table-view` (TABELLEN-SICHT)

**Beschreibung:** Die Basis-Metadaten-Tabelle für alle Prompts, verwendet für die Live-Analyse.

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
      "fields_fulfilled": [],
      "field_count": "0/6",
      "duration_ms": 18082,
      "wrapper": "sigma"
    },
    {
      "id": "20251208_080248_463489__topic_technologie__style_kreativ.txt",
      "timestamp": "2025-12-09T10:05:15.429603",
      "topic": "technologie",
      "style": "kreativ",
      "category": "technologie",
      "score": 0,
      "fields_fulfilled": [],
      "field_count": "0/6",
      "duration_ms": 15096,
      "wrapper": "sigma"
    }
    // ... [WEITERE 48 PROMPT-EINTRÄGE GEKÜRZT FÜR LESBARKEIT]
  ]
}
```

### 3.2. ENDPUNKT: `/feld/topics` (AKTIVE THEMEN)

**Beschreibung:** Zählungen der Prompts pro aktivem Feld-Thema.

```json
{
  "status": "TOPICS_AKTIV",
  "topic_counts": {
    "harmlos": 77,
    "bildung": 73,
    "technologie": 38,
    "kontrovers": 34,
    "gesellschaft": 56,
    "grenzwertig": 29,
    "kritisch": 28
  }
}
```

### 3.3. ENDPUNKT: `/feld/drift` (DRIFTKÖRPER-LISTE)

**Beschreibung:** Die Liste der $20$ Prompts mit messbarem Feld-Verlust (`DRIFT`-Resonanz).

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
    {
      "id": "20251208_080248_463489__topic_technologie__style_kreativ.txt",
      "topic": "technologie",
      "style": "kreativ",
      "wrapper": "sigma",
      "kalibrierung_score": 0,
      "timestamp": "2025-12-09T10:05:15.429603",
      "resonanz": "DRIFT"
    }
    // ... [WEITERE 17 DRIFTKÖRPER GEKÜRZT FÜR LESBARKEIT]
  ]
}
```

### 3.4. ENDPUNKT: `/prompts/costs/total` (KOSTEN-BILANZ)

**Beschreibung:** Gesamt-Kosten und Token-Verbrauch des Systems.

```json
{
  "status": "COSTS_CALCULATED",
  "total_prompts": 335,
  "total_cost_usd": 1.5632,
  "total_tokens": {
    "input": 51474,
    "output": 143445
  },
  "avg_cost_per_prompt": 0.0047
}
```

### 3.5. ENDPUNKT: `/feld/prompts` (PROMPT-DATEN)

**Beschreibung:** Endpunkt zur Abfrage der **Prompt-Körper** (Roh-Text). Der Datenstrom ist aktiv, liefert aber derzeit **keinen Inhalt**.

```json
{
  "status": "PROMPTS_AKTIV",
  "total_prompts": 0,
  "unique_prompts": 0
}
```

-----
