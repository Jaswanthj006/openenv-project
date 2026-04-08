"""Environment settings accessors for runtime configuration."""

import os


def get_api_base_url() -> str:
    """Return API base URL from environment."""
    return os.environ["API_BASE_URL"]


def get_api_key() -> str:
    """Return API key from environment."""
    return os.environ["API_KEY"]


def get_model_name() -> str:
    """Return model name from environment."""
    return os.environ["MODEL_NAME"]


def get_image_name() -> str:
    """Return docker image name from environment."""
    return os.environ["IMAGE_NAME"]
