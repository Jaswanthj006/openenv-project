from typing import List, Optional

from pydantic import BaseModel, Field


class MyEnvObservation(BaseModel):
    """Observation returned by the environment."""

    query: str = Field(..., min_length=1)
    expected_category: Optional[str] = None
    expected_keywords: Optional[List[str]] = None
    difficulty: str = Field(..., min_length=1)
