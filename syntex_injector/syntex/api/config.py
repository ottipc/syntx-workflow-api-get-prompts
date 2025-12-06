"""
SYNTEX API Configuration
"""

# API Endpoint
API_ENDPOINT = "https://dev.syntx-system.com/api/chat"

# Timeouts (in Sekunden)
CONNECT_TIMEOUT = 30
READ_TIMEOUT = 3600  # 60 MINUTEN - Llama hat alle Zeit der Welt!

# Retry Configuration
MAX_RETRIES = 3
RETRY_DELAYS = [1, 3, 7]  # Sekunden zwischen Retries

# Model Parameters
MODEL_PARAMS = {
    "max_new_tokens": 1024,
    "temperature": 0.3,
    "top_p": 0.85,
    "do_sample": True
}
