# ---------- 1단계: 만드는 곳 (builder) ----------
# 파이썬 베이스 이미지는 태그만이 아니라 다이제스트(@sha256:...)로 고정하면 더 안전해요 (11주 참고).
FROM python:3.13-slim AS builder

# uv 바이너리를 버전을 박아서 가져와요. (latest 를 쓰지 않아요)
COPY --from=ghcr.io/astral-sh/uv:0.13.9 /uv /uvx /bin/

# UV_COMPILE_BYTECODE: 파이썬 바이트코드를 미리 만들어 시작을 빠르게
# UV_LINK_MODE=copy:   캐시와 대상이 다른 파일시스템일 때 나는 경고를 없애요
# UV_PYTHON_DOWNLOADS=0: 이미지에 이미 있는 파이썬만 써요 (두 단계가 같은 파이썬)
# UV_NO_DEV=1:         개발용 패키지(pytest 등)는 설치하지 않아요
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0 \
    UV_NO_DEV=1

WORKDIR /app

# 의존성만 먼저 설치 -> 소스가 바뀌어도 이 층은 캐시를 재사용해요
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

# 모델은 빌드할 때 학습해서 이미지 안에 넣어요 (수 초). 같은 코드 -> 같은 모델.
COPY train.py ./
RUN .venv/bin/python train.py /app/model

# ---------- 2단계: 실행하는 곳 (final) ----------
FROM python:3.13-slim

# root 가 아닌 사용자로 실행해요
RUN useradd --system --uid 10001 --user-group --no-create-home app

WORKDIR /app
# 만드는 곳에서 "결과물"만 가져와요: 가상환경과 모델. 빌드 도구와 캐시는 안 따라와요.
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/model /app/model
COPY app ./app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MODEL_PATH=/app/model/model.joblib

USER app
EXPOSE 8000

# 슬림 이미지에는 curl 이 없어서 파이썬으로 /health 를 확인해요.
# 200 이 아니면 예외가 나서 "unhealthy" 가 돼요.
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
