"""
전문가 연습 문제 — 정답 예시

먼저 스스로 풀어본 후 참고하세요!

실행: python3 solutions.py  (표준 라이브러리만 사용, 외부 의존성 없음)

⚠️ 원래 이 단계는 FastAPI/pandas/Pillow 등 외부 라이브러리를 다루지만,
   저장소 정책(stdlib-only)에 따라 동일한 개념을 표준 라이브러리로 구현합니다.
   각 문제의 실무 도구는 docstring/주석으로 안내합니다.
"""

import base64
import csv
import hashlib
import hmac
import html.parser
import json
import math
import os
import re
import shutil
import smtplib
import sqlite3
import statistics
import tempfile
import time
import urllib.parse
import zipfile
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from email.message import EmailMessage
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Optional


# ════════════════════════════════════════════════
# 01. 디자인 패턴
# ════════════════════════════════════════════════

# === 문제 1.1: Singleton 로거 ===
class SingletonLogger:
    """어디서 생성해도 같은 인스턴스를 공유하는 로거."""

    _instance: Optional["SingletonLogger"] = None

    def __new__(cls) -> "SingletonLogger":
        # 핵심 아이디어: __new__ 에서 인스턴스 생성을 한 번만 허용
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.logs = []
        return cls._instance

    def log(self, message: str) -> str:
        self.logs.append(message)
        return message


# === 문제 1.2: Factory ===
class Circle:
    def __init__(self, r: float):
        self.r = r

    def area(self) -> float:
        return math.pi * self.r**2

    def perimeter(self) -> float:
        return 2 * math.pi * self.r


class Rectangle:
    def __init__(self, w: float, h: float):
        self.w, self.h = w, h

    def area(self) -> float:
        return self.w * self.h

    def perimeter(self) -> float:
        return 2 * (self.w + self.h)


class Triangle:
    def __init__(self, base: float, height: float, side_a: float, side_b: float):
        self.base, self.height = base, height
        self.side_a, self.side_b = side_a, side_b

    def area(self) -> float:
        return self.base * self.height / 2

    def perimeter(self) -> float:
        return self.base + self.side_a + self.side_b


_SHAPE_CREATORS: dict[str, Callable[..., Any]] = {
    "circle": Circle,
    "rectangle": Rectangle,
    "triangle": Triangle,
}


def create_shape(kind: str, **dimensions: float):
    """문자열 종류로 객체를 생성하는 팩토리 함수."""
    # 핵심 아이디어: 분기문 대신 매핑 테이블로 생성기를 조회
    creator = _SHAPE_CREATORS.get(kind)
    if creator is None:
        raise ValueError(f"알 수 없는 도형: {kind}")
    return creator(**dimensions)


# === 문제 1.3: Observer ===
class StockPrice:
    """주식 가격 피험자(subject) — 구독자에게 변동을 통지."""

    def __init__(self, symbol: str, price: float):
        self.symbol = symbol
        self.price = price
        self._observers: list[Callable[[str, float, float], None]] = []

    def attach(self, observer: Callable[[str, float, float], None]) -> None:
        self._observers.append(observer)

    def detach(self, observer: Callable[[str, float, float], None]) -> None:
        self._observers.remove(observer)

    def set_price(self, new_price: float) -> None:
        old, self.price = self.price, new_price
        for observer in self._observers:  # 핵심 아이디어: subject 는 구독자를 모른 채 통지만 한다
            observer(self.symbol, old, new_price)


class ChangeLog:
    """가격 변동 이벤트를 기록하는 옵저버."""

    def __init__(self):
        self.events: list[tuple[str, float, float]] = []

    def __call__(self, symbol: str, old: float, new: float) -> None:
        self.events.append((symbol, old, new))


# === 문제 1.4: Strategy ===
def bubble_sort(data: list[int]) -> list[int]:
    arr = data.copy()
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def insertion_sort(data: list[int]) -> list[int]:
    arr = data.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def quick_sort(data: list[int]) -> list[int]:
    if len(data) <= 1:
        return data.copy()
    pivot, rest = data[0], data[1:]
    left = [x for x in rest if x <= pivot]
    right = [x for x in rest if x > pivot]
    return quick_sort(left) + [pivot] + quick_sort(right)


SORT_STRATEGIES: dict[str, Callable[[list[int]], list[int]]] = {
    "bubble": bubble_sort,
    "insertion": insertion_sort,
    "quick": quick_sort,
}


class Sorter:
    """정렬 알고리즘을 런타임에 교체 가능한 컨텍스트."""

    def __init__(self, strategy: str = "quick"):
        self.strategy_name = strategy

    @property
    def strategy(self) -> Callable[[list[int]], list[int]]:
        return SORT_STRATEGIES[self.strategy_name]

    def sort(self, data: list[int]) -> list[int]:
        return self.strategy(data)


# === 문제 1.5: Command + Undo ===
class Command(ABC):
    """execute 로 실행하고 undo 로 되돌리는 커맨드 객체."""

    def __init__(self):
        self.before: Optional[str] = None  # 실행 직전 상태(되돌림용)

    @abstractmethod
    def _apply(self, doc: str) -> str: ...

    def execute(self, doc: str) -> str:
        self.before = doc
        return self._apply(doc)

    def undo(self) -> str:
        assert self.before is not None
        return self.before


class AppendText(Command):
    def __init__(self, text: str):
        super().__init__()
        self.text = text

    def _apply(self, doc: str) -> str:
        return doc + self.text


class InsertAt(Command):
    def __init__(self, pos: int, text: str):
        super().__init__()
        self.pos, self.text = pos, text

    def _apply(self, doc: str) -> str:
        return doc[: self.pos] + self.text + doc[self.pos :]


class DeleteAt(Command):
    def __init__(self, pos: int, count: int):
        super().__init__()
        self.pos, self.count = pos, count

    def _apply(self, doc: str) -> str:
        return doc[: self.pos] + doc[self.pos + self.count :]


class TextEditor:
    """커맨드 스택으로 실행 취소를 지원하는 에디터."""

    def __init__(self, doc: str = ""):
        self.doc = doc
        self.history: list[Command] = []

    def execute(self, command: Command) -> None:
        # 핵심 아이디어: 요청을 객체로 만들어 적재 → undo/redo/replay 자유
        self.doc = command.execute(self.doc)
        self.history.append(command)

    def undo(self) -> bool:
        if not self.history:
            return False
        command = self.history.pop()
        self.doc = command.undo()
        return True


# ════════════════════════════════════════════════
# 02. 웹 개발 (stdlib 등가 구현)
# ════════════════════════════════════════════════
# 실무에서는 FastAPI(+Pydantic)+SQLAlchemy+python-jose 조합을 사용한다.
# 여기선 같은 개념(라우팅·검증·토큰·DB·CRUD)을 표준 라이브러리로 재현한다.


# === 문제 2.1 + 2.2: 미니 라우터 & 요청 검증 (FastAPI/Pydantic 대체) ===
FAKE_USERS_DB: dict[int, dict] = {
    1: {"id": 1, "name": "김철수"},
    42: {"id": 42, "name": "이영희"},
}


class MiniRouter:
    """method + path 패턴으로 핸들러를 찾아 호출하는 초소형 프레임워크."""

    def __init__(self):
        self.routes: dict[tuple[str, tuple[str, ...]], Callable] = {}

    def get(self, pattern: str):
        def decorator(func: Callable) -> Callable:
            self.routes[("GET", tuple(pattern.strip("/").split("/")))] = func
            return func

        return decorator

    def dispatch(self, path: str) -> tuple[int, dict]:
        """'/users/42?verbose=1' 형태를 파싱해 핸들러 실행 → (status, body)."""
        path_part, _, query_part = path.partition("?")
        query = urllib.parse.parse_qs(query_part)
        segments = path_part.strip("/").split("/")
        for (method, pattern_segments), handler in self.routes.items():
            if method != "GET" or len(pattern_segments) != len(segments):
                continue
            params: dict[str, Any] = {}
            matched = True
            for pat, seg in zip(pattern_segments, segments):
                if pat.startswith("<") and pat.endswith(">"):
                    params[pat[1:-1]] = seg
                elif pat != seg:
                    matched = False
                    break
            if matched:
                params.update({k: v[-1] for k, v in query.items()})
                result = handler(**params)
                status = result.pop("_status", 200)
                return status, result
        return 404, {"error": f"경로를 찾을 수 없음: {path}"}


router = MiniRouter()


@router.get("/hello")
def hello() -> dict:
    return {"message": "Hello, World!"}


@router.get("/square")
def square(n: str = "0") -> dict:
    try:
        number = int(n)  # Pydantic 검증에 해당하는 수동 변환/검증
    except ValueError:
        return {"_status": 400, "error": "n 은 정수여야 합니다"}
    return {"n": number, "square": number**2}


@router.get("/users/<user_id>")
def get_user_route(user_id: str) -> dict:
    user = FAKE_USERS_DB.get(int(user_id)) if user_id.isdigit() else None
    if user is None:
        return {"_status": 404, "error": "사용자 없음"}
    return dict(user)


EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


class ValidationError(Exception):
    """요청 본문이 스키마를 벗어났을 때 발생."""


@dataclass
class CreateUserRequest:
    """Pydantic BaseModel 대체 — 생성 시 자동 검증."""

    email: str
    name: str
    age: int

    def __post_init__(self):
        if not EMAIL_RE.match(self.email):
            raise ValidationError(f"잘못된 이메일: {self.email}")
        if not (2 <= len(self.name) <= 30):
            raise ValidationError("이름은 2~30 자")
        if not (0 < self.age < 150):
            raise ValidationError("나이는 1~149 세")


def create_user(store: dict[int, dict], payload: dict) -> dict:
    req = CreateUserRequest(**payload)  # 검증 실패 시 ValidationError
    user_id = max(store, default=0) + 1
    store[user_id] = {"id": user_id, **vars(req)}
    return store[user_id]


def get_user(store: dict[int, dict], user_id: int) -> Optional[dict]:
    return store.get(user_id)


# === 문제 2.3: 인증 — HMAC-SHA256 기반 JWT-like 토큰 ===
class InvalidTokenError(Exception):
    pass


def _b64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _b64url_decode(encoded: str) -> bytes:
    padding = "=" * (-len(encoded) % 4)
    return base64.urlsafe_b64decode(encoded + padding)


def jwt_encode(payload: dict, secret: str, expires_in: int = 3600) -> str:
    """header.payload.signature 3-part 토큰 발급."""
    header = {"alg": "HS256", "typ": "JWT"}
    body = {**payload, "exp": int(time.time()) + expires_in}
    head_b64 = _b64url_encode(json.dumps(header).encode())
    body_b64 = _b64url_encode(json.dumps(body).encode())
    signature = hmac.new(
        secret.encode(), f"{head_b64}.{body_b64}".encode(), hashlib.sha256
    ).digest()
    return f"{head_b64}.{body_b64}.{_b64url_encode(signature)}"


def jwt_decode(token: str, secret: str) -> dict:
    """서명 검증 + 만료 확인 후 payload 반환."""
    try:
        head_b64, body_b64, sig_b64 = token.split(".")
    except ValueError:
        raise InvalidTokenError("토큰 형식 오류")
    expected = hmac.new(
        secret.encode(), f"{head_b64}.{body_b64}".encode(), hashlib.sha256
    ).digest()
    # 핵심 아이디어: 서명 비교는 반드시 상수 시간 비교(hmac.compare_digest)로
    if not hmac.compare_digest(_b64url_decode(sig_b64), expected):
        raise InvalidTokenError("서명 불일치")
    payload = json.loads(_b64url_decode(body_b64))
    if payload.get("exp", 0) < time.time():
        raise InvalidTokenError("만료된 토큰")
    return payload


# === 문제 2.4: DB 연동 — SQLAlchemy 대신 sqlite3 ===
class UserRepository:
    """사용자 영속화 리포지토리 (SQLite)."""

    def __init__(self, db_path: str | Path = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # 행을 dict 처럼 접근
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS users ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "email TEXT UNIQUE NOT NULL, name TEXT NOT NULL)"
        )

    def create(self, email: str, name: str) -> dict:
        try:
            cur = self.conn.execute(
                "INSERT INTO users (email, name) VALUES (?, ?)", (email, name)
            )
            self.conn.commit()
        except sqlite3.IntegrityError as exc:
            raise ValueError("중복된 이메일") from exc
        return dict(self.get(cur.lastrowid))

    def get(self, user_id: int) -> Optional[sqlite3.Row]:
        return self.conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()

    def list_all(self) -> list[sqlite3.Row]:
        return self.conn.execute("SELECT * FROM users ORDER BY id").fetchall()

    def delete(self, user_id: int) -> bool:
        cur = self.conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.conn.commit()
        return cur.rowcount == 1


# === 문제 2.5: 완전한 CRUD — Todo API + 테스트 ===
class TodoStore:
    """Todo CRUD (실무에서는 FastAPI 엔드포인트 + DB 로 확장)."""

    def __init__(self):
        self._items: dict[int, dict] = {}
        self._next_id = 1

    def create(self, title: str) -> dict:
        todo = {"id": self._next_id, "title": title, "done": False}
        self._items[todo["id"]] = todo
        self._next_id += 1
        return todo

    def read(self, todo_id: int) -> Optional[dict]:
        return self._items.get(todo_id)

    def update(self, todo_id: int, title: Optional[str] = None,
               done: Optional[bool] = None) -> Optional[dict]:
        todo = self.read(todo_id)
        if todo is None:
            return None
        if title is not None:
            todo["title"] = title
        if done is not None:
            todo["done"] = done
        return todo

    def delete(self, todo_id: int) -> bool:
        return self._items.pop(todo_id, None) is not None

    def list_all(self) -> list[dict]:
        return list(self._items.values())


def run_todo_tests() -> None:
    """CRUD 전 경로를 검증하는 자체 테스트 스위트."""
    store = TodoStore()
    created = store.create("블로그 글쓰기")
    second = store.create("테스트 작성")
    assert created["id"] == 1 and second["id"] == 2
    assert len(store.list_all()) == 2
    assert store.update(created["id"], done=True)["done"] is True
    assert store.update(created["id"], title="기술 블로그")["title"] == "기술 블로그"
    assert store.read(9999) is None and store.update(9999) is None
    assert store.delete(second["id"]) is True
    assert store.delete(second["id"]) is False
    assert len(store.list_all()) == 1


# ════════════════════════════════════════════════
# 03. 데이터 분석 (NumPy/pandas 대체 — 순수 stdlib)
# ════════════════════════════════════════════════

# === 문제 3.1: NumPy 기본 → 리스트 컴프리헨션 등가 ===
def make_matrix(rows: int = 10, cols: int = 10) -> list[list[int]]:
    """rows × cols 정수 행렬 (numpy.array 대체)."""
    return [[r * cols + c for c in range(cols)] for r in range(rows)]


def filter_even_flat(matrix: list[list[int]]) -> list[int]:
    return [x for row in matrix for x in row if x % 2 == 0]


# === 문제 3.2: DataFrame → dict 행 목록 등가 ===
STUDENTS = [
    {"name": "민수", "kor": 90, "eng": 85, "math": 80},
    {"name": "지연", "kor": 70, "eng": 95, "math": 100},
    {"name": "철수", "kor": 60, "eng": 75, "math": 70},
    {"name": "수빈", "kor": 88, "eng": 92, "math": 79},
    {"name": "도윤", "kor": 77, "eng": 66, "math": 90},
]


def column(rows: list[dict], key: str) -> list:
    """df[key] 에 해당하는 열 추출."""
    return [row[key] for row in rows]


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def top_student_by_average(students: list[dict]) -> str:
    scored = [
        (mean([s["kor"], s["eng"], s["math"]]), s["name"]) for s in students
    ]
    return max(scored)[1]


# === 문제 3.3: CSV 분석 (결측치 처리 + 기본 통계) ===
def load_csv_rows(path: Path) -> list[dict]:
    """CSV 를 읽어 빈 칸을 None 으로 변환."""
    with open(path, newline="", encoding="utf-8") as f:
        rows = []
        for raw in csv.DictReader(f):
            rows.append({k: (v if v != "" else None) for k, v in raw.items()})
        return rows


def dropna_rows(rows: list[dict]) -> list[dict]:
    """결측치가 하나라도 있는 행 제거 (df.dropna())."""
    return [row for row in rows if all(v is not None for v in row.values())]


def fill_missing(rows: list[dict], key: str, default) -> list[dict]:
    """특정 열의 결측치를 채움 (df.fillna({key: default}))."""
    return [{**row, key: default if row[key] is None else row[key]} for row in rows]


def describe_numeric(rows: list[dict], key: str) -> dict[str, float]:
    """결측치를 제외한 최소/최대/평균 (df[col].describe())."""
    values = [float(row[key]) for row in rows if row[key] is not None]
    return {"min": min(values), "max": max(values), "mean": mean(values)}


# === 문제 3.4: 그룹화 (groupby 집계) ===
SALES = [
    {"date": "2026-07-01", "category": "식품", "amount": 100},
    {"date": "2026-07-15", "category": "의류", "amount": 200},
    {"date": "2026-08-01", "category": "식품", "amount": 50},
    {"date": "2026-08-10", "category": "의류", "amount": 300},
]

def group_sum(rows: list[dict], key_fn: Callable[[dict], str],
              value_key: str) -> dict[str, int]:
    """키 함수로 묶어 값 합계 — pandas groupby().sum() 등가."""
    totals: dict[str, int] = defaultdict(int)
    for row in rows:
        totals[key_fn(row)] += row[value_key]
    return dict(totals)


def sales_by_category(rows: list[dict]) -> dict[str, int]:
    return group_sum(rows, lambda r: r["category"], "amount")


def sales_by_month(rows: list[dict]) -> dict[str, int]:
    return group_sum(rows, lambda r: r["date"][:7], "amount")


# === 문제 3.5: 시각화 (matplotlib 대체 — ASCII 차트) ===
def ascii_histogram(values: list[float], bins: int = 5, width: int = 40) -> str:
    """값 분포를 히스토그램 막대 문자열로."""
    lo, hi = min(values), max(values)
    span = (hi - lo) / bins or 1
    counts = [0] * bins
    for v in values:
        idx = min(int((v - lo) / span), bins - 1)
        counts[idx] += 1
    unit = max(counts) / width if max(counts) else 1
    lines = []
    for i, count in enumerate(counts):
        edge = lo + i * span
        bars = "█" * round(count / unit) if count else ""
        lines.append(f"{edge:7.1f} │{bars} ({count})")
    return "\n".join(lines)


def five_number_summary(values: list[float]) -> dict[str, float]:
    """박스플롯의 다섯 숫자 요약(최소·Q1·중앙값·Q3·최대)."""
    ordered = sorted(values)

    def quantile(q: float) -> float:
        pos = (len(ordered) - 1) * q
        low = math.floor(pos)
        frac = pos - low
        high = min(low + 1, len(ordered) - 1)
        return ordered[low] + (ordered[high] - ordered[low]) * frac

    return {
        "min": ordered[0],
        "q1": quantile(0.25),
        "median": quantile(0.5),
        "q3": quantile(0.75),
        "max": ordered[-1],
    }


# ════════════════════════════════════════════════
# 04. 자동화
# ════════════════════════════════════════════════

EXTENSION_MAP = {
    ".jpg": "images", ".png": "images", ".gif": "images",
    ".pdf": "documents", ".txt": "documents", ".docx": "documents",
    ".zip": "archives", ".tar.gz": "archives",
}


# === 문제 4.1: 파일 정리 ===
def organize_downloads(folder: Path) -> dict[str, int]:
    """확장자별 하위 폴더로 파일 이동 — 폴더별 파일 수 반환."""
    moved: dict[str, int] = {}
    for file_path in sorted(folder.iterdir()):
        if not file_path.is_file():
            continue
        target_dir = EXTENSION_MAP.get(file_path.suffix.lower(), "기타")
        dest = folder / target_dir
        dest.mkdir(exist_ok=True)
        shutil.move(str(file_path), dest / file_path.name)
        moved[target_dir] = moved.get(target_dir, 0) + 1
    return moved


# === 문제 4.2: 웹 스크래퍼 ===
class _HeadlineParser(html.parser.HTMLParser):
    """h1~h3 헤드라인 텍스트 수집기 (BeautifulSoup 대체)."""

    def __init__(self):
        super().__init__()
        self.headlines: list[str] = []
        self._stack: list[tuple[str, list[str]]] = []

    def handle_starttag(self, tag, attrs):
        if tag in ("h1", "h2", "h3"):
            self._stack.append((tag, []))

    def handle_endtag(self, tag):
        if self._stack and self._stack[-1][0] == tag:
            _, buf = self._stack.pop()
            text = "".join(buf).strip()
            if text:
                self.headlines.append(text)

    def handle_data(self, data):
        if self._stack:
            self._stack[-1][1].append(data)


def scrape_headlines(html_text: str) -> list[str]:
    parser = _HeadlineParser()
    parser.feed(html_text)
    return parser.headlines


SAMPLE_NEWS_HTML = """
<html><body>
  <h1>오늘의 주요 뉴스</h1>
  <h2 class="headline">경제: 금리 동결 발표</h2>
  <h2 class="headline">과학: 새로운 소행성 발견</h2>
  <h2 class="headline">스포츠: 국가대표 승리</h2>
  <h2 class="headline">문화: 서점 베스트셀러 공개</h2>
  <h2 class="headline">기술: 신형 칩 공개</h2>
  <h2 class="headline">사회: 대중교통 개편 안내</h2>
  <h2 class="headline">날씨: 주말 폭염 주의보</h2>
  <h2 class="headline">국제: 정상회담 일정 확정</h2>
  <h2 class="headline">연예: 영화제 초청작 발표</h2>
  <h2 class="headline">교육: 새 학사 일정 공지</h2>
  <h3>여론 조사 결과 요약</h3>
</body></html>
"""


def headlines_to_json(html_text: str, out_path: Path) -> list[str]:
    headlines = scrape_headlines(html_text)
    out_path.write_text(
        json.dumps(headlines, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return headlines


def fetch_live_html(url: str, timeout: float = 5.0) -> str:
    """실제 사이트용 함수 (검증에선 오프라인 유지를 위해 실행하지 않음).

    with urllib.request.urlopen(url, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, errors="replace")
    """


# === 문제 4.3: 자동 백업 ===
def backup_zip(src_dir: Path, zip_path: Path) -> int:
    """디렉토리 전체를 ZIP 으로 압축, 담긴 파일 수 반환."""
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in sorted(src_dir.rglob("*")):
            if file_path.is_file():
                arcname = file_path.relative_to(src_dir)
                zf.write(file_path, arcname)
    with zipfile.ZipFile(zip_path) as zf:
        return sum(1 for name in zf.namelist())


def nightly_backup_plan(src_dir: Path) -> str:
    """매일 자정 실행 계획 문자열 (실제 무한 루프는 데몬/cron 에 맡긴다).

    코드 방식: while True 로 다음 자정까지 sleep 후 backup_zip 호출.
    운영 방식: cron `0 0 * * * python backup.py` 권장.
    """
    now = datetime.now()
    next_midnight = (now + timedelta(days=1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    seconds_left = (next_midnight - now).total_seconds()
    return (
        f"백업 대상: {src_dir}\n"
        f"다음 실행까지 {seconds_left:.0f}초 (자정)\n"
        f"cron 등록: 0 0 * * * /usr/bin/python3 backup.py {src_dir}"
    )


# === 문제 4.4: 이미지 리사이즈 ===
def resize_images(folder: Path, max_px: int = 800) -> str:
    """폴더 내 모든 이미지를 max_px 이하로 축소 (Pillow 필요).

    Pillow 가 없으면 건너뜀 메시지 반환 — 스크립트는 항상 종료 코드 0.
    """
    try:
        from PIL import Image  # type: ignore[import-not-found]
    except ImportError:
        return "⏭ Pillow 미설치 — 건너뜀 (pip install pillow)"

    resized = 0
    for image_path in sorted(folder.iterdir()):
        suffix = image_path.suffix.lower()
        if suffix not in (".jpg", ".jpeg", ".png", ".gif"):
            continue
        with Image.open(image_path) as img:
            w, h = img.size
            scale = min(1.0, max_px / max(w, h))
            if scale < 1.0:
                img.resize((round(w * scale), round(h * scale))).save(image_path)
                resized += 1
    return f"✅ {resized}개 이미지 리사이즈 완료"


# === 문제 4.5: 시간표 알림 ===
def build_morning_email(todos: list[str], today: date) -> EmailMessage:
    """오늘의 일정으로 아침 메일 본문 작성."""
    lines = "\n".join(f"- {todo}" for todo in todos) or "- 오늘 일정 없음"
    message = EmailMessage()
    message["Subject"] = f"📋 오늘의 일정 ({today:%Y-%m-%d})"
    message["To"] = "me@example.com"
    message.set_content(
        f"오늘 {today:%m월 %d일} 일정입니다:\n\n{lines}\n\n즐거운 하루 되세요!"
    )
    return message


def send_email(message: EmailMessage, smtp_host: str = "localhost") -> None:
    """실제 전송은 환경변수로 명시적 활성화했을 때만 실행 (테스트 안전)."""
    if os.environ.get("EXPERT_SEND_EMAIL") != "1":
        raise RuntimeError(
            "전송 방지: EXPERT_SEND_EMAIL=1 환경변수를 설정한 경우에만 발송"
        )
    with smtplib.SMTP(smtp_host) as smtp:
        smtp.send_message(message)


# ════════════════════════════════════════════════
# 05. 베스트 프랙티스
# ════════════════════════════════════════════════

# === 문제 5.1: 리팩토링 (지저분한 코드 → Pythonic) ===
def total_price_dirty(items: list[dict]) -> float:
    """❌ 개선 전: 인덱스 루프 + 누적 변수."""
    total = 0
    for i in range(len(items)):
        total = total + items[i]["price"] * items[i]["qty"]
    return total


def total_price_pythonic(items: list[dict]) -> float:
    """✅ 개선 후: 컴프리헨션 + sum."""
    return sum(item["price"] * item["qty"] for item in items)


def greeting_dirty(names: list[str]) -> str:
    """❌ 개선 전: 문자열 += 연결 (O(n²))."""
    result = ""
    for i in range(len(names)):
        if i == len(names) - 1:
            result = result + names[i]
        else:
            result = result + names[i] + ", "
    return result


def greeting_pythonic(names: list[str]) -> str:
    """✅ 개선 후: join 한 번으로 연결 (O(n))."""
    return ", ".join(names)


def first_even_dirty(numbers: list[int]):
    """❌ 개선 전: 존재 플래그 관리."""
    found = None
    for n in numbers:
        if n % 2 == 0:
            found = n
            break
    return found  # 없으면 None


def first_even_pythonic(numbers: list[int], default: int | None = None):
    """✅ 개선 후: next + 제너레이터 (LBYL 대신 선언형)."""
    return next((n for n in numbers if n % 2 == 0), default)


def append_tag_dirty(tag: str, tags: list[str] = []) -> list[str]:
    """❌ 위험한 코드: 기본 인자는 '한 번만' 생성되어 호출 간 공유된다."""
    tags.append(tag)
    return tags


def append_tag_clean(tag: str, tags: list[str] | None = None) -> list[str]:
    """✅ 개선 후: None 센티널로 호출마다 새 리스트."""
    result = tags if tags is not None else []
    result.append(tag)
    return result


# === 문제 5.2: 코드 리뷰 체크리스트 ===
REVIEW_CHECKLIST: list[str] = [
    "네이밍: 변수/함수 이름이 역할을 설명하는가",
    "단일 책임: 함수가 한 가지 일만 하는가",
    "타입 힌트: 공개 함수에 힌트가 있는가",
    "예외 처리: 구체적 예외를 잡고 무시하지 않는가",
    "매직 넘버: 상수로 명명되었는가",
    "중복 제거(DRY): 같은 로직이 반복되지 않는가",
    "문서화: 복잡한 로직에 docstring/주석이 있는가",
    "테스트 가능성: 의존성 주입/순수 함수로 분리 가능한가",
    "보안: 입력 검증, 시크릿 하드코딩 여부 확인",
    "성능: 명백한 O(n²)/무한 메모리 패턴은 없는가",
]


# === 문제 5.3: 타입 힌트 추가 ===
def average_score_untyped(scores):
    # ❌ 원래 코드 — scores 가 뭔지, 뭘 반환하는지 알 수 없다
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def average_score_typed(scores: list[float]) -> float:
    """✅ 힌트 추가 버전 — 읽는 사람과 mypy 모두 이해한다."""
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


# === 문제 5.4: 도구 설정 샘플 ===
TOOL_CONFIGS: dict[str, str] = {
    "pyproject.toml [tool.black]": "[tool.black]\nline-length = 100\n",
    "ruff (pyproject.toml)": (
        "[tool.ruff]\nline-length = 100\n"
        "[tool.ruff.lint]\nselect = [\"E\", \"F\", \"I\", \"B\"]\n"
    ),
    "mypy (pyproject.toml)": (
        "[tool.mypy]\npython_version = \"3.12\"\nstrict = true\n"
    ),
    ".pre-commit-config.yaml": (
        "repos:\n"
        "  - repo: https://github.com/psf/black\n"
        "    rev: 24.4.2\n"
        "    hooks:\n"
        "      - id: black\n"
        "  - repo: https://github.com/astral-sh/ruff-pre-commit\n"
        "    rev: v0.4.4\n"
        "    hooks:\n"
        "      - id: ruff\n"
    ),
}


# === 문제 5.5 + 6.5: GitHub Actions CI ===
TEST_CI_YAML = """\
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install pytest
      - run: pytest
"""

BUILD_CI_YAML = """\
name: lint-test-build
on: [push]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install ruff
      - run: ruff check .
  test:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install pytest
      - run: pytest
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install build
      - run: python -m build
"""


# ════════════════════════════════════════════════
# 06. 프로젝트 구조
# ════════════════════════════════════════════════

SRC_LAYOUT_PYPROJECT = """\
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "pkg-sample"
version = "0.1.0"

[tool.setuptools.packages.find]
where = ["src"]
"""


# === 문제 6.1: 기본 구조 (src layout) ===
def create_src_layout(root: Path) -> dict[str, Path]:
    """src layout 패키지 골격 생성 — 생성된 파일 경로 반환."""
    src_pkg = root / "src" / "pkg_sample"
    tests = root / "tests"
    src_pkg.mkdir(parents=True)
    tests.mkdir(parents=True)
    files = {
        "pyproject": root / "pyproject.toml",
        "__init__": src_pkg / "__init__.py",
        "core": src_pkg / "core.py",
        "test": tests / "test_core.py",
    }
    files["pyproject"].write_text(SRC_LAYOUT_PYPROJECT, encoding="utf-8")
    files["__init__"].write_text("", encoding="utf-8")
    files["core"].write_text(
        'def add(a: float, b: float) -> float:\n    """두 수를 더한다."""\n'
        "    return a + b\n",
        encoding="utf-8",
    )
    files["test"].write_text(
        "from pkg_sample.core import add\n\n\ndef test_add():\n"
        "    assert add(2, 3) == 5\n",
        encoding="utf-8",
    )
    return files


# === 문제 6.2: 도메인 분리 (ToDo 앱 4계층) ===
class Status(str, Enum):
    TODO = "할 일"
    DONE = "완료"


@dataclass
class Todo:  # ── 계층 1: 도메인 (순수 비즈니스 모델)
    id: int
    title: str
    status: Status = Status.TODO


class TodoRepository(ABC):  # ── 계층 2: 저장소 인터페이스
    @abstractmethod
    def add(self, todo: Todo) -> None: ...

    @abstractmethod
    def get(self, todo_id: int) -> Optional[Todo]: ...

    @abstractmethod
    def all(self) -> list[Todo]: ...

    @abstractmethod
    def update(self, todo: Todo) -> None: ...


class InMemoryTodoRepository(TodoRepository):  # ── 교체 가능한 구현
    def __init__(self):
        self._items: dict[int, Todo] = {}

    def add(self, todo: Todo) -> None:
        self._items[todo.id] = todo

    def get(self, todo_id: int) -> Optional[Todo]:
        return self._items.get(todo_id)

    def all(self) -> list[Todo]:
        return list(self._items.values())

    def update(self, todo: Todo) -> None:
        self._items[todo.id] = todo


class TodoService:  # ── 계층 3: 서비스 (유스케이스)
    def __init__(self, repo: TodoRepository):
        # 핵심 아이디어: 서비스는 추상 리포지토리에만 의존 (DIP)
        self.repo = repo
        self._next_id = 1

    def add_todo(self, title: str) -> Todo:
        todo = Todo(id=self._next_id, title=title)
        self._next_id += 1
        self.repo.add(todo)
        return todo

    def complete(self, todo_id: int) -> bool:
        todo = self.repo.get(todo_id)
        if todo is None:
            return False
        todo.status = Status.DONE
        self.repo.update(todo)
        return True

    def list_todos(self) -> list[Todo]:
        return self.repo.all()


def format_todo(todo: Todo) -> str:  # ── 계층 4: 프레젠테이션
    mark = "✅" if todo.status is Status.DONE else "⬜"
    return f"{mark} [{todo.id}] {todo.title}"


# === 문제 6.3: 의존성 주입 ===
class Notifier(ABC):
    @abstractmethod
    def send(self, to: str, message: str) -> None: ...


class EmailNotifier(Notifier):
    def __init__(self):
        self.sent: list[tuple[str, str]] = []

    def send(self, to: str, message: str) -> None:
        self.sent.append((to, message))


class BroadcastService:
    """알림 수단을 외부에서 주입받는다 — 테스트 시 가짜로 교체 용이."""

    def __init__(self, notifier: Notifier):
        self.notifier = notifier

    def broadcast(self, recipients: list[str], message: str) -> int:
        for recipient in recipients:
            self.notifier.send(recipient, message)
        return len(recipients)


# === 문제 6.4: 환경 설정 (pydantic-settings 대체) ===
@dataclass
class Settings:
    """환경별 설정 — 환경변수 > 기본값 순으로 해석."""

    debug: bool = False
    port: int = 8000
    db_url: str = "sqlite:///local.db"

    @classmethod
    def from_env(cls, prefix: str = "APP_") -> "Settings":
        def getenv(key: str, fallback: str) -> str:
            return os.environ.get(prefix + key, fallback)

        return cls(
            debug=getenv("DEBUG", "false").lower() == "true",
            port=int(getenv("PORT", "8000")),
            db_url=getenv("DB_URL", "sqlite:///local.db"),
        )


# ════════════════════════════════════════════════
# 캡스톤 프로젝트 안내 (problems.md 참고)
# ════════════════════════════════════════════════
CAPSTONE_GUIDE = """\
🚀 캡스톤 프로젝트는 problems.md 에서 하나(A~F)를 골라 완성하세요.
   필수 산출물: README · pyproject.toml · 테스트 커버리지 80%+ · 타입 힌트
              · CI/CD · 의존성 주입 · 에러 처리/로깅 (Docker 는 선택)
   예: 프로젝트 D(task tracker)라면 Typer CLI + Rich 출력 + ~/.config 설정
"""

# ════════════════════════════════════════════════
# 검증 — python3 solutions.py 로 실행
# ════════════════════════════════════════════════
if __name__ == "__main__":
    # ── 01. 디자인 패턴 ──
    logger_a = SingletonLogger()
    logger_b = SingletonLogger()
    assert logger_a is logger_b          # 같은 인스턴스
    logger_a.log("첫 메시지")
    logger_b.log("둘째 메시지")
    assert logger_a.logs == ["첫 메시지", "둘째 메시지"]  # 상태 공유

    circle = create_shape("circle", r=1)
    rect = create_shape("rectangle", w=3, h=4)
    tri = create_shape("triangle", base=3, height=4, side_a=4, side_b=5)
    assert math.isclose(circle.area(), math.pi)
    assert math.isclose(rect.area(), 12) and math.isclose(rect.perimeter(), 14)
    assert math.isclose(tri.area(), 6) and math.isclose(tri.perimeter(), 12)
    try:
        create_shape("hexagon")
        assert False
    except ValueError:
        pass

    stock = StockPrice("ACME", 100.0)
    change_log = ChangeLog()
    stock.attach(change_log)
    stock.set_price(105.0)
    assert change_log.events == [("ACME", 100.0, 105.0)]
    stock.detach(change_log)
    stock.set_price(110.0)               # 구독 해제 후에는 통지 없음
    assert len(change_log.events) == 1

    sample_data = [5, 3, 1, 4, 2]
    expected_sorted = [1, 2, 3, 4, 5]
    for name in SORT_STRATEGIES:
        assert Sorter(name).sort(sample_data) == expected_sorted
    sorter = Sorter("bubble")
    assert sorter.sort(sample_data) == expected_sorted
    sorter.strategy_name = "quick"       # 런타임 전략 교체
    assert sorter.sort(sample_data) == expected_sorted

    editor = TextEditor()
    editor.execute(AppendText("abc"))
    assert editor.doc == "abc"
    editor.execute(InsertAt(1, "X"))
    assert editor.doc == "aXbc"
    editor.execute(DeleteAt(0, 1))
    assert editor.doc == "Xbc"
    assert editor.undo() and editor.undo() and editor.undo()
    assert editor.doc == ""
    assert not editor.undo()             # 되돌릴 항목 없음
    print("✅ 01. 디자인 패턴 (5 문제)")

    # ── 02. 웹 개발 (stdlib 등가 구현) ──
    status, body = router.dispatch("/hello")
    assert status == 200 and body == {"message": "Hello, World!"}
    status, body = router.dispatch("/square?n=7")
    assert status == 200 and body == {"n": 7, "square": 49}
    status, body = router.dispatch("/square?n=abc")
    assert status == 400                 # Pydantic 검증 실패에 해당
    status, body = router.dispatch("/users/42")
    assert status == 200 and body["name"] == "이영희"
    status, body = router.dispatch("/users/9999")
    assert status == 404

    user_store: dict[int, dict] = {}
    created_user = create_user(user_store, {
        "email": "hong@example.com", "name": "홍길동", "age": 30,
    })
    assert created_user["id"] == 1
    assert get_user(user_store, 1)["name"] == "홍길동"
    for bad_payload in (
        {"email": "잘못된@@이메일", "name": "홍길동", "age": 30},
        {"email": "hong@example.com", "name": "홍길동", "age": 300},
    ):
        try:
            create_user(user_store, bad_payload)
            assert False
        except ValidationError:
            pass

    secret = "study-secret"
    token = jwt_encode({"sub": "hong"}, secret, expires_in=60)
    decoded = jwt_decode(token, secret)
    assert decoded["sub"] == "hong" and "exp" in decoded
    try:
        jwt_decode(token, "다른 시크릿")
        assert False
    except InvalidTokenError:
        pass
    expired_token = jwt_encode({"sub": "hong"}, secret, expires_in=-1)
    try:
        jwt_decode(expired_token, secret)
        assert False
    except InvalidTokenError:
        pass
    head, tampered_body, sig = token.split(".")
    try:
        jwt_decode(f"{head}.{tampered_body[:-1]}0.{sig}", secret)
        assert False
    except InvalidTokenError:
        pass

    with tempfile.TemporaryDirectory() as tmp:
        user_repo = UserRepository(Path(tmp) / "users.db")
        kim = user_repo.create(email="kim@example.com", name="김철수")
        assert kim["id"] == 1
        try:
            user_repo.create(email="kim@example.com", name="김철수2")
            assert False
        except ValueError:
            pass                       # UNIQUE 제약 → 도메인 예외로 번역
        assert len(user_repo.list_all()) == 1
        assert user_repo.delete(kim["id"]) is True
        assert user_repo.get(kim["id"]) is None
        user_repo.conn.close()

    run_todo_tests()
    print("✅ 02. 웹 개발 (5 문제)")

    # ── 03. 데이터 분석 ──
    matrix = make_matrix(10, 10)
    evens = filter_even_flat(matrix)
    assert len(evens) == 50 and sum(evens) == 2450

    assert column(STUDENTS, "kor") == [90, 70, 60, 88, 77]
    assert top_student_by_average(STUDENTS) == "지연"

    with tempfile.TemporaryDirectory() as tmp:
        csv_path = Path(tmp) / "scores.csv"
        csv_path.write_text(
            "name,score,city\n"
            "Alice,90,Seoul\n"
            "Bob,,Busan\n"
            "Carol,85,\n"
            "Dave,70,Daegu\n",
            encoding="utf-8",
        )
        raw_rows = load_csv_rows(csv_path)
        assert len(raw_rows) == 4 and raw_rows[1]["score"] is None
        complete_rows = dropna_rows(raw_rows)
        assert [r["name"] for r in complete_rows] == ["Alice", "Dave"]
        filled_rows = fill_missing(raw_rows, "score", 0)
        stats = describe_numeric(filled_rows, "score")
        assert stats["min"] == 0 and stats["max"] == 90
        assert math.isclose(stats["mean"], 61.25)

    by_cat = sales_by_category(SALES)
    by_month = sales_by_month(SALES)
    assert by_cat == {"식품": 150, "의류": 500}
    assert by_month == {"2026-07": 300, "2026-08": 350}

    distribution = list(range(1, 101))
    hist = ascii_histogram(distribution, bins=5)
    assert hist.count("\n") == 4 and "█" in hist   # 5개 막대
    summary = five_number_summary(distribution)
    nums = [summary[k] for k in ("min", "q1", "median", "q3", "max")]
    assert nums == sorted(nums)                    # 단조 증가
    assert summary["median"] == 50.5
    print("✅ 03. 데이터 분석 (5 문제)")

    # ── 04. 자동화 ──
    with tempfile.TemporaryDirectory() as tmp:
        downloads = Path(tmp) / "downloads"
        downloads.mkdir()
        for filename in ("a.jpg", "b.png", "c.pdf", "d.txt", "e.zip", "f.bin"):
            (downloads / filename).write_bytes(b"x")
        moved_counts = organize_downloads(downloads)
        assert moved_counts == {"images": 2, "documents": 2, "archives": 1,
                                "기타": 1}
        assert (downloads / "images" / "a.jpg").exists()

        news_json = Path(tmp) / "headlines.json"
        headlines = headlines_to_json(SAMPLE_NEWS_HTML, news_json)
        assert len(headlines) >= 10                # 헤드라인 10개+
        assert json.loads(news_json.read_text(encoding="utf-8")) == headlines

        docs = Path(tmp) / "docs"
        docs.mkdir()
        (docs / "report.txt").write_text("보고서", encoding="utf-8")
        (docs / "notes.md").write_text("메모", encoding="utf-8")
        archive = Path(tmp) / "backup.zip"
        assert backup_zip(docs, archive) == 2      # ZIP 안 파일 수
        plan = nightly_backup_plan(docs)
        assert "cron" in plan                      # 매일 자정 실행 계획

        result = resize_images(downloads, max_px=800)
        assert result.startswith(("✅", "⏭"))      # Pillow 유무와 무관하게 통과

        today = date(2026, 8, 25)
        mail = build_morning_email(["스크럼 회의", "코드 리뷰"], today)
        assert f"{today:%m월 %d일}" in mail.get_content()
        assert "스크럼 회의" in mail.get_content()
        try:
            send_email(mail)                       # 가드가 작동해 전송 차단
            assert False
        except RuntimeError:
            pass
    print("✅ 04. 자동화 (5 문제)")

    # ── 05. 베스트 프랙티스 ──
    cart = [{"price": 1500, "qty": 2}, {"price": 500, "qty": 3}]
    assert total_price_dirty(cart) == total_price_pythonic(cart) == 4500

    names_list = ["민수", "지연", "철수"]
    assert greeting_dirty(names_list) == greeting_pythonic(names_list)

    assert first_even_dirty([1, 3, 4]) == first_even_pythonic([1, 3, 4]) == 4
    assert first_even_pythonic([1, 3], default=-1) == -1

    dirty_first = append_tag_dirty("python")
    dirty_second = append_tag_dirty("study")     # 기본 리스트가 공유되는 버그!
    assert dirty_first is dirty_second
    clean_first = append_tag_clean("python")
    clean_second = append_tag_clean("study")
    assert clean_first is not clean_second
    assert clean_first == ["python"] and clean_second == ["study"]

    assert len(REVIEW_CHECKLIST) >= 8
    assert average_score_untyped([80, 90, 100]) == average_score_typed(
        [80, 90, 100]
    ) == 90.0
    assert average_score_typed([]) == 0.0

    assert "line-length" in TOOL_CONFIGS["pyproject.toml [tool.black]"]
    assert "select" in TOOL_CONFIGS["ruff (pyproject.toml)"]
    assert "strict" in TOOL_CONFIGS["mypy (pyproject.toml)"]
    assert "repos:" in TOOL_CONFIGS[".pre-commit-config.yaml"]

    assert "on:" in TEST_CI_YAML and "pytest" in TEST_CI_YAML
    for job_name in ("lint:", "test:", "build:"):
        assert job_name in BUILD_CI_YAML         # 린트 → 테스트 → 빌드 파이프라인
    print("✅ 05. 베스트 프랙티스 (5 문제)")

    # ── 06. 프로젝트 구조 ──
    with tempfile.TemporaryDirectory() as tmp:
        project_root = Path(tmp)
        layout_files = create_src_layout(project_root)
        for label, path in layout_files.items():
            assert path.exists(), f"{label} 파일 미생성"

        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "pkg_sample.core", layout_files["core"]
        )
        core_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(core_mod)
        assert core_mod.add(2, 3) == 5
        assert "assert add" in layout_files["test"].read_text(encoding="utf-8")

    service = TodoService(InMemoryTodoRepository())
    grocery = service.add_todo("장보기")
    study = service.add_todo("파이썬 학습")
    assert grocery.id == 1 and study.id == 2
    assert service.complete(grocery.id) is True
    assert service.complete(999) is False
    rendered = "\n".join(format_todo(todo) for todo in service.list_todos())
    assert rendered.splitlines()[0].startswith("✅")   # 완료 표시
    assert "장보기" in rendered

    email_notifier = EmailNotifier()
    broadcaster = BroadcastService(email_notifier)     # 구현체를 주입
    assert broadcaster.broadcast(["a@x.com", "b@x.com"], "배포 완료") == 2
    assert len(email_notifier.sent) == 2

    class _FakeNotifier(Notifier):
        def __init__(self):
            self.sent: list[tuple[str, str]] = []

        def send(self, to: str, message: str) -> None:
            self.sent.append((to, message))

    fake_notifier = _FakeNotifier()
    BroadcastService(fake_notifier).broadcast(["test@x.com"], "안녕")
    assert fake_notifier.sent == [("test@x.com", "안녕")]  # 주입만 바꿔 교체

    default_settings = Settings.from_env()
    assert default_settings.port == 8000 and default_settings.debug is False
    os.environ["APP_DEBUG"] = "true"
    os.environ["APP_PORT"] = "9000"
    try:
        overridden = Settings.from_env()
        assert overridden.debug is True and overridden.port == 9000
    finally:
        os.environ.pop("APP_DEBUG", None)
        os.environ.pop("APP_PORT", None)

    print(CAPSTONE_GUIDE)
    print("✅ 06. 프로젝트 구조 (5 문제)")

    print("\n🎉 모든 테스트 통과! (본문 30문제 · 캡스톤은 problems.md 참고)")
