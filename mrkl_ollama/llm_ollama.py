# llm_ollama.py
import requests
from typing import Optional, Dict, Any

class OllamaLLM:
    def __init__(self, model: str = "qwen2.5:7b-instruct", host: str = "http://localhost:11434"):
        self.model = model
        self.host = host.rstrip("/")
        self.gen_url = f"{self.host}/api/generate"

    def generate(self, prompt: str, temperature: float = 0.2, system: Optional[str] = None, stop: Optional[list] = None, max_tokens: int = 512) -> str:
        """
        使用 /api/generate（流式也可，这里用非流式）调用 Ollama。
        """
        payload: Dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "options": {"temperature": temperature},
            "stream": False
        }
        if system:
            payload["system"] = system
        if stop:
            payload["stop"] = stop

        r = requests.post(self.gen_url, json=payload, timeout=120)
        r.raise_for_status()
        data = r.json()
        return data.get("response", "").strip()
