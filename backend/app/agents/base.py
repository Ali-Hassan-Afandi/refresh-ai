import json
from groq import Groq
from app.core.config import settings
class GroqAgent:
    def __init__(self,role:str):
        self.role=role; self.client=Groq(api_key=settings.groq_api_key) if settings.groq_api_key else None
    def json_call(self,instruction:str)->dict:
        if not self.client: raise RuntimeError("GROQ_API_KEY is missing")
        r=self.client.chat.completions.create(
          model=settings.groq_model,temperature=.2,max_completion_tokens=220,
          response_format={"type":"json_object"},
          messages=[{"role":"user","content":f"You are ReFresh AI's {self.role}. Return JSON only. Do not reveal chain-of-thought. {instruction}"}])
        return json.loads(r.choices[0].message.content or "{}")
