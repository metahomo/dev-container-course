import os
import platform

from fastapi import FastAPI

app = FastAPI(title="hello-api")


@app.get("/")
def root():
    return {"message": "안녕하세요, 컨테이너!"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/whoami")
def whoami():
    # 컨테이너 안에서 어떤 사용자로 도는지 확인하려는 용도
    return {"user_id": os.getuid(), "python": platform.python_version()}
