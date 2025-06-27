# llm_agents/ai_reviewer.py
import requests

def ai_reviewer(text):
    print("\nOllama Reviewer: Refining the chapter for clarity and grammar...\n")
    prompt = f"Improve the clarity, grammar, and flow of the following rewritten chapter:\n\n{text}"
    return query_ollama(prompt)

def query_ollama(prompt):
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        })
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        print(" Failed to connect to Ollama. Make sure it's running.")
        raise SystemExit(e)
