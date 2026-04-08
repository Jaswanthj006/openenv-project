# Customer Support OpenEnv

## Project Overview
Customer Support OpenEnv is a benchmark-ready OpenEnv project designed for hackathon validation and deployment. It simulates real-world customer support workflows and exposes the environment through a lightweight API for evaluation and agent interaction.

## Objective
Build and evaluate an agent that can handle customer support requests across increasing difficulty levels by:
- Classifying user intent
- Producing concise and relevant support replies
- Generating complete, polite, and solution-oriented responses

## Environment Design
The environment is a single-step task environment focused on practical support interactions.  
Each episode:
1. `reset()` selects a task (`easy`, `medium`, or `hard`)
2. Agent submits one action via `step()`
3. Environment returns reward and marks episode complete

The design is deterministic for grading, with normalized reward scoring in `[0.0, 1.0]`.

## Action Space
The agent action payload:

```json
{
  "message": "string"
}
```

## Observation Space
The environment observation schema:

```json
{
  "query": "string",
  "expected_category": "string | null",
  "expected_keywords": ["string"] | null,
  "difficulty": "string"
}
```

Equivalent structure:

```python
{
  "query": str,
  "expected_category": Optional[str],
  "expected_keywords": Optional[List[str]],
  "difficulty": str
}
```

## Task Descriptions

### Easy
- Goal: classify the user query category
- Expected categories: `billing`, `technical`, `general`
- Example behavior: return the correct category label

### Medium
- Goal: generate a short, appropriate customer support reply
- Grading focuses on required support keywords

### Hard
- Goal: generate a high-quality complete response
- Must include:
  - Greeting
  - Solution guidance
  - Polite closing

## Reward Logic

### Easy
- Exact category match:
  - Match -> `1.0`
  - No match -> `0.0`

### Medium
- Keyword overlap ratio:
  - `matched_keywords / total_expected_keywords`
- Partial credit supported

### Hard
Weighted structure-based scoring:
- Greeting present -> `+0.3`
- Solution keywords present -> up to `+0.4`
- Polite closing present -> `+0.3`

Final hard reward is clamped to `[0.0, 1.0]`.

## Project Structure

```text
env_module/
server/
inference/
configs/
```

Suggested high-level contents:
- `env_module/`: environment logic, tasks, observations, actions, reward graders
- `server/`: FastAPI endpoints (`/reset`, `/step`, `/state`)
- `inference/`: validator-facing inference runner
- `configs/`: constants, prompts, and runtime settings accessors

## Setup Instructions

### 1) Install dependencies
```bash
pip3 install -r requirements.txt
```

### 2) Start API server
```bash
uvicorn server.app:app --host 0.0.0.0 --port 7860
```

## API Testing Instructions

### Health check
```bash
curl http://localhost:7860/
```

### Reset endpoint (required validator check)
```bash
curl -X POST http://localhost:7860/reset
```

### Step endpoint
```bash
curl -X POST http://localhost:7860/step \
  -H "Content-Type: application/json" \
  -d '{"message":"technical"}'
```

### State endpoint
```bash
curl http://localhost:7860/state
```

## Inference
The inference module is validator-oriented and:
- Uses the OpenAI client through a proxy-compatible `base_url`
- Interacts with the environment via OpenEnv-style runtime methods
- Produces strict run logs:
  - `[START] ...`
  - `[STEP] ...`
  - `[END] ...`
- Always emits `[END]` even when errors occur

## Environment Variables
Set the following variables before running inference:

- `API_BASE_URL`
- `API_KEY`
- `MODEL_NAME`
- `IMAGE_NAME`

These are required runtime values and should be provided by your execution environment (local, CI, or HF Space).

## Evaluation Criteria
Project evaluation is based on:
- Endpoint correctness and API stability
- Deterministic reward behavior
- Reward normalization (`0.0` to `1.0`)
- Partial reward support
- Task coverage (`easy`, `medium`, `hard`)
- Inference log format compliance
- Clean modular separation (env/server/inference/configs)

## Deployment
This project is structured for Docker and Hugging Face Spaces style deployment:
- FastAPI server exposed on port `7860`
- Root-level dependency file (`requirements.txt`)
- Root metadata (`openenv.yaml`)
- Runtime-ready entrypoint via `server/app.py`

## Compliance Checklist
- [x] Real-world environment scenario (customer support)
- [x] Three task levels: easy, medium, hard
- [x] Typed action and observation models
- [x] Deterministic graders (no random grading)
- [x] Partial reward implemented
- [x] Rewards normalized to `[0.0, 1.0]`
- [x] HTTP API endpoints: `POST /reset`, `POST /step`, `GET /state`
- [x] `/reset` returns HTTP 200
- [x] Inference uses OpenAI client via proxy settings
- [x] Inference outputs `[START]`, `[STEP]`, `[END]`
- [x] Configuration centralized under `configs/`
