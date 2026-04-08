from __future__ import annotations

from typing import Optional

from env_module.env import MyEnvV4Env


env: Optional[MyEnvV4Env] = None


async def get_env() -> MyEnvV4Env:
    """Return a singleton environment instance."""
    global env
    if env is None:
        env = MyEnvV4Env()
    return env
