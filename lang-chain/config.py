import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("openai_api_key")
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    MODEL_NAME = "gpt-3.5-turbo"
    TEMPERATURE = 0
    VECTOR_DB_PATH = "vectorstore"
    MAX_CONTEXT_TOKENS = 4000
    ALLOWED_EXTENSIONS = {'pdf', 'txt'}