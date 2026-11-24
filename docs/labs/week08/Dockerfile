# 8주차 실습: uv 공식 Docker 가이드 방식의 한 단계(single-stage) 이미지
FROM python:3.13-slim-trixie

# uv 실행 파일만 공식 이미지에서 복사 (버전 고정)
COPY --from=ghcr.io/astral-sh/uv:0.13.9 /uv /uvx /bin/

WORKDIR /app

# 바이트코드 미리 만들기, 캐시와 대상이 다른 파일시스템이어도 경고 없이 복사
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# 1) 의존성만 먼저 설치: pyproject.toml / uv.lock 이 안 바뀌면 이 층은 캐시를 재사용해요
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# 2) 내 소스는 나중에 복사: 코드만 바뀌면 여기부터 다시 만들어요
COPY app ./app

# 가상환경의 실행 파일을 PATH 맨 앞에
ENV PATH="/app/.venv/bin:$PATH"

# root 가 아닌 사용자로 실행
RUN useradd --create-home --uid 1000 appuser
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
