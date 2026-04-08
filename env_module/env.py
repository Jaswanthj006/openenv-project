import random
from typing import Any, Dict, Tuple

from env_module.actions import MyEnvV4Action
from env_module.observation import MyEnvObservation
from env_module.reward import compute_reward
from env_module.tasks import all_tasks


class MyEnvV4Env:
    """
    OpenEnv-compatible customer support automation environment.

    This is a single-step environment:
    - reset() selects one task and returns the initial observation.
    - step() grades the submitted action and terminates the episode.
    """

    def __init__(self) -> None:
        self._tasks = all_tasks()
        self._ordered_difficulties = ("easy", "medium", "hard")
        self._current_task: Dict[str, Any] | None = None
        self._last_reward: float = 0.0
        self._done: bool = False

    def _next_task(self) -> Dict[str, Any]:
        """
        Select a random task difficulty.

        Randomness is only used for task selection.
        """
        difficulty = random.choice(self._ordered_difficulties)
        return self._tasks[difficulty]

    def _build_observation(self) -> MyEnvObservation:
        if self._current_task is None:
            raise RuntimeError("Environment not initialized. Call reset() first.")
        return MyEnvObservation(
            query=self._current_task["query"],
            expected_category=self._current_task["expected_category"],
            expected_keywords=self._current_task["expected_keywords"],
            difficulty=self._current_task["difficulty"],
        )

    async def reset(self) -> Tuple[MyEnvObservation, float, bool]:
        """
        Reset environment state and return initial timestep data.

        Returns:
            (observation, reward, done)
        """
        self._current_task = self._next_task()
        self._last_reward = 0.0
        self._done = False
        return self._build_observation(), 0.0, False

    async def step(self, action: MyEnvV4Action) -> Tuple[MyEnvObservation, float, bool]:
        """
        Evaluate agent action for the current task.

        Returns:
            (observation, reward, done)
        """
        if self._current_task is None:
            raise RuntimeError("Environment not initialized. Call reset() first.")
        if self._done:
            raise RuntimeError("Episode already finished. Call reset() for a new task.")

        reward = compute_reward(
            difficulty=self._current_task["difficulty"],
            action_message=action.message,
            expected_category=self._current_task["expected_category"],
            expected_keywords=self._current_task["expected_keywords"],
        )
        self._last_reward = reward
        self._done = True
        return self._build_observation(), reward, True

    async def state(self) -> Dict[str, Any]:
        """Return current environment state for orchestration/debugging."""
        observation = self._build_observation() if self._current_task is not None else None
        return {
            "observation": observation,
            "reward": self._last_reward,
            "done": self._done,
            "has_active_task": self._current_task is not None,
        }

    @classmethod
    async def from_docker_image(cls, image_name: str) -> "MyEnvV4Env":
        """Create environment instance from image identifier."""
        _ = image_name
        return cls()

    async def close(self) -> None:
        """Close environment resources."""
        return None
