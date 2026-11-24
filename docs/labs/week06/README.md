# 6주 실습: 매일 백업하는 스크립트

- 장소: WSL(Ubuntu) 터미널. Mac 터미널에서도 1·3·4·6단계는 같고, 다른 점은 단계마다 표시했어요
- 예상 시간: 3.5시간
- 만드는 것: 폴더를 날짜가 붙은 `.tar.gz` 로 백업하고 오래된 것을 지우는 스크립트 + 그것을 매일 실행하는 cron 줄
- 파일: [`backup.sh`](backup.sh), [`crontab-example.txt`](crontab-example.txt)

## 0단계. 준비

```bash
$ mkdir -p ~/lab06/data/sub && cd ~/lab06
$ echo "첫째 파일" > data/a.txt
$ echo "둘째 파일" > data/sub/b.txt
$ curl -O https://raw.githubusercontent.com/metahomo/dev-container-course/main/docs/labs/week06/backup.sh
$ curl -O https://raw.githubusercontent.com/metahomo/dev-container-course/main/docs/labs/week06/crontab-example.txt
$ chmod +x backup.sh
$ ls
backup.sh  crontab-example.txt  data
```

## 1단계. SSH 키 만들기

이미 `~/.ssh/id_ed25519` 가 있으면(3주) **덮어쓰지 않도록** 이 실습에서는 이름을 따로 줘요.

```bash
$ ssh-keygen -t ed25519 -C "lab06" -f ~/.ssh/id_ed25519_lab06
Generating public/private ed25519 key pair.
Enter passphrase (empty for no passphrase):
...
Your identification has been saved in /home/내이름/.ssh/id_ed25519_lab06
Your public key has been saved in /home/내이름/.ssh/id_ed25519_lab06.pub
$ ls -l ~/.ssh/id_ed25519_lab06*
-rw------- 1 내이름 내이름 411 Nov 24 12:51 /home/내이름/.ssh/id_ed25519_lab06
-rw-r--r-- 1 내이름 내이름  98 Nov 24 12:51 /home/내이름/.ssh/id_ed25519_lab06.pub
```

이렇게 나오면 성공: 파일이 둘이고 비공개 키는 `-rw-------`, 공개 키(`.pub`)는 `-rw-r--r--` 예요. 공개 키는 `cat ~/.ssh/id_ed25519_lab06.pub` 로 볼 수 있어요. `ssh-ed25519 AAAA…` 로 시작하는 한 줄이에요. (Mac 의 경로는 `/Users/내이름/.ssh/…` 예요.)

## 2단계. config 와 접속 연습

서버가 있다면(학교·클라우드·친구 컴퓨터) `~/.ssh/config` 에 별명을 만들어요. 없다면 두 가지 중 하나로 연습해요.

**방법 A. GitHub 에 접속해 보기 (3주에서 SSH 키를 GitHub 에 등록했을 때)**

```bash
$ ssh -T git@github.com
Hi 내GitHub이름! You've successfully authenticated, but GitHub does not provide shell access.
```

이렇게 나오면 성공: "successfully authenticated" 가 보이면 키 로그인이 되는 거예요. ([출처: GitHub 문서](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/testing-your-ssh-connection))

**방법 B. 내 컴퓨터(localhost)로 접속하기 (선택)**

```bash
$ sudo apt install openssh-server
$ sudo systemctl enable --now ssh
$ cat ~/.ssh/id_ed25519_lab06.pub >> ~/.ssh/authorized_keys
$ chmod 600 ~/.ssh/authorized_keys
$ ssh -i ~/.ssh/id_ed25519_lab06 localhost
```

이렇게 나오면 성공: 처음에 지문 질문에 `yes` 를 하면 내 컴퓨터에 한 번 더 로그인한 프롬프트가 떠요. `exit` 로 돌아와요. 끝나면 `sudo systemctl disable --now ssh` 로 꺼 둬요. (`sudo` 와 `systemctl` 은 5주에 배웠어요.)

그리고 `~/.ssh/config` 에 별명을 적어 봐요.

```bash
$ nano ~/.ssh/config
```

```text
Host lab06
    HostName localhost
    User 내이름
    IdentityFile ~/.ssh/id_ed25519_lab06
```

`chmod 600 ~/.ssh/config` 로 권한을 닫고 `ssh lab06` 으로 접속돼요. 접속된 상태에서 `scp backup.sh lab06:~/` 로 파일도 보내 봐요.

## 3단계. 스크립트 실행해 보기

먼저 문법 검사부터 해요. 아무것도 안 나오면 문법에 문제가 없다는 뜻이에요.

```bash
$ bash -n backup.sh
```

인자를 일부러 틀리게 줘서 오류 처리와 종료 코드를 봐요.

```bash
$ ./backup.sh
사용법: ./backup.sh 백업할폴더 백업둘폴더 [남길개수]
$ echo $?
2
$ ./backup.sh nodir backups
오류: 백업할 폴더가 없어요: nodir
$ echo $?
1
```

이제 진짜 백업이에요.

```bash
$ ./backup.sh data backups 3
백업 완료: backups/data-20261124-125107.tar.gz
$ ls backups
backup.log  data-20261124-125107.tar.gz
$ tar -tzf backups/data-*.tar.gz
data/
data/sub/
data/a.txt
data/sub/b.txt
```

이렇게 나오면 성공: `tar -tzf` 가 압축 안의 파일 목록을 보여줘요. (파일 이름의 날짜·시각은 달라요. 순서도 시스템마다 조금 달라요.)

## 4단계. 오래된 백업 지우기와 로그

몇 초 간격으로 여러 번 실행하고(이름에 초까지 들어가요) **3개만 남는지** 봐요.

```bash
$ for i in 1 2 3 4; do ./backup.sh data backups 3; sleep 1; done
$ ls backups
backup.log  data-20261124-125109.tar.gz  data-20261124-125110.tar.gz  data-20261124-125111.tar.gz
$ cat backups/backup.log
2026-11-24 12:51:07 시작: data -> backups/data-20261124-125107.tar.gz
2026-11-24 12:51:07 완료: data-20261124-125107.tar.gz
...
2026-11-24 12:51:11 삭제: data-20261124-125108.tar.gz
```

이렇게 나오면 성공: `.tar.gz` 가 3개만 있고, 로그에 `삭제:` 줄이 남아요. 4주에 배운 도구로 로그를 읽어 봐요.

```bash
$ grep -c 삭제 backups/backup.log
$ tail -n 3 backups/backup.log
```

### 스크립트 읽기 숙제

`backup.sh` 를 열어서 5주·6주 개념을 찾아 보세요.

1. `set -euo pipefail` 을 지우고 `./backup.sh nodir backups` 를 실행하면 무엇이 달라질까요?
2. `KEEP="${3:-5}"` 는 인자가 없을 때 몇 개를 남기나요?
3. 어떤 줄이 종료 코드 2 를 만드나요?

??? note "답 보기"
    1. 이 스크립트는 `if [ ! -d ... ]` 로 직접 검사해서 같은 오류가 나요. 하지만 `tar` 가 실패해도 멈추지 않고 "완료" 로그를 남기는 식의 조용한 실패가 생기므로, `set -euo pipefail` 은 지우지 않는 게 좋아요.
    2. 5개예요 (`:-5` 는 "없으면 5").
    3. `usage` 함수의 `exit 2` 예요.

!!! note "이 스크립트의 한계"
    폴더 이름에 **공백**이 있으면 오래된 백업 지우기 부분(`for old in $(ls ...)`)이 깨질 수 있어요. 연습에서는 공백 없는 이름만 써요. 더 튼튼하게 고치는 것은 도전 과제예요.

## 5단계. cron 에 등록하기

`crontab-example.txt` 를 열어서 줄을 확인해요.

```bash
$ cat crontab-example.txt
```

시험은 **매분** 실행으로 해요. 경로를 내 사용자 이름으로 바꿔서 등록해요.

```bash
$ crontab -e
```

편집기에서 아래 한 줄을 붙여 넣고 저장해요(`내이름` 은 `whoami` 로 확인).

```text
* * * * * /home/내이름/lab06/backup.sh /home/내이름/lab06/data /home/내이름/lab06/backups 3 >> /home/내이름/lab06/cron.log 2>&1
```

```bash
$ crontab -l
* * * * * /home/내이름/lab06/backup.sh ...
$ sleep 130
$ ls ~/lab06/backups
$ cat ~/lab06/cron.log
백업 완료: /home/내이름/lab06/backups/data-20261124-130001.tar.gz
```

이렇게 나오면 성공: 1~2분 안에 새 백업이 생기고 `cron.log` 에 "백업 완료" 줄이 쌓여요. 안 되면 5주 본문의 cron 항목과 이 주의 "막히면" 표를 확인해요(`systemctl status cron`).

!!! danger "시험이 끝나면 매분 줄을 꼭 지워요"
    `crontab -e` 로 열어서 그 줄을 지우거나(또는 `# ` 를 앞에 붙여 주석으로), 매일 새벽 3시 30분으로 바꾸고(`30 3 * * *`) 저장해요. 지우지 않으면 하루에 1440개씩 백업 파일이 생겨요. (`KEEP` 이 3이라 3개만 남지만 로그와 CPU 는 계속 써요.) 모두 지우려면 `crontab -r` 이에요 — 내 일정표 전체가 사라지니 `crontab -l` 로 먼저 확인해요.

## 6단계. uv 로 파이썬 환경 만들기

```bash
$ curl -LsSf https://astral.sh/uv/install.sh | sh
$ uv --version
uv 0.13.9
```

버전 숫자는 달라도 돼요. 설치가 끝나면 터미널을 새로 열어요.

```bash
$ mkdir -p ~/lab06/pyproj && cd ~/lab06/pyproj
$ uv init --no-package
Initialized project `pyproj`
$ ls -A
.git  .gitignore  .python-version  README.md  main.py  pyproject.toml
$ uv run main.py
Hello from pyproj!
$ uv add requests
$ uv run python -c "import requests; print('ok')"
ok
$ ls -A
.git  .gitignore  .python-version  .venv  README.md  main.py  pyproject.toml  uv.lock
```

이렇게 나오면 성공: `.venv` 와 `uv.lock` 이 생기고 `ok` 가 나와요. (`uv --version`, 설치되는 라이브러리 버전, `.git` 폴더의 유무는 uv 버전·설정에 따라 달라요.) `cat pyproject.toml` 로 `dependencies` 에 `requests` 가 들어간 것도 확인해요.

## 정리

```bash
$ crontab -l            # 매분 줄이 지워졌는지 확인
$ rm -r ~/lab06/backups # 시험으로 만든 백업 지우기 (경로를 다시 읽고 엔터)
```

`~/lab06/backup.sh` 는 두고, 앞으로 내 폴더 백업에 써도 돼요.
