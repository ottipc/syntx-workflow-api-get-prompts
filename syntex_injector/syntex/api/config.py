"""
API Configuration für SYNTEX System
"""

# 7B Model Endpoint
API_ENDPOINT = "https://dev.syntx-system.com/api/chat"

# Model Parameters für SYNTEX-Analyse
MODEL_PARAMS = {
    "max_new_tokens": 1024,    # Längere Outputs für detaillierte Analyse
    "temperature": 0.3,        # Niedriger für präzise Kalibrierung
    "top_p": 0.85,
    "do_sample": True
}

# Retry Configuration
MAX_RETRIES = 3
RETRY_DELAYS = [1, 3, 7]  # Exponential Backoff

# Timeouts
CONNECT_TIMEOUT = 30
READ_TIMEOUT = 1800
