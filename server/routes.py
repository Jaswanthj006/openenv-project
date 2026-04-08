from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from container import get_env
from env_module.actions import MyEnvV4Action


router = APIRouter()


def _to_dict(value: Any) -> Any:
    if value is None:
        return None
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if hasattr(value, "dict"):
        return value.dict()
    return value


def _normalize_step_result(result: Any) -> Dict[str, Any]:
    """
    Normalize env output from either tuple-form or object-form:
    - (observation, reward, done)
    - object with observation/reward/done attributes
    """
    if isinstance(result, tuple) and len(result) == 3:
        observation, reward, done = result
    else:
        observation = getattr(result, "observation")
        reward = getattr(result, "reward")
        done = getattr(result, "done")

    return {
        "observation": _to_dict(observation),
        "reward": float(reward),
        "done": bool(done),
    }


@router.post("/reset")
async def reset_endpoint() -> JSONResponse:
    try:
        env = await get_env()
        result = await env.reset()
        payload = _normalize_step_result(result)
        return JSONResponse(content=payload, status_code=200)
    except Exception as exc:
        return JSONResponse(content={"error": str(exc)}, status_code=200)


@router.post("/step")
async def step_endpoint(body: Dict[str, Any]) -> JSONResponse:
    try:
        env = await get_env()
        action = MyEnvV4Action(**body)
        result = await env.step(action)
        payload = _normalize_step_result(result)
        return JSONResponse(content=payload, status_code=200)
    except Exception as exc:
        return JSONResponse(content={"error": str(exc)}, status_code=200)


@router.get("/state")
async def state_endpoint() -> JSONResponse:
    try:
        env = await get_env()
        state = await env.state()
        return JSONResponse(content={"state": _to_dict(state)}, status_code=200)
    except Exception as exc:
        return JSONResponse(content={"error": str(exc)}, status_code=200)
