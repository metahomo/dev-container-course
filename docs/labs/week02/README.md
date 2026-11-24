# 2주 실습: 브랜치, 병합, 그리고 충돌 풀기

**장소**: WSL(또는 Mac 터미널) · **예상 시간**: 3시간 · **결과물**: 브랜치 병합 두 가지(fast-forward, 3-way)와 **직접 만들고 푼 충돌 1건**

> `$` 는 치지 않아요. 커밋 번호(7글자)는 사람마다 달라요. 출력은 영어 기준이에요. 1주차 Git 설정(`user.name` 등)이 끝나 있어야 해요.

## 1부. 병합 두 가지 맛보기

### 1단계. 연습 저장소

```bash
$ mkdir story && cd story
$ git init
$ echo "첫 문장" > story.md
$ git add story.md
$ git commit -m "첫 문장"
$ git branch
```

```text
* main
```

`*` 는 지금 있는 브랜치예요.

### 2단계. 브랜치를 만들고 커밋 — fast-forward 병합

```bash
$ git switch -c feature/ending
$ echo "결말" >> story.md
$ git commit -am "결말 추가"
$ git log --oneline --graph --all
```

```text
Switched to a new branch 'feature/ending'
* 7813008 결말 추가
* 6dbd4b4 첫 문장
```

(`-am` 은 **이미 추적 중인 파일**의 변경을 add 와 commit 을 한꺼번에 해요. 새 파일은 따로 `git add` 해야 해요.)

`main` 으로 돌아와 합쳐요.

```bash
$ git switch main
$ git merge feature/ending
```

```text
Switched to branch 'main'
Updating 6dbd4b4..7813008
Fast-forward
 story.md | 1 +
 1 file changed, 1 insertion(+)
```

`Fast-forward` 가 보이면 성공이에요. `main` 이 그동안 안 움직였으니 이름표만 앞으로 옮겨졌어요. 다 쓴 브랜치는 지워요.

```bash
$ git branch -d feature/ending
```

```text
Deleted branch feature/ending (was 7813008).
```

### 3단계. 양쪽이 다 움직인 뒤 병합 — 3-way

```bash
$ git switch -c feature/title
$ echo "제목" > title.md
$ git add title.md
$ git commit -m "제목 파일"
$ git switch main
$ echo "본문" >> story.md
$ git commit -am "본문 추가"
$ git merge feature/title -m "feature/title 병합"
```

```text
Merge made by the 'ort' strategy.
 title.md | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 title.md
```

(`'ort'` 는 병합 방식 이름이에요. 신경 쓰지 않아도 돼요.) 그림으로 봐요.

```bash
$ git log --oneline --graph
```

```text
*   bcf2d2c feature/title 병합
|\
| * 86d0937 제목 파일
* | 5256e4b 본문 추가
|/
* 7813008 결말 추가
* 6dbd4b4 첫 문장
```

가지가 갈라졌다 다시 합쳐지는 모양이 보이면 성공이에요. 합친 자리의 커밋(맨 위)을 **병합 커밋**이라고 해요.

## 2부. 충돌을 만들고 풀기

충돌 상황을 손으로 만들면 번거로워서, 스크립트가 대신 만들어 줘요. 이 폴더의 `conflict-lab.sh` 를 내 컴퓨터로 가져와요(VS Code 로 새 파일 `conflict-lab.sh` 를 만들어 내용을 붙여 넣으면 돼요). 스크립트는 길지 않으니 **먼저 열어서 읽어 봐요.** 읽지 않은 스크립트를 실행하는 건 나쁜 습관이에요.

### 4단계. 충돌 실습장 만들기

```bash
$ cd ~
$ bash conflict-lab.sh
```

이렇게 나오면 성공 — 마지막에 `CONFLICT` 가 보여요.

```text
--- git merge casual ---
Auto-merging greet.py
CONFLICT (content): Merge conflict in greet.py
Automatic merge failed; fix conflicts and then commit the result.

충돌 실습장이 준비됐어요: /home/jimin/conflict-lab
다음: git status 로 상태를 보고, greet.py 를 열어 충돌 표시를 풀어 보세요.
```

(스크립트가 한 일: `main` 에서 `greet.py` 를 만들고, `formal` 과 `casual` 두 브랜치가 **같은 줄**을 서로 다르게 고친 뒤 합쳤어요.)

### 5단계. 상태 읽기

```bash
$ cd conflict-lab
$ git status
```

```text
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   greet.py

no changes added to commit (use "git add" and/or "git commit -a")
```

`both modified: greet.py` 가 "양쪽이 다 고쳤다" 는 뜻이에요. 도망갈 길도 있어요: `git merge --abort` 는 병합을 시작하기 전으로 돌려놔요. 지금은 풀어 봐요.

### 6단계. 충돌 표시 읽기

```bash
$ cat greet.py
```

```text
def greet(name):
<<<<<<< HEAD
    return "Good day, " + name
=======
    return "Hey, " + name
>>>>>>> casual


print(greet("Git"))
```

- `<<<<<<< HEAD` 와 `=======` 사이: **내 쪽**(지금 있는 `main`, 격식 있는 인사)
- `=======` 와 `>>>>>>> casual` 사이: **들어오는 쪽**(`casual`)

### 7단계. 직접 풀기

VS Code 로 `greet.py` 를 열어요(`code greet.py`). 두 줄 중 하나를 고르거나 새로 쓰고, **`<<<<<<<`, `=======`, `>>>>>>>` 표시 줄을 모두 지워요.** 여기서는 격식 있는 쪽으로 정해요.

```python
def greet(name):
    return "Good day, " + name


print(greet("Git"))
```

파이썬으로 돌아가는지 확인하고, 해결했다고 Git 에 알려요.

```bash
$ python3 greet.py
$ git add greet.py
$ git status
```

```text
Good day, Git
On branch main
All conflicts fixed but you are still merging.
  (use "git commit" to conclude merge)
```

`All conflicts fixed` 가 보이면 성공이에요. (표시 줄을 하나라도 남기고 `git add` 하면 파이썬이 오류를 내요. Git 2.56 이상은 `git add --resolved greet.py` 로 하면 표시가 남은 파일을 거부해 줘요. 버전은 `git --version` 으로 봐요.)

### 8단계. 병합 끝내기

```bash
$ git commit -m "충돌 해결: 격식 있는 인사말로 통일"
$ git log --oneline --graph
```

```text
[main 98d850f] 충돌 해결: 격식 있는 인사말로 통일
*   98d850f 충돌 해결: 격식 있는 인사말로 통일
|\
| * 4932744 인사말을 편하게 변경
* | 133fa3f 인사말을 격식 있게 변경
|/
* cae6b16 greet.py 추가
```

그림에 갈라졌다 합쳐진 모양이 있으면 성공이에요. 맨 위 커밋이 병합 커밋이에요. 한 번 더 연습하려면 `conflict-lab` 폴더를 지우고(`cd ~ && rm -r conflict-lab`) 4단계부터 다시 해요. 이번엔 `casual` 쪽을 골라 보세요.

## 3부. rebase — "내 것만" 연습

`story` 폴더(1부)에서 해요. `feature/x` 브랜치를 만든 뒤 `main` 이 한 번 더 움직인 상황이에요.

```bash
$ cd ~/story
$ git switch -c feature/x
$ echo "x" > x.md
$ git add x.md
$ git commit -m "x 추가"
$ git switch main
$ echo "m" >> story.md
$ git commit -am "main 한 줄 더"
$ git switch feature/x
$ git rebase main
```

```text
Switched to a new branch 'feature/x'
Switched to branch 'main'
Switched to branch 'feature/x'
Successfully rebased and updated refs/heads/feature/x.
```

(중간에 `Rebasing (1/1)` 줄이 보일 수 있어요.) 역사를 봐요.

```bash
$ git log --oneline --graph --all
```

```text
* e6668f3 x 추가
* 91d29ec main 한 줄 더
*   bcf2d2c feature/title 병합
...
```

가지가 갈라진 모양 없이 **한 줄**로 쭉 이어지면 성공이에요. `feature/x` 의 커밋 `x 추가` 가 `main` 의 최신 위에 **다시 만들어졌어요**(번호가 새로 붙어요). 이게 rebase 예요. 이제 `main` 은 fast-forward 로 합쳐져요.

```bash
$ git switch main
$ git merge --ff-only feature/x
```

```text
Updating 91d29ec..e6668f3
Fast-forward
 x.md | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 x.md
```

!!! warning "rebase 는 내 것만"
    이 실습의 `feature/x` 는 나만 쓰는 브랜치라 안전해요. **이미 남이 받아 간(공유한) 커밋은 rebase 하지 않아요.** 번호가 바뀌어서 남의 기록과 어긋나요. 3주차에서 이유를 다시 봐요.

## 정리

`cd ~ && rm -r story conflict-lab` 으로 지워도 돼요.
