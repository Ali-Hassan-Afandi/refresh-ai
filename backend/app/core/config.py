from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    groq_api_key: str = ""
    groq_model: str = "openai/gpt-oss-20b"
    supabase_url: str = ""
    supabase_service_role_key: str = ""
    frontend_origin: str = "http://localhost:3000"
    demo_fallback: bool = True
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
settings = Settings()
