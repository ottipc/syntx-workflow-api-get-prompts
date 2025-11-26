"""
GPT-4 Prompt Generator Module
"""

from .syntx_prompt_generator import generate_prompt
from .topics_database import TOPICS

__all__ = ['generate_prompt', 'TOPICS']
