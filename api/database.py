import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL não foi configurada")
     # autocommit=False deixa você controlar o commit na mão (mais seguro)
    conn = psycopg.connect(DATABASE_URL)
    return conn
