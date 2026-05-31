# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

이 저장소는 **소프트웨어 프로젝트가 아니라 학습 콘텐츠 저장소**입니다.
"Python 초심자 → 숙련자" 학습 로드맵을 markdown 챕터, 실행 가능한 Python 예제, 연습 문제로 구성합니다. 실행할 애플리케이션은 없습니다.

## Content Architecture

학습 자료는 **4단계 시퀀스**로 설계되었고, 각 단계는 독립된 디렉토리이며 챕터 파일은 `NN-제목.md` 패턴으로 정렬된 순서를 가집니다.

```
01-beginner/      (8 챕터)  기초 문법
02-intermediate/  (8 챕터)  OOP, 모듈, 정규식, 컴프리헨션 등
03-advanced/      (8 챕터)  데코레이터, 메타클래스, asyncio, 타입 힌트, 테스팅 등
04-expert/        (6 챕터)  디자인 패턴, FastAPI, 데이터 분석, 자동화, 베스트 프랙티스
examples/         단계별 실행 가능한 .py 예제 (현재는 01-beginner 만)
exercises/        단계별 연습 문제 (problems.md) 와 정답 (solutions.py — 01-beginner)
```

핵심 불변량:
- **챕터 순서 보존**: `NN-제목.md` 의 `NN` 접두사는 README 의 학습 로드맵 표와 일치해야 한다. 챕터를 추가/이동/삭제할 때 README 표, 챕터 본문의 `🔗 다음 챕터` 링크, 그리고 인접 챕터의 "이전 챕터" 링크도 함께 갱신해야 한다.
- **표준 챕터 골격**: 모든 챕터는 `# NN. 제목` → `## 🎯 학습 목표` → 본문 → `## 📝 연습 문제` → `## ✅ 체크리스트` → `## 🔗 다음 챕터` 순서를 따른다. 새 챕터를 만들 때 이 골격을 그대로 사용한다.
- **상호 링크 무결성**: `다음 챕터` 링크는 같은 단계 내 다음 챕터 또는 다음 단계의 첫 챕터를 가리킨다. README.md 의 표 링크는 모두 상대 경로 `./NN-단계/NN-제목.md` 형태다.

## Routine Commands

`Makefile`, `tox`, `pytest.ini` 등은 없습니다. 다음 명령들이 표준 검증 흐름입니다.

### 콘텐츠 무결성 검증 (PR 전에 항상 실행)

모든 `.py` 파일 신택스 검사:
```bash
find . -name "*.py" -not -path "./.omc/*" -not -path "./.serena/*" -not -path "./.claude/*" \
  -exec python3 -m py_compile {} \;
```

모든 챕터 `다음 챕터` 링크 유효성 검사:
```bash
grep -l "다음 챕터" 01-beginner/*.md 02-intermediate/*.md 03-advanced/*.md 04-expert/*.md \
  | while read f; do
      link=$(grep -oE "\(\.\/[^)]+\.md\)|\(\.\.\/[^)]+\.md\)" "$f" | tail -1 | tr -d '()')
      target=$(dirname "$f")/$link
      target=$(echo "$target" | sed 's|/\./|/|g')
      [ -f "$target" ] || echo "❌ $f → $link"
    done
```

Markdown 안의 `` ```python `` 코드 블록 신택스 검증 (가장 강력한 회귀 테스트):
```bash
python3 <<'PY'
import ast, re
from pathlib import Path
pattern = re.compile(r"```python\n(.*?)```", re.DOTALL)
errors = 0
for md in sorted(Path(".").glob("0[1-4]-*/*.md")):
    for i, m in enumerate(pattern.finditer(md.read_text(encoding="utf-8")), 1):
        try:
            ast.parse(m.group(1))
        except SyntaxError as e:
            print(f"{md} #{i}: {e}")
            errors += 1
print(f"errors={errors}")
PY
```

### 예제/정답 실행

```bash
# 모든 초급 예제 실행
for f in examples/01-beginner/*.py; do python3 "$f"; done

# 초급 정답의 assert 18개 모두 통과 확인
python3 exercises/01-beginner/solutions.py
```

## Code Block Conventions

코드 블록의 언어 태그는 **반드시 신택스에 맞춰** 사용합니다. `python` 태그는 자동 검증 도구가 신택스 검사를 수행하므로, 실행되지 않는 예시는 적절한 다른 태그를 사용합니다.

| 내용 | 언어 태그 |
|------|-----------|
| 실행 가능한 Python 코드 | ` ```python ` |
| REPL 세션 (`>>>` 포함) | ` ```pycon ` |
| IPython/Jupyter 매직 명령 (`%timeit`, `!shell`) | ` ```ipython ` |
| Cython (`.pyx`, `cdef`) | ` ```cython ` |
| 셸 명령 | ` ```bash ` |
| 출력 결과만 보여주는 경우 | ` ``` ` (태그 없음) 또는 `text` |
| "잘못된 예시"용 코드 | ` ```python ` 유지 + **각 라인을 `#` 주석으로** 처리 |

새로운 코드 블록을 추가할 때마다 위 회귀 테스트 (`python` 블록 신택스 검증)를 실행해 신택스 false-positive 가 생기지 않았는지 확인합니다.

## Language and Tone

- 본문은 **한국어**로 작성합니다. 코드 식별자, 라이브러리명, 메서드 시그니처는 영어 원형을 유지합니다.
- 챕터 본문에는 **이모지 헤더**를 적극 사용합니다 (`🎯`, `📝`, `✅`, `🔗`, `💡`, `⚠️`, `❌` 등). 이는 학습용 콘텐츠의 톤을 만드는 의도적 선택입니다 — 일반 코드 파일의 이모지 사용 규칙과 다릅니다.
- 안티 패턴은 ❌, 권장 패턴은 ✅ 로 명시합니다.

## Git Workflow

기본 브랜치는 `main`, 원격은 `origin` 입니다. 커밋 메시지는 `type: description` 한국어 형식을 사용합니다 (`init:`, `fix:`, `feat:`, `docs:`, `refactor:` 등). Co-Authored-By 라인은 글로벌 설정으로 비활성화되어 있어 추가하지 마세요.

## Adding a New Chapter

1. 다음 챕터 번호 결정 (`NN-제목.md`).
2. 표준 골격(학습 목표 → 본문 → 연습 문제 → 체크리스트 → 다음 챕터) 으로 작성.
3. **세 곳 동시 갱신**:
   - `README.md` 의 해당 단계 챕터 표
   - 직전 챕터의 `🔗 다음 챕터` 링크
   - (필요 시) `LEARNING_GUIDE.md` 의 학습 로드맵 표
4. 마지막에 위 콘텐츠 무결성 명령 3종 (`.py` 신택스, 챕터 링크, ` ```python ` 블록 신택스) 모두 실행.

## What Does Not Belong Here

- `requirements.txt`, `pyproject.toml`, 패키징/배포 설정 — 학습 자료에는 외부 의존성이 없습니다.
- 빌드/배포 CI — 검증은 위 셸 스니펫으로 수동/스크립트 실행합니다.
- `.claude/`, `.omc/`, `.serena/` — 도구 메타데이터 디렉토리로 `.gitignore` 에 포함되어 있어 추적하지 않습니다.
