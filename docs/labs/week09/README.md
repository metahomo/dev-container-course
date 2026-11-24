# 9주차 실습: 데이터 남기기, 이름으로 부르기, 설정 넣기

- 장소: WSL2 Ubuntu(또는 Mac 터미널) + Docker
- 시간: 약 3시간
- 폴더: 이 폴더(`docs/labs/week09`)에서 실행해요. 파일: `site/index.html`, `app.env.example`, `backup.sh`, `restore.sh`
- "이렇게 나오면 성공" 의 출력은 **예시**예요.

## 1. 컨테이너를 지우면 데이터도 사라진다

```bash
docker run --name box alpine sh -c 'echo hello > /note.txt'
docker rm box
docker run --rm alpine cat /note.txt
```

이렇게 나오면 성공(예시): `cat: can't open '/note.txt': No such file or directory`. 첫 컨테이너의 파일은 그 컨테이너와 함께 갔어요.

## 2. named volume 으로 남기기

```bash
docker volume create notes
docker run --rm -v notes:/data alpine sh -c 'echo hello > /data/note.txt'
docker run --rm -v notes:/data alpine cat /data/note.txt
docker volume ls
docker volume inspect notes
```

두 번째 `run` 은 `hello` 를 출력해요. 컨테이너는 둘 다 지워졌지만 `notes` 볼륨은 남아 있어요. `docker volume ls` 에 `notes` 가 보이면 성공이에요.

## 3. bind mount 로 내 파일을 컨테이너에 연결

```bash
docker run -d --name web -p 8080:80 -v "$PWD/site":/usr/share/nginx/html:ro nginx
curl -s localhost:8080 | grep h1
```

`<h1>바인드 마운트로 보는 내 파일</h1>` 이 나오면 성공이에요. 이제 `site/index.html` 의 제목을 편집기에서 바꾸고 저장한 뒤 다시 `curl` 해 보세요. 컨테이너를 다시 만들지 않았는데도 바뀐 글이 나와요. `:ro` 는 컨테이너가 이 폴더를 읽기만 하게 해요.

```bash
docker rm -f web
```

## 4. 백업과 복원

2번에서 만든 `notes` 볼륨을 백업하고, 새 볼륨으로 복원해요.

```bash
./backup.sh notes
ls backup
```

`backup/notes-날짜-시간.tgz` 가 보여요(예시: `notes-20261124-153000.tgz`). 이제 복원이에요. 파일 이름은 방금 만들어진 것으로 바꿔 쓰세요.

```bash
./restore.sh backup/notes-20261124-153000.tgz notes-copy
docker run --rm -v notes-copy:/data alpine cat /data/note.txt
```

`hello` 가 나오면 성공이에요. 원본 볼륨을 지워도 백업 파일로 살릴 수 있어요.

## 5. 사용자 정의 네트워크와 이름(DNS)

```bash
docker network create mynet
docker run -d --name web --network mynet nginx
docker run --rm --network mynet alpine wget -qO- http://web
```

`<title>Welcome to nginx!</title>` 이 포함된 HTML 이 나오면 성공이에요. 주소에 IP 가 아니라 컨테이너 이름 `web` 을 썼어요. 포트를 `-p` 로 열지 않았는데도 같은 네트워크 안에서는 서로 접근돼요.

```bash
docker network inspect mynet
docker rm -f web
docker network rm mynet
```

## 6. 환경 변수와 --env-file

```bash
docker run --rm -e GREETING=hello alpine sh -c 'echo "$GREETING"'
cp app.env.example app.env
docker run --rm --env-file app.env alpine sh -c 'echo "$GREETING / $APP_MODE"'
```

두 번째 줄이 `안녕하세요 / practice` 로 나오면 성공이에요. `app.env` 는 `.gitignore` 에 들어 있어서 커밋되지 않아요.

## 7. DB 데이터를 컨테이너를 지워도 남게 하기

```bash
docker run -d --name db --env-file app.env -v pgdata:/var/lib/postgresql/data postgres:17
docker logs db 2>&1 | tail -n 3
```

`database system is ready to accept connections` 가 보이면 준비된 거예요(처음 몇 초는 초기화 중이라 이 문장이 두 번 나올 수 있어요).

```bash
docker exec db psql -U postgres -c "CREATE TABLE memo (id serial, text text);"
docker exec db psql -U postgres -c "INSERT INTO memo (text) VALUES ('남아 있을까요?');"
docker exec db psql -U postgres -c "SELECT * FROM memo;"
```

이제 컨테이너를 지우고 **같은 볼륨**으로 새로 만들어요.

```bash
docker rm -f db
docker run -d --name db --env-file app.env -v pgdata:/var/lib/postgresql/data postgres:17
sleep 5
docker exec db psql -U postgres -c "SELECT * FROM memo;"
```

예전에 넣은 `남아 있을까요?` 행이 그대로 나오면 성공이에요(예시):

```text
 id |      text
----+----------------
  1 | 남아 있을까요?
(1 row)
```

볼륨 없이 했다면 `relation "memo" does not exist` 오류가 나요. 이번 주의 핵심이에요.

## 8. 정리

```bash
docker rm -f db
docker volume rm notes notes-copy pgdata
rm -rf backup app.env
```

`docker volume rm` 은 데이터를 **되돌릴 수 없게** 지워요. 남기고 싶은 볼륨은 목록에서 빼세요.

## 확인할 것

- [ ] 볼륨 없이 지운 컨테이너의 파일은 사라진다는 것을 봤다
- [ ] DB 컨테이너를 지우고 다시 만들어도 `memo` 행이 남았다
- [ ] 이름(`web`)으로 다른 컨테이너를 불러 봤다
- [ ] `app.env` 가 Git 에 올라가지 않는다는 걸 `git status` 로(또는 `.gitignore` 로) 확인했다
