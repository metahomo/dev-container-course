# 10주차 실습: Compose 로 API + PostgreSQL 한 번에

- 장소: WSL2 Ubuntu(또는 Mac 터미널) + Docker (Compose 포함)
- 시간: 약 3시간
- 폴더: 이 폴더(`docs/labs/week10`)에서 실행해요.
- "이렇게 나오면 성공" 의 출력은 **예시**예요.

```text
week10/
├─ compose.yaml        api + db, 볼륨, 네트워크, healthcheck
├─ Dockerfile          8주차의 한 단계 Dockerfile 과 같아요
├─ app/main.py         /health, /hits (DB 에 방문 횟수 저장)
├─ pyproject.toml, uv.lock
├─ .env.example        비밀번호 예시 (복사해서 .env 로)
└─ .dockerignore, .gitignore
```

## 1. 비밀번호 파일 준비

```bash
cp .env.example .env
```

`.env` 의 `DB_PASSWORD=` 뒤를 나만의 연습용 값으로 바꿔 주세요(영문·숫자 권장). `.env` 는 `.gitignore` 에 들어 있어서 커밋되지 않아요. 안 만들어도 `compose.yaml` 의 기본값으로 돌아가요.

## 2. compose.yaml 점검

```bash
docker compose config --quiet && echo OK
```

`OK` 가 나오면 파일 문법이 맞는 거예요. 틀리면 줄 번호가 있는 오류가 나와요.

## 3. 올리기

```bash
docker compose up -d --build
docker compose ps
```

이렇게 나오면 성공(예시):

```text
NAME             IMAGE          ...   SERVICE   STATUS                    PORTS
week10-api-1     week10-api     ...   api       Up 10 seconds             0.0.0.0:8000->8000/tcp
week10-db-1      postgres:17    ...   db        Up 20 seconds (healthy)   5432/tcp
```

`db` 의 상태가 `(health: starting)` 에서 `(healthy)` 로 바뀐 **뒤에** `api` 가 시작돼요. 처음에는 `api` 가 잠시 안 보일 수 있어요.

## 4. 써 보기

```bash
curl localhost:8000/health
curl localhost:8000/hits
curl localhost:8000/hits
curl localhost:8000/hits
```

이렇게 나오면 성공(예시):

```text
{"status":"ok"}
{"hits":1}
{"hits":2}
{"hits":3}
```

로그도 봐요.

```bash
docker compose logs api
docker compose logs -f db
```

(`-f` 는 `Ctrl+C` 로 빠져나와요.)

## 5. 컨테이너를 지워도 숫자가 남는지

```bash
docker compose down
docker compose ps
docker compose up -d
curl localhost:8000/hits
```

`down` 후 `ps` 는 목록이 비고, 다시 올린 뒤 `/hits` 가 `{"hits":4}` 처럼 **이어진 숫자**를 돌려주면 성공이에요. 볼륨 `pgdata` 가 남아 있어서예요. 처음 몇 초는 `curl` 이 실패할 수 있어요. 잠시 뒤 다시 해 보세요.

## 6. 일부러 망가뜨려 보기

DB 를 멈춰요.

```bash
docker compose stop db
curl -s -w ' %{http_code}\n' localhost:8000/hits
docker compose start db
```

멈춰 있는 동안 `503` 과 `DB 에 연결하지 못했어요` 가 보이고, DB 를 다시 켜면 몇 초 뒤 정상으로 돌아와요. 앱이 살아 있어도 DB 문제를 이렇게 알려 주는 게 좋은 동작이에요.

## 7. 정리

숫자도 지우려면 볼륨까지 지워요. 데이터가 사라지니 연습일 때만 하세요.

```bash
docker compose down -v
docker image rm week10-api
rm .env
```

(`down -v` 후 `docker volume ls` 에서 `pgdata` 가 보이지 않으면 성공이에요. 이미지 이름은 `docker images` 로 확인하세요.)

## 생각해 보기

- `compose.yaml` 에서 `depends_on` 블록을 지우고 `docker compose down -v` 후 `up -d` 하면 어떻게 될까요? `docker compose logs api` 로 확인하세요(앱은 `/hits` 를 부를 때 접속하므로 바로 죽지는 않아요. 왜일까요?).
- `ports` 로 DB 의 5432 를 내 PC 에 열어야 할까요? 열면 어떤 위험이 있을까요?

## 확인할 것

- [ ] `docker compose ps` 에서 `db` 가 `healthy` 였다
- [ ] `down` 후 `up` 해도 `hits` 숫자가 이어졌다
- [ ] `.env` 가 `git status` 에 나타나지 않는다
- [ ] 실습 후 `docker compose ps -a` 가 비어 있다
