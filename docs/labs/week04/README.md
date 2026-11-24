# 4주 실습: 로그 파일에서 오류만 골라내기

- 장소: WSL(Ubuntu) 터미널 — Mac 은 터미널(zsh)에서도 가능, 다른 점은 `이렇게 나오면 성공` 아래에 표시
- 예상 시간: 3시간
- 만드는 것: `~/lab04/errors.txt`(오류 줄 모음)와 `~/lab04/report.txt`(요약)
- 연습용 로그 `sample.log` 는 이 강좌를 위해 직접 만든 **가짜 데이터**(30줄)예요. 강좌 저장소와 같은 라이선스를 따라요.

## 0단계. 준비

```bash
$ mkdir -p ~/lab04
$ cd ~/lab04
$ curl -O https://raw.githubusercontent.com/metahomo/dev-container-course/main/docs/labs/week04/sample.log
$ ls
sample.log
```

!!! note "curl 이 안 되면"
    이 저장소를 `git clone` 했다면(1~3주에서 배워요) `cp` 로 복사해도 돼요: `cp <저장소 경로>/docs/labs/week04/sample.log ~/lab04/`

로그 한 줄은 이런 모양이에요. 공백으로 칸이 나뉘어요.

```text
2026-11-20 09:02:10 ERROR auth user=jiwoo wrong password
날짜        시각     수준  서비스 내용
```

수준은 `INFO`(보통), `WARN`(주의), `ERROR`(오류) 세 가지예요.

## 1단계. 탐색: 지금 어디에 뭐가 있나

```bash
$ pwd
/home/내이름/lab04
$ ls -l
total 4
-rw-r--r-- 1 내이름 내이름 1557 Nov 24 12:50 sample.log
$ cd ..
$ pwd
/home/내이름
$ cd lab04
$ cd ~/lab04
```

이렇게 나오면 성공: `pwd` 가 `/home/내이름/lab04` 로 끝나요. (`ls -l` 의 크기·날짜는 다를 수 있어요.)

## 2단계. 만들고, 복사하고, 옮기고, 지우기

연습용 폴더 안에서만 지워요. 지우기 전에는 항상 `pwd` 와 `ls` 로 확인해요.

```bash
$ mkdir -p practice/notes
$ touch practice/notes/a.txt
$ cp sample.log practice/copy.log
$ mv practice/copy.log practice/renamed.log
$ ls practice
notes  renamed.log
$ rm practice/renamed.log
$ rm -r practice
$ ls
sample.log
```

이렇게 나오면 성공: 마지막 `ls` 에 `sample.log` 만 남아요.

## 3단계. 내용 보기

```bash
$ head -n 3 sample.log
2026-11-20 09:00:01 INFO web GET /index 200 12ms
2026-11-20 09:00:03 INFO web GET /login 200 25ms
2026-11-20 09:00:04 INFO auth user=minsu login ok
$ tail -n 2 sample.log
2026-11-20 09:17:21 ERROR web POST /enroll 500 22ms
2026-11-20 09:18:00 INFO web GET /index 200 11ms
$ wc -l sample.log
30 sample.log
```

`less sample.log` 도 열어서 방향키로 넘겨 보고 `q` 로 나와 보세요. (Mac 의 `wc` 는 숫자 앞에 공백이 더 붙어요.)

## 4단계. grep 으로 오류만 골라내기

```bash
$ grep ERROR sample.log
2026-11-20 09:02:10 ERROR auth user=jiwoo wrong password
2026-11-20 09:02:14 ERROR auth user=jiwoo wrong password
2026-11-20 09:03:30 ERROR web GET /courses/99 404 4ms
2026-11-20 09:06:47 ERROR db connection timeout after 30s
2026-11-20 09:06:48 ERROR web GET /courses 500 30012ms
2026-11-20 09:11:33 ERROR web GET /admin 403 3ms
2026-11-20 09:15:00 ERROR db disk almost full 95%
2026-11-20 09:17:21 ERROR web POST /enroll 500 22ms
$ grep -c ERROR sample.log
8
$ grep -c WARN sample.log
4
```

## 5단계. 리다이렉션으로 파일에 저장

```bash
$ grep ERROR sample.log > errors.txt
$ wc -l errors.txt
8 errors.txt
$ cat errors.txt | head -n 2
2026-11-20 09:02:10 ERROR auth user=jiwoo wrong password
2026-11-20 09:02:14 ERROR auth user=jiwoo wrong password
```

## 6단계. 파이프로 요약 만들기

서비스별 오류 수를 세어 `report.txt` 에 모아요.

```bash
$ echo "오류 개수: $(grep -c ERROR sample.log)" > report.txt
$ echo "--- 서비스별 오류" >> report.txt
$ grep ERROR sample.log | cut -d' ' -f4 | sort | uniq -c | sort -rn >> report.txt
$ cat report.txt
오류 개수: 8
--- 서비스별 오류
      4 web
      2 db
      2 auth
```

이렇게 나오면 성공: 숫자 8, 그리고 web 4 · db 2 · auth 2. (`uniq -c` 앞 공백 개수는 시스템마다 달라요.)

## 도전 문제

각 문제는 **명령 한 줄**로 풀어요. 먼저 직접 풀고, 아래 풀이와 비교해요.

1. 응답 코드가 `4xx` 또는 `5xx` 인 줄을 모두 보여주세요(공백으로 둘러싸인 세 자리 숫자).
2. `jiwoo` 가 로그인에 성공하기 전에 몇 번 틀렸나요? (`jiwoo` 의 `ERROR` 줄 수)
3. `login ok` 가 몇 번 나오나요?
4. `disk` 가 들어 있는 줄을 줄 번호와 함께 보여주세요.
5. `report.txt` 맨 아래에 "가장 느린 요청 3개"(`ms` 앞 숫자 기준)를 덧붙이세요.

??? note "풀이 명령과 기대 출력"
    ```bash
    # 1
    $ grep -E ' (4|5)[0-9]{2} ' sample.log
    2026-11-20 09:03:30 ERROR web GET /courses/99 404 4ms
    2026-11-20 09:06:48 ERROR web GET /courses 500 30012ms
    2026-11-20 09:11:33 ERROR web GET /admin 403 3ms
    2026-11-20 09:17:21 ERROR web POST /enroll 500 22ms

    # 2
    $ grep ERROR sample.log | grep -c jiwoo
    2

    # 3
    $ grep -c "login ok" sample.log
    3

    # 4
    $ grep -n disk sample.log
    26:2026-11-20 09:15:00 ERROR db disk almost full 95%

    # 5
    $ echo "--- 가장 느린 요청 3개" >> report.txt
    $ grep -o '[0-9]*ms' sample.log | sort -n | tail -n 3 >> report.txt
    $ tail -n 4 report.txt
    --- 가장 느린 요청 3개
    1200ms
    1500ms
    30012ms
    ```
    5번에서 `grep -o` 는 줄 전체가 아니라 **맞는 부분만** 보여줘요. `sort -n` 은 숫자 크기 순으로 정렬해서, `tail -n 3` 이 가장 큰 3개를 골라요.

## 정리

```bash
$ ls ~/lab04
errors.txt  report.txt  sample.log
```

연습 파일은 지워도 되고 두어도 돼요. 지우려면 `rm -r ~/lab04` — 경로를 한 번 더 읽고 엔터를 눌러요.
