# llm_agents/ai_writer.py
import requests

def ai_writer(text):
    print("\n Ollama Writer: Spinning the chapter...\n")
    prompt = f"Rewrite this chapter in simpler, modern English while keeping the original meaning:\n\n{text}"
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
        print("Failed to connect to Ollama. Make sure it's running.")
        raise SystemExit(e)
