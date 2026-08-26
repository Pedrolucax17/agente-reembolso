import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

def get_database_url() -> str:
    user = os.getenv("DB_USER")
    pwd = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    if not all([user, pwd, host, port, db_name]):
        raise SystemExit("Please set environment variables")
    sslmode = os.getenv("DB_SSLMODE")
    return f"postgresql://{user}:{pwd}@{host}:{port}/{db_name}?sslmode={sslmode}"

def main():
    sql_dir = BASE_DIR / "sql"

    sql_files = sorted(sql_dir.glob("*.sql"))

    if not sql_files:
        print("Nenhum arquivo .sql encontrado")
        return

    database_url = get_database_url()

    print(f"Encontrados {len(sql_files)} scripts SQL.")

    with psycopg.connect(database_url) as conn:
        for sql_file in sql_files:
            print(f"Executando {sql_file.name}")

            sql = sql_file.read_text(encoding="utf-8")

            conn.execute(sql)

    print("Banco inicializado com sucesso")

if __name__ == "__main__":
    main()