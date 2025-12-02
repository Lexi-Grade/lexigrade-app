import os
import dotenv


class Settings:
    def __init__(self):
        dotenv.load_dotenv()
        self.models_service_url = os.getenv('MODELS_SERVICE_URL')
        self.hf_repo_spanish_url = os.getenv('HF_REPO_SPANISH_URL')
        self.hf_repo_english_url = os.getenv('HF_REPO_ENGLISH_URL')
        self.datasets_base_path = os.getenv('DATASETS_BASE_PATH')
settings = Settings()