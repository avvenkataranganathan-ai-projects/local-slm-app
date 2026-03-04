from fastapi import FastAPI
from pydantic import BaseModel
import requests
import time

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/generate"

class PromptRequest(BaseModel):
    prompt: str
    model: str = "tinyllama"

@app.post("/generate")
def generate(request: PromptRequest):
    start = time.time()

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": request.model,
            "prompt": request.prompt,
            "stream": False
        }
    )

    end = time.time()

    return {
        "model": request.model,
        "latency_seconds": round(end - start, 2),
        "output": response.json().get("response", "")
    }