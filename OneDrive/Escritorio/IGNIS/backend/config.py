"""Configuration for IGNIS backend."""
import os
import tempfile

# SQLite database path: use IGNIS_DB_PATH env, else temp dir (avoids OneDrive/sandbox disk I/O issues)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if os.environ.get("IGNIS_DB_PATH"):
    DATABASE_PATH = os.environ["IGNIS_DB_PATH"]
else:
    DATABASE_PATH = os.path.join(tempfile.gettempdir(), "ignis.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# API
API_PREFIX = "/api"

# CORS
CORS_ORIGINS = ["*"]  # Allow frontend on different port
