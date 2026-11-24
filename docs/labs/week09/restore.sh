#!/usr/bin/env bash
# 사용법: ./restore.sh 백업파일.tgz 새볼륨이름
# 백업 파일의 내용을 (새) 볼륨에 풀어요.
set -euo pipefail

FILE="${1:?백업 파일을 적어 주세요}"
VOLUME="${2:?복원할 볼륨 이름을 적어 주세요}"

[ -f "$FILE" ] || { echo "파일이 없어요: $FILE" >&2; exit 1; }

docker volume create "$VOLUME" >/dev/null
docker run --rm \
  -v "${VOLUME}:/data" \
  -v "$(cd "$(dirname "$FILE")" && pwd):/backup:ro" \
  alpine tar xzf "/backup/$(basename "$FILE")" -C /data

echo "복원 완료: ${VOLUME}"
