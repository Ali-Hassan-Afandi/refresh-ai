from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.config import settings
app=FastAPI(title="ReFresh AI API",version="1.0.0")
app.add_middleware(CORSMiddleware,allow_origins=list(dict.fromkeys([settings.frontend_origin,"http://localhost:3000"])),allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(router)
@app.get("/")
def root(): return {"service":"ReFresh AI API","docs":"/docs"}
@app.get("/health")
def health(): return {"status":"ok","service":"refresh-ai-api","model_provider":"groq-online"}
