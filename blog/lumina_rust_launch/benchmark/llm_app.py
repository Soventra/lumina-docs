import os
os.environ.pop("DATABASE_URL", None)
os.environ["LUMINA_LOCAL_MODEL_COST_MAP"] = "True"

from fastapi import FastAPI, Request
import lumina
import uvicorn

lumina.suppress_debug_info = True
lumina.telemetry = False

app = FastAPI()


@app.post("/v1/chat/completions")
async def chat(req: Request):
    body = await req.json()
    resp = await lumina.acompletion(
        model="openai/mock",
        messages=body["messages"],
        api_base="http://127.0.0.1:9001/v1",
        api_key="sk-mock",
        num_retries=0,
    )
    return resp.model_dump()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9002, log_level="warning")
