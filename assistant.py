import yaml
from memory import Memory
import os
import openai

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not set in environment variables.")
openai.api_key = openai_api_key

class Assistant:
    def __init__(self, config_path="config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        self.memory = Memory(self.config["memory"]["persist_directory"])
        self.provider = self.config["llm"]["provider"]

        if self.provider == "openai":
            import openai
            openai.api_key = self.config["llm"]["api_key"]
            self.openai = openai
        elif self.provider == "ollama":
            import requests
            self.requests = requests

    def _call_openai(self, prompt):
        response = self.openai.ChatCompletion.create(
            model=self.config["llm"]["model"],
            messages=[
                {"role": "system", "content": self.config["personality"]["system_prompt"]},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message["content"]

    def _call_ollama(self, prompt):
        url = "http://localhost:11434/api/chat"
        payload = {
            "model": self.config["llm"]["model"],
            "messages": [
                {"role": "system", "content": self.config["personality"]["system_prompt"]},
                {"role": "user", "content": prompt}
            ]
        }
        resp = self.requests.post(url, json=payload)
        return resp.json()["message"]["content"]

    def chat(self, user_input):
        past_contexts = self.memory.search(user_input)
        context_text = "\n".join([doc for docs in past_contexts for doc in docs])

        prompt = f"Relevant past context:\n{context_text}\n\nUser: {user_input}"
        ai_response = self._call_openai(prompt) if self.provider == "openai" else self._call_ollama(prompt)

        self.memory.add(user_input, ai_response)
        return ai_response
