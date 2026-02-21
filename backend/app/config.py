from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Alcohol Label Verifier"
    max_file_size_mb: int = 10
    max_files: int = 10
    tesseract_cmd: str = "tesseract"

    class Config:
        env_file = ".env"


settings = Settings()
