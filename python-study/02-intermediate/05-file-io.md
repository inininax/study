# 05. 파일 I/O와 컨텍스트 매니저

## 🎯 학습 목표
- 다양한 형식의 파일을 읽고 쓸 수 있다
- pathlib 을 활용한다
- 컨텍스트 매니저를 직접 만든다
- CSV, JSON, 바이너리 파일을 다룬다

## 1. 파일 I/O 기본 복습

### 1.1 파일 열기 모드
```python
# 모드 조합: r/w/a/x + b/t + +
# r: 읽기 (기본)
# w: 쓰기 (덮어쓰기)
# a: 추가
# x: 새 파일 (있으면 에러)
# b: 바이너리
# t: 텍스트 (기본)
# +: 읽기/쓰기

with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()
```

### 1.2 읽기 메서드
```python
with open("file.txt", "r", encoding="utf-8") as f:
    # 전체 읽기
    content = f.read()

    # 일정 바이트만
    chunk = f.read(100)

    # 한 줄
    line = f.readline()

    # 모든 줄 (리스트)
    lines = f.readlines()

    # 한 줄씩 (메모리 효율적)
    for line in f:
        print(line.rstrip())
```

### 1.3 쓰기 메서드
```python
with open("file.txt", "w", encoding="utf-8") as f:
    f.write("Hello\n")
    f.write("World\n")
    f.writelines(["Line 1\n", "Line 2\n"])
```

### 1.4 위치 제어
```python
with open("file.txt", "r+", encoding="utf-8") as f:
    print(f.tell())  # 현재 위치
    f.seek(5)        # 5번째 바이트로 이동
    f.read(10)
    f.seek(0)        # 처음으로
    f.seek(0, 2)     # 끝으로 (0=처음, 1=현재, 2=끝)
```

## 2. pathlib (현대적 방식)

`os.path` 의 대체. **권장 ✅**

### 2.1 Path 생성
```python
from pathlib import Path

# 다양한 방법
p = Path("data/users.txt")
p = Path("data") / "users.txt"     # / 연산자
p = Path.home() / "Documents"
p = Path.cwd()                      # 현재 디렉토리
```

### 2.2 경로 정보
```python
p = Path("/Users/alice/docs/report.pdf")

print(p.name)        # report.pdf
print(p.stem)        # report
print(p.suffix)      # .pdf
print(p.suffixes)    # ['.pdf']
print(p.parent)      # /Users/alice/docs
print(p.parents[0])  # /Users/alice/docs
print(p.parents[1])  # /Users/alice
print(p.parts)       # ('/', 'Users', 'alice', 'docs', 'report.pdf')
print(p.absolute())
print(p.is_absolute())  # True
```

### 2.3 경로 조작
```python
p = Path("docs/notes.txt")

# 확장자 변경
p.with_suffix(".md")           # docs/notes.md

# 파일명 변경
p.with_name("readme.txt")      # docs/readme.txt

# stem 변경
p.with_stem("summary")         # docs/summary.txt

# 상대경로 계산
Path("/a/b/c").relative_to("/a")  # b/c
```

### 2.4 파일 존재/타입 확인
```python
p = Path("file.txt")

print(p.exists())     # True/False
print(p.is_file())    # 파일인가
print(p.is_dir())     # 디렉토리인가
print(p.is_symlink()) # 심볼릭 링크인가
```

### 2.5 디렉토리 작업
```python
# 디렉토리 생성
Path("new_folder").mkdir(exist_ok=True)
Path("a/b/c").mkdir(parents=True, exist_ok=True)

# 디렉토리 내용 (얕은)
for item in Path(".").iterdir():
    print(item)

# 패턴 매칭 (현재 디렉토리)
for py in Path(".").glob("*.py"):
    print(py)

# 재귀적 패턴 매칭
for py in Path(".").rglob("*.py"):
    print(py)

# 또는
for py in Path(".").glob("**/*.py"):
    print(py)
```

### 2.6 파일 작업
```python
p = Path("file.txt")

# 읽기/쓰기 (편리)
p.write_text("Hello!", encoding="utf-8")
content = p.read_text(encoding="utf-8")

# 바이너리
p.write_bytes(b"\x00\x01")
data = p.read_bytes()

# 삭제
p.unlink(missing_ok=True)       # 파일
Path("dir").rmdir()             # 빈 디렉토리만

# 이름 변경 / 이동
p.rename("newname.txt")

# 메타데이터
stat = p.stat()
print(stat.st_size)             # 크기
print(stat.st_mtime)            # 수정 시간
```

## 3. CSV 파일

### 3.1 기본 사용
```python
import csv

# 쓰기
with open("data.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "age", "city"])
    writer.writerow(["Alice", 25, "Seoul"])
    writer.writerow(["Bob", 30, "Busan"])

# 읽기
with open("data.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        print(row)
```

> ⚠️ `newline=""` 필수! 안 그러면 줄바꿈이 이상해질 수 있음.

### 3.2 DictWriter / DictReader
```python
# 딕셔너리로 쓰기
fieldnames = ["name", "age", "city"]
with open("users.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({"name": "Alice", "age": 25, "city": "Seoul"})
    writer.writerow({"name": "Bob", "age": 30, "city": "Busan"})

# 딕셔너리로 읽기
with open("users.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['name']} ({row['age']})")
```

### 3.3 옵션 설정
```python
# 탭으로 구분
csv.writer(f, delimiter="\t")

# 인용 처리
csv.writer(f, quoting=csv.QUOTE_ALL)       # 모든 필드 따옴표
csv.writer(f, quoting=csv.QUOTE_NONNUMERIC) # 숫자 외 따옴표

# 방언 (Excel 등)
csv.writer(f, dialect="excel")
```

## 4. JSON 파일

### 4.1 기본 사용
```python
import json

data = {
    "name": "Alice",
    "age": 25,
    "hobbies": ["reading", "coding"],
    "address": {"city": "Seoul", "zip": "12345"},
}

# Python → JSON 파일
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# JSON 파일 → Python
with open("data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
print(loaded["name"])
```

### 4.2 문자열로 변환
```python
# Python → JSON 문자열
json_str = json.dumps(data, ensure_ascii=False, indent=2)
print(json_str)

# JSON 문자열 → Python
parsed = json.loads(json_str)
```

### 4.3 옵션
```python
# 한글 깨짐 방지 (필수)
json.dumps(data, ensure_ascii=False)

# 보기 좋게 (들여쓰기)
json.dumps(data, indent=2)

# 정렬
json.dumps(data, sort_keys=True)

# 콤팩트
json.dumps(data, separators=(',', ':'))
```

### 4.4 커스텀 객체 직렬화
```python
from datetime import datetime

class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

def custom_encoder(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, User):
        return {"name": obj.name, "age": obj.age}
    raise TypeError(f"직렬화 불가: {type(obj)}")

data = {
    "user": User("Alice", 25),
    "created": datetime.now(),
}

json_str = json.dumps(data, default=custom_encoder, ensure_ascii=False)
print(json_str)
```

## 5. 바이너리 파일

### 5.1 기본
```python
# 바이너리 쓰기
with open("data.bin", "wb") as f:
    f.write(b"\x00\x01\x02\x03")

# 바이너리 읽기
with open("data.bin", "rb") as f:
    data = f.read()
    print(data.hex())  # 00010203
```

### 5.2 파일 복사
```python
def copy_file(src, dst, chunk_size=4096):
    with open(src, "rb") as fin, open(dst, "wb") as fout:
        while chunk := fin.read(chunk_size):
            fout.write(chunk)

copy_file("image.jpg", "backup.jpg")
```

### 5.3 이미지 정보 읽기 (예시)
```python
def get_png_dimensions(path):
    with open(path, "rb") as f:
        f.seek(16)              # PNG 헤더의 크기 위치
        width = int.from_bytes(f.read(4), "big")
        height = int.from_bytes(f.read(4), "big")
    return width, height
```

## 6. pickle — Python 객체 직렬화

```python
import pickle

class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# 저장
user = User("Alice", 25)
with open("user.pkl", "wb") as f:
    pickle.dump(user, f)

# 로드
with open("user.pkl", "rb") as f:
    loaded = pickle.load(f)
print(loaded.name)

# 문자열로
data = pickle.dumps(user)       # bytes
restored = pickle.loads(data)
```

> ⚠️ **보안 주의**: 신뢰할 수 없는 pickle 데이터는 로드하지 마세요. 임의 코드 실행 가능!

## 7. 압축 파일

### 7.1 zipfile
```python
import zipfile

# 생성
with zipfile.ZipFile("archive.zip", "w", zipfile.ZIP_DEFLATED) as zf:
    zf.write("file1.txt")
    zf.write("file2.txt")
    zf.writestr("readme.txt", "압축 파일입니다")

# 압축 해제
with zipfile.ZipFile("archive.zip", "r") as zf:
    zf.extractall("extracted/")
    # 또는 개별
    zf.extract("file1.txt", "extracted/")

# 목록 보기
with zipfile.ZipFile("archive.zip") as zf:
    for info in zf.infolist():
        print(info.filename, info.file_size)
```

### 7.2 tarfile
```python
import tarfile

# 생성 (gzip 압축)
with tarfile.open("archive.tar.gz", "w:gz") as tf:
    tf.add("folder/")

# 해제
with tarfile.open("archive.tar.gz", "r:gz") as tf:
    tf.extractall("extracted/")
```

## 8. 임시 파일

```python
import tempfile

# 임시 파일
with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
    f.write("임시 데이터")
    temp_path = f.name
print(f"임시 파일: {temp_path}")

# 임시 디렉토리
with tempfile.TemporaryDirectory() as tmpdir:
    print(f"임시 디렉토리: {tmpdir}")
    # 블록 종료 시 자동 삭제
```

## 9. 컨텍스트 매니저 만들기

### 9.1 클래스 기반
```python
class FileManager:
    def __init__(self, filename, mode="r", encoding="utf-8"):
        self.filename = filename
        self.mode = mode
        self.encoding = encoding

    def __enter__(self):
        self.file = open(self.filename, self.mode, encoding=self.encoding)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        return False  # 예외 다시 발생

with FileManager("data.txt", "w") as f:
    f.write("Hello!")
```

### 9.2 데코레이터 기반 (간편 ✅)
```python
from contextlib import contextmanager

@contextmanager
def open_file(filename, mode="r"):
    f = open(filename, mode, encoding="utf-8")
    try:
        yield f
    finally:
        f.close()

with open_file("data.txt", "w") as f:
    f.write("Hello!")
```

### 9.3 자원 자동 정리
```python
from contextlib import contextmanager
import time

@contextmanager
def timer(label="실행"):
    start = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start
        print(f"{label}: {elapsed:.4f}초")

with timer("계산"):
    sum(range(10_000_000))
```

### 9.4 여러 컨텍스트 한 번에
```python
from contextlib import ExitStack

filenames = ["a.txt", "b.txt", "c.txt"]
with ExitStack() as stack:
    files = [stack.enter_context(open(name)) for name in filenames]
    # 모든 파일을 동시에 다룸
    for f in files:
        print(f.read())
```

### 9.5 예외 억제
```python
from contextlib import suppress

# FileNotFoundError 만 무시
with suppress(FileNotFoundError):
    Path("missing.txt").unlink()
```

## 10. 실전 예제

### 예제 1: 로그 파일 분석
```python
from pathlib import Path
from collections import Counter

def analyze_log(log_path):
    error_count = 0
    levels = Counter()

    with open(log_path, encoding="utf-8") as f:
        for line in f:
            # 형식: "2026-05-12 10:00:00 [INFO] message"
            parts = line.split("[")
            if len(parts) > 1:
                level = parts[1].split("]")[0]
                levels[level] += 1
                if level == "ERROR":
                    error_count += 1

    print(f"총 에러: {error_count}")
    print(f"레벨별 분포: {dict(levels)}")

# analyze_log("app.log")
```

### 예제 2: JSON ↔ CSV 변환
```python
import json
import csv

def json_to_csv(json_path, csv_path):
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    if not data:
        return

    fieldnames = list(data[0].keys())
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def csv_to_json(csv_path, json_path):
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = list(reader)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
```

### 예제 3: 디렉토리 통계
```python
from pathlib import Path
from collections import Counter

def stats(directory):
    p = Path(directory)
    if not p.is_dir():
        return None

    total_size = 0
    extensions = Counter()
    file_count = 0

    for f in p.rglob("*"):
        if f.is_file():
            file_count += 1
            total_size += f.stat().st_size
            extensions[f.suffix.lower()] += 1

    return {
        "file_count": file_count,
        "total_size_mb": total_size / 1024 / 1024,
        "extensions": dict(extensions.most_common(5)),
    }

print(stats("."))
```

## 📝 연습 문제

### 문제 1: 파일 복사
한 줄씩 읽어서 다른 파일로 복사하는 프로그램을 작성하세요.

### 문제 2: 단어 빈도 JSON
텍스트 파일을 읽어 단어 빈도를 JSON 파일로 저장하세요.

### 문제 3: CSV 필터링
CSV 파일을 읽어 특정 조건을 만족하는 행만 새 CSV 로 저장하세요.

### 문제 4: 디렉토리 트리
디렉토리 경로를 받아 트리 구조로 출력하는 프로그램을 작성하세요.
```
.
├── file1.txt
├── folder/
│   ├── file2.txt
│   └── file3.py
└── readme.md
```

### 문제 5: 컨텍스트 매니저
파일이 존재하면 백업을 만들고 작업하는 컨텍스트 매니저를 작성하세요.

## ✅ 체크리스트
- [ ] pathlib 으로 경로를 다룬다
- [ ] CSV 파일을 읽고 쓴다
- [ ] JSON 파일을 다룬다
- [ ] 바이너리 파일을 처리할 수 있다
- [ ] with 문과 컨텍스트 매니저를 이해한다
- [ ] @contextmanager 데코레이터를 사용한다

## 🔗 다음 챕터
👉 [06. 정규표현식](./06-regex.md)
