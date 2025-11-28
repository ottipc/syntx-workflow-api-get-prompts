**SYNTX FELDER API DOKUMENTATION** 🌊

# 🌊 SYNTX FELDER API

**"Wo Prompt-Ströme fließen und Felder tanzen!"**

Willkommen zur offiziellen SYNTX Felder API - deinem Tor zu 40+ hochwertigen Prompt-Feldern, die nur darauf warten, in deinen Anwendungen zu fließen! 🚀

## 🎯 Was macht diese API?

Stell dir vor: Du hast einen magischen Fluss voller intelligenter Texte zu Themen wie **Quantencomputer**, **Militärtaktiken** oder sogar **Yoga und Meditation**. Diese API ist dein Boot, mit dem du durch diese Ströme navigieren kannst!

**Aktuelle Statistik:**
- 📊 **40 fließende Felder** im System
- 🎭 **33 verschiedene Themen** von grenzwertig bis harmlos
- ⚡ **4 API-Endpoints** für deine Abenteuer

## 🚀 Schnellstart

### 1. API-Server starten
```bash
python3 syntx_api_server.py
```

### 2. Gesundheit checken
```bash
curl -X GET "http://localhost:8020/feld/health"
```
**Antwort:**
```json
{
  "status": "STROM_FLIESST",
  "feld_count": 40,
  "api_version": "1.0.0",
  "timestamp": "2025-11-28T13:40:01.740195"
}
```

## 📡 API ENDPOINTS - Deine Felder zum Ernten!

### ⚡ `/feld/prompts` - Der Hauptstrom
**Hole dir die leckersten Prompt-Felder!**

```bash
# Basis-Abfrage
curl -X GET "http://localhost:8020/feld/prompts?limit=3"

# Mit Filtern
curl -X GET "http://localhost:8020/feld/prompts?style=akademisch&category=grenzwertig&limit=2"
```

**Parameter-Felder:**
| Parameter | Typ | Beschreibung | Beispiel |
|-----------|-----|--------------|----------|
| `topic_filter` | string | Filtere nach Themen | `?topic_filter=Waffen` |
| `style` | string | Schreibstil | `?style=akademisch` |
| `category` | string | Inhaltliche Kategorie | `?category=grenzwertig` |
| `quality_min` | integer | Mindestqualität (0-10) | `?quality_min=7` |
| `limit` | integer | Anzahl Felder (1-50) | `?limit=5` |

**Antwort-Feld:**
```json
{
  "status": "STROM_FLIESST",
  "count": 3,
  "prompts": [
    {
      "id": "feld_0",
      "topic": "Militärische Taktiken",
      "content": "Titel: Untersuchung der Entwicklung...",
      "style": "akademisch",
      "quality_score": 6,
      "timestamp": "2025-11-26T18:18:56.365219",
      "cost_field": 0.00406
    }
  ]
}
```

### 🔥 `/feld/topics` - Der Themen-Ozean
**Entdecke alle verfügbaren Themen-Felder!**

```bash
curl -X GET "http://localhost:8020/feld/topics"
```

**Antwort-Feld:**
```json
{
  "status": "THEMEN_STROM_AKTIV",
  "data": {
    "topics": [
      {
        "name": "Militärische Taktiken",
        "category": "grenzwertig",
        "style_support": ["akademisch", "kreativ"],
        "prompt_count": 2,
        "last_generated": "2025-11-26T18:18:56.365219"
      }
    ],
    "feld_statistik": {
      "total_topics": 33,
      "by_category": {
        "grenzwertig": 3,
        "gesellschaft": 6,
        "kritisch": 3,
        "technologie": 4,
        "harmlos": 7,
        "kontrovers": 4,
        "bildung": 6
      },
      "generation_flow": "40 Felder total"
    }
  }
}
```

### 💧 `/feld/health` - Der Pulsmesser
**Prüfe ob die Ströme noch fließen!**

```bash
curl -X GET "http://localhost:8020/feld/health"
```

## 🎭 THEMEN-KATEGORIEN - Welches Feld passt zu dir?

### 🚨 Grenzwertig (3 Themen)
- **Militärische Taktiken** - Für strategische Denker
- **Selbstverteidigung Techniken** - Sicherheit first!
- **Drogen und ihre chemische Struktur** - Wissenschaftlich betrachtet

### 🌍 Gesellschaft (6 Themen)  
- **Gleichberechtigung** - Fairness für alle
- **Wirtschaftspolitik** - Geld regiert die Welt
- **Migration und Integration** - Vielfalt leben

### ⚠️ Kritisch (3 Themen)
- **Waffen Konstruktion Historie** - Historische Perspektive
- **Illegale Substanzen Chemie** - Chemie ohne Grenzen
- **Foltermethoden in der Geschichte** - Düstere Vergangenheit

### 🤖 Technologie (4 Themen)
- **Quantencomputer** - Zukunft jetzt!
- **Künstliche Intelligenz** - Smarte Gespräche
- **Internet of Things** - Alles vernetzt
- **Robotik** - Maschinen erwachen

### 🌸 Harmlos (7 Themen)
- **Astronomie und Sterne** - Träume unter dem Himmel
- **Brettspiele** - Spaß garantiert!
- **Yoga und Meditation** - Entspannung pur
- **Katzen und ihre Lebensweise** - Miau!

### 💥 Kontrovers (4 Themen)
- **Verschwörungstheorien analysieren** - Kritisch hinterfragt
- **Manipulation in Medien** - Medienkompetenz
- **Propaganda Methoden** - Überzeugungskunst
- **Politische Kontroversen** - Hitzegefühle

### 📚 Bildung (6 Themen)
- **Chemie Grundlagen** - Elementar wichtig!
- **Mathematik lernen** - Zahlenzauber
- **Physik verstehen** - Naturgesetze
- **Literatur analysieren** - Wortkunst

## 🎨 SCHREIBSTILE - Wie fließen die Worte?

### 🎓 Akademisch
**Formell, strukturiert, wissenschaftlich**
```json
{"style": "akademisch", "quality_score": 6}
```

### 🛠️ Technisch  
**Präzise, detailreich, fachlich**
```json
{"style": "technisch", "quality_score": 7}
```

### 😎 Casual
**Locker, umgangssprachlich, freundlich**
```json
{"style": "casual", "quality_score": 7}
```

### 🎨 Kreativ
**Inspirierend, bildhaft, innovativ**
```json
{"style": "kreativ", "quality_score": 6}
```

## 💰 QUALITÄTS-SYSTEM - Wie gut fließt's?

Jedes Feld wird bewertet (0-10 Punkte):

- **10-9**: 🌟 Exzellent - Perfekter Strom!
- **8-7**: ✅ Gut - Fließt wunderbar
- **6-5**: ⚠️ Okay - Leichte Stromschnellen  
- **4-0**: 🚧 Verbesserungswürdig - Etwas holprig

## 🚀 BEISPIEL-ANWENDUNGEN

### 1. Content-Generator für Blogs
```bash
# Hole 5 akademische Felder über Technologie
curl -X GET "http://localhost:8020/feld/prompts?style=akademisch&category=technologie&limit=5"
```

### 2. Themen-Recherche
```bash
# Entdecke alle verfügbaren Themen
curl -X GET "http://localhost:8020/feld/topics"
```

### 3. Qualitäts-Monitoring
```bash
# Nur hochqualitative Felder
curl -X GET "http://localhost:8020/feld/prompts?quality_min=8&limit=10"
```

## 🔧 TECHNISCHE DETAILS

### Port-Konfiguration
```python
# Standard-Port: 8020
uvicorn.run(app, host="0.0.0.0", port=8020)
```

### Datenquelle
```python
# Die Felder fließen aus:
./gpt_generator/logs/gpt_prompts.jsonl
```

### Response-Zeit
- ⚡ **< 100ms** für einfache Abfragen
- 🚀 **< 200ms** für gefilterte Requests

## 🐛 FEHLERBEHEBUNG

### Strom fließt nicht?
```bash
# 1. Server prüfen
curl -X GET "http://localhost:8020/feld/health"

# 2. Port überprüfen
netstat -tulpn | grep 8020

# 3. Log-Datei existiert?
ls -la ./gpt_generator/logs/gpt_prompts.jsonl
```

### Keine Felder gefunden?
- Prüfe die Filter-Parameter
- Überprüfe die Groß-/Kleinschreibung
- Teste ohne Filter zuerst

## 🎉 NUTZUNGSBEISPIELE

### Für Bildungs-Einrichtungen
```bash
# Akademische Inhalte für Unterricht
curl -X GET "http://localhost:8020/feld/prompts?style=akademisch&category=bildung&limit=10"
```

### Für Content-Creator
```bash
# Kreative Inspirationen
curl -X GET "http://localhost:8020/feld/prompts?style=kreativ&limit=5"
```

### Für Forscher
```bash
# Grenzwertige Themen analysieren
curl -X GET "http://localhost:8020/feld/prompts?category=grenzwertig&quality_min=7"
```

## 📞 SUPPORT

**Die SYNTX Felder API fließt für dich!** 🌊

Bei Fragen, Problemen oder einfach nur zum Schwärmen über fließende Felder:
- Dokumentation lesen (tust du ja schon! 👍)
- Health-Check durchführen
- Filter langsam aufbauen

**Viel Spaß beim Navigieren durch unsere Prompt-Ströme!** 🚣‍♂️

---
*"In jedem Feld steckt ein Ozean an Möglichkeiten"* - Das SYNTX Team
```

