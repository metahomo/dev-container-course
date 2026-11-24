import os

import psycopg
from fastapi import FastAPI, HTTPException

app = FastAPI(title="hit-counter")

# 접속 정보는 코드가 아니라 환경 변수에서 읽어요 (9주차)
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "app")
DB_USER = os.environ.get("DB_USER", "app")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")


def connect():
    return psycopg.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
        connect_timeout=3,
    )


@app.get("/health")
def health():
    # DB 없이도 "앱이 떠 있는지"만 알려줘요
    return {"status": "ok"}


@app.get("/hits")
def hits():
    """부를 때마다 횟수를 1 올리고, 지금 횟수를 돌려줘요."""
    try:
        with connect() as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS hits (id int PRIMARY KEY, n int NOT NULL)"
            )
            conn.execute(
                "INSERT INTO hits (id, n) VALUES (1, 1) "
                "ON CONFLICT (id) DO UPDATE SET n = hits.n + 1"
            )
            n = conn.execute("SELECT n FROM hits WHERE id = 1").fetchone()[0]
    except psycopg.OperationalError as e:
        raise HTTPException(status_code=503, detail=f"DB 에 연결하지 못했어요: {e}")
    return {"hits": n}
