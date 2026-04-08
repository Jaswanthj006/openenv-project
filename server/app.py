from __future__ import annotations

from fastapi import FastAPI
import uvicorn

from routes import router


app = FastAPI()
app.include_router(router)


@app.get("/")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
