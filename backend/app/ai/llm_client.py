import os

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY")

    def enabled(self) -> bool:
        return bool(self.api_key)

    def complete(self, prompt: str) -> str:
        raise NotImplementedError("Plug in provider-specific logic")
