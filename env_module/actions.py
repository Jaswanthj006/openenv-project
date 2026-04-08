from pydantic import BaseModel, Field


class MyEnvAction(BaseModel):
    """Action payload submitted by an agent for a single environment step."""

    message: str = Field(..., min_length=1, description="Agent output text")


class MyEnvV4Action(MyEnvAction):
    """Alias model for OpenEnv validator compatibility."""
