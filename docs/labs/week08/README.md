# 8주차 실습: 내 FastAPI 앱을 이미지로

- 장소: WSL2 Ubuntu(또는 Mac 터미널) + Docker, uv 설치됨
- 시간: 약 3시간
- 폴더: 이 폴더(`docs/labs/week08`)에서 모든 명령을 실행해요.
- "이렇게 나오면 성공" 의 출력은 **예시**예요. 이미지 ID·크기·시간은 달라요.

```text
week08/
├─ app/main.py            작은 FastAPI 앱 (/, /health, /whoami)
├─ pyproject.toml, uv.lock  의존성(고정)
├─ Dockerfile             한 단계 이미지
├─ Dockerfile.multistage  멀티스테이지 이미지
└─ .dockerignore
```

## 1. 앱을 먼저 컨테이너 없이 돌려 보기

```bash
uv run uvicorn app.main:app --port 8000
```

다른 터미널에서:

```bash
curl localhost:8000/
curl localhost:8000/health
```

이렇게 나오면 성공(예시):

```text
{"message":"안녕하세요, 컨테이너!"}
{"status":"ok"}
```

처음 한 번은 uv 가 `.venv` 를 만드느라 시간이 걸려요. 확인했으면 앱 터미널에서 `Ctrl+C` 로 끄세요.

## 2. 한 단계 이미지 빌드

```bash
docker build -t hello-api:single .
```

이렇게 나오면 성공(예시): 단계마다 `=> [3/5] RUN ...` 처럼 진행 줄이 나오고, 끝에 `naming to docker.io/library/hello-api:single` 이 보여요.

```bash
docker run -d --name api -p 8000:8000 hello-api:single
curl localhost:8000/health
curl localhost:8000/whoami
```

`/whoami` 에서 `"user_id":1000` 이 나오면 root 가 아닌 사용자로 돌고 있다는 뜻이에요. (`python` 값은 이미지의 파이썬 버전이라 `3.13.x` 로 나와요.)

```bash
docker logs api
```

`GET /health ... 200 OK` 줄이 보여요.

## 3. 캐시가 먹는지 보기

앱 코드를 살짝 고쳐요. `app/main.py` 의 인사말 글자를 바꿔요. 그리고 다시 빌드해요.

```bash
docker build -t hello-api:single .
```

출력에서 의존성 설치 단계(`RUN --mount=...uv sync`)가 `CACHED` 로 표시되고, `COPY app ./app` 부터 다시 만들어지면 성공이에요(예시):

```text
 => CACHED [4/6] RUN --mount=type=cache,...
 => [5/6] COPY app ./app
```

이번엔 일부러 순서를 망쳐 봐요. 복사본을 만들어 `WORKDIR /app` 바로 아래에 `COPY . .` 한 줄을 넣어요(소스를 설치보다 **위**에 두는 잘못된 순서).

```bash
cp Dockerfile /tmp/Dockerfile.bad
nano /tmp/Dockerfile.bad
docker build -f /tmp/Dockerfile.bad -t hello-api:bad .
```

`app/main.py` 를 또 한 글자 고치고 같은 빌드를 다시 해 보세요. 이번에는 의존성 설치 단계가 `CACHED` 가 아니라 매번 다시 실행돼요. 확인했으면 `docker rmi hello-api:bad` 로 지워요.

## 4. 멀티스테이지 이미지와 크기 비교

```bash
docker build -f Dockerfile.multistage -t hello-api:multi .
docker images hello-api
```

이렇게 나오면 성공(예시, 숫자는 달라요):

```text
REPOSITORY   TAG      IMAGE ID       CREATED          SIZE
hello-api    multi    ...            10 seconds ago   ...MB
hello-api    single   ...            3 minutes ago    ...MB
```

두 크기를 아래 표에 적어 보세요. (직접 잰 값만 적어요.)

| 이미지 | 크기 |
|---|---|
| hello-api:single | |
| hello-api:multi | |

`single` 컨테이너를 멈추고 `multi` 도 똑같이 확인해요.

```bash
docker rm -f api
docker run -d --name api -p 8000:8000 hello-api:multi
curl localhost:8000/whoami
```

## 5. 이미지 안을 들여다보기

```bash
docker history hello-api:single
docker exec api ls /app
```

`docker history` 는 층별 크기를 보여줘요. 어느 층이 가장 큰지 찾아 보세요(보통 파이썬 기본 이미지와 의존성 설치 층이에요). `ls /app` 에 `.venv` 와 `app` 이 보이고, `multi` 에는 uv 가 없어요.

```bash
docker exec api which uv
```

`multi` 에서는 아무것도 출력되지 않아요(`single` 에서는 `/bin/uv`).

## 6. 정리

```bash
docker rm -f api
docker rmi hello-api:single hello-api:multi
```

## 확인할 것

- [ ] `/whoami` 의 `user_id` 가 1000 이다
- [ ] 코드만 고쳐 빌드했을 때 의존성 설치 단계가 `CACHED` 였다
- [ ] 두 이미지 크기를 표에 적었다
- [ ] 실습 후 `docker ps -a` 에 `api` 가 없다
