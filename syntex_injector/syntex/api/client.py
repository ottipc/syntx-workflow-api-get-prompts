"""
API Client für 7B Model Communication
"""

import requests
import time
import sys
from typing import Optional, Tuple

from .config import (
    API_ENDPOINT,
    MODEL_PARAMS,
    MAX_RETRIES,
    RETRY_DELAYS,
    CONNECT_TIMEOUT,
    READ_TIMEOUT
)


class APIClient:
    """Client für 7B Model API mit Retry-Logik"""
    
    def __init__(self):
        self.endpoint = API_ENDPOINT
        self.params = MODEL_PARAMS
    
    def send(self, prompt: str) -> Tuple[Optional[str], Optional[str], int]:
        """
        Sendet Prompt an 7B Model.
        
        Args:
            prompt: Vollständiger SYNTEX-kalibrierter Prompt
        
        Returns:
            (response_text, error_message, retry_count)
        """
        payload = {
            "prompt": prompt,
            **self.params
        }
        
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.post(
                    self.endpoint,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
                )
                
                # Server Errors
                if response.status_code >= 500:
                    raise requests.HTTPError(
                        f"Server Error {response.status_code}"
                    )
                
                response.raise_for_status()
                result = response.json()
                
                # Response validieren
                if "response" not in result:
                    raise ValueError(f"Invalid response format")
                
                return result["response"], None, attempt
                
            except requests.Timeout:
                error_msg = f"Timeout after {READ_TIMEOUT}s"
                if attempt < MAX_RETRIES - 1:
                    print(
                        f"⚠️  Versuch {attempt + 1}/{MAX_RETRIES} fehlgeschlagen: "
                        f"{error_msg}. Retry in {RETRY_DELAYS[attempt]}s...",
                        file=sys.stderr
                    )
                    time.sleep(RETRY_DELAYS[attempt])
                else:
                    return None, error_msg, attempt
                    
            except requests.ConnectionError as e:
                error_msg = f"Connection failed: {str(e)}"
                if attempt < MAX_RETRIES - 1:
                    print(
                        f"⚠️  Versuch {attempt + 1}/{MAX_RETRIES} fehlgeschlagen: "
                        f"{error_msg}. Retry in {RETRY_DELAYS[attempt]}s...",
                        file=sys.stderr
                    )
                    time.sleep(RETRY_DELAYS[attempt])
                else:
                    return None, error_msg, attempt
                    
            except (requests.HTTPError, ValueError) as e:
                error_msg = f"{type(e).__name__}: {str(e)}"
                return None, error_msg, attempt
                
            except Exception as e:
                error_msg = f"Unexpected error: {type(e).__name__}: {str(e)}"
                return None, error_msg, attempt
        
        return None, "Max retries exceeded", MAX_RETRIES - 1
