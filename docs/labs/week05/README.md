# 5주 실습: 내 파이썬 앱을 서비스로 띄우기

- 장소: WSL(Ubuntu) 터미널. 1~4단계는 Mac 터미널에서도 거의 되지만, `apt`·`systemd`·`journalctl` 은 **Linux 에만** 있어요
- 예상 시간: 3.5시간
- 만드는 것: 터미널을 닫아도 돌고, 죽어도 되살아나는 작은 웹 앱 서비스
- 파일: [`app.py`](app.py)(표준 라이브러리만 쓰는 작은 HTTP 앱), [`myapp.service`](myapp.service)(서비스 파일 예시)

## 0단계. 준비

```bash
$ mkdir -p ~/lab05 && cd ~/lab05
$ curl -O https://raw.githubusercontent.com/metahomo/dev-container-course/main/docs/labs/week05/app.py
$ curl -O https://raw.githubusercontent.com/metahomo/dev-container-course/main/docs/labs/week05/myapp.service
$ ls
app.py  myapp.service
$ python3 --version
```

이렇게 나오면 성공: 파일 두 개가 보이고 `Python 3.…` 버전이 나와요.

## 1단계. 권한과 sudo 살펴보기

```bash
$ whoami
$ id
$ ls -l app.py
-rw-r--r-- 1 내이름 내이름 1856 Nov 24 12:50 app.py
$ chmod 755 app.py
$ ls -l app.py
-rwxr-xr-x 1 내이름 내이름 1856 Nov 24 12:50 app.py
$ chmod 644 app.py
$ sudo --version | head -n 1
```

이렇게 나오면 성공: 권한 글자가 `-rw-r--r--` → `-rwxr-xr-x` → 다시 `-rw-r--r--` 로 바뀌어요. `sudo --version` 첫 줄에 `sudo-rs` 가 보이는지 확인해 보세요(이 강좌에서는 Ubuntu 26.04 기본이 sudo-rs 라고 조사한 자료를 따랐어요). 비밀번호는 `sudo` 를 처음 쓸 때만 물어봐요.

## 2단계. apt 로 `tree` 설치

```bash
$ sudo apt update
$ sudo apt install tree
$ tree ~/lab05
/home/내이름/lab05
├── app.py
└── myapp.service

0 directories, 2 files
$ sudo apt remove tree
```

이렇게 나오면 성공: `tree` 가 폴더 구조를 나무 모양으로 그려줘요. (설치 중 `[Y/n]` 에는 `Y`.)

## 3단계. 앱을 직접 띄우고 확인하기

터미널을 두 개 열어요(Windows Terminal 의 `+` 탭). **첫 번째 터미널**에서:

```bash
$ cd ~/lab05
$ python3 app.py
http://127.0.0.1:8000 에서 기다리는 중 (pid=4321)
```

**두 번째 터미널**에서:

```bash
$ curl localhost:8000/
{"message": "안녕하세요, 리눅스!", "pid": 4321}
$ curl localhost:8000/health
{"status": "ok", "uptime_seconds": 12}
$ curl -i localhost:8000/nope | head -n 1
HTTP/1.0 404 Not Found
```

이렇게 나오면 성공: JSON 이 돌아와요. (`pid`·`uptime_seconds` 값은 달라요.) 첫 번째 터미널에서 `Ctrl+C` 를 눌러 끝내면 `신호 2 를 받았어요. 정리하고 끝냅니다.` 가 나와요.

!!! tip "포트가 이미 쓰이고 있다면"
    `PORT=8080 python3 app.py` 처럼 포트를 바꿔 띄울 수 있어요. 아래 단계의 `8000` 도 같이 바꿔요.

## 4단계. 백그라운드와 kill: SIGTERM 과 SIGKILL

```bash
$ python3 app.py &
[1] 4400
http://127.0.0.1:8000 에서 기다리는 중 (pid=4400)
$ jobs
[1]+  Running                 python3 app.py &
$ pgrep -f app.py
4400
$ kill 4400
신호 15 를 받았어요. 정리하고 끝냅니다.
$ jobs
[1]+  Done                    python3 app.py
```

이렇게 나오면 성공: `kill`(SIGTERM)을 받은 앱이 **스스로 메시지를 남기고** 끝나요.

이번엔 강제 종료와 비교해요.

```bash
$ python3 app.py &
$ kill -9 %1
[1]+  Killed                  python3 app.py
```

이렇게 나오면 성공: `Killed` 만 나오고 `정리하고 끝냅니다` 메시지는 **없어요.** 앱이 정리할 기회가 없었다는 뜻이에요.

!!! warning "남은 앱이 없는지 확인"
    `pgrep -f app.py` 에 아무것도 안 나오는지 확인해요. 남아 있으면 `kill PID` 로 끝내요. 다음 단계의 서비스와 포트가 겹쳐요.

## 5단계. systemd 서비스로 등록

먼저 systemd 가 켜져 있는지 확인해요.

```bash
$ systemctl is-system-running
running
```

오류가 나면 5주 본문의 "WSL 에서 systemd 켜기" 를 먼저 해요.

서비스 파일의 `내사용자이름` 을 내 사용자 이름으로 바꿔서 `/etc/systemd/system/` 에 저장해요.

```bash
$ sed "s/내사용자이름/$USER/g" ~/lab05/myapp.service | sudo tee /etc/systemd/system/myapp.service
$ sudo systemctl daemon-reload
$ sudo systemctl enable --now myapp
$ systemctl status myapp
```

이렇게 나오면 성공: `status` 화면에 `Active: active (running)` 이 보이고 `Main PID:` 가 있어요. `curl localhost:8000/health` 가 JSON 을 돌려줘요.

### 로그 보기

```bash
$ journalctl -u myapp -n 10
```

이렇게 나오면 성공: `http://127.0.0.1:8000 에서 기다리는 중` 과 `GET /health` 요청 기록이 보여요(날짜·컴퓨터 이름이 앞에 붙어요).

## 6단계. 죽여도 되살아나는지 확인

```bash
$ systemctl show -p MainPID myapp
MainPID=5100
$ sudo kill -9 5100          # 위에서 나온 번호로
$ sleep 4
$ systemctl show -p MainPID myapp
MainPID=5133
$ curl localhost:8000/health
```

이렇게 나오면 성공: `MainPID` 가 **다른 번호로 바뀌고** 요청이 다시 돼요. (`Restart=on-failure`, `RestartSec=3` 덕분이에요.) 이번에는 정상 중지예요.

```bash
$ sudo systemctl stop myapp
$ journalctl -u myapp -n 3
```

`stop` 은 SIGTERM 을 보내므로 `신호 15 를 받았어요` 가 로그에 남아요.

## 정리

실습이 끝나면 서비스를 지워 둬요. 켜 두면 컴퓨터가 켜질 때마다 앱이 뜨고 포트를 차지해요.

```bash
$ sudo systemctl disable --now myapp
$ sudo rm /etc/systemd/system/myapp.service
$ sudo systemctl daemon-reload
$ systemctl status myapp
Unit myapp.service could not be found.
```
