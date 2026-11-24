# 자원 제한 실습표

컨테이너가 컴퓨터의 메모리와 CPU 를 **마음대로 쓰지 못하게** 상한을 걸고, 넘기면 어떻게 되는지 직접 봐요. 아래 값은 Docker 공식 문서(Resource constraints)의 옵션 설명을 따랐어요.

| 옵션 | 뜻 (공식 문서 기준) |
|---|---|
| `--memory` (`-m`) | 컨테이너가 쓸 수 있는 메모리의 최댓값. 최솟값은 `6m` |
| `--memory-swap` | `--memory` 와 함께 쓸 때만 의미가 있어요. `--memory` 와 **같은 값**이면 스왑을 쓰지 못해요 |
| `--cpus` | CPU 를 얼마나 쓸 수 있는지. `--cpus="1.5"` 는 1.5 개 분량 |
| OOM | 메모리 부족(Out Of Memory)이 나면 기본적으로 커널이 컨테이너 안의 프로세스를 죽여요 |

## 실습 1. 메모리 상한을 넘겨 보기

64MB 로 제한하고 200MB 를 쓰려 해요.

```bash
docker run --name oom -m 64m --memory-swap 64m python:3.13-slim \
  python -c "x = b'a' * (200*1024*1024); print('여기까지 오면 제한이 안 걸린 거예요')"
echo "종료 코드: $?"
docker inspect -f '{{.State.OOMKilled}}' oom
```

**이렇게 나오면 성공** (모양 예시) — 문구 `여기까지...` 는 나오지 않아야 해요.

```text
종료 코드: 137
true
```

137 은 "강제 종료(신호 9)" 를 뜻하는 흔한 코드이고, `OOMKilled` 가 `true` 면 메모리 초과로 죽었다는 표시예요. 지우기: `docker rm oom`

## 실습 2. 제한 없이 돌려 비교하기

```bash
docker run --rm python:3.13-slim \
  python -c "x = b'a' * (200*1024*1024); print('200MB 사용 성공', len(x))"
```

```text
200MB 사용 성공 209715200
```

(내 컴퓨터·Docker 의 메모리가 200MB 도 안 되면 다르게 나올 수 있어요.)

## 실습 3. 실행 중인 컨테이너의 사용량 보기

```bash
docker run -d --rm --name limited -m 128m --cpus 0.5 week11-demo:0.1.0
docker stats --no-stream limited
docker stop limited
```

`docker stats` 의 `MEM USAGE / LIMIT` 칸에 `/ 128MiB` 가 보이면 제한이 걸린 거예요. (이미지 이름은 내 것으로 바꿔요.)

## 실습 4. Compose 에서 걸기

12주 `compose.yaml` 에는 아래처럼 들어 있어요. Compose 명세의 서비스 속성이에요.

```yaml
    mem_limit: 512m
    cpus: 1.0
    pids_limit: 100
```

- `mem_limit`: 메모리 상한 (바이트 값 문자열)
- `cpus`: CPU 개수(소수 가능), `0.000` 이면 제한 없음
- `pids_limit`: 컨테이너 안에서 만들 수 있는 프로세스 수 상한

## 기록표

| 실험 | 명령의 제한 | 결과(종료 코드, OOMKilled) | 알게 된 것 |
|---|---|---|---|
| 1 | `-m 64m --memory-swap 64m` | | |
| 2 | 없음 | | |
| 3 | `-m 128m --cpus 0.5` | `MEM USAGE / LIMIT` = | |

## 생각해 보기

내 ML 서비스는 모델을 메모리에 올려요. 모델이 150MB 면 `mem_limit` 을 몇으로 잡아야 할까요? 너무 작으면 위 실습 1처럼 죽고, 너무 크면 한 컨테이너가 컴퓨터를 독차지해요. 평소 사용량(`docker stats`)을 재고, 그보다 넉넉히 잡는 게 출발점이에요.
