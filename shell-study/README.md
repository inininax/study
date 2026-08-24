# shell-study

Bash 셸 스크립트 학습 예제 모음입니다.

## 디렉터리 구성

| 경로 | 내용 |
|------|------|
| `bash/basic.sh` | Bash 기초 문법 정리 — shebang, 매개변수(`$0`, `$1`, `$@`, `$#`) 등 주석 위주의 치트시트 |
| `bash/read-input-bash3.sh` | 사용자 입력 읽기 및 문자열 조건 비교(read, if) 연습 |
| `bash/replace-text-in-file.sh` | `sed`로 파일 내 텍스트 치환(`${env}` → `goenv`, `${service}` → `goservice`) |
| `bash/data/input.txt` | 치환 연습용 입력 데이터 |
| `res/dummy.txt` | 더미 테스트 파일 |

## 실행 방법

```bash
chmod +x bash/basic.sh
./bash/basic.sh

# sed 치환 예제 (결과는 ../out/output.txt 에 저장)
./bash/replace-text-in-file.sh
```
