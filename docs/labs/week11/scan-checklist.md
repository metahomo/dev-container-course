# 이미지 점검표

이미지 하나를 레지스트리에 올리기 **전에** 이 표를 채워요. ○ 통과 · × 미통과(이유 적기) · △ 해당 없음. 도구가 없어도 "손으로 확인" 열만으로 대부분 채울 수 있어요.

- 점검한 이미지: `ghcr.io/______/______:______`
- 날짜: ________ 점검한 사람: ________

## A. 이름과 태그

| # | 점검 | 손으로 확인 | 결과 |
|---|---|---|---|
| A1 | 태그가 `latest` 하나뿐이 아니다 (버전 `0.1.0` 또는 `sha-...` 가 있다) | `docker images` | |
| A2 | 이름이 모두 소문자이고 소유자가 내 계정이다 | 이름 눈으로 확인 | |
| A3 | `FROM` 의 베이스 이미지에 태그가 있다 (`FROM python` 처럼 태그 없음은 ×) | Dockerfile | |
| A4 | 베이스 이미지 태그가 `latest` 가 아니다 | Dockerfile | |

## B. 비밀값과 내용

| # | 점검 | 손으로 확인 | 결과 |
|---|---|---|---|
| B1 | `.env`, 토큰, 키 파일이 이미지에 없다 | `docker run --rm 이미지 ls -a /app` | |
| B2 | `.dockerignore` 에 `.git`, `.venv`, `.env` 가 있다 | 파일 열기 | |
| B3 | 비밀값을 `ENV`/`ARG`/`RUN echo` 로 박지 않았다 | `docker image history --no-trunc 이미지` 에서 검색 | |
| B4 | 개발용 도구(테스트, 컴파일러)가 최종 이미지에 없다 (멀티스테이지) | Dockerfile 의 `FROM` 개수 | |

## C. 실행 방식

| # | 점검 | 손으로 확인 | 결과 |
|---|---|---|---|
| C1 | root 가 아닌 사용자로 실행한다 | `docker image inspect 이미지 --format '{{.Config.User}}'` 가 비어 있지 않다 | |
| C2 | `--read-only` 로 돌려도 앱이 동작한다 (쓸 곳은 tmpfs/볼륨) | `docker run --rm --read-only ...` | |
| C3 | `--cap-drop ALL` 로 돌려도 앱이 동작한다 | `docker run --rm --cap-drop ALL ...` | |
| C4 | 헬스체크가 있다 (`HEALTHCHECK` 또는 compose `healthcheck`) | `docker ps` 의 STATUS 에 `(healthy)` | |
| C5 | 메모리·CPU 제한을 걸어 돌려 봤다 | [resource-limits.md](resource-limits.md) | |

## D. 취약점과 부품 목록

| # | 점검 | 도구 | 결과 |
|---|---|---|---|
| D1 | 취약점 요약을 한 번 봤고, 심각도 높음(High/Critical)의 개수를 적었다: ____ | `docker scout quickview 이미지` | |
| D2 | 베이스 이미지를 최신 패치 태그로 올리면 줄어드는지 확인했다 | `docker scout quickview` 의 베이스 이미지 제안 | |
| D3 | (선택) SBOM(소프트웨어 부품 목록)을 파일로 뽑아 저장했다 | `syft 이미지 -o spdx-json=./sbom.json` | |

!!! warning "점검 도구도 공격받아요"
    2026-03 에 이미지 점검 도구 Trivy 의 배포물이 변조된 사건이 있었어요(악성 v0.69.4 바이너리, GitHub Action 태그 변조, Docker Hub 이미지 변조). 그래서 도구를 받을 때도 같은 원칙을 써요: **버전 고정, 가능하면 다이제스트·커밋 해시 고정, 설치 스크립트를 파이프로 바로 실행하지 않기.** 출처는 [GitHub 보안 권고 GHSA-69fq-xp46-6x23](https://github.com/aquasecurity/trivy/security/advisories/GHSA-69fq-xp46-6x23) 이에요.

## E. 공급망(만들고 올리는 과정)

| # | 점검 | 손으로 확인 | 결과 |
|---|---|---|---|
| E1 | CI 의 외부 Action 이 `@main`/`@v1` 이 아니라 **커밋 해시**로 고정돼 있다 | `.github/workflows/*.yml` 의 `uses:` | |
| E2 | CI 가 쓰는 권한이 최소다 (`permissions:` 를 적고, push 하는 작업에만 `packages: write`) | 워크플로 파일 | |
| E3 | 토큰을 파일·저장소에 두지 않았다 (`GITHUB_TOKEN` 또는 환경 변수) | `git grep -i token` | |

## 결과

- × 가 있는 항목과 고친 방법:

| 항목 | 이유 | 고친 방법 |
|---|---|---|
| | | |

- 최종 판정: 올려도 된다 / 고친 뒤 다시 점검
