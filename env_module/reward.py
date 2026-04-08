from typing import Iterable, List


def normalize_text(value: str) -> str:
    """Normalize text for deterministic comparisons."""
    return value.strip().lower()


def _contains_any(text: str, terms: Iterable[str]) -> bool:
    normalized_text = normalize_text(text)
    return any(term in normalized_text for term in terms)


def grade_easy(action_message: str, expected_category: str) -> float:
    """
    Easy grading: exact category match.

    Reward:
    - 1.0 if predicted category equals expected category
    - 0.0 otherwise
    """
    predicted = normalize_text(action_message)
    expected = normalize_text(expected_category)
    return 1.0 if predicted == expected else 0.0


def grade_medium(action_message: str, expected_keywords: List[str]) -> float:
    """
    Medium grading: proportion of expected keywords present in reply.

    Reward:
    - matched_keywords / total_keywords
    """
    if not expected_keywords:
        return 0.0

    normalized_message = normalize_text(action_message)
    normalized_keywords = [normalize_text(keyword) for keyword in expected_keywords]
    matched = sum(1 for keyword in normalized_keywords if keyword in normalized_message)
    reward = matched / len(normalized_keywords)
    return max(0.0, min(1.0, reward))


def grade_hard(action_message: str, solution_keywords: List[str]) -> float:
    """
    Hard grading:
    - greeting present: +0.3
    - solution keywords present: +0.4 (scaled by match proportion)
    - polite closing present: +0.3
    """
    normalized_message = normalize_text(action_message)
    reward = 0.0

    greeting_terms = ("hello", "hi", "dear", "good morning", "good afternoon")
    closing_terms = ("thank you", "thanks", "best regards", "sincerely", "have a great day")

    if _contains_any(normalized_message, greeting_terms):
        reward += 0.3

    if solution_keywords:
        normalized_keywords = [normalize_text(keyword) for keyword in solution_keywords]
        matched = sum(1 for keyword in normalized_keywords if keyword in normalized_message)
        reward += 0.4 * (matched / len(normalized_keywords))

    if _contains_any(normalized_message, closing_terms):
        reward += 0.3

    return max(0.0, min(1.0, reward))


def compute_reward(difficulty: str, action_message: str, expected_category: str, expected_keywords: List[str]) -> float:
    """Dispatch deterministic grader by difficulty."""
    normalized_difficulty = normalize_text(difficulty)

    if normalized_difficulty == "easy":
        return grade_easy(action_message=action_message, expected_category=expected_category)
    if normalized_difficulty == "medium":
        return grade_medium(action_message=action_message, expected_keywords=expected_keywords)
    if normalized_difficulty == "hard":
        return grade_hard(action_message=action_message, solution_keywords=expected_keywords)
    return 0.0
