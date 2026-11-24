# 11주 실습. 이미지를 레지스트리에 올리고 점검표를 통과시키기

내 이미지에 **버전 태그**를 달아 GHCR(GitHub Container Registry)에 올리고, **점검표**로 검사한 뒤, **자원 제한**이 실제로 걸리는지 확인해요.

| 항목 | 내용 |
|---|---|
| 예상 시간 | 3시간 |
| 장소 | Docker + GitHub (WSL 터미널) |
| CPU/GPU | CPU 만 |
| 준비 | Docker 동작, GitHub 계정, 10주까지 만든 FastAPI 이미지(없으면 아래 작은 예제로) |
| 라이선스 | 이 강좌 코드 라이선스(저장소 `LICENSE`) |

!!! note "Docker 를 못 깔았다면"
    GitHub Codespaces(학생 혜택 포함 월 무료 시간 한도 있음)나 Killercoda 같은 웹 실습장에서 같은 명령을 쳐요. Play with Docker 는 2026-03-01 에 중단됐으니 쓰지 않아요.

## 0단계. 연습용 작은 이미지 만들기

내 앱 이미지가 이미 있으면 건너뛰고, 아래 `내이미지` 를 그 이름으로 바꿔요. 없으면 작은 예제를 만들어요.

```bash
mkdir -p ~/week11-lab && cd ~/week11-lab
cat > app.py <<'PY'
import http.server

class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok\n")

http.server.HTTPServer(("0.0.0.0", 8000), H).serve_forever()
PY
cat > Dockerfile <<'EOF2'
FROM python:3.13-slim
RUN useradd --system --uid 10001 --user-group --no-create-home app
WORKDIR /app
COPY app.py .
USER app
EXPOSE 8000
CMD ["python", "app.py"]
EOF2
docker build -t week11-demo:dev .
```

**이렇게 나오면 성공** — 마지막 줄 근처에 `naming to docker.io/library/week11-demo:dev` 같은 줄이 보여요(빌더 버전에 따라 모양은 조금 달라요).

## 1단계. 태그 규칙 익히기

같은 이미지에 이름표(태그)를 여러 개 붙여 봐요. 커밋 해시는 `git rev-parse --short HEAD` 로 얻는데, git 저장소가 아니면 `abc1234` 로 연습해요.

```bash
docker tag week11-demo:dev week11-demo:0.1.0
docker tag week11-demo:dev week11-demo:sha-abc1234
docker images week11-demo
```

**이렇게 나오면 성공** — 세 줄이 보이고 IMAGE ID 가 모두 같아요(이름표만 다른 같은 이미지).

```text
REPOSITORY    TAG           IMAGE ID       CREATED          SIZE
week11-demo   0.1.0         ...            ...              ...
week11-demo   dev           ...            ...              ...
week11-demo   sha-abc1234   ...            ...              ...
```

**생각해 보기**: 내일 코드를 고쳐 다시 빌드해서 `latest` 를 덮어쓰면, 어제 `latest` 를 받아 간 사람과 오늘 받는 사람의 이미지는 같을까요? (답: 아니에요. 그래서 배포에는 `0.1.0` 이나 `sha-...` 처럼 바뀌지 않는 이름표를 써요.)

## 2단계. GHCR 에 올리기

1. GitHub → Settings → Developer settings → Personal access tokens → **Tokens (classic)** 에서 `write:packages` 권한(올리기)이 있는 토큰을 만들어요. 토큰은 비밀번호예요. 파일·채팅·저장소에 붙이지 않아요.
2. 터미널에서 토큰을 환경 변수에 넣고 로그인해요. (`내아이디` 는 GitHub 사용자 이름.)

```bash
read -rs CR_PAT        # 붙여넣고 Enter (화면에 안 보여요)
export CR_PAT
echo $CR_PAT | docker login ghcr.io -u 내아이디 --password-stdin
```

```text
Login Succeeded
```

3. GHCR 이름은 `ghcr.io/소유자/이미지이름:태그` 형식이고 **소문자**여야 해요. 이름표를 새로 붙이고 올려요.

```bash
docker tag week11-demo:0.1.0 ghcr.io/내아이디/week11-demo:0.1.0
docker push ghcr.io/내아이디/week11-demo:0.1.0
```

4. GitHub 프로필 → **Packages** 에 `week11-demo` 가 보이면 성공이에요. 처음 올린 패키지는 **비공개(private)** 예요. 공개로 바꾸는 건 패키지 설정에서 하고, 연습용 이미지는 확인이 끝나면 지워도 돼요.
5. 다 쓴 토큰은 GitHub 설정에서 삭제하고 `unset CR_PAT` 해요.

## 3단계. 점검표로 검사하기

[scan-checklist.md](scan-checklist.md) 를 열어 내 이미지에 항목별로 ○/× 를 적어요. 도구로 확인하는 부분은 아래 명령을 써요.

```bash
docker scout quickview week11-demo:0.1.0
docker image history week11-demo:0.1.0
docker image inspect week11-demo:0.1.0 --format '{{.Config.User}}'
```

- `docker scout quickview` 는 Docker 계정 로그인이 필요할 수 있어요. 취약점 개수 요약과 베이스 이미지 갱신 제안이 나와요.
- 마지막 줄은 이미지에 박힌 실행 사용자예요. `app` 처럼 나오면 root 가 아니에요. 비어 있으면 root 로 돌아가요.

## 4단계. 읽기 전용·비root 로 돌려 보기

```bash
docker run --rm --read-only --cap-drop ALL week11-demo:0.1.0 python -c "open('/app/x','w')"
```

**이렇게 나오면 성공** — 오류가 나야 정상이에요. 파일 시스템이 읽기 전용이거나 쓰기 권한이 없다는 뜻의 `OSError` 가 나와요.

```bash
docker run --rm week11-demo:0.1.0 id
```

```text
uid=10001(app) gid=... groups=...
```

## 5단계. 자원 제한 걸어 보기

[resource-limits.md](resource-limits.md) 의 실습표를 따라 해요. 메모리를 일부러 넘겨 컨테이너가 꺼지는 걸 직접 봐요.

## 6단계. 정리

```bash
docker rm -f $(docker ps -aq --filter name=oom) 2>/dev/null
docker rmi ghcr.io/내아이디/week11-demo:0.1.0 week11-demo:0.1.0 week11-demo:dev week11-demo:sha-abc1234
docker logout ghcr.io
```

## 막히면

| 증상 | 원인 | 해결 |
|---|---|---|
| `denied: permission_denied` / `unauthorized` | 토큰에 `write:packages` 없음, 또는 `-u` 의 아이디가 다름 | 토큰 권한 확인 후 다시 로그인 |
| `invalid reference format` | 이미지 이름에 대문자 | 모두 소문자로 |
| `docker scout` 명령이 없음 / 로그인 요구 | Docker Desktop 이 아닌 환경이거나 미로그인 | 점검표의 수동 항목(`history`, `inspect`)만으로 먼저 진행 |
| 비root 인데 파일 쓰기 오류 | 그 폴더 소유자가 root | 쓸 폴더는 `tmpfs`·볼륨으로, 또는 `COPY --chown` |

## 더 읽기

- [GHCR 사용법(GitHub Docs)](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [`docker scout quickview`(Docker Docs)](https://docs.docker.com/reference/cli/docker/scout/quickview/)
