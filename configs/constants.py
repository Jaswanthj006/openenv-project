"""Project-wide fixed constants for the OpenEnv hackathon modules."""

from typing import List


TASK_NAME: str = "customer_support"
BENCHMARK_NAME: str = "my_env_v4"

MAX_STEPS: int = 5
SUCCESS_SCORE_THRESHOLD: float = 0.3

DEFAULT_TEMPERATURE: float = 0.7
DEFAULT_MAX_TOKENS: int = 120

VALID_CATEGORIES: List[str] = ["billing", "technical", "general"]

GREETING_KEYWORDS: List[str] = ["hello", "hi", "dear"]
CLOSING_KEYWORDS: List[str] = ["thank you", "thanks", "regards"]
