from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GROQ_API_KEY: str
    PINECONE_API_KEY: str
    MONGODB_URI: str
    GROQ_MODEL: str = "openai/gpt-oss-20b"
    PINECONE_INDEX_NAME: str = "rag-research-assistant-bge"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()