# 7주차 실습: 공식 이미지로 웹 서버 띄우고 지우기

- 장소: WSL2 Ubuntu(또는 Mac 터미널) + Docker. 못 깔았다면 [7주차 글의 무료 실습장](../../weeks/week07.md) 중 하나에서 해요.
- 시간: 약 3시간
- 아래 "이렇게 나오면 성공" 의 출력은 **예시**예요. Docker 버전에 따라 ID·시간·글씨가 조금 달라요.
- 이 실습은 Docker 공식 문서의 모양을 따라 썼어요.

## 0. Docker 확인

```bash
docker version
docker login
```

성공하면 Client 와 Server 정보가 둘 다 나와요. Server 줄이 없으면 Docker 엔진이 꺼져 있는 거예요(글의 "막히면" 참고).

## 1. hello-world

```bash
docker run hello-world
```

이렇게 나오면 성공(예시):

```text
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
...
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

```bash
docker ps -a
```

`hello-world` 컨테이너가 `Exited` 상태로 보여요. 프로그램이 끝났으니 컨테이너도 멈춘 거예요.

## 2. nginx 띄우기

```bash
docker run -d --name web -p 8080:80 nginx
docker ps
```

이렇게 나오면 성공(예시):

```text
CONTAINER ID   IMAGE   COMMAND                  CREATED         STATUS         PORTS                  NAMES
3f2a1b9c8d7e   nginx   "/docker-entrypoint.…"   5 seconds ago   Up 4 seconds   0.0.0.0:8080->80/tcp   web
```

브라우저에서 `http://localhost:8080` 을 열거나 터미널에서 확인해요.

```bash
curl -s localhost:8080 | head -n 5
```

`<!DOCTYPE html>` 과 `<title>Welcome to nginx!</title>` 이 보이면 성공이에요.

## 3. 로그 보기

```bash
docker logs web
```

방금 `curl` 한 요청이 `GET / HTTP/1.1" 200` 같은 줄로 남아 있어요. 브라우저에서 새로고침한 뒤 `docker logs -f web` 으로 줄이 늘어나는 걸 지켜보고, `Ctrl+C` 로 빠져나와요(컨테이너는 계속 돌아요).

## 4. 안에 들어가기

```bash
docker exec -it web bash
```

프롬프트가 `root@3f2a1b9c8d7e:/#` 처럼 바뀌어요. 컨테이너 안이에요.

```bash
ls /usr/share/nginx/html
cat /etc/os-release | head -n 2
exit
```

`index.html` 이 보이면 성공이에요. `exit` 후에도 `docker ps` 에 web 이 그대로 있어요.

## 5. 컨테이너 안 파일은 컨테이너와 함께 사라진다

```bash
docker exec web sh -c 'echo 안녕 > /tmp/memo.txt'
docker exec web cat /tmp/memo.txt
docker stop web
docker rm web
docker run -d --name web -p 8080:80 nginx
docker exec web cat /tmp/memo.txt
```

마지막 줄은 이렇게 나오면 성공이에요(예시): `cat: /tmp/memo.txt: No such file or directory`. 같은 이미지로 새로 만든 컨테이너라서 메모가 없어요.

## 6. 파이썬 이미지

```bash
docker run --rm python:3.13-slim python -c "print('컨테이너에서 안녕')"
docker run --rm -it python:3.13-slim python
```

두 번째는 컨테이너 안의 파이썬 대화형 창이에요. `exit()` 로 나와요. `--rm` 덕분에 나오면 컨테이너가 자동으로 지워져요.

## 7. 정리

```bash
docker rm -f web
docker ps -a
docker images
```

`docker ps -a` 에 `web` 이 없어야 해요. `hello-world` 가 남아 있으면 `docker rm 컨테이너ID` 로 지워요. 이미지는 다음 주에도 쓸 수 있으니 남겨 두어도 되고, 디스크가 아쉬우면 `docker rmi nginx hello-world python:3.13-slim` 으로 지워요.

## 확인할 것

- [ ] `docker ps -a` 가 비어 있다(또는 내가 남기려 한 것만 있다)
- [ ] 같은 이미지(`nginx`)로 컨테이너를 두 번 만들었고, 두 번째에는 `/tmp/memo.txt` 가 없었다
