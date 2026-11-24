# 12주 실습. 붓꽃 추론 서비스를 컨테이너로 넘겨주기

작은 ML 추론 서비스(붓꽃 품종 맞히기)를 **Dockerfile → compose.yaml → GitHub Actions → GHCR → 다른 컴퓨터** 순서로 옮겨 봐요. 이 폴더는 **출발점 예시**예요. 그대로 따라 하고, 종합 프로젝트에서는 내 모델·내 API 로 바꿔요.

| 항목 | 내용 |
|---|---|
| 예상 시간 | 3~4시간 (Docker 설치가 되어 있다면) |
| 장소 | WSL(파이썬 단계) + Docker + GitHub |
| CPU/GPU | CPU 만 써요 |
| 데이터·모델 라이선스 | 붓꽃 데이터: R. A. Fisher, [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/53/iris), CC BY 4.0 · scikit-learn: BSD-3-Clause |
| 코드 라이선스 | 이 강좌의 코드 라이선스(저장소 `LICENSE`) |

## 폴더 구성

| 파일 | 하는 일 |
|---|---|
| `train.py` | 붓꽃 150건으로 로지스틱 회귀를 학습해 `model/model.joblib` 저장 (수 초) |
| `app/main.py` | FastAPI. `GET /health`, `POST /predict` |
| `pyproject.toml` | 의존성 (uv). 개발용(pytest)은 `dev` 그룹 |
| `test_app.py` | pytest 5개. 모델을 임시 폴더에 직접 학습해서 써요 |
| `Dockerfile` | 멀티스테이지 + uv + 비root + HEALTHCHECK. 모델은 빌드 중 학습 |
| `compose.yaml` | 앱 1개 + 헬스체크 + 읽기 전용·자원 제한 |
| `ci.yml` | 시험 → 이미지 빌드 → GHCR push. `.github/workflows/ci.yml` 로 복사해 써요 |

## 0단계. 내 저장소로 복사

GitHub 에서 빈 공개 저장소 `iris-service` 를 만들고 clone 한 뒤, 이 폴더의 파일을 **저장소 맨 위**에 복사해요. `ci.yml` 은 `.github/workflows/ci.yml` 로 옮겨요.

```bash
git clone git@github.com:내아이디/iris-service.git
cd iris-service
# (이 폴더의 파일을 복사한 뒤)
mkdir -p .github/workflows && mv ci.yml .github/workflows/ci.yml
ls
```

**이렇게 나오면 성공**

```text
Dockerfile  README.md  app  compose.yaml  pyproject.toml  test_app.py  train.py
```

`compose.yaml` 의 `OWNER` 를 내 GitHub 사용자 이름(소문자)으로 바꿔요.

`.dockerignore` 도 만들어요. 8주에 배운 것에 아래를 더해요. 이게 없으면 `.venv` 와 `.git` 이 이미지로 딸려 들어가요.

```text
.git
.venv
__pycache__
model
.github
```

## 1단계. 학습해 보기 (Docker 없이)

```bash
uv run --no-project --with scikit-learn==1.9.1 python train.py
```

**이렇게 나오면 성공** (처음에는 패키지를 받느라 10여 초 걸려요)

```text
{'accuracy': 0.9667, 'n_train': 120, 'n_test': 30}
저장했어요: model/model.joblib
```

## 2단계. 시험하고 앱 띄우기 (Docker 없이)

의존성을 고정하는 `uv.lock` 을 만들어요. 이 파일도 **커밋**해야 CI 와 Docker 빌드가 같은 버전을 써요.

```bash
uv lock
uv run pytest -q
```

```text
.....                                                                    [100%]
5 passed in 0.58s
```

앱을 띄우고 **다른 터미널**에서 확인해요.

```bash
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000
```

```bash
curl -s localhost:8000/health
curl -s -X POST localhost:8000/predict -H 'content-type: application/json' -d '{"features":[5.1,3.5,1.4,0.2]}'
```

```text
{"status":"ok","model_loaded":true}
{"label":"setosa","probability":0.9784}
```

앱 터미널에서 `Ctrl+C` 로 꺼요. (이 숫자는 이 강좌 저자가 같은 코드로 직접 돌려 얻은 값이에요. 같은 버전이면 같게 나와요.)

## 3단계. 이미지 빌드와 실행 (Docker)

```bash
docker build -t iris-service:dev .
docker run --rm -d --name iris -p 8000:8000 iris-service:dev
docker ps
```

**이렇게 나오면 성공** (모양 예시 — STATUS 칸이 `starting` 에서 `healthy` 로 바뀌어요)

```text
CONTAINER ID   IMAGE              ...   STATUS                    PORTS                    NAMES
3f2a9c1d7e10   iris-service:dev   ...   Up 15 seconds (healthy)   0.0.0.0:8000->8000/tcp   iris
```

```bash
curl -s localhost:8000/health
docker exec iris id          # root 가 아닌지 확인
docker stop iris
```

`id` 결과에 `uid=10001(app)` 이 보이면 비root 로 도는 거예요.

## 4단계. Compose 로 띄우기

```bash
docker compose up --build -d
docker compose ps
curl -s localhost:8000/health
docker compose down
```

`docker compose ps` 의 STATUS 에 `(healthy)` 가 보이면 성공이에요. 8000 번 포트가 이미 쓰이고 있으면 `HOST_PORT=8080 docker compose up -d` 처럼 바꿔요.

## 5단계. GitHub Actions 로 자동 빌드·push

```bash
git add .
git commit -m "ML 추론 서비스 첫 버전"
git push origin main
```

저장소의 **Actions** 탭에서 `test` → `image` 작업이 초록색이 되는지 봐요. 끝나면 저장소 오른쪽 **Packages** 에 `iris-service` 가 생겨요. 태그는 `sha-` 로 시작하는 7자리 커밋 해시예요.

버전 태그를 달면 `1.0.0` 같은 태그도 붙어요.

```bash
git tag v1.0.0 && git push origin v1.0.0
```

!!! warning "GHCR 패키지는 처음엔 비공개예요"
    GitHub 문서: 처음 올린 패키지의 기본 공개 범위는 private 이에요. 다른 사람이 로그인 없이 받게 하려면 GitHub 의 패키지 설정(Package settings)에서 공개로 바꿔야 해요. 공개로 바꾸기 전에 이미지에 비밀값이 없는지 한 번 더 확인해요.

## 6단계. 다른 컴퓨터에서 받아 실행

다른 컴퓨터(친구 PC, Codespaces, Killercoda 등)에서 Docker 가 되는 터미널을 열어요. 태그 `sha-abc1234` 는 내 것으로 바꿔요.

```bash
docker pull ghcr.io/내아이디/iris-service:sha-abc1234
docker run --rm -d --name iris -p 8000:8000 ghcr.io/내아이디/iris-service:sha-abc1234
curl -s localhost:8000/health
docker stop iris
```

패키지가 비공개이면 먼저 로그인해요 (읽기 권한 `read:packages` 토큰).

```bash
echo $CR_PAT | docker login ghcr.io -u 내아이디 --password-stdin
```

저장소 전체를 clone 한 컴퓨터라면 Compose 로도 돼요. `--no-build` 는 "빌드하지 말고 받은 이미지를 써" 라는 뜻이에요.

```bash
IMAGE_TAG=sha-abc1234 docker compose pull
IMAGE_TAG=sha-abc1234 docker compose up -d --no-build
docker compose ps
docker compose down
```

## 막히면

| 증상 | 원인 | 해결 |
|---|---|---|
| 빌드가 `uv.lock` 이 없다고 실패 | 2단계의 `uv lock` 을 안 했거나 커밋하지 않음 | `uv lock` 후 `git add uv.lock` |
| `unauthorized` / `denied` 로 push 실패 | `packages: write` 권한 없음 또는 Actions 쓰기 권한 막힘 | `ci.yml` 의 `permissions` 확인. 저장소 설정의 Actions 권한 확인 |
| 다른 PC 에서 `pull access denied` | 패키지가 비공개 | 공개로 바꾸거나 `docker login ghcr.io` |
| `unhealthy` 로 표시 | 모델 파일이 없거나 앱이 죽음 | `docker logs iris` 로 오류 확인. `MODEL_PATH` 확인 |
| `read-only file system` 오류 | `read_only: true` 인데 앱이 파일을 쓰려 함 | 쓰는 경로를 `tmpfs` 나 볼륨으로 열어 줘요 |
| `port is already allocated` | 호스트 포트 사용 중 | `HOST_PORT=8080` 처럼 다른 번호 |

## 직접 실행하지 못한 부분

이 폴더를 만든 서버에는 Docker 가 없어서 `Dockerfile`·`compose.yaml` 은 **문법·규칙 점검**만 했고, `ci.yml` 은 YAML 파싱과 공식 문서(Action 입력 이름) 대조만 했어요. 파이썬 쪽(학습·pytest·앱 응답)은 실제로 돌려 확인했어요. 3~6단계에서 이 글과 다르게 나오면 이슈로 알려 주세요.
