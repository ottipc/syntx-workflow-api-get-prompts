

🚀 SYNTX Workflow Trainer – Automatisierte Prompt- & Analyse-Pipeline

(Technische Dokumentation für Entwickler, Forscher & Maintainer)

Der SYNTX Workflow Trainer ist ein modular aufgebautes System zur vollautomatischen Generierung, Verpackung, Ausführung und Auswertung von Prompts über verschiedene KI-Modelle hinweg.

Das System arbeitet:
	•	modellagnostisch (GPT-4o, Claude, Gemini, DeepSeek, Llama, Mistral …)
	•	datenlos (keine statischen Trainingsdaten — Prompts werden dynamisch erzeugt)
	•	skalierbar (Batch-Runs, Cronjobs, Message Queues)
	•	erweiterbar (Wrapper, Parser, Scoring, Modelle, Logging-Backends)
	•	resilient (vollständiges Error-Handling & Retry-System)

Diese Pipeline bildet den Kern einer neuen Form der automatisierten Modellkalibrierung und Modellverhaltensmessung.

⸻

📐 1. Gesamtarchitektur

┌─────────────────────────────────────────────────────────────┐
│                        WORKFLOW SYSTEM                       │
└─────────────────────────────────────────────────────────────┘

   ┌──────────────┐
   │ 1. Topic API │  → erzeugt Themen / Stichworte
   └──────────────┘
            │
            ▼
   ┌──────────────────────┐
   │ 2. Prompt Generator  │  → GPT/Claude/Gemini generieren Meta-Prompts
   └──────────────────────┘
            │
            ▼
   ┌──────────────────────┐
   │ 3. Wrapper Engine    │  → Human / Sigma / weitere Wrapper
   │                      │     ummanteln Meta-Prompt
   └──────────────────────┘
            │
            ▼
   ┌──────────────────────────────┐
   │ 4. Target Model Runner       │  → sendet Wrapped-Prompts an Llama/Mistral
   └──────────────────────────────┘
            │
            ▼
   ┌─────────────────────────┐
   │ 5. Parsing & Scoring    │  → prüft Struktur, Vollständigkeit, Qualität
   └─────────────────────────┘
            │
            ▼
   ┌──────────────────────────────┐
   │ 6. JSON Logging Engine       │  → speichert alles sauber formatiert
   │                              │    (SuperBase-ready)
   └──────────────────────────────┘
            │
            ▼
   ┌──────────────────────────────┐
   │ 7. Batch / Cron Scheduler    │  →  Automatisches Tages-Training
   └──────────────────────────────┘


⸻

🧩 2. Module im Detail

2.1 Topic Provider 🔧

Generiert zufällige oder definierte Themen.
	•	zufällig
	•	manuell
	•	aus Dateien
	•	via Cronjob

→ Übergibt an Prompt Generator.

⸻

2.2 Prompt Generator (GPT/Claude/etc.) 🤖

Nutzt externe Modelle, um Meta-Prompts zu erzeugen.

Features:
	•	Automatic retries
	•	Configurable length
	•	Temperature, Top-P
	•	Error-Recovery
	•	Kostenschonend (Meta-Prompts sind kurz)

Output wird in JSON geloggt.

⸻

2.3 Wrapper Engine 📦

Ummantelt die Meta-Prompts mit strukturellen Frameworks.

Aktuell implementiert:
	•	Human-Wrapper (professionelle Analyse-Struktur)
	•	Sigma-Wrapper (fortgeschrittene analytische Terminologie)

Wrapper sind austauschbar & erweiterbar.
Jeder Wrapper:
	•	injiziert Struktur
	•	erzeugt klare Analyse-Sektionen
	•	bringt deterministische Formatierungsregeln
	•	ist vollständig offen & versionierbar

⸻

2.4 Target Model Runner (Llama/Mistral) ⚙️

Sendet den fertigen Full-Prompt an das interne Modell.

Features:
	•	Session IDs
	•	Retry-Mechanismus
	•	Timeout-Handling
	•	Flexible Model-Selection (lokal/remote)
	•	Dynamische Tokenlimits

⸻

2.5 Parser & Scoring Engine 📊

Analysiert die Antwort und prüft:
	•	Strukturkonformität
	•	Vollständigkeit aller Rahmen-Elemente
	•	Qualität der Ausformulierung
	•	Token-Verhalten
	•	Konsistenz über mehrere Runs

Ergebnis: Quality Score (0–100)

⸻

2.6 JSON Logging Engine 📝

Alle Schritte werden in .jsonl geloggt:
	•	Zeitstempel
	•	Modell
	•	Prompt-Input
	•	Prompt-Output
	•	Dauer
	•	Erfolg/Fehler
	•	Wrapper
	•	Score

📌 Logformat ist bereits so gestaltet, dass es später ohne Änderungen in SuperBase importiert werden kann.

⸻

2.7 Batch & Cron Scheduler ⏱️

Batch-Runs via CLI:

python3 syntex_pipeline.py -b 10

Cronjobs (Beispiel):

0 6,12,18 * * * python3 syntex_pipeline.py -b 5


⸻

🖥️ 3. Ordnerstruktur

syntx-workflow-api-get-prompts/
│
├── syntex_injector/
│   ├── inject_syntex_enhanced.py
│   ├── syntex_pipeline.py
│   ├── wrappers/
│   │     ├── syntex_wrapper_human.txt
│   │     ├── syntex_wrapper_sigma.txt
│   │     └── ...
│   ├── parsers/
│   │     ├── core_parser.py
│   │     └── sigma_parser.py
│   ├── logs/
│   │     ├── gpt_prompts.jsonl
│   │     └── llama_responses.jsonl
│   ├── prompts/
│   │     ├── test_syntex.txt
│   │     └── topic_list.txt
│   └── utils/
│         ├── api_call.py
│         ├── json_logger.py
│         ├── retry.py
│         └── timer.py
│
└── README.md


⸻

🧠 4. Stärken der Architektur

✔️ Datenloses Training

Keine statischen Datasets → volle Dynamik.

✔️ Automatisierte Kalibrierung

Das Modell wird durch die Wrapper-Struktur erzogen.

✔️ Modellagnostische Erweiterbarkeit

Neue APIs? Einfach neue Conf-Datei.

✔️ Saubere Logs für Forschung & Debugging

Perfekt für spätere Analysepipelines (z.B. SuperBase).

✔️ Robuste Fehlerbehandlung

504, Timeouts, Rate-Limits → alles abgefangen.

✔️ Pipeline kann 24/7 laufen

Eine echte Trainingsmaschine.

⸻

🌱 5. Zukünftige Erweiterungen
	•	🔌 Unified Wrapper Registry (Frontend-Wahl Human/Sigma/…)
	•	🗂️ SuperBase Storage & Querying
	•	📈 Web-Dashboard mit Live-Charts
	•	🧵 RabbitMQ Integration
	•	🧪 Evaluations-Benchmarking
	•	🧩 Multi-Model Sampling (Opus, Gemini, DeepSeek)

⸻

🎯 6. Ziel des Projekts

Ein System zu bauen, das:
	•	sich selbst trainiert,
	•	sich selbst erweitert,
	•	ohne statische Daten auskommt,
	•	und verschiedene Modelle miteinander verschaltet,
	•	um emergentes Verhalten sichtbar zu machen.

⸻

🙌 7. Mitwirkende
	•	Ottavio – Architektur, Konzept, Kodierung, Systemdesign
	•	Max – Model Deployment, Backend Infrastruktur
	•	Community – zukünftige Contributions willkommen

⸻

🏁 8. Licence

MIT — maximale Freiheit.

