#!/usr/bin/env bash
# 충돌 실습장을 자동으로 만들어요.
# 사용법: bash conflict-lab.sh [폴더이름]   (기본 폴더 이름: conflict-lab)
# 끝나면 그 폴더 안에서 "병합 충돌" 상태로 멈춰 있어요. 풀어 보는 건 여러분 몫이에요.

set -euo pipefail

DIR="${1:-conflict-lab}"

if [ -e "$DIR" ]; then
    echo "이미 '$DIR' 이(가) 있어요. 지우거나 다른 이름을 쓰세요: bash conflict-lab.sh 다른이름" >&2
    exit 1
fi

mkdir "$DIR"
cd "$DIR"

# 이 폴더 안에서만 쓰는 설정이에요. (전역 설정은 건드리지 않아요.)
git init -q -b main
git config user.name  "${GIT_AUTHOR_NAME:-$(git config --global user.name || echo student)}"
git config user.email "${GIT_AUTHOR_EMAIL:-$(git config --global user.email || echo student@example.com)}"

# 1) main: 인사 함수 하나
cat > greet.py <<'PY'
def greet(name):
    return "Hello, " + name


print(greet("Git"))
PY
git add greet.py
git commit -q -m "greet.py 추가"

# 2) formal 브랜치: 같은 줄을 격식 있게 바꿈
git switch -q -c formal
sed 's/"Hello, "/"Good day, "/' greet.py > greet.tmp && mv greet.tmp greet.py
git commit -q -am "인사말을 격식 있게 변경"

# 3) casual 브랜치: main 에서 갈라져 같은 줄을 편하게 바꿈
git switch -q main
git switch -q -c casual
sed 's/"Hello, "/"Hey, "/' greet.py > greet.tmp && mv greet.tmp greet.py
git commit -q -am "인사말을 편하게 변경"

# 4) main 에 formal 을 합침 (main 은 그동안 안 움직였으니 fast-forward)
git switch -q main
git merge -q formal

# 5) casual 을 합치면 같은 줄이 서로 달라서 충돌
echo "--- git merge casual ---"
git merge casual || true

echo
echo "충돌 실습장이 준비됐어요: $(pwd)"
echo "다음: git status 로 상태를 보고, greet.py 를 열어 충돌 표시를 풀어 보세요."
