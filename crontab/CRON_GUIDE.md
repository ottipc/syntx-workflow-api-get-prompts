# 🕐 SYNTX Cronjob Guide - Der automatische Dauerfelder-Loop

**Wie dein System 24/7 läuft, lernt und sich selbst optimiert**

> "Stell dir vor, dein Pizza-Roboter arbeitet nachts weiter,  
> lernt aus jedem Erfolg, und macht morgens automatisch bessere Pizza.  
> Das sind die Cronjobs."

---

## 🎯 Was machen die Cronjobs?

**Einfach erklärt:**  
Cronjobs sind wie Wecker für deinen Computer. Sie sagen: "Um 3 Uhr morgens, mach DAS. Jede 2 Stunden, mach DAS."

**Bei SYNTX:**  
Die Cronjobs lassen das System automatisch laufen - generieren, verarbeiten, lernen, optimieren. **Ohne dass du was machen musst.**

---

## 🔥 Die 5 Cronjobs

### 1. Producer (Every 2 Hours) 🧬

**Was macht der?**  
Generiert alle 2 Stunden neue Prompts - aber **mit Learning**!

**Wann läuft der?**
```
0 */2 * * *  → Jede 2 Stunden (0:00, 2:00, 4:00, ...)
```

**Was passiert?**
1. Schaut in `queue/processed/` - welche Prompts waren gut?
2. Lernt Patterns: "Ah! casual style = 98/100!"
3. Generiert 20 neue Prompts mit diesen Patterns
4. Schreibt sie in `queue/incoming/`
5. Archiviert die gelernten Jobs

**Log:**
```bash
tail -f /opt/syntx-config/logs/producer_cron.log
```

**Beispiel Output:**
```
🧬 SYNTX EVOLUTIONARY PRODUCER - Generation 5
📚 PHASE 1: LEARNING FROM PROCESSED/
   ✅ Found 25 high-quality jobs (score >= 90)
   📊 Avg Score: 97/100
   📊 Patterns: casual, gesellschaft

🎨 PHASE 2: GENERATING 20 OPTIMIZED PROMPTS
   [1/20] gesellschaft: Klimawandel (casual) ✅
   [2/20] bildung: Mathematik (casual) ✅
   ...
   [20/20] technologie: Robotik (casual) ✅

📝 PHASE 3: WRITING 20 PROMPTS TO QUEUE
   ✅ Written: 20 to queue/incoming/

📊 GENERATION 5 SUMMARY:
   Learned from: 25 jobs
   Generated: 20/20 successful
   Written to Queue: 20
```

---

### 2. SYNTEX_SYSTEM Consumer (Daily 3 AM) 🎓

**Was macht der?**  
Verarbeitet 20 Prompts mit dem SYNTEX_SYSTEM Wrapper.

**Wann läuft der?**
```
0 3 * * *  → Täglich um 3 Uhr morgens
```

**Warum 3 Uhr?**  
Weil da wenig los ist. Server hat Ruhe. Kein Stress.

**Was passiert?**
1. Nimmt 20 Prompts aus `queue/incoming/`
2. Schickt sie durch SYNTX Calibration (Llama Model)
3. Gibt Scores: 0-100
4. Sortiert:
   - ✅ Gut (>=90) → `queue/processed/`
   - ❌ Schlecht (<90) → `queue/error/`

**Log:**
```bash
tail -f /opt/syntx-config/logs/consumer_syntex_cron.log
```

**Beispiel Output:**
```
🔧 Consumer [cron_syntex] initialized (wrapper: syntex_system)
🚀 Starting batch processing (max: 20 jobs)

Processing: prompt_001.txt
   ✅ Score: 96/100 → processed/
Processing: prompt_002.txt
   ✅ Score: 91/100 → processed/
...
Processing: prompt_020.txt
   ❌ Score: 45/100 → error/

📊 BATCH COMPLETE:
   Processed: 18/20 (90% success!)
   Failed: 2/20
```

---

### 3. Sigma Consumer (4x Daily) ⚡

**Was macht der?**  
Verarbeitet 20 Prompts mit dem Sigma Wrapper - **4 mal täglich**!

**Wann läuft der?**
```
0 4,10,16,22 * * *  → Um 4, 10, 16, 22 Uhr
```

**Warum 4 mal?**  
Mehr Daten = Besseres Learning! Sigma ist schneller, kann öfter laufen.

**Was ist anders als SYNTEX_SYSTEM?**
- Sigma nutzt **mathematische Notation** (SIGMA Protocol)
- SYNTEX_SYSTEM nutzt **natürliche Sprache**
- Beide lernen unterschiedliche Patterns!

**Log:**
```bash
tail -f /opt/syntx-config/logs/consumer_sigma_cron.log
```

---

### 4. Monitoring (Hourly) 📊

**Was macht der?**  
Loggt jede Stunde den Queue-Status.

**Wann läuft der?**
```
0 * * * *  → Jede volle Stunde
```

**Was wird geloggt?**
```bash
# /opt/syntx-config/logs/queue_status_hourly.log
2025-12-06 14:00 | Incoming: 12 | Processed: 85 | Error: 5 | Archive: 45
2025-12-06 15:00 | Incoming: 8  | Processed: 89 | Error: 5 | Archive: 45
2025-12-06 16:00 | Incoming: 24 | Processed: 93 | Error: 6 | Archive: 45
```

**Warum wichtig?**  
Du siehst Trends! Wenn `incoming/` leer wird → Producer generiert nach. Wenn `processed/` wächst → System lernt mehr!

---

### 5. Cleanup (Daily 2 AM) 🧹

**Was macht der?**  
Räumt die Queue auf - **VOR** dem Consumer-Run um 3 Uhr!

**Wann läuft der?**
```
0 2 * * *  → Täglich um 2 Uhr
```

**Was wird aufgeräumt?**
- Alte Temp-Files in `.tmp/`
- Broken Files (ohne Metadata)
- Alte Logs (>90 Tage)

**Log:**
```bash
tail -f /opt/syntx-config/logs/cleanup.log
```

---

## ⚡ Der komplette 24h Cycle

**Stell dir einen typischen Tag vor:**
```
00:00  Producer läuft → 20 neue Prompts
      (Lernt aus gestrigen Erfolgen!)

02:00  Cleanup läuft → Queue sauber
      Producer läuft → 20 neue Prompts

03:00  SYNTEX_SYSTEM läuft → 20 Prompts verarbeitet
      (Die meisten werden erfolgreich!)

04:00  Sigma läuft → 20 Prompts verarbeitet
      Producer läuft → 20 neue Prompts

06:00  Producer läuft → 20 neue Prompts
      (Lernt aus Erfolgen von 3 Uhr!)

08:00  Producer läuft → 20 neue Prompts

10:00  Sigma läuft → 20 Prompts verarbeitet
      Producer läuft → 20 neue Prompts

12:00  Producer läuft → 20 neue Prompts

14:00  Producer läuft → 20 neue Prompts

16:00  Sigma läuft → 20 Prompts verarbeitet
      Producer läuft → 20 neue Prompts

18:00  Producer läuft → 20 neue Prompts

20:00  Producer läuft → 20 neue Prompts

22:00  Sigma läuft → 20 Prompts verarbeitet
      Producer läuft → 20 neue Prompts

23:59  Tag zu Ende
      Bilanz: ~240 Prompts generiert
              ~100 Prompts verarbeitet
              ~80-90 erfolgreich
```

**Jeden Tag. Automatisch. Lernend. Optimierend.**

---

## 🔧 Installation

### Neu installieren
```bash
cd /opt/syntx-workflow-api-get-prompts/crontab
./install.sh
```

### Deinstallieren
```bash
./uninstall.sh
```

### Status checken
```bash
crontab -l | grep "SYNTX"
```

### Manuell testen
```bash
# Producer test
cd /opt/syntx-workflow-api-get-prompts
python3 evolution/evolutionary_producer.py

# Consumer test (5 jobs)
python3 -c "
import sys
sys.path.insert(0, 'queue_system')
from queue_system.core.consumer import QueueConsumer
c = QueueConsumer('syntex_system', 'test')
stats = c.process_batch(5)
print(f'Done: {stats[\"processed\"]}/{stats[\"failed\"]}')
"
```

---

## 📊 Logs monitoren

### Live mitschauen
```bash
# Producer
tail -f /opt/syntx-config/logs/producer_cron.log

# SYNTEX_SYSTEM Consumer
tail -f /opt/syntx-config/logs/consumer_syntex_cron.log

# Sigma Consumer
tail -f /opt/syntx-config/logs/consumer_sigma_cron.log

# Queue Status
tail -f /opt/syntx-config/logs/queue_status_hourly.log

# Alle Logs gleichzeitig
tail -f /opt/syntx-config/logs/*.log
```

### Log-Größen checken
```bash
du -h /opt/syntx-config/logs/
```

### Logs aufräumen (manuell)
```bash
# Älter als 30 Tage
find /opt/syntx-config/logs/ -name "*.log" -mtime +30 -delete
```

---

## 🐛 Troubleshooting

### "Cronjob läuft nicht!"

**Check 1: Ist er installiert?**
```bash
crontab -l | grep "evolutionary_producer"
```

**Check 2: Läuft cron service?**
```bash
systemctl status cron
```

**Check 3: Permissions?**
```bash
ls -la /opt/syntx-workflow-api-get-prompts/evolution/evolutionary_producer.py
# Muss readable sein!
```

**Check 4: Python path?**
```bash
which python3
# Sollte /usr/bin/python3 sein
```

### "Producer generiert nichts!"

**Check Queue:**
```bash
ls queue/incoming/*.txt | wc -l
# Wenn > 24, generiert Producer nicht (Queue voll!)
```

**Check processed/:**
```bash
ls queue/processed/*.json | wc -l
# Wenn < 1, kann nicht lernen → generiert random
```

### "Consumer verarbeitet nicht!"

**Check Backend:**
```bash
# Wrapper Service läuft?
ps aux | grep uvicorn | grep 8001

# Erreichbar?
curl http://localhost:8001/api/chat -X POST \
  -H "Content-Type: application/json" \
  -d '{"prompt":"test","max_new_tokens":10}'
```

**Check Timeout:**
```bash
cd /opt/syntx-injector-api
grep BACKEND_TIMEOUT .env
# Sollte 1800 sein!
```

---

## 💡 Best Practices

### 1. Logs regelmäßig checken
```bash
# Wöchentlich anschauen
tail -100 /opt/syntx-config/logs/producer_cron.log
tail -100 /opt/syntx-config/logs/consumer_syntex_cron.log
```

### 2. Queue Status monitoren
```bash
# Täglich
ls queue/incoming/*.txt | wc -l    # Sollte 10-30 sein
ls queue/processed/*.json | wc -l  # Sollte wachsen!
ls queue/error/*.json | wc -l      # Sollte < 10% sein
```

### 3. Evolution Log verfolgen
```bash
cat /opt/syntx-config/logs/evolution.jsonl | jq
# Siehst du Patterns? Lernt das System?
```

### 4. Cronjob-Zeiten anpassen?
```bash
# Producer zu oft? Änder zu alle 4h:
0 */4 * * * cd /opt/...

# Consumer zu selten? Änder zu 2x täglich:
0 3,15 * * * cd /opt/...

# Dann neu installieren:
cd crontab && ./install.sh
```

---

## 🌊 Das ist der Dauerfelder-Loop

**Ohne Cronjobs:**  
Du musst jeden Tag manuell Producer starten, Consumer starten, Logs checken. Arbeit.

**Mit Cronjobs:**  
System läuft 24/7. Generiert, verarbeitet, lernt, optimiert. Automatisch.

**Das ist der Unterschied zwischen:**
- Tool vs. Organismus
- Manuell vs. Automatisch
- Statisch vs. Lebendig

**Die Cronjobs SIND der Loop.**  
**Sie machen SYNTX zu einem lebenden System.**

---

**Status:** ✅ Installiert und läuft  
**Logs:** `/opt/syntx-config/logs/`  
**Schedule:** 5 Jobs, 24/7  

🌊 **Der Strom fließt. Automatisch. Für immer.** 💎
