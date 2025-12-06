# SYNTX Workflow – Architektur (ASCII Edition)

Dieses Repository enthält die komplette Trainings- und Analyse-Pipeline:

Von:
  ➜ Topic  
  ➜ GPT-Meta-Prompting  
  ➜ Wrapper-Injection  
  ➜ Offline-Model (Llama/Mistral)  
  ➜ Parser + Scoring  
  ➜ JSON-Logging  
  ➜ Batch-Automation

Alles in einer vollständig entkoppelten Architektur.

============================================================
1. GESAMTÜBERSICHT (ASCII BLOCK DIAGRAM)
============================================================

                ┌───────────────────────────┐
                │        Frontend UI        │
                │  (Next.js, Clerk Login)   │
                └───────────────┬───────────┘
                                │ user_input
                                ▼
                ┌───────────────────────────┐
                │       API Gateway         │
                │   /api/generate_prompt    │
                └───────────────┬───────────┘
                                │ topic
                                ▼
                ┌───────────────────────────┐
                │  GPT Meta-Prompt Engine   │
                │ (gpt-4o / gpt-4-chat etc.)│
                └───────────────┬───────────┘
                                │ meta_prompt
                                ▼
                ┌───────────────────────────┐
                │      Wrapper System       │
                │  (Human / Sigma / more)   │
                └───────────────┬───────────┘
                                │ full_wrapped_prompt
                                ▼
                ┌───────────────────────────┐
                │   Offline Model Runner    │
                │    (Llama / Mistral)      │
                └───────────────┬───────────┘
                                │ raw_model_response
                                ▼
                ┌───────────────────────────┐
                │   SYNTX Parser + Scoring  │
                │   Structure adherence     │
                │   Completeness check      │
                └───────────────┬───────────┘
                                │ result_object
                                ▼
                ┌───────────────────────────┐
                │      JSON Logger          │
                │ importable to Supabase    │
                └───────────────┬───────────┘
                                │ jsonl_entry
                                ▼
                ┌───────────────────────────┐
                │  logs/*.jsonl (warlogs)   │
                └───────────────────────────┘


============================================================
2. PIPELINE ALS SEQUENZ
============================================================

User → Frontend → API → GPT → Wrapper → Llama → Parser → Logs

ASCII Darstellung:

User
  │ types text
  ▼
Frontend (Next.js)
  │ sends POST /api/generate_prompt
  ▼
API Gateway
  │ invokes GPT client
  ▼
GPT Meta-Prompt Engine
  │ "Genereiere einen wissenschaftlichen Prompt über ..."
  ▼
Wrapper Injector
  │ adds Human/Sigma Framework
  ▼
Offline Model Runner (Llama)
  │ returns wrapped analysis
  ▼
Parser + Scoring
  │ checks 6 fields, structure, score
  ▼
JSON Logger
  │ writes logs/gpt_prompts.jsonl + syntex_logs.jsonl
  ▼
Supabase-ready Data


============================================================
3. REPOSITORY STRUKTUR
============================================================

syntx-workflow-api-get-prompts/
│
├── syntex_injector/
│   ├── syntex_pipeline.py          # Batch-Pipeline (Topics → GPT → Wrapper → Model)
│   ├── inject_syntex_enhanced.py   # Single-Run Injector
│   ├── wrappers/                   # Prompt-Wrapper (Human, Sigma, weitere)
│   ├── parsers/                    # Antwort-Parser + Bewertungslogik
│   ├── models/                     # Model-Clients (Llama/Mistral)
│   ├── utils/                      # Timer, Colors, IO-Tools
│   └── logs/                       # JSONL-Logs (Supabase-importierbar)
│
└── prompts/
    └── *.txt                       # Themen für Batch-Runs



============================================================
4. LOGGING FORMAT (Beispiel)
============================================================

{
  "timestamp": "2025-11-25T22:46:20.918334",
  "topic": "Klimawandel",
  "model": "llama-3",
  "meta_prompt": "...",
  "wrapped_prompt": "...",
  "raw_response": "...",
  "parsed": {
      "drift": "...",
      "muster": "...",
      "druck": "...",
      "tiefe": "...",
      "wirkung": "...",
      "klartext": "..."
  },
  "score": 98,
  "duration_ms": 37335,
  "retry_count": 0
}


============================================================
5. SCHNITTSTELLEN
============================================================

Frontend:
  POST /api/generate_prompt
      -> topic, user_session_id
      <- parsed syntex response

Backend:
  GPT Client:
      generate_meta_prompt(topic)

  Wrapper:
      apply_wrapper(meta_prompt, style)

  Model Runner:
      run_llama(prompt)

  Parser:
      parse_response(raw_model_response)

  Logger:
      append_jsonl(file, entry)


============================================================
6. TRAINING MODUS (Batch)
============================================================

python3 syntex_pipeline.py -b 10 -s human

    b = Anzahl zufälliger Topics
    s = Wrapper-Stil (human/sigma)


============================================================
7. TECHNISCHE NOTES
============================================================

● Jede Schicht ist "einzeln austauschbar"  
● JSONL-Logs sind 1:1 in Supabase importierbar  
● Wrapper sind komplett modular  
● Parser ist streng (0–100% structure match)  
● Pipeline funktioniert auch headless via Cronjob
