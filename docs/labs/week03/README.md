# 3주 실습: GitHub 로 함께 일하기

**장소**: WSL + GitHub(무료 계정 필요) · **예상 시간**: 3~4시간 · **결과물**: ① 내 GitHub 저장소 `devenv-course` ② 나(또는 친구)와 주고받은 PR 1개 ③ PR 에서 자동으로 도는 pytest(초록 체크)

> `$` 는 치지 않아요. 커밋 번호·경로는 사람마다 달라요. 이 폴더의 `calc.py`, `test_calc.py`, `.github-workflow-example.yml` 은 3~4단계에서 쓰는 견본이에요.
> **GitHub 웹 화면은 글을 쓴 시점과 달라질 수 있어요.** 단추 이름이 다르면 비슷한 이름을 찾거나 [GitHub Docs 한국어](https://docs.github.com/ko)에서 찾아요. 0단계의 명령과 출력은 실제로 실행해 확인했어요. 하지만 GitHub 웹 화면과 진짜 GitHub 에 연결하는 1~6단계는 작성 중 실제 GitHub 에서 해 보지 못했어요. 그 단계의 출력은 GitHub 문서와 같은 명령의 로컬 실행을 바탕으로 쓴 예시예요.

## 0단계. (GitHub 없이) 원격 저장소 연습 — 인터넷 없이도 가능

진짜 GitHub 를 쓰기 전에, **내 컴퓨터 폴더를 "원격" 처럼 써서** clone·push·pull 을 연습해요. 이 단계는 지워도 되는 연습이에요.

```bash
$ mkdir ~/remote-lab && cd ~/remote-lab
$ git init --bare remote.git
$ git clone remote.git me
```

```text
Cloning into 'me'...
warning: You appear to have cloned an empty repository.
done.
```

`--bare` 는 작업 폴더 없이 기록만 보관하는 저장소예요(서버 역할). 빈 저장소라는 경고는 정상이에요. 이제 내 쪽에서 커밋하고 push 해요.

```bash
$ cd me
$ echo "# calc" > README.md
$ git add README.md
$ git commit -m "README 추가"
$ git push -u origin main
```

```text
To /home/jimin/remote-lab/remote.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

(`-u` 는 "앞으로 `git push`·`git pull` 만 쳐도 이 곳과 짝지어라" 는 뜻이에요. 진짜 GitHub 에서는 위에 `Enumerating objects…` 같은 진행 줄이 더 나와요.)

**친구 역할**로 다른 폴더에 clone 해서 고치고 push 해요. 그다음 내 쪽에서 pull 해요.

```bash
$ cd ~/remote-lab
$ git clone remote.git friend
$ cd friend
$ echo "친구가 추가" >> README.md
$ git commit -am "친구: README 수정"
$ git push
$ cd ../me
$ git pull
$ git log --oneline
```

pull 의 끝에서 이렇게 나오면 성공이에요.

```text
Updating 7f8776e..a427988
Fast-forward
 README.md | 1 +
 1 file changed, 1 insertion(+)
```

`git log --oneline` 에 커밋이 두 개(`친구: README 수정`, `README 추가`) 보이면 돼요. 지울 때는 `cd ~ && rm -r remote-lab`.

## 1단계. GitHub 계정과 SSH 키

1. [github.com](https://github.com) 에서 가입해요(무료). 이메일은 1주차 `user.email` 과 같게 하면 좋아요.
2. WSL 에서 SSH 키를 만들어요. (**키는 비밀번호 대신 쓰는 열쇠 한 쌍**이에요. 공개키는 GitHub 에 주고, 비밀키는 내 컴퓨터에만 둬요.)

```bash
$ ssh-keygen -t ed25519 -C "내메일@example.com"
```

물어보면 **Enter**(기본 위치)를 누르고, 암호(passphrase)는 정해도 되고 Enter 로 비워도 돼요. 이렇게 나오면 성공이에요(글자는 달라요).

```text
Generating public/private ed25519 key pair.
Your identification has been saved in /home/jimin/.ssh/id_ed25519
Your public key has been saved in /home/jimin/.ssh/id_ed25519.pub
```

3. **공개키**(`.pub`)를 화면에 찍어서 복사해요.

```bash
$ cat ~/.ssh/id_ed25519.pub
```

`ssh-ed25519 AAAA…… 내메일@example.com` 한 줄이 나와요. **`.pub` 가 없는 `id_ed25519`(비밀키)는 절대 복사·공유하지 않아요.**

4. GitHub 웹에서 오른쪽 위 프로필 → **Settings → SSH and GPG keys → New SSH key** 에 붙여 넣고 저장해요. ([GitHub Docs: SSH 키](https://docs.github.com/ko/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent))
5. 연결을 확인해요.

```bash
$ ssh -T git@github.com
```

처음엔 "접속해도 되는지" 물어봐요. GitHub Docs 에 적힌 지문(fingerprint)과 같은지 확인하고 `yes`. 아래와 비슷한 문장이 나오면 성공이에요(`내아이디` 는 내 GitHub 아이디).

```text
Hi 내아이디! You've successfully authenticated, but GitHub does not provide shell access.
```

## 2단계. 내 저장소 만들기와 clone

1. GitHub 웹에서 **New repository**: 이름 `devenv-course`, **Public**, README 는 **체크하지 않고** 만들어요(빈 저장소).
2. 만든 뒤 보이는 **SSH 주소**(`git@github.com:내아이디/devenv-course.git`)를 복사해요.

```bash
$ cd ~
$ git clone git@github.com:내아이디/devenv-course.git
$ cd devenv-course
```

빈 저장소라는 경고가 나오면 정상이에요(0단계와 같아요). 이제 이 폴더에 이 주의 견본 파일(`calc.py`, `test_calc.py`)을 넣어요. VS Code 로 `code .` 를 열어 새 파일 두 개를 만들고 이 폴더의 내용을 붙여 넣어요. 그리고 시험을 돌려 봐요.

```bash
$ uv run --no-project --with pytest python -m pytest
```

```text
============================= test session starts ==============================
platform linux -- Python 3.x.x, pytest-x.x.x, pluggy-x.x.x
rootdir: /home/jimin/devenv-course
collected 5 items

test_calc.py .....                                                       [100%]

============================== 5 passed in 0.01s ===============================
```

`5 passed` 가 보이면 성공이에요. 버전 숫자는 달라요. 파이썬이 만든 캐시를 기록하지 않게 `.gitignore` 를 같이 만들고 올려요.

```bash
$ printf '__pycache__/\n.pytest_cache/\n.venv/\n' > .gitignore
$ git add .
$ git status --short
```

```text
A  .gitignore
A  calc.py
A  test_calc.py
```

```bash
$ git commit -m "계산기와 시험 추가"
$ git push -u origin main
```

GitHub 의 저장소 웹 페이지를 새로고침해서 파일 세 개가 보이면 성공이에요. (처음 한 번 `git push` 가 `main` 이름을 못 찾는다면 `git branch` 로 지금 브랜치 이름부터 확인해요.)

## 3단계. 브랜치 → PR → 병합

새 기능(거듭제곱)을 **브랜치에서** 만들고 PR 로 합쳐요.

```bash
$ git switch -c feature/power
```

`calc.py` 맨 아래에 함수를 더하고, `test_calc.py` 에 시험도 하나 더해요(`from calc import ...` 줄에 `power` 도 추가).

```python
def power(a, b):
    return a ** b
```

```python
def test_power():
    assert power(2, 3) == 8
```

```bash
$ uv run --no-project --with pytest python -m pytest
$ git add calc.py test_calc.py
$ git commit -m "거듭제곱 함수 power 추가"
$ git push -u origin feature/power
```

```text
branch 'feature/power' set up to track 'origin/feature/power'.
```

(push 출력에 PR 을 만들 수 있는 주소가 나오기도 해요.) 이제 GitHub 웹에서:

1. 저장소 페이지에 뜨는 **Compare & pull request** 를 눌러요(안 보이면 **Pull requests → New pull request**).
2. 제목과 설명을 써요("무엇을, 왜" 한두 줄).
3. 본인 PR 은 본인이 리뷰할 수 있어요. **Files changed** 에서 바뀐 줄을 보고, 줄 옆 `+` 로 댓글을 하나 달아 봐요.
4. **Merge pull request** 를 눌러 합쳐요.

GitHub 에서 합친 뒤, 내 컴퓨터에도 반영해요.

```bash
$ git switch main
$ git pull
$ git log --oneline
```

`main` 에 `거듭제곱 함수 power 추가`(와 병합 커밋)가 보이면 성공이에요.

**친구와 해 보기(선택)**: 친구를 저장소의 **Collaborator** 로 초대하면(Settings → Collaborators) 친구가 clone 해서 브랜치·PR 을 올리고, 내가 리뷰할 수 있어요. 친구가 없다면 3단계처럼 **나 자신과 PR 을 주고받아도** 같은 연습이에요.

## 4단계. 이슈 하나 만들고 PR 로 닫기

저장소의 **Issues → New issue** 에 "나눗셈에서 0 으로 나눌 때 안내 문구 개선" 같은 할 일을 하나 써요. 3단계처럼 브랜치에서 고친 뒤 PR 설명에 `Closes #1`(이슈 번호)을 써 두면, PR 을 합칠 때 이슈가 같이 닫혀요.

## 5단계. GitHub Actions 로 시험 자동 실행

저장소에 `.github/workflows/` 폴더를 만들고 이 폴더의 견본 `.github-workflow-example.yml` 을 `test.yml` 로 복사해요.

```bash
$ git switch -c ci/add-pytest
$ mkdir -p .github/workflows
```

VS Code 로 `.github/workflows/test.yml` 파일을 만들고 `.github-workflow-example.yml` 의 내용을 붙여 넣어요. 그리고 올려요.

```bash
$ git add .github/workflows/test.yml
$ git commit -m "CI: pull request 마다 pytest 실행"
$ git push -u origin ci/add-pytest
```

GitHub 에서 PR 을 만들면 PR 화면 아래쪽에 검사 목록이 떠요. 처음엔 노란 점(실행 중)이고, 잠시 뒤 **초록 체크**가 되면 성공이에요. 저장소 위쪽의 **Actions** 탭에서도 실행 기록이 보여요. 공개 저장소의 표준 러너는 무료예요([GitHub Actions 과금 문서](https://docs.github.com/en/billing/concepts/product-billing/github-actions)).

**일부러 실패시켜 보기**: 같은 브랜치에서 `calc.py` 의 `add` 를 `return a - b` 로 바꾸고 push 해요. 내 컴퓨터에서 시험을 돌려도 같은 결과가 나와요.

```text
test_calc.py F....                                                       [100%]
...
FAILED test_calc.py::test_add - assert -1 == 5
========================= 1 failed, 4 passed in 0.01s ==========================
```

GitHub PR 에도 **빨간 X** 가 떠요. 다시 `return a + b` 로 고쳐서 push 하면 초록으로 돌아와요. 초록이 된 PR 을 합쳐요.

> 견본의 `actions/checkout@v7`, `actions/setup-python@v7` 의 `@v7` 은 "이 도구의 7 번대 최신" 이라는 뜻이에요. 2026-03 에 보안 도구 Trivy 의 GitHub Action 태그가 변조된 공급망 사고가 있었어요([Aqua 블로그](https://www.aquasec.com/blog/trivy-supply-chain-attack/)). 그래서 중요한 저장소에서는 이런 이름표(태그) 대신 **커밋 번호로 고정**하는 걸 권장해요.

## 6단계. fork 맛보기(선택)

남의 공개 저장소에는 내가 직접 push 할 수 없어요. 그때 **fork**(내 계정으로 저장소를 복사)해서 고치고, 원래 저장소로 PR 을 보내요.

1. 친구(또는 강좌 운영자가 알려 준 연습용) 공개 저장소에서 **Fork** 를 눌러요.
2. 내 fork 를 clone 해요: `git clone git@github.com:내아이디/저장소이름.git`
3. 원본을 `upstream` 이라는 이름으로 등록해 두면 최신 변경을 받을 수 있어요.

```bash
$ git remote add upstream git@github.com:원본주인/저장소이름.git
$ git remote -v
```

```text
origin	git@github.com:내아이디/저장소이름.git (fetch)
origin	git@github.com:내아이디/저장소이름.git (push)
upstream	git@github.com:원본주인/저장소이름.git (fetch)
upstream	git@github.com:원본주인/저장소이름.git (push)
```

4. 브랜치에서 고쳐 내 fork 에 push 하고, GitHub 에서 **Compare & pull request** 로 원본에 PR 을 보내요.

## 정리

`devenv-course` 저장소는 **계속 쓸 거예요**(이후 주차 결과물을 쌓아요). 0단계의 `remote-lab` 은 지워도 돼요.
