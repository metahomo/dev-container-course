#!/usr/bin/env bash
# 사용법: ./backup.sh 볼륨이름 [백업폴더]
# 볼륨 안의 파일을 .tgz 하나로 묶어요. (DB 는 멈춘 뒤에 하세요)
set -euo pipefail

VOLUME="${1:?볼륨 이름을 적어 주세요. 예: ./backup.sh pgdata}"
DEST="${2:-./backup}"
FILE="${VOLUME}-$(date +%Y%m%d-%H%M%S).tgz"

mkdir -p "$DEST"
# 볼륨을 읽기 전용(:ro)으로 붙이고, 내 폴더를 /backup 으로 붙여서 tar 로 묶어요
docker run --rm \
  -v "${VOLUME}:/data:ro" \
  -v "$(cd "$DEST" && pwd):/backup" \
  alpine tar czf "/backup/${FILE}" -C /data .

echo "백업 완료: ${DEST}/${FILE}"
