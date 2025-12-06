# SYNTX Crontab Configuration

Automated scheduling for SYNTX queue processing.

## 📋 Jobs Overview

**Producer** - Every 2 hours
- Self-regulating (only runs if queue needs work)

**Consumer Human** - Daily at 3 AM
- Processes 20 jobs with human wrapper

**Consumer Sigma** - 4x daily (4am, 10am, 4pm, 10pm)
- Processes 20 jobs with sigma wrapper

**Monitoring** - Hourly + Daily cleanup

## 🚀 Quick Start
```bash
./crontab/install.sh
```

## 📊 View Status
```bash
crontab -l
```

## 🗑️ Remove
```bash
./crontab/uninstall.sh
```
