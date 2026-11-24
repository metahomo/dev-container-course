# 명령어 치트시트

자주 쓰는 명령을 모았어요. 외우는 쪽이 아니라 **찾아보는 쪽**이에요. 주의 칸에 **위험**이라고 적힌 명령은 지우거나 되돌릴 수 없는 것이니, [공부하는 법](how-to-study.md#danger)을 먼저 읽으세요. 모든 명령은 WSL(Ubuntu) 터미널 기준이에요.

!!! tip "모르는 옵션은"
    `명령 --help` 또는 `man 명령` 으로 확인해요. (`man` 은 `q` 로 나가요.)

## Git

| 명령 | 하는 일 | 주의 |
|---|---|---|
| `git config --global init.defaultBranch main` | 새 저장소의 기본 가지 이름을 `main` 으로 | 한 번만. Git 3.0 부터 기본값이 돼요 |
| `git config --global user.name "이름"` · `user.email "메일"` | 커밋에 찍힐 이름·메일 | 공개 저장소에는 이 메일이 보여요 |
| `git init` | 현재 폴더를 저장소로 | 홈(`~`)에서 하지 마세요 |
| `git status` | 지금 상태 보기 | 막히면 가장 먼저 쳐요 |
| `git add 파일` · `git add .` | 커밋할 변경을 스테이징에 올림 | `.` 은 전부. 비밀 파일이 섞이지 않게 `.gitignore` 먼저 |
| `git commit -m "메시지"` | 변경을 기록 | 메시지는 "무엇을 왜" |
| `git log --oneline` | 기록을 한 줄씩 | `--graph` 를 붙이면 가지 모양 |
| `git diff` · `git diff --staged` | 바뀐 내용 보기 | |
| `git switch 가지` · `git switch -c 새가지` | 가지 이동 · 만들며 이동 | 저장 안 한 변경이 있으면 막힐 수 있어요 |
| `git branch` | 가지 목록 | |
| `git merge 가지` | 가지를 현재 가지에 합침 | 충돌하면 파일을 고치고 `git add` 후 `git commit` |
| `git restore 파일` | 저장 안 한 변경을 버림 | **위험**: 그 변경은 못 되살려요 |
| `git restore --staged 파일` | 스테이징만 취소 | 파일 내용은 그대로 |
| `git reset --hard` | 마지막 커밋 상태로 전부 되돌림 | **위험**: 저장 안 한 변경이 사라져요 |
| `git clean -fd` | 추적 안 하는 파일·폴더 삭제 | **위험**: 먼저 `git clean -nd` 로 미리 보기 |
| `git rebase` | 가지를 다른 기록 위로 옮김 | **조심**: 이미 올린 가지에는 쓰지 마세요 |
| `git remote add origin 주소` | 원격 저장소 등록 | |
| `git push -u origin main` | 원격에 올림 | 처음 한 번만 `-u` |
| `git push --force` | 원격 기록을 덮어씀 | **위험**: 팀 작업을 지워요. `--force-with-lease` 가 그나마 안전 |
| `git pull` | 원격 변경을 받아 합침 | 하기 전에 `git status` |
| `git clone 주소` | 원격 저장소를 복사 | |
| `gh auth login` · `gh pr create` | GitHub CLI 로 로그인 · PR 만들기 | gh 설치 필요([cli.github.com](https://cli.github.com/)) |

## Linux (셸)

| 명령 | 하는 일 | 주의 |
|---|---|---|
| `pwd` | 지금 위치 | |
| `ls` · `ls -la` | 파일 목록 · 숨김 파일 포함 자세히 | |
| `cd 경로` · `cd ..` · `cd ~` | 이동 · 위로 · 홈으로 | |
| `mkdir -p a/b` | 폴더 만들기(중간 폴더도) | |
| `touch 파일` | 빈 파일 만들기 | |
| `cp 원본 대상` · `cp -r 폴더 대상` | 복사 | 같은 이름이 있으면 덮어써요 |
| `mv 원본 대상` | 옮기기·이름 바꾸기 | 덮어쓸 수 있어요 |
| `rm 파일` | 파일 삭제 | **위험**: 휴지통 없음 |
| `rm -r 폴더` | 폴더 삭제 | **위험** |
| `rm -rf 경로` | 묻지 않고 통째로 삭제 | **매우 위험**: 경로를 두 번 확인 |
| `cat 파일` · `less 파일` | 내용 보기 · 한 쪽씩(`q` 로 나가요) | |
| `head -n 5 파일` · `tail -f 파일` | 앞 5줄 · 끝을 계속 따라 보기 | `tail -f` 는 `Ctrl+C` 로 멈춰요 |
| `grep "찾을말" 파일` | 줄 찾기 | `-r` 폴더 안, `-i` 대소문자 무시 |
| `find . -name "*.py"` | 파일 이름으로 찾기 | |
| `명령 > 파일` · `명령 >> 파일` | 출력을 파일로(덮어씀) · 덧붙임 | `>` 는 기존 내용을 지워요 |
| `명령1 \| 명령2` | 앞 출력을 뒤 입력으로(파이프) | |
| `chmod +x 파일` | 실행 권한 주기 | `chmod -R 777` 은 **위험** |
| `sudo 명령` | 관리자 권한으로 실행 | **주의**: 이해한 뒤에만 |
| `sudo apt update && sudo apt install 패키지` | 패키지 목록 갱신 후 설치 | |
| `ps aux` · `kill PID` | 프로세스 보기 · 끝내기 | 숫자(PID)를 확인하고 |
| `echo $PATH` · `export 이름=값` | 환경 변수 보기 · 정하기 | 그 창에서만 유효 |
| `ssh 사용자@주소` | 원격 접속 | 비밀 키(`id_ed25519`)를 남에게 주지 마세요 |
| `curl -O 주소` | 파일 내려받기 | `curl ... \| sh` 는 **위험**: 내용을 읽고 실행 |
| `history` · `Ctrl+R` | 이전 명령 · 검색 | |
| `Ctrl+C` | 실행 중인 명령 멈춤 | |

## Docker

| 명령 | 하는 일 | 주의 |
|---|---|---|
| `docker --version` · `docker info` | 설치·상태 확인 | |
| `docker login` | Docker Hub 로그인 | 받기 한도 완화에 도움이 돼요 |
| `docker pull 이미지:태그` | 이미지 받기 | 태그를 쓰세요(`latest` 는 바뀔 수 있어요) |
| `docker run --rm 이미지` | 컨테이너를 만들어 실행, 끝나면 삭제 | |
| `docker run -d -p 8080:80 --name web nginx` | 백그라운드로, 내 8080 을 컨테이너 80 에 연결 | 포트가 이미 쓰이면 실패 |
| `docker run -it 이미지 bash` | 안에 들어가 직접 만지기 | `exit` 로 나와요 |
| `docker ps` · `docker ps -a` | 실행 중 · 전체 컨테이너 | |
| `docker logs -f 이름` | 로그 따라 보기 | `Ctrl+C` 로 빠져나와도 컨테이너는 계속 돌아요 |
| `docker exec -it 이름 bash` | 돌고 있는 컨테이너 안으로 | |
| `docker stop 이름` · `docker start 이름` | 멈춤 · 다시 시작 | |
| `docker rm 이름` | 컨테이너 삭제 | **주의**: 안의 저장 안 한 데이터는 사라져요 |
| `docker rm -f 이름` | 돌고 있는 것도 강제 삭제 | **위험** |
| `docker images` | 이미지 목록 | |
| `docker rmi 이미지` | 이미지 삭제 | 쓰는 컨테이너가 있으면 막혀요 |
| `docker build -t 이름:태그 .` | Dockerfile 로 이미지 빌드 | 마지막 `.` 은 빌드 위치 |
| `docker volume ls` · `docker volume create 이름` | 볼륨 목록 · 만들기 | |
| `docker volume rm 이름` | 볼륨 삭제 | **위험**: 데이터가 사라져요 |
| `docker network ls` | 네트워크 목록 | |
| `docker system df` | 디스크 사용량 | 지우기 전에 보기 |
| `docker system prune` | 안 쓰는 컨테이너·네트워크·댕글링 이미지 삭제 | **위험**: 먼저 무엇이 지워질지 읽어요 |
| `docker system prune -a --volumes` | 쓰지 않는 이미지·볼륨까지 삭제 | **매우 위험**: 데이터 손실 |
| `docker tag 이미지 레지스트리/이름:태그` · `docker push ...` | 이름 붙이기 · 레지스트리에 올리기 | 비밀·키가 이미지 안에 없는지 확인 |
| `docker scout quickview 이미지` | 이미지 취약점 요약 | Docker Scout CLI 필요 |

## Compose

옛 `docker-compose`(하이픈) 대신 **`docker compose`(띄어쓰기)** 를 써요. 파일 이름은 `compose.yaml`이고, 최상위 `version:` 은 쓰지 않아요. ([Compose 역사 문서](https://docs.docker.com/compose/intro/history/))

| 명령 | 하는 일 | 주의 |
|---|---|---|
| `docker compose up` | 파일에 적힌 서비스를 모두 띄움 | 터미널을 차지해요. `Ctrl+C` 로 멈춤 |
| `docker compose up -d` | 백그라운드로 | |
| `docker compose up -d --build` | 이미지를 다시 빌드하며 | 소스를 고쳤을 때 |
| `docker compose ps` | 서비스 상태 | |
| `docker compose logs -f 서비스` | 로그 따라 보기 | |
| `docker compose exec 서비스 bash` | 서비스 안으로 | |
| `docker compose config` | 합쳐진 설정 확인 · 문법 점검 | 파일을 고친 뒤 먼저 쳐요 |
| `docker compose stop` · `start` | 멈춤 · 재시작 | 데이터는 그대로 |
| `docker compose down` | 서비스와 네트워크 삭제 | 볼륨은 남아요 |
| `docker compose down -v` | 볼륨까지 삭제 | **위험**: DB 데이터가 사라져요 |

## 더 읽기

- [용어집](glossary.md) · [공부하는 법](how-to-study.md) · [실습 환경 만들기](setup.md)
- [Git 공식 문서](https://git-scm.com/docs) · [Docker 공식 문서](https://docs.docker.com/)
