# 12주 계획표

주 6~8시간(읽기 2 · 실습 3~4 · 문제·정리 1~2)을 기준으로 잡았어요.

| 주 | 주제 | 이번 주 결과물 | 실습 장소 |
|---|---|---|---|
| [0](../weeks/week00.md) | 터미널과 WSL — Windows Terminal, WSL2 Ubuntu, VS Code, 파일 경로 | WSL 안에서 `hello.py` 실행 | PC |
| **1부 Git·GitHub** | | | |
| [1](../weeks/week01.md) | Git 첫걸음 — 저장소, 스테이징, 커밋, 로그, 되돌리기, `.gitignore` | 커밋 10개로 기록한 내 프로젝트 | WSL |
| [2](../weeks/week02.md) | 브랜치와 병합 — 브랜치, merge, 충돌 해결, rebase 는 조심히 | 충돌을 직접 만들고 풀기 | WSL |
| [3](../weeks/week03.md) | GitHub 로 함께 일하기 — 원격 저장소, SSH 키, PR·리뷰·이슈, GitHub Actions 맛보기 | 친구(또는 나 자신)와 PR 주고받기 + 시험 자동 실행 | WSL + GitHub |
| **2부 Linux** | | | |
| [4](../weeks/week04.md) | 셸과 파일 시스템 — 디렉터리 구조, 경로, 파일 다루기, 파이프·리다이렉션, grep·find | 로그 파일에서 오류만 골라내기 | WSL |
| [5](../weeks/week05.md) | 권한·프로세스·서비스 — 사용자·그룹·권한, 프로세스·신호, 패키지(apt), systemd | 내 파이썬 앱을 서비스로 띄우기 | WSL |
| [6](../weeks/week06.md) | 원격 접속과 자동화 — SSH, 셸 스크립트, cron, 환경 변수, 로그 | 매일 백업하는 스크립트 | WSL |
| **3부 Docker** | | | |
| [7](../weeks/week07.md) | 컨테이너와 이미지 — 가상머신과 차이, 이미지·컨테이너·레지스트리, 생명주기 | 공식 이미지로 웹 서버 띄우고 지우기 | Docker |
| [8](../weeks/week08.md) | Dockerfile 과 빌드 — 레이어·캐시, `.dockerignore`, 멀티스테이지, uv 로 파이썬 앱 | 내 FastAPI 앱 이미지(작고 빠르게) | Docker |
| [9](../weeks/week09.md) | 볼륨·네트워크·설정 — 데이터 남기기, 백업, 포트·네트워크, 환경 변수·비밀값 | DB 데이터가 컨테이너를 지워도 남기 | Docker |
| [10](../weeks/week10.md) | Compose 로 여러 서비스 — `compose.yaml`, 의존·헬스체크·준비 상태, 재시작 정책 | API + DB 한 번에 띄우기 | Docker |
| **4부 ML 컨테이너 운영** | | | |
| [11](../weeks/week11.md) | 배포·보안·자원·GPU — 레지스트리에 올리기, 태그 규칙, 이미지 점검·SBOM, root 로 돌리지 않기, CPU·메모리 제한, GPU 컨테이너 | 내 이미지를 레지스트리에 올리고 점검표 통과 | Docker + GitHub |
| [12](../weeks/week12.md) | **종합 프로젝트** — ML 추론 서비스를 컨테이너로: Dockerfile → Compose → CI 자동 빌드 → 레지스트리 → 다른 컴퓨터에서 실행 | 데모 + README(넘겨주기 문서) | 전부 |

## 12주가 길다면

0·1주를 합치고, 5·6주를 합치고, 11주는 보안·자원 부분만 봐도 돼요.
