# 교재와 자료

이 강좌는 교재 한 권을 따라가지 않아요. 대신 **공개 자료를 먼저·같이·나중에** 나눠 안내해요. 모두 2026-11-24 조사 기준이고, 확인하지 못한 건 "확인 필요"라고 적었어요.

## 1. 먼저 읽을 것

처음 시작할 때 가장 도움이 되는 자료예요.

| 자료 | 언어 | 무료 | 왜 먼저인가 | 출처 |
|---|---|---|---|---|
| [Microsoft WSL 설치 문서](https://learn.microsoft.com/en-us/windows/wsl/install) | 영어(한국어판 있는지 확인 필요) | 예 | 0주 준비의 기준 문서(2026-06-02 갱신) | 직접 열람 |
| [GitHub Docs 한국어 "헬로 월드"](https://docs.github.com/ko/get-started/start-your-journey/hello-world) | 한국어 | 예 | GitHub 첫걸음을 한국어 공식 글로 | 직접 열람 |
| [Pro Git 2판 한국어판](https://git-scm.com/book/ko/v2) 1~3장 | 한국어 | 예(CC BY-NC-SA 3.0) | Git 개념의 표준 책. 1~3장만 필수 | 직접 열람 |
| [The Linux Command Line](https://www.linuxcommand.org/tlcl.php) 1~10장 | 영어 | 예(무료 PDF, CC BY-NC-ND 3.0) | 셸 명령의 정석. 인터넷 판은 7판(release 25.12) | 직접 열람 |

## 2. 같이 볼 것

해당 주차를 공부하는 동안 옆에 펴 두세요.

| 자료 | 언어 | 무료 | 쓰임 | 출처 |
|---|---|---|---|---|
| [GitHub Skills — Introduction to GitHub](https://github.com/skills/introduction-to-github) | 영어 | 예(공개 저장소) | 브라우저로 1시간 안쪽의 실습. 새 안내 주소(learn.github.com/skills)의 코스 목록은 확인하지 못했어요 | 검색·저장소 확인 |
| [생활코딩 "지옥에서 온 Git"](https://opentutorials.org/course/2708) | 한국어 | 공개 | 원리 설명이 좋아요. 2019-12 글이고, 쪽에 "GITn 시리즈로 대체"라고 적혀 있어요. 신판의 위치는 확인 필요 | 직접 열람 |
| [Linux Journey](https://labex.io/linuxjourney) | 영어 | 예(계정 선택) | 브라우저로 하는 Linux 연습. linuxjourney.com 은 LabEx 로 옮겼어요 | 검색 |
| [uv 문서](https://docs.astral.sh/uv/) · [uv Docker 가이드](https://docs.astral.sh/uv/guides/integration/docker/) | 영어 | 예 | 8주 Dockerfile 실습의 기준(바이너리 복사, 캐시 마운트, 멀티스테이지) | 직접 열람 |
| [Docker 공식 문서](https://docs.docker.com/get-started/) | 영어 | 예 | 2026-11-19 개편으로 첫 길이 AI 에이전트용 "Docker Sandboxes" 가 됐어요. 입문은 Guides 쪽 실습이 더 맞아요 | 직접 열람 |
| [Docker 가이드: 컨테이너 시작](https://docs.docker.com/guides/lab-container-getting-started/) | 영어 | 예 | Docker Desktop 확장(Labspaces)으로 하는 실습. Desktop 4.10 이상 필요 | 검색 |
| [Compose 역사 문서](https://docs.docker.com/compose/intro/history/) | 영어 | 예 | `version:` 키가 무시된다는 근거 등 | 직접 열람 |
| [containers.dev](https://containers.dev/) | 영어 | 예 | 12주 프로젝트의 `devcontainer.json` | 검색 |

## 3. 나중에 볼 것

강좌를 마친 뒤 깊이 들어가고 싶을 때 보세요.

| 자료 | 언어 | 비고 |
|---|---|---|
| [MIT Missing Semester 2026](https://missing.csail.mit.edu/2026) | 영어(영상) | 2026-01 강의. 셸·Git 등. 속도가 빨라요 |
| Pro Git 나머지 장 | 한국어 | 한국어판의 마지막 릴리스는 2023-01로, 영어 원본(2026-05)보다 3년가량 뒤져요 |
| 처음부터 제대로 배우는 도커/쿠버네티스(제이펍, 개정신판 2025-09) | 한국어, 유료 | 627쪽(서점 페이지 기준). 분량이 커요 |
| 개발자를 위한 쉬운 도커(위키북스, 2025-03) | 한국어, 유료 | 확인 필요: 내용이 이 강좌와 얼마나 맞는지는 직접 읽어 보지 않았어요 |
| Docker Deep Dive(Nigel Poulton) | 영어, 유료 | 2026 판이 있는지 확인 필요 |
| 쿠버네티스 공식 문서([한국어 블로그 포함](https://kubernetes.io/ko/blog/2026/08/26/kubernetes-v1-37-release/)) | 한국어·영어 | 1.37 은 2026-08-26 출시 |

!!! note "자격증 책은 이 강좌와 맞지 않아요"
    리눅스마스터 2급 같은 자격증 대비 자료는 실습 강좌에는 맞지 않아요. 2026 시험 일정 등은 공식 자료를 확인하지 못했어요.

## 4. 주차별 대응

| 주 | 강좌 주제 | 먼저·같이 볼 자료 |
|---|---|---|
| 0 | 터미널과 WSL | Microsoft WSL 문서 |
| 1 | Git 첫걸음 | Pro Git 1~2장, 지옥에서 온 Git |
| 2 | 브랜치와 병합 | Pro Git 3장 |
| 3 | GitHub 로 함께 일하기 | GitHub Docs 한국어, GitHub Skills, [GitHub SSH 키 문서](https://docs.github.com/ko/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) |
| 4 | 셸과 파일 시스템 | The Linux Command Line 1~6장, Linux Journey |
| 5 | 권한·프로세스·서비스 | The Linux Command Line(권한·프로세스 장) |
| 6 | 원격 접속과 자동화 | The Linux Command Line(스크립트 장), uv 문서 |
| 7 | 컨테이너와 이미지 | Docker 공식 문서 Guides |
| 8 | Dockerfile 과 빌드 | uv Docker 가이드, [멀티플랫폼 문서](https://docs.docker.com/build/building/multi-platform/) |
| 9 | 볼륨·네트워크·설정 | Docker 공식 문서 |
| 10 | Compose | Compose 문서·역사 문서 |
| 11 | 배포·보안·자원·GPU | [Docker Scout 문서](https://docs.docker.com/scout/explore/analysis/), [Trivy 권고문](https://github.com/aquasecurity/trivy/security/advisories/GHSA-69fq-xp46-6x23), [NVIDIA Container Toolkit 문서](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) |
| 12 | 종합 프로젝트 | containers.dev, GitHub Actions 문서 |

(장 번호는 책 판마다 달라요. 장 제목으로 찾으세요.)

## 5. 한국어 자료의 빈틈

솔직하게 말할게요.

- **Pro Git 한국어판은 3년 가까이 뒤져 있어요.** 한국어 저장소의 마지막 릴리스는 2023-01-15(2.1.80)이고, 영어 원본은 2026-05-25(2.1.450)예요. 갱신 계획은 확인하지 못했어요. 명령은 대부분 같지만 새 기능은 영어 원본이나 [Git 공식 문서](https://git-scm.com/docs)에서 보세요.
- **The Linux Command Line 의 무료 한국어판은 없어요.** 한국어판은 종이책만 있어요.
- **Docker 공식 문서에는 한국어 선택이 없어요.** 영어 문서를 읽는 연습이 필요해요. 이 강좌는 필요한 부분을 한국어로 풀어 쓰고 링크를 달았어요.
- **Play with Docker 를 안내하는 한국어 글이 아직 많아요.** 2026-03-01 에 중단됐으니 따라 하지 마세요.
- **옛 글은 `docker-compose`(하이픈) 와 `version:` 키를 써요.** 지금은 `docker compose`(띄어쓰기)와 `version:` 생략이 맞아요. ([Compose 역사 문서](https://docs.docker.com/compose/intro/history/))
- 영어가 어려우면 브라우저 번역을 켜고 **명령과 코드는 번역하지 말고 그대로** 읽으세요.

## 6. 라이선스 주의

이 강좌의 글은 CC BY 4.0, 코드는 MIT 예요. 위 자료의 라이선스는 각자 달라요(예: Pro Git 은 CC BY-NC-SA 3.0, TLCL 은 CC BY-NC-ND 3.0). 내려받아 다시 올리지 말고 **링크로** 쓰세요.
