"""
Queue System Configuration
"""
from pathlib import Path

# Base Paths
QUEUE_BASE = Path("queue")
QUEUE_INCOMING = QUEUE_BASE / "incoming"
QUEUE_PROCESSING = QUEUE_BASE / "processing"
QUEUE_PROCESSED = QUEUE_BASE / "processed"
QUEUE_ERROR = QUEUE_BASE / "error"
QUEUE_ARCHIVE = QUEUE_BASE / "archive"
QUEUE_TMP = QUEUE_BASE / ".tmp"

# Thresholds
QUEUE_MIN_THRESHOLD = 5    # Unter 5 → Producer aktiviert
QUEUE_MAX_THRESHOLD = 50   # Über 50 → Producer wartet
QUEUE_CRITICAL_THRESHOLD = 100  # Alarm!

# Producer Settings
PRODUCER_BATCH_SIZE = 20
PRODUCER_CHECK_INTERVAL_HOURS = 2

# Consumer Settings
CONSUMER_BATCH_SIZE = 20
CONSUMER_MAX_WORKERS = 3
CONSUMER_PROCESSING_TIMEOUT = 3600  # 1 Stunde

# Cleanup Settings
ARCHIVE_AFTER_DAYS = 30
ERROR_RETENTION_DAYS = 90
