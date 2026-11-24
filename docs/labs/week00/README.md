# 0주 실습: WSL 안에서 `hello.py` 실행

**장소**: PC(Windows 는 PowerShell → WSL, Mac 은 터미널) · **예상 시간**: 1~2시간(내려받기 포함) · **결과물**: WSL 안의 `~/hello-wsl/hello.py` 를 `uv run` 으로 실행

> 줄 맨 앞의 `PS>` 는 Windows PowerShell, `$` 는 WSL(또는 Mac) 터미널이에요. 이 기호는 **치지 않아요**. 출력 예시는 컴퓨터마다 이름·숫자가 조금 달라요.

## 1단계. Windows Terminal 열기 (Windows)

시작 메뉴에서 "터미널"(Terminal)을 찾아 열어요. 없으면 Microsoft Store 에서 "Windows Terminal" 을 설치해요.

## 2단계. WSL 설치 (Windows)

시작 메뉴에서 "터미널" 을 **우클릭 → 관리자 권한으로 실행** 으로 열고 쳐요.

```powershell
PS> wsl --install
```

끝나면 **컴퓨터를 다시 시작**해요. 다시 켜면 Ubuntu 창이 저절로 열려서 사용자 이름과 비밀번호를 물어봐요.

- 사용자 이름: 영문 소문자(예: `jimin`)
- 비밀번호: 칠 때 화면에 아무 글자도 안 보여도 정상이에요. 잊지 마세요.

이렇게 나오면 성공 — 프롬프트가 아래처럼 바뀌어요.

```text
jimin@내컴퓨터이름:~$
```

> 막히면: `wsl --install` 이 도움말만 보여 주면 `wsl --list --online` 으로 이름을 보고 `wsl --install -d Ubuntu` 를 쳐요. 진행률이 0% 에서 멈추면 `wsl --install --web-download -d Ubuntu`.

## 3단계. 우분투 버전과 WSL 2 확인

WSL 안(`$`)에서:

```bash
$ head -3 /etc/os-release
```

`NAME="Ubuntu"` 와 `VERSION="26.04…"` 비슷한 줄이 나와요. (버전 숫자가 다르면 그 버전을 적어 두고 계속 진행해도 돼요.)

PowerShell 쪽 새 탭에서:

```powershell
PS> wsl --list --verbose
```

```text
  NAME      STATE           VERSION
* Ubuntu    Running         2
```

`VERSION` 이 `2` 면 성공이에요.

## 4단계. 홈 폴더에서 일하기

```bash
$ cd ~
$ pwd
```

```text
/home/jimin
```

`/mnt/c/...` 로 시작하는 곳이 아니라 `/home/내이름` 이어야 해요. 프로젝트 파일은 여기에 둬요.

## 5단계. VS Code 로 WSL 폴더 열기

Windows 쪽에 VS Code 를 설치하고(설치 때 "Add to PATH" 선택), VS Code 에서 **WSL** 확장(`ms-vscode-remote.remote-wsl`)을 설치해요. 그다음 WSL 터미널에서:

```bash
$ mkdir hello-wsl
$ cd hello-wsl
$ code .
```

VS Code 창이 열리고 왼쪽 아래에 **WSL: Ubuntu** 표시가 보이면 성공이에요. (처음엔 필요한 구성요소를 받느라 조금 걸려요.)

## 6단계. uv 설치

WSL 터미널에서:

```bash
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

설치가 끝나면 **터미널 창을 닫았다 다시 열고**(그리고 `cd ~/hello-wsl`) 확인해요.

```bash
$ uv --version
```

```text
uv 0.13.9
```

숫자는 달라도 `uv 0.` 으로 시작하는 줄이 나오면 성공이에요. (`curl` 이 없다고 하면 `sudo apt update && sudo apt install -y curl` 먼저.)

## 7단계. `hello.py` 만들고 실행

`hello-wsl` 폴더 안에서 파일을 만들어요. VS Code 에서 새 파일 `hello.py` 를 만들어 붙여 넣어도 되고, 터미널에서 아래처럼 해도 돼요.

```bash
$ cat > hello.py <<'EOF'
import platform

name = input("이름이 뭐예요? ")
print(f"안녕, {name}! 여기는 {platform.system()} 이에요.")
EOF
```

실행해요.

```bash
$ uv run hello.py
```

이렇게 나오면 성공 — 이름을 치면 아래처럼 돼요. **WSL 이면 `Linux`**, Mac 이면 `Darwin` 이 나와요.

```text
이름이 뭐예요? 지민
안녕, 지민! 여기는 Linux 이에요.
```

`Linux` 가 보이면 "Windows 위에서 Linux 가 내 파이썬을 돌렸다" 는 뜻이에요.

## 8단계. Windows 쪽에서 내 파일 찾아보기

WSL 터미널에서 현재 폴더를 Windows 탐색기로 열어요.

```bash
$ explorer.exe .
```

주소창에 `\\wsl$` 가 들어간 경로로 열리면 성공이에요. (Mac 은 `open .`)

## 정리

`hello-wsl` 폴더는 지워도 돼요: `cd ~ && rm -r hello-wsl`. 1주차부터는 Git 으로 기록하는 폴더를 새로 만들어요.
