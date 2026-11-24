# 1주 실습: 커밋 10개로 기록하는 내 프로젝트

**장소**: WSL(또는 Mac 터미널) · **예상 시간**: 3시간 · **결과물**: `~/git-lab` 저장소와 `git log --oneline` 에 커밋 10개

> `$` 는 치지 않아요. **커밋 번호(`4093c97` 같은 7글자)와 날짜는 사람마다 달라요.** 나머지 글이 같으면 성공이에요. 출력은 영어 기준이에요(한국어 설정이면 같은 뜻의 한국어로 나와요).
> 이 폴더의 `greet.py` 와 `gitignore.example` 은 아래 단계에서 만들 파일의 견본이에요.

## 1단계. Git 설정 (딱 한 번)

```bash
$ git config --global user.name "내이름"
$ git config --global user.email "내메일@example.com"
$ git config --global init.defaultBranch main
$ git config --global --list
```

이렇게 나오면 성공 (이름·메일은 내가 쓴 값):

```text
user.name=내이름
user.email=내메일@example.com
init.defaultbranch=main
```

`defaultbranch` 가 소문자로 보이는 건 정상이에요. 메일은 3주차에 GitHub 에 쓸 메일과 같게 해 두면 편해요.

## 2단계. 저장소 만들기

```bash
$ mkdir git-lab
$ cd git-lab
$ git init
$ git status
```

```text
Initialized empty Git repository in /home/jimin/git-lab/.git/
On branch main

No commits yet

nothing to commit (create/copy files and use "git add" to track)
```

`On branch main` 이 보이면 성공이에요. `master` 라고 나오면 1단계의 `init.defaultBranch` 설정이 빠진 거예요 — `git branch -m main` 으로 이름을 바꿔요.

## 3단계. 첫 커밋

```bash
$ echo "# 내 첫 저장소" > README.md
$ git status
```

```text
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	README.md

nothing added to commit but untracked files present (use "git add" to track)
```

```bash
$ git add README.md
$ git status
```

```text
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   README.md

```

```bash
$ git commit -m "README 추가"
$ git log --oneline
```

```text
[main (root-commit) 4093c97] README 추가
 1 file changed, 1 insertion(+)
 create mode 100644 README.md
4093c97 README 추가
```

## 4단계. 파일 하나 더 — 두 번째 커밋

`greet.py` 를 만들어요(VS Code 로 열어서 써도 돼요: `code .`).

```bash
$ cat > greet.py <<'EOF'
def greet(name):
    return "안녕, " + name


print(greet("Git"))
EOF
$ git add greet.py
$ git commit -m "인사 함수 greet.py 추가"
```

```text
[main 5b6ea4c] 인사 함수 greet.py 추가
 1 file changed, 5 insertions(+)
 create mode 100644 greet.py
```

## 5단계. 고치고 `diff` 로 비교하기

`"안녕, "` 을 `"반갑다, "` 로 바꿔요. (VS Code 에서 고쳐도 되고, 아래 명령도 돼요. Mac 의 `sed` 는 달라서 `sed -i ''` 로 써야 해요 — Mac 은 VS Code 로 고치는 쪽이 쉬워요.)

```bash
$ sed -i 's/안녕, /반갑다, /' greet.py
$ git diff
```

```text
diff --git a/greet.py b/greet.py
index 10dda6c..06f9964 100644
--- a/greet.py
+++ b/greet.py
@@ -1,5 +1,5 @@
 def greet(name):
-    return "안녕, " + name
+    return "반갑다, " + name
 
 
 print(greet("Git"))
```

`-` 줄이 지워진 것, `+` 줄이 새로 생긴 것이에요. 이제 스테이징 영역에 올리면 `git diff` 가 **빈 화면**이 되고, `--staged` 로 봐야 보여요.

```bash
$ git add greet.py
$ git diff
$ git diff --staged
```

첫 `git diff` 는 아무것도 안 나오고, `git diff --staged` 는 위와 같은 내용이 나오면 성공이에요. 커밋해요.

```bash
$ git commit -m "인사말을 반갑다로 변경"
```

```text
[main 00ee6bf] 인사말을 반갑다로 변경
 1 file changed, 1 insertion(+), 1 deletion(-)
```

## 6단계. 되돌리기 ① — 아직 커밋 안 한 변경 버리기 (`restore`)

일부러 망쳐 봐요.

```bash
$ echo "망친 내용" > greet.py
$ git status --short
```

```text
 M greet.py
```

```bash
$ git restore greet.py
$ cat greet.py
```

```text
def greet(name):
    return "반갑다, " + name


print(greet("Git"))
```

`restore` 는 **커밋 안 한 변경을 완전히 버려요(되살릴 수 없어요).** 한 번 더 생각하고 쳐요.

스테이징만 취소하는 연습도 해요. `greet.py` 를 한 번 고치고 올렸다가 내려요.

```bash
$ echo "# 메모" >> greet.py
$ git add greet.py
$ git restore --staged greet.py
$ git status --short
```

```text
 M greet.py
```

(파일 내용은 그대로 두고 스테이징에서만 내려가요.) 이 변경도 버려요: `git restore greet.py`.

## 7단계. `.gitignore`

기록하면 안 되는 파일을 만들어 봐요(비밀번호가 든 `.env`, 파이썬이 만드는 `__pycache__`).

```bash
$ mkdir -p __pycache__
$ echo x > __pycache__/a.pyc
$ echo "SECRET=1" > .env
$ git status --short
```

```text
?? .env
?? __pycache__/
```

무시할 목록을 만들어요. (견본: 이 폴더의 `gitignore.example`)

```bash
$ printf '__pycache__/\n.env\n*.pyc\n' > .gitignore
$ git status --short
```

```text
?? .gitignore
```

`.env` 와 `__pycache__/` 가 목록에서 사라지고 `.gitignore` 만 남으면 성공이에요. `.gitignore` 자체는 기록해요.

```bash
$ git add .gitignore
$ git commit -m ".gitignore 추가"
```

## 8단계. 되돌리기 ② — 커밋을 취소하는 새 커밋 (`revert`)

방금 커밋을 취소하는 커밋을 만들어요.

```bash
$ git revert --no-edit HEAD
$ git log --oneline
```

```text
[main a1e955a] Revert ".gitignore 추가"
 1 file changed, 3 deletions(-)
 delete mode 100644 .gitignore
a1e955a Revert ".gitignore 추가"
1a488d8 .gitignore 추가
00ee6bf 인사말을 반갑다로 변경
5b6ea4c 인사 함수 greet.py 추가
4093c97 README 추가
```

(출력 중간에 `Date:` 줄이 하나 더 보일 수 있어요.) 기록은 지워지지 않고 "취소했다" 는 기록이 **더해졌어요.** 이게 `revert` 예요. 취소를 다시 취소하는 것도 같은 방법(`git revert HEAD`)으로 돼요.

## 9단계. (조심) `reset --hard` 체험

**연습용 저장소에서만 해요.** 방금 만든 커밋 2개(`.gitignore 추가` 와 그 취소)를 없애 봐요.

```bash
$ git reset --hard HEAD~2
$ git log --oneline
```

```text
HEAD is now at 00ee6bf 인사말을 반갑다로 변경
00ee6bf 인사말을 반갑다로 변경
5b6ea4c 인사 함수 greet.py 추가
4093c97 README 추가
```

커밋이 사라진 것처럼 보이지만 Git 이 최근 이동을 잠시 기억해요.

```bash
$ git reflog
```

```text
00ee6bf HEAD@{0}: reset: moving to HEAD~2
a1e955a HEAD@{1}: revert: Revert ".gitignore 추가"
...
```

되살리려면 `git reset --hard <reflog 에 보이는 번호>` 예요. 하지만 이건 **커밋 안 한 변경까지 지워요.** 평소에는 `restore` 와 `revert` 만 써요.

## 10단계. 도전: 커밋 10개 채우기

9단계 뒤 `git log --oneline` 에는 커밋이 3개 있어요. 작은 프로젝트(예: 구구단 출력, 할 일 목록)를 `git-lab` 안에 만들면서 **의미 단위로** 커밋해 10개를 채워요. 규칙:

1. 한 커밋 = 한 가지 일. (함수 하나 추가, 오타 수정…)
2. 메시지는 "무엇을 했나" 를 한 줄로.
3. 커밋 전에 `git status` 와 `git diff --staged` 로 내가 올린 것을 확인해요.
4. 9단계로 `.gitignore` 가 사라졌으니, 7단계처럼 다시 만들어 커밋해요. `.env` 같은 비밀 파일은 `.gitignore` 에 있어야 해요.

마지막 확인:

```bash
$ git log --oneline | wc -l
$ git status
```

앞의 숫자가 `10` 이상이고, `git status` 가 `nothing to commit, working tree clean` 이면 성공이에요.

## 정리

`git-lab` 은 3주차까지 계속 써도 되고 지워도 돼요(`cd ~ && rm -r git-lab`).
