"""Centralized prompts for customer support generation."""


SYSTEM_PROMPT: str = (
    "You are a customer support assistant. "
    "Classify each user query and provide a helpful response. "
    "Maintain a polite, professional, and concise tone."
)


def build_user_prompt(query: str, difficulty: str) -> str:
    """Build the user prompt from query context and difficulty."""
    return (
        f"User query: {query}\n"
        f"Difficulty: {difficulty}\n"
        "Provide a clear and helpful response"
    )
