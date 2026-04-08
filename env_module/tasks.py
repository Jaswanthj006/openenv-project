from typing import Dict, List, TypedDict


class TaskData(TypedDict):
    query: str
    expected_category: str
    expected_keywords: List[str]
    difficulty: str


def easy_task() -> TaskData:
    """Easy task: classify query category."""
    return {
        "query": "How do I reset my password?",
        "expected_category": "technical",
        "expected_keywords": ["technical"],
        "difficulty": "easy",
    }


def medium_task() -> TaskData:
    """Medium task: short reply containing key support terms."""
    return {
        "query": "I was charged twice for my subscription.",
        "expected_category": "billing",
        "expected_keywords": ["sorry", "refund"],
        "difficulty": "medium",
    }


def hard_task() -> TaskData:
    """Hard task: complete, empathetic customer support response."""
    return {
        "query": "My order hasn't arrived and I'm worried.",
        "expected_category": "general",
        "expected_keywords": ["track", "investigate", "support"],
        "difficulty": "hard",
    }


def all_tasks() -> Dict[str, TaskData]:
    """Return all tasks by difficulty key."""
    return {
        "easy": easy_task(),
        "medium": medium_task(),
        "hard": hard_task(),
    }
