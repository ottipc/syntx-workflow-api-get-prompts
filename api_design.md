# SYNTX Queue API - Frontend Schnittstelle

## Base URL
```
https://dev.syntx-system.com/queue-api
```

## Endpoints

### 1. GET /status
**Purpose:** Real-time Queue Status

**Response:**
```json
{
  "timestamp": "2025-11-28T10:30:00Z",
  "queue": {
    "incoming": 19,
    "processing": 0,
    "processed": 1,
    "error": 0
  },
  "state": "BALANCED",
  "producer": {
    "should_run": true,
    "batch_size": 10
  },
  "health": "OK"
}
```

---

### 2. GET /stats
**Purpose:** System Statistics

**Response:**
```json
{
  "total_jobs": 1250,
  "success_rate": 98.5,
  "average_quality": 97.8,
  "average_duration_ms": 52341,
  "wrappers": {
    "human": {
      "count": 625,
      "avg_quality": 98.2,
      "avg_duration_ms": 53120
    },
    "sigma": {
      "count": 625,
      "avg_quality": 97.4,
      "avg_duration_ms": 51562
    }
  },
  "daily_stats": {
    "today": 45,
    "yesterday": 87,
    "last_7_days": 412
  }
}
```

---

### 3. GET /jobs/recent
**Purpose:** Recent Jobs List

**Query Params:**
- `limit` (default: 20)
- `status` (incoming|processing|processed|error)
- `wrapper` (human|sigma)

**Response:**
```json
{
  "jobs": [
    {
      "id": "20251128_101353_896630",
      "topic": "Gesundheitssysteme",
      "style": "kreativ",
      "status": "processed",
      "wrapper": "human",
      "quality_score": 98,
      "duration_ms": 59451,
      "created_at": "2025-11-28T10:13:53Z",
      "processed_at": "2025-11-28T10:20:52Z"
    },
    // ...
  ],
  "total": 1250,
  "page": 1
}
```

---

### 4. GET /jobs/:id
**Purpose:** Job Details

**Response:**
```json
{
  "id": "20251128_101353_896630",
  "topic": "Gesundheitssysteme",
  "style": "kreativ",
  "category": "gesellschaft",
  "status": "processed",
  "wrapper": "human",
  "worker_id": "test",
  
  "gpt_prompt": "Erkläre Gesundheitssysteme kreativ...",
  
  "syntex_result": {
    "quality_score": {
      "total_score": 98,
      "field_completeness": 100,
      "structure_adherence": 96,
      "fields": {
        "drift": true,
        "hintergrund_muster": true,
        "druckfaktoren": true,
        "tiefe": true,
        "wirkung": true,
        "klartext": true
      }
    },
    "response": "1. DRIFT: The situation here...",
    "duration_ms": 59451,
    "session_id": "e6468efd"
  },
  
  "timestamps": {
    "created_at": "2025-11-28T10:13:53Z",
    "processed_at": "2025-11-28T10:20:52Z"
  }
}
```

---

### 5. POST /producer/trigger
**Purpose:** Force Producer Run

**Body:**
```json
{
  "force": true,
  "count": 10
}
```

**Response:**
```json
{
  "triggered": true,
  "batch_size": 10,
  "status": "running",
  "job_id": "prod_20251128_103045"
}
```

---

### 6. GET /logs/tail
**Purpose:** Live Log Streaming (SSE)

**Query Params:**
- `source` (producer|consumer_human|consumer_sigma|monitor)
- `lines` (default: 50)

**Response:** Server-Sent Events
```
event: log
data: {"timestamp": "...", "level": "INFO", "message": "..."}

event: log
data: {"timestamp": "...", "level": "SUCCESS", "message": "..."}
```

---

### 7. GET /health
**Purpose:** System Health Check

**Response:**
```json
{
  "status": "healthy",
  "checks": {
    "queue_accessible": true,
    "llama_backend": true,
    "gpt_api": true,
    "disk_space": "85% free",
    "cron_running": true
  },
  "uptime_seconds": 345678
}
```

---

### 8. POST /jobs/:id/retry
**Purpose:** Retry Failed Job

**Response:**
```json
{
  "job_id": "20251128_101353_896630",
  "status": "moved_to_incoming",
  "retry_count": 2
}
```

---

### 9. GET /analytics/quality
**Purpose:** Quality Score Analytics

**Query Params:**
- `days` (default: 7)
- `wrapper` (optional)

**Response:**
```json
{
  "period": "last_7_days",
  "data": [
    {
      "date": "2025-11-28",
      "avg_quality": 97.8,
      "count": 45
    },
    // ...
  ],
  "distribution": {
    "90-100": 892,
    "80-89": 45,
    "70-79": 12,
    "below_70": 1
  }
}
```

---

### 10. DELETE /jobs/:id
**Purpose:** Delete Job (Admin)

**Response:**
```json
{
  "deleted": true,
  "job_id": "20251128_101353_896630"
}
```

