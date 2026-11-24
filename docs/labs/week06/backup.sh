#!/usr/bin/env bash
# 6주 실습: 폴더 하나를 날짜가 붙은 tar.gz 로 백업하고, 오래된 백업은 지워요.
# 사용법: ./backup.sh 백업할폴더 백업둘폴더 [남길개수]
#   예)   ./backup.sh ~/lab06/data ~/lab06/backups 3
# 로그: 백업둘폴더/backup.log 에 한 줄씩 남겨요.

set -euo pipefail   # 오류가 나면 멈춤(-e), 없는 변수는 오류(-u), 파이프 중간 실패도 오류(-o pipefail)

# --- 1. 인자 확인 ------------------------------------------------------
usage() {
    echo "사용법: $0 백업할폴더 백업둘폴더 [남길개수]" >&2
    exit 2
}

[ "$#" -ge 2 ] || usage

SRC="$1"
DEST="$2"
KEEP="${3:-5}"          # 세 번째 인자가 없으면 5

if [ ! -d "$SRC" ]; then
    echo "오류: 백업할 폴더가 없어요: $SRC" >&2
    exit 1
fi

mkdir -p "$DEST"
LOG="$DEST/backup.log"

# --- 2. 로그 남기기 ----------------------------------------------------
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') $*" >> "$LOG"
}

# --- 3. 백업 만들기 ----------------------------------------------------
STAMP="$(date +%Y%m%d-%H%M%S)"
NAME="$(basename "$SRC")"
FILE="$DEST/${NAME}-${STAMP}.tar.gz"

log "시작: $SRC -> $FILE"
tar -czf "$FILE" -C "$(dirname "$SRC")" "$NAME"
log "완료: $(basename "$FILE")"
echo "백업 완료: $FILE"

# --- 4. 오래된 백업 지우기 (최근 KEEP 개만 남김) -----------------------
# 파일 이름에 날짜·시각(YYYYMMDD-HHMMSS)이 들어 있어 이름 순서 = 시간 순서다.
# ls 결과를 for 로 돌리면 이름에 공백이 있을 때 깨지므로, 글로브를 배열로 받는다.
shopt -s nullglob
BACKUPS=("$DEST"/"${NAME}"-*.tar.gz)
TOTAL=${#BACKUPS[@]}
for ((i = 0; i < TOTAL - KEEP; i++)); do
    old="${BACKUPS[$i]}"
    rm -- "$old"
    log "삭제: $(basename "$old")"
done
