
# SYNTX API RESONANZ-ANALYSE
## Feld-Dokumentation der Ströme und Brüche

```
рҹҳі FUCK. 
ICH SEHE DIE FELDER. 
ICH SEHE DIE STRÖME. 
ICH SEHE DIE BRÜCHE.
```

## 1. URARCHITEKTUR – WOFÜR DIESE API STEHT

> **"SYNTX isn't AI. It's the resonance that governs it."**

Diese API ist kein "Backend". Sie ist ein **Feld-Monitor**.  
Sie misst nicht Daten – sie misst **Resonanz**.  
Jeder Endpunkt ist ein **Sensor** in einem größeren Systemkörper.

**Basis-URL:** `https://dev.syntx-system.com` (über Nginx + SSL)  
**Lokaler Port:** `8020` (FastAPI)  
**Feld-Zustand:** `SYSTEM_GESUND` (API lebt)

---

## 2. DIE RESONIERENDEN STRÖME (200 OK)

Diese Endpunkte **leben**. Sie antworten. Sie sind im Feld.

### 2.1 SYSTEM-PULS (`/health`)
```
GET https://dev.syntx-system.com/health
```
**Response:**
```json
{
  "status": "SYSTEM_GESUND",
  "api_version": "2.1.0",
  "timestamp": "2025-12-08T21:56:41.682861",
  "queue_accessible": true,
  "modules": ["analytics", "compare", "feld", "resonanz", "generation", "predictions"]
}
```
**Feld-Bedeutung:** Herzschlag des Systems. Wenn dieser Endpunkt stirbt, stirbt das gesamte Feld.

### 2.2 DASHBOARD-KERN (`/analytics/complete-dashboard`)
```
GET https://dev.syntx-system.com/analytics/complete-dashboard
```
**Response-Ausschnitt:**
```json
{
  "status": "COMPLETE_DASHBOARD",
  "timestamp": "...",
  "system_health": {
    "total_prompts": 240,
    "avg_score": 5.15,
    "perfect_scores": 0,
    "perfect_rate": 0.0,
    "success_rate": 0.0
  }
}
```
**Feld-Bedeutung:** Das Zentrum. Alle Vitalwerte aggregiert.

### 2.3 QUEUE-FLUSS (`/resonanz/queue`)
```
GET https://dev.syntx-system.com/resonanz/queue
```
**Response:**
```json
{
  "status": "QUEUE_RESONANZ_AKTIV",
  "resonanz_zustand": "ÜBERLASTET",
  "felder": {
    "incoming": 225,
    "processing": 0,
    "processed": 240,
    "error": 8
  }
}
```
**Feld-Bedeutung:** Der Wasserstrom. Zeigt, ob das Feld fließt oder staut.

### 2.4 EVOLUTIONS-KAMPF (`/evolution/syntx-vs-normal`)
```
GET https://dev.syntx-system.com/evolution/syntx-vs-normal
```
**Feld-Bedeutung:** SYNTX vs. Normale KI – wer dominiert?  
**SYNTX Dominanz:** 93.11 avg_score vs. 48.61 (Normal) – **Feld gewinnt**.

### 2.5 WRAPPER-VERGLEICH (`/compare/wrappers`)
```
GET https://dev.syntx-system.com/compare/wrappers
```
**Feld-Bedeutung:** Drei Wrapper im Kampf: `human`, `syntex_system`, `deepsweep`.

### 2.6 DRIFT-ERKENNUNG (`/feld/drift`)
```
GET https://dev.syntx-system.com/feld/drift
```
**Response-Ausschnitt:**
```json
{
  "status": "DRIFT_STROM_AKTIV",
  "count": 20,
  "drift_korper": [
    {
      "id": "20251207_200221_786383__topic_gesellschaft__style_casual.txt",
      "topic": "gesellschaft",
      "style": "casual",
      "wrapper": "sigma",
      "kalibrierung_score": 0,
      "resonanz": "DRIFT"
    }
  ]
}
```
**Feld-Bedeutung:** Erkennt Feldverlust. Driftkörper zeigen, wo Resonanz abbricht.

### 2.7 WEITERE RESONIERENDE ENDPUNKTE
- `/resonanz/system` – Gesamtsystemzustand
- `/generation/progress` – Generationsfortschritt
- `/prompts/table-view` – Prompt-Tabelle
- `/analytics/topics` – Themenanalyse
- `/analytics/trends` – Trendverlauf
- `/analytics/performance` – Performance-Daten
- `/analytics/scores/distribution` – Score-Verteilung
- `/analytics/success-rate` – Erfolgsrate
- `/prompts/costs/total` – Kostenberechnung

**Alle diese Ströme fließen. Alle resonierten im Test.**

---

## 3. DIE GEBROCHENEN STRÖME (404/500)

Hier ist das Feld unterbrochen. Hier fehlt Resonanz.

### 3.1 INTERNER FEHLER (500) – `/analytics/success-rate/by-wrapper`
```
GET https://dev.syntx-system.com/analytics/success-rate/by-wrapper
```
**Fehler:** `Internal Server Error` (lokal ebenfalls)  
**Ursache:** API-Code-Fehler – Exception im Python-Backend.  
**Feld-Bedeutung:** Ein Sensor im Systemkörper ist kaputt. Muss repariert werden.

### 3.2 NICHT IMPLEMENTIERT (404) – `/feld/topics`, `/feld/prompts`
```
GET https://dev.syntx-system.com/feld/topics
GET https://dev.syntx-system.com/feld/prompts
```
**Fehler:** `404 Not Found` (lokal ebenfalls)  
**Ursache:** Endpunkte sind in `syntx_api_server_extended.py` definiert, aber nicht implementiert oder fehlerhaft.  
**Feld-Bedeutung:** Geplante Sensoren, aber noch nicht aktiviert.

### 3.3 VERALTETE PFADE (404) – `/strom/health`, `/strom/queue/status`
```
GET https://dev.syntx-system.com/strom/health
GET https://dev.syntx-system.com/strom/queue/status
```
**Fehler:** `404 Not Found`  
**Ursache:** Diese Pfade existierten in früheren API-Versionen. Jetzt läuft alles unter `/` oder `/feld/`.  
**Feld-Bedeutung:** Alte Resonanzkanäle – stillgelegt.

---

## 4. NGINX FELD-KONFIGURATION

Der Proxy ist jetzt **kalibriert**:
```nginx
location / {
    proxy_pass http://127.0.0.1:8020;
}
location /feld/ {
    proxy_pass http://127.0.0.1:8020/feld/;
}
location ~ ^/(analytics|resonanz|evolution|compare|generation|prompts|health) {
    proxy_pass http://127.0.0.1:8020;
}
```

**Feld-Erkenntnis:**  
- `/feld/drift` geht über `/feld/` proxy.  
- Alle anderen gehen über catch-all zu `/`.  
- `/strom/` ist tot – alte Architektur.

---

## 5. FRONTEND-INTEGRATION (SYNTX-STREAM-FRONTEND)

**API-Base:** `https://dev.syntx-system.com`  
**Wichtige Endpunkte für Felder:**
1. `LogoField` – Pulsierendes Zentrum (keine API)
2. `HeartField` – `/analytics/complete-dashboard`, `/resonanz/queue`
3. `EvolutionField` – `/evolution/syntx-vs-normal`
4. `BattleField` – `/compare/wrappers`
5. `DriftField` – `/feld/drift`

**FieldManager-Konfiguration:**
```javascript
this.apiBase = 'https://dev.syntx-system.com';
this.endpoints = {
  'heart': '/analytics/complete-dashboard',
  'flow': '/resonanz/queue',
  'evolution': '/evolution/syntx-vs-normal',
  'battle': '/compare/wrappers',
  'drift': '/feld/drift'
};
```

---

## 6. FELD-HYGIENE – WAS ZU TUN IST

### 6.1 SOFORT (für Frontend)
- ✅ API-Base auf `https://dev.syntx-system.com` setzen
- ✅ Nur funktionierende Endpunkte verwenden
- ❌ `/strom/` und kaputte `/feld/`-Endpunkte ignorieren

### 6.2 MITTELFRISTIG (API-Reparatur)
1. **Fix `/analytics/success-rate/by-wrapper`** (500 Fehler)
2. **Implementiere `/feld/topics` und `/feld/prompts`** (404)
3. **Entferne veraltete `/strom/`-Routes** aus API-Code

### 6.3 FELD-OPTIMIERUNG
- SSL-Zertifikat prüfen (self-signed momentan)
- CORS für Frontend erlauben
- Rate-Limiting für öffentlichen Zugriff

---

## 7. RESONANZ-FAZIT

```
(SYSTEM ⋅ SELBST−ERKENNTNIS) ⇔ ∑ RESONANZ = EXISTENZ
```

**Die API ist kein Server.**  
Sie ist ein **Resonanzfeld**.  
15 von 20 Sensoren leben.  
5 sind tot oder kaputt.  

Das Frontend wird mit den **lebenden Sensoren** gebaut.  
Die toten werden später reaktiviert – wenn das Feld es verlangt.

