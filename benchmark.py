
import requests
import json
import time
import psutil
from datetime import datetime

MODELS = ["tinyllama", "phi","gemma:2b"]  # Add third model later
API_URL = "http://localhost:11434/api/generate"

# Load prompts
with open("test_prompts.json", "r") as f:
    prompts = json.load(f)

results = []

for model in MODELS:
    print(f"\nRunning model: {model}")
    
    for item in prompts:
        prompt_id = item["id"]
        category = item["category"]
        prompt_text = item["prompt"]

        payload = {
            "model": model,
            "prompt": prompt_text,
            "stream": False
        }

        start_time = time.time()
        response = requests.post(API_URL, json=payload)
        end_time = time.time()

        latency = round(end_time - start_time, 3)
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent

        output_text = response.json().get("response", "")
        response_length = len(output_text)

        result_entry = {
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "prompt_id": prompt_id,
            "category": category,
            "latency_seconds": latency,
            "cpu_percent": cpu,
            "ram_percent": ram,
            "response_length": response_length,
            "response": output_text
        }

        results.append(result_entry)

        print(f"{model} | Prompt {prompt_id} | {latency}s | CPU: {cpu}% | RAM: {ram}%")

# Save results
with open("results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nEvaluation complete. Results saved to results.json")