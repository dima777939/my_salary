from os import environ
from pathlib import Path
from dotenv import load_dotenv


from databases import Database
from sqlalchemy.orm import declarative_base


env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


DB_USER = environ.get("POSTGRES_USER", "user_db")
DB_PASSWORD = environ.get("POSTGRES_PASSWORD", "userpassword")
DB_HOST = environ.get("POSTGRES_HOST", "db")
DB_NAME = environ.get("POSTGRES_DB", "database")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"


Base = declarative_base()

database = Database(DATABASE_URL)
