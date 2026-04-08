from __future__ import annotations

import asyncio
import os
from typing import List, Optional

from openai import OpenAI

from env_module.actions import MyEnvV4Action
from env_module.env import MyEnvV4Env


MAX_STEPS = 5
TEMPERATURE = 0.7
MAX_TOKENS = 120
SUCCESS_SCORE_THRESHOLD = 0.3


def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}")


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    safe_action = action.replace("\n", " ").strip()
    error_value = "null" if error is None else error.replace("\n", " ").strip()
    print(
        f"[STEP]  step={step} action={safe_action} reward={reward:.2f} "
        f"done={str(done).lower()} error={error_value}"
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    clamped_score = max(0.0, min(1.0, score))
    reward_text = ",".join(f"{value:.2f}" for value in rewards)
    print(
        f"[END]   success={str(success).lower()} steps={steps} "
        f"score={clamped_score:.2f} rewards={reward_text}"
    )


def build_prompt(step: int, observation: object) -> str:
    query = getattr(observation, "query", "")
    difficulty = getattr(observation, "difficulty", "")
    return (
        "You are a customer support agent.\n"
        "Provide one concise message that includes both:\n"
        "1) A category classification label from: billing, technical, general.\n"
        "2) A helpful customer-facing reply.\n"
        f"Current step: {step}\n"
        f"Difficulty: {difficulty}\n"
        f"Customer query: {query}\n"
        "Respond with plain text only."
    )


def get_model_response(client: OpenAI, prompt: str) -> str:
    try:
        completion = client.chat.completions.create(
            model=os.environ["MODEL_NAME"],
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a customer support assistant. "
                        "Always provide a helpful response and include "
                        "classification and reply in one message."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
        text = completion.choices[0].message.content
        if text is None:
            return "hello"
        return text.strip()
    except Exception:
        return "hello"


def _normalize_result(result: object) -> object:
    if isinstance(result, tuple) and len(result) == 3:
        observation, reward, done = result

        class ResultObject:
            def __init__(self, obs: object, rew: float, is_done: bool) -> None:
                self.observation = obs
                self.reward = rew
                self.done = is_done

        return ResultObject(observation, float(reward), bool(done))
    return result


async def main() -> None:
    rewards: List[float] = []
    history: List[str] = []
    steps_taken = 0
    success = False
    score = 0.0
    env_instance: Optional[MyEnvV4Env] = None
    started = False

    try:
        client = OpenAI(
            base_url=os.environ["API_BASE_URL"],
            api_key=os.environ["API_KEY"],
        )

        env_instance = await MyEnvV4Env.from_docker_image(os.environ["IMAGE_NAME"])

        task_name = "customer_support_automation"
        benchmark_name = "openenv"
        model_name = os.environ["MODEL_NAME"]
        log_start(task=task_name, env=benchmark_name, model=model_name)
        started = True

        result = _normalize_result(await env_instance.reset())

        for step in range(1, MAX_STEPS + 1):
            if bool(getattr(result, "done", False)):
                break

            observation = getattr(result, "observation", None)
            prompt = build_prompt(step=step, observation=observation)
            action_text = get_model_response(client=client, prompt=prompt)

            action = MyEnvV4Action(message=action_text)

            error_message: Optional[str] = None
            try:
                result = _normalize_result(await env_instance.step(action))
                reward_value = getattr(result, "reward", 0.0)
                reward = float(reward_value) if reward_value is not None else 0.0
                done = bool(getattr(result, "done", False))
            except Exception as exc:
                reward = 0.0
                done = True
                error_message = str(exc)

            rewards.append(reward)
            history.append(action_text)
            steps_taken = step

            log_step(
                step=step,
                action=action_text,
                reward=reward,
                done=done,
                error=error_message,
            )

            if done:
                break

        score = sum(rewards) / (MAX_STEPS * 1.0)
        score = max(0.0, min(1.0, score))
        success = score >= SUCCESS_SCORE_THRESHOLD
    except Exception:
        success = False
    finally:
        if env_instance is not None:
            try:
                await env_instance.close()
            except Exception:
                pass

        if not started:
            try:
                log_start(
                    task="customer_support_automation",
                    env="openenv",
                    model=os.environ["MODEL_NAME"],
                )
            except Exception:
                pass

        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception:
        log_end(success=False, steps=0, score=0.0, rewards=[])
