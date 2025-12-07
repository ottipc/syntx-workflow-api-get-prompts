# SYNTX Production API v2.1

**Advanced Analytics & Monitoring REST API**

---

## 🌊 Overview

REST API providing real-time monitoring, ML predictions, statistical analysis, and performance tracking for the SYNTX processing system.

**Base URL**: `http://dev.syntx-system.com:8020`

**Documentation**: `http://dev.syntx-system.com:8020/docs`

---

## 📊 API Endpoints

### Analytics Module

#### Dashboard
```
GET /analytics/dashboard
```
System overview with health metrics, queue status, quality stats, and activity summary.

**Response:**
```json
{
  "status": "DASHBOARD_AKTIV",
  "gesamt_health": 2356.86,
  "queue": {
    "incoming": 121,
    "processing": 1,
    "processed": 177,
    "error": 8
  },
  "qualität": {
    "durchschnitt": 22.03,
    "success_rate": 12.86,
    "trend": "STEIGEND"
  },
  "aktivität": {
    "total_jobs": 100,
    "generationen": 3,
    "top_topics": {...},
    "wrappers": {...}
  }
}
```

#### Success Rate
```
GET /analytics/success-rate
GET /analytics/success-rate/by-wrapper
GET /analytics/success-rate/by-topic
```
Success rate analysis overall, by wrapper, or by topic.

#### Trends & Predictions
```
GET /analytics/trends
```
ML-powered trend analysis with predictions.

**Response:**
```json
{
  "status": "TRENDS_AKTIV",
  "current_avg": 42.8,
  "trend": "STABIL",
  "velocity": 0.74,
  "predicted_next": 76.0,
  "moving_average": [...],
  "outliers": {
    "count": 15,
    "indices": [...]
  }
}
```

#### Performance Analysis
```
GET /analytics/performance
GET /analytics/performance/by-topic
GET /analytics/performance/hourly
```
Processing performance metrics and bottleneck detection.

#### Statistical Analysis
```
GET /analytics/correlation/topic-score
GET /analytics/outliers
```
Topic-score correlation analysis and outlier detection.

---

### Comparison Module

#### Wrapper Comparison
```
GET /compare/wrappers
GET /compare/wrappers/{wrapper1}/{wrapper2}
```
Compare wrapper performance.

**Response:**
```json
{
  "status": "WRAPPER_COMPARISON_AKTIV",
  "wrappers": {
    "syntex_system": {
      "total_jobs": 38,
      "avg_score": 32.0,
      "success_rate": 23.68,
      "avg_duration_ms": 42445.82,
      "top_topics": {...}
    }
  }
}
```

#### Topic Comparison
```
GET /compare/topics/{topic1}/{topic2}
```
Compare topic performance across wrappers.

---

### Core Monitoring

#### Drift Detection
```
GET /feld/drift?limit=20&topic=X&wrapper=Y&min_score=50
GET /feld/drift/{job_id}
```
Monitor semantic drift in processing.

#### Resonanz Monitoring
```
GET /resonanz/queue
GET /resonanz/system
```
Queue health and system resonance status.

#### Evolution Progress
```
GET /generation/progress
```
Track evolution learning progress.

---

### System

#### Health Check
```
GET /health
```
API health status.

#### API Info
```
GET /
```
API information and available endpoints.

---

## 🚀 Quick Start

### Using curl
```bash
# Dashboard
curl -s http://localhost:8020/analytics/dashboard | jq

# Trends
curl -s http://localhost:8020/analytics/trends | jq

# Wrapper comparison
curl -s http://localhost:8020/compare/wrappers | jq
```

### Using Python
```python
import requests

# Get dashboard
response = requests.get('http://localhost:8020/analytics/dashboard')
data = response.json()
print(f"Health: {data['gesamt_health']}")
print(f"Success Rate: {data['qualität']['success_rate']}%")

# Get predictions
response = requests.get('http://localhost:8020/analytics/trends')
data = response.json()
print(f"Predicted next: {data['predicted_next']}")
```

### Using JavaScript
```javascript
// Get dashboard
fetch('http://localhost:8020/analytics/dashboard')
  .then(res => res.json())
  .then(data => {
    console.log('Health:', data.gesamt_health);
    console.log('Success Rate:', data.qualität.success_rate);
  });
```

---

## 🔧 Service Management
```bash
# Start API
sudo systemctl start syntx-api

# Check status
sudo systemctl status syntx-api

# Restart
sudo systemctl restart syntx-api

# Logs
sudo journalctl -u syntx-api -f
```

---

## 📈 Current Metrics

### System Performance
- **Total Jobs**: 177 processed
- **Success Rate**: 6.57%
- **Avg Processing Time**: 67.7s
- **Queue Status**: 121 incoming, 1 processing

### Best Wrapper
**SYNTEX_SYSTEM**
- Average Score: 32.0
- Success Rate: 23.68%
- Avg Duration: 42.4s
- Total Jobs: 56

### Top Topics
1. gesellschaft (26.85 avg)
2. kritisch (23.56 avg)
3. kontrovers (22.36 avg)

---

## 🛠️ Development

### Architecture
```
syntx_api_production_v2.py
├── analytics/
│   ├── dashboard.py
│   ├── success_rate.py
│   ├── advanced.py
│   └── performance.py
├── compare/
│   ├── wrappers.py
│   └── topics.py
└── utils/
    ├── log_loader.py
    └── algorithms.py
```

### Adding Endpoints

1. Create module in `analytics/` or `compare/`
2. Define router with FastAPI
3. Import in `syntx_api_production_v2.py`
4. Include router: `app.include_router(module.router)`
5. Restart service

**Example:**
```python
from fastapi import APIRouter

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/new-endpoint")
async def new_endpoint():
    return {"status": "NEW_ENDPOINT_AKTIV"}
```

### Testing
```bash
# Test endpoint
curl -s http://localhost:8020/analytics/new-endpoint | jq

# Check all endpoints
curl -s http://localhost:8020/openapi.json | jq '.paths | keys'
```

---

## 📊 ML Algorithms

### Trend Analysis
- **Moving Average**: 5-window smoothing
- **Velocity**: Rate of change calculation
- **Prediction**: Linear regression forecasting
- **Trend Detection**: STEIGEND/STABIL/FALLEND

### Statistical Methods
- **Outlier Detection**: Z-score (threshold: 2.0)
- **Correlation**: Deviation from mean analysis
- **Performance Profiling**: Duration-based bottlenecks
- **Efficiency Ratios**: Score/duration calculations

---

## 🎯 API Features

✅ **30+ REST Endpoints**
✅ **ML Predictions & Trends**
✅ **Statistical Analysis**
✅ **Real-time Monitoring**
✅ **Performance Tracking**
✅ **Wrapper Comparison**
✅ **Queue Management**
✅ **Evolution Progress**
✅ **Interactive Docs**
✅ **JSON Responses**

---

## 🔗 Links

- **Production**: http://dev.syntx-system.com:8020
- **Docs**: http://dev.syntx-system.com:8020/docs
- **Health**: http://dev.syntx-system.com:8020/health

---

**SYNTX API v2.1 - Production Ready** 💎🔥🌊⚡
