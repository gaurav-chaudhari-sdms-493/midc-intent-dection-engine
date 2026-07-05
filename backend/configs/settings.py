import os
from dotenv import load_dotenv

load_dotenv()

# Project
PROJECT_NAME = os.getenv("PROJECT_NAME")
ENVIRONMENT = os.getenv("ENVIRONMENT")

# FastAPI
BACKEND_HOST = os.getenv("BACKEND_HOST")
BACKEND_PORT = int(os.getenv("BACKEND_PORT"))

# PostgreSQL
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# Redis
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))

# MinIO
MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER")
MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD")

# Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
OLLAMA_DEFAULT_MODEL = os.getenv("OLLAMA_DEFAULT_MODEL")

# n8n
N8N_PORT = int(os.getenv("N8N_PORT"))
N8N_BASIC_AUTH_ACTIVE = os.getenv("N8N_BASIC_AUTH_ACTIVE")

# JWT
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES"))

# CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS")
