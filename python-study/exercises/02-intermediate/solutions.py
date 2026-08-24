"""
중급 연습 문제 — 정답 예시

먼저 스스로 풀어본 후 참고하세요!

실행: python3 solutions.py  (표준 라이브러리만 사용, 외부 의존성 없음)
"""

import argparse
import calendar
import csv
import hashlib
import importlib
import json
import math
import re
import shutil
import sys
import tempfile
import time
from abc import ABC, abstractmethod
from collections import Counter
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from functools import reduce
from itertools import islice
from pathlib import Path
from typing import Any, Callable


# ════════════════════════════════════════════════
# 01. 함수 심화
# ════════════════════════════════════════════════

# === 문제 1.1: 람다와 정렬 ===
def sort_by(data: list[dict], key: str, reverse: bool = False) -> list[dict]:
    """딕셔너리 리스트를 특정 키 기준으로 정렬한다."""
    # 핵심 아이디어: sorted 의 key 인자에 람다를 넣어 정렬 기준 지정
    return sorted(data, key=lambda item: item[key], reverse=reverse)


# === 문제 1.2: 함수 합성 ===
def compose(f: Callable, g: Callable) -> Callable:
    """두 함수를 합성: compose(f, g)(x) == f(g(x))"""
    # 핵심 아이디어: 클로저로 g 의 결과를 f 에 전달
    return lambda x: f(g(x))


# === 문제 1.3: 클로저 카운터 ===
def make_counter(start: int = 0, step: int = 1) -> Callable[[], int]:
    """호출할 때마다 step 씩 증가하는 값을 반환하는 카운터."""
    # 핵심 아이디어: nonlocal 로 바깥 변수를 클로저 안에서 갱신
    count = start

    def counter() -> int:
        nonlocal count
        value = count
        count += step
        return value

    return counter


# === 문제 1.4: 메모이제이션 데코레이터 ===
def memoize(func: Callable) -> Callable:
    """동일 인자에 대한 결과를 캐싱하는 데코레이터 (lru_cache 미사용)."""
    # 핵심 아이디어: (args, kwargs) 튜플을 dict 키로 삼아 결과 저장
    cache: dict[tuple, Any] = {}

    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper


# === 문제 1.5: map/filter/reduce ===
def even_square_sum(nums: list[int]) -> int:
    """짝수를 걸러 제곱한 뒤 모두 더한다 — map/filter/reduce 만 사용."""
    # 핵심 아이디어: filter(짝수) → map(제곱) → reduce(합산) 파이프라인
    return reduce(
        lambda acc, n: acc + n,
        map(lambda n: n * n, filter(lambda n: n % 2 == 0, nums)),
    )


# ════════════════════════════════════════════════
# 02. OOP
# ════════════════════════════════════════════════

# === 문제 2.1 + 4.3: BankAccount & 사용자 정의 예외 ===
class InsufficientFundsError(Exception):
    """잔액 부족 시 발생하는 사용자 정의 예외."""


class BankAccount:
    """입금/출금/잔액 확인이 가능한 계좌."""

    def __init__(self, owner: str, balance: int = 0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: int) -> int:
        if amount <= 0:
            raise ValueError("입금액은 양수여야 합니다")
        self.balance += amount
        return self.balance

    def withdraw(self, amount: int) -> int:
        if amount <= 0:
            raise ValueError("출금액은 양수여야 합니다")
        if amount > self.balance:
            # 핵심 아이디어: 상황에 맞는 커스텀 예외로 호출자가 원인을 구분하게 함
            raise InsufficientFundsError(
                f"잔액 부족: 잔액 {self.balance}, 요청 {amount}"
            )
        self.balance -= amount
        return self.balance


# === 문제 2.2: 도형 다형성 ===
class Shape(ABC):
    """면적/둘레 계산을 자식에게 강제하는 추상 부모 클래스."""

    @abstractmethod
    def area(self) -> float: ...

    @abstractmethod
    def perimeter(self) -> float: ...


class Rectangle(Shape):
    def __init__(self, w: float, h: float):
        self.w, self.h = w, h

    def area(self) -> float:
        return self.w * self.h

    def perimeter(self) -> float:
        return 2 * (self.w + self.h)


class Circle(Shape):
    def __init__(self, r: float):
        self.r = r

    def area(self) -> float:
        return math.pi * self.r**2

    def perimeter(self) -> float:
        return 2 * math.pi * self.r


class Triangle(Shape):
    def __init__(self, base: float, height: float, left: float, right: float):
        self.base, self.height = base, height
        self.left, self.right = left, right

    def area(self) -> float:
        return self.base * self.height / 2

    def perimeter(self) -> float:
        return self.base + self.left + self.right


# === 문제 2.3: Vector 클래스 ===
class Vector:
    """2D 벡터 — 연산자 오버로딩의 대표 예."""

    def __init__(self, x: float, y: float):
        self.x, self.y = x, y

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector":
        return Vector(self.x * scalar, self.y * scalar)

    def dot(self, other: "Vector") -> float:
        return self.x * other.x + self.y * other.y

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self) -> "Vector":
        m = self.magnitude
        if m == 0:
            raise ValueError("영벡터는 정규화할 수 없습니다")
        return Vector(self.x / m, self.y / m)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Vector) and self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"


# === 문제 2.4: 도서관 시스템 ===
@dataclass
class Book:
    title: str
    total: int
    available: int


class Library:
    """같은 책 여러 권 보유 가능 — 대출/반납 관리."""

    def __init__(self):
        self.books: dict[str, Book] = {}

    def add_book(self, title: str, copies: int = 1) -> None:
        if title in self.books:
            self.books[title].total += copies
            self.books[title].available += copies
        else:
            self.books[title] = Book(title, copies, copies)

    def borrow(self, title: str) -> None:
        book = self._get(title)
        if book.available <= 0:
            raise ValueError(f"'{title}' 은 현재 모두 대출 중입니다")
        book.available -= 1

    def return_book(self, title: str) -> None:
        book = self._get(title)
        if book.available >= book.total:
            raise ValueError(f"'{title}' 은 모두 반납된 상태입니다")
        book.available += 1

    def available(self, title: str) -> int:
        return self._get(title).available

    def _get(self, title: str) -> Book:
        if title not in self.books:
            raise KeyError(f"보유하지 않은 책: {title}")
        return self.books[title]


# === 문제 2.5: dataclass Product ===
@dataclass
class Product:
    """@dataclass 는 __init__/__repr__/__eq__ 를 자동 생성한다."""

    name: str = ""
    price: int = 0
    category: str = ""


def products_sorted_by_price(products: list[Product]) -> list[Product]:
    # 핵심 아이디어: key=lambda 로 정렬 기준 필드 지정
    return sorted(products, key=lambda p: p.price)


def products_in_category(products: list[Product], category: str) -> list[Product]:
    return [p for p in products if p.category == category]


# ════════════════════════════════════════════════
# 03. 모듈
# ════════════════════════════════════════════════

# === 문제 3.1: 계산기 모듈 ===
# 실제 프로젝트에서는 이 함수들을 calculator.py 로 분리하고
# `from calculator import add` 처럼 임포트한다. 여기선 한 파일에 정의.


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("0 으로 나눌 수 없습니다")
    return a / b


# === 문제 3.2: shapes 패키지 ===
SHAPES_INIT = """\
from .circle import Circle
from .rectangle import Rectangle

__all__ = ["Circle", "Rectangle"]
"""
SHAPES_CIRCLE = """\
import math

class Circle:
    def __init__(self, r):
        self.r = r
    def area(self):
        return math.pi * self.r ** 2
"""
SHAPES_RECTANGLE = """\
class Rectangle:
    def __init__(self, w, h):
        self.w, self.h = w, h
    def area(self):
        return self.w * self.h
"""


def build_shapes_package(root: Path) -> None:
    """shapes/ 패키지를 실제로 만든다 (검증부에서 임포트해 확인)."""
    pkg = root / "shapes"
    pkg.mkdir()
    (pkg / "__init__.py").write_text(SHAPES_INIT, encoding="utf-8")
    (pkg / "circle.py").write_text(SHAPES_CIRCLE, encoding="utf-8")
    (pkg / "rectangle.py").write_text(SHAPES_RECTANGLE, encoding="utf-8")


# === 문제 3.3: 가상 환경 (실행 불가 — 절차 안내) ===
VENV_GUIDE = """\
python3 -m venv .venv                 # 가상 환경 생성
source .venv/bin/activate             # 활성화 (Windows: .venv\\Scripts\\activate)
pip install requests beautifulsoup4   # 패키지 설치
pip freeze > requirements.txt         # 의존성 기록
"""


# === 문제 3.4: 날짜 차이 ===
def days_between(a: date, b: date) -> int:
    """두 날짜 사이의 일수 (순서 무관)."""
    # 핵심 아이디어: date 끼리 빼면 timedelta 가 나온다
    return abs((b - a).days)


def time_diff(d1: datetime, d2: datetime) -> timedelta:
    """두 시점 사이의 시간 차이."""
    return abs(d2 - d1)


# === 문제 3.5: 단어 빈도 (Counter) ===
def top_words(text: str, n: int = 10) -> list[tuple[str, int]]:
    """가장 흔한 단어 n개를 (단어, 빈도) 리스트로 반환."""
    # 핵심 아이디어: Counter.most_common(n) 한 방 처리
    return Counter(text.lower().split()).most_common(n)


# ════════════════════════════════════════════════
# 04. 예외 처리
# ════════════════════════════════════════════════

# === 문제 4.1: 안전한 나눗셈 ===
def safe_divide(a_str: str, b_str: str) -> str:
    """문자열 입력을 나눗셈 — 0 나눗셈/비숫자를 각각 처리."""
    # 핵심 아이디어: 예외 종류별로 다른 except 절
    try:
        a, b = float(a_str), float(b_str)
    except ValueError:
        return "오류: 숫자를 입력하세요"
    try:
        return f"{a / b:g}"
    except ZeroDivisionError:
        return "오류: 0 으로 나눌 수 없습니다"


# === 문제 4.2: 파일 안전 읽기 ===
def read_config(path: str | Path) -> tuple[bool, str, str]:
    """파일을 안전하게 읽는다 → (성공 여부, 내용, 오류 메시지)."""
    try:
        return True, Path(path).read_text(encoding="utf-8"), ""
    except FileNotFoundError:
        return False, "", "파일이 없습니다"
    except PermissionError:
        return False, "", "권한이 없습니다"


# === 문제 4.3: 사용자 정의 예외 → 2.1 의 BankAccount 와 통합됨 ===


# === 문제 4.4: 재시도 데코레이터 ===
def retry(times: int = 3, delay: float = 1.0) -> Callable:
    """실패 시 최대 times 번 재시도하는 데코레이터 팩토리."""
    # 핵심 아이디어: 데코레이터가 인자를 받으려면 한 겹 더 감싼다 (팩토리)

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            last_exc: Exception | None = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_exc = exc
                    if attempt < times and delay:
                        time.sleep(delay)
            raise RuntimeError(f"{times}번 모두 실패") from last_exc

        return wrapper

    return decorator


# === 문제 4.5: 검증 함수들 ===
EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")
PASSWORD_RE = re.compile(
    r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_\-+=~]).{8,20}$"
)
PHONE_RE = re.compile(r"^010-\d{4}-\d{4}$")


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_RE.match(email))


def is_valid_password(password: str) -> bool:
    """8-20자, 대소문자/숫자/특수문자 포함 — (?=...) lookahead 로 조건 나열."""
    return bool(PASSWORD_RE.match(password))


def is_valid_phone(phone: str) -> bool:
    return bool(PHONE_RE.match(phone))


# ════════════════════════════════════════════════
# 05. 파일 I/O
# ════════════════════════════════════════════════

# === 문제 5.1: 파일 복사 ===
def copy_lines(src: Path, dst: Path) -> int:
    """한 줄씩 읽어 다른 파일로 복사, 복사한 줄 수 반환."""
    count = 0
    with open(src, encoding="utf-8") as fin, open(dst, "w", encoding="utf-8") as fout:
        for line in fin:  # 파일 객체 순회 = 한 줄씩 읽기 (메모리 안전)
            fout.write(line)
            count += 1
    return count


# === 문제 5.2: 단어 빈도 → JSON ===
def word_freq_to_json(text_path: Path, json_path: Path) -> dict[str, int]:
    text = text_path.read_text(encoding="utf-8")
    freq = dict(Counter(text.lower().split()))
    json_path.write_text(
        json.dumps(freq, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return freq


# === 문제 5.3: CSV 필터링 ===
def filter_csv(src: Path, dst: Path, predicate: Callable[[dict], bool]) -> int:
    """조건을 만족하는 행만 새 CSV 로 저장, 저장한 행 수 반환."""
    with open(src, newline="", encoding="utf-8") as fin, open(
        dst, "w", newline="", encoding="utf-8"
    ) as fout:
        reader = csv.DictReader(fin)
        writer = csv.DictWriter(fout, fieldnames=reader.fieldnames)
        writer.writeheader()
        count = 0
        for row in reader:
            if predicate(row):
                writer.writerow(row)
                count += 1
    return count


# === 문제 5.4: 디렉토리 트리 ===
def tree_lines(root: Path, prefix: str = "") -> list[str]:
    """`tree` 명령처럼 디렉토리 구조를 그림 문자열 목록으로 반환."""
    lines: list[str] = []
    entries = sorted(root.iterdir(), key=lambda p: (p.is_file(), p.name))
    for i, entry in enumerate(entries):
        last = i == len(entries) - 1
        connector = "└── " if last else "├── "
        lines.append(prefix + connector + entry.name)
        if entry.is_dir():
            extension = "    " if last else "│   "
            lines.extend(tree_lines(entry, prefix + extension))
    return lines


# === 문제 5.5: 백업 컨텍스트 매니저 ===
@contextmanager
def opened_with_backup(path: str | Path, mode: str = "r"):
    """파일을 열기 전 자동으로 .bak 백업을 만드는 컨텍스트 매니저."""
    # 핵심 아이디어: @contextmanager — yield 앞(준비)/뒤(정리) 코드 감싸기
    target = Path(path)
    backup = target.with_suffix(target.suffix + ".bak")
    if target.exists():
        shutil.copy2(target, backup)
    f = open(target, mode, encoding="utf-8")
    try:
        yield f
    finally:
        f.close()


# ════════════════════════════════════════════════
# 06. 정규표현식
# ════════════════════════════════════════════════

PHONE_FIND_RE = re.compile(r"\b010-\d{4}-\d{4}\b")


# === 문제 6.1: 전화번호 추출 ===
def extract_phones(text: str) -> list[str]:
    """텍스트에서 010-XXXX-XXXX 형식을 모두 추출."""
    return PHONE_FIND_RE.findall(text)


# === 문제 6.2: 이메일 마스킹 ===
def mask_email(email: str) -> str:
    """alice@example.com → a****@example.com"""
    local, _, domain = email.partition("@")
    return f"{local[0]}****@{domain}" if local else email


# === 문제 6.3: 날짜 형식 변환 ===
def convert_date(text: str) -> str:
    """2026/05/12 → 2026-05-12 (캡처 그룹 역참조 \\1-\\2-\\3)."""
    return re.sub(r"(\d{4})/(\d{2})/(\d{2})", r"\1-\2-\3", text)


# === 문제 6.4: 숫자 추출 ===
def extract_numbers(text: str) -> list[int]:
    return [int(m) for m in re.findall(r"\d+", text)]


# === 문제 6.5: 비밀번호 정규식 → 4.5 의 PASSWORD_RE / is_valid_password 재사용 ===


# ════════════════════════════════════════════════
# 07. 컴프리헨션과 제너레이터
# ════════════════════════════════════════════════

# === 문제 7.1: 짝수 제곱 ===
def even_squares() -> list[int]:
    return [n * n for n in range(1, 21) if n % 2 == 0]


# === 문제 7.2: 단어 길이 딕셔너리 ===
def word_lengths(words: list[str]) -> dict[str, int]:
    return {word: len(word) for word in words}


# === 문제 7.3: 평면화 ===
def flatten(nested: list[list]) -> list:
    # 핵심 아이디어: for 문 두 개를 왼쪽→오른쪽 순서로 읽는다
    return [item for row in nested for item in row]


# === 문제 7.4: 무한 카운터 제너레이터 ===
def infinite_counter(start: int = 0, step: int = 1):
    """필요할 때만 값을 만드는(lazy) 무한 제너레이터."""
    current = start
    while True:
        yield current
        current += step


# === 문제 7.5: 파일 grep 제너레이터 ===
def grep_lines(path: str | Path, pattern: str):
    """패턴이 포함된 줄만 하나씩 yield — 큰 파일도 스트리밍 처리."""
    with open(path, encoding="utf-8") as f:
        for line in f:
            if pattern in line:
                yield line.rstrip("\n")


# === 문제 7.6: 짝 만들기 ===
def pairwise(items):
    """인접한 두 원소씩 yield: (1,2), (2,3), (3,4) ..."""
    it = iter(items)
    prev = next(it, None)
    for cur in it:
        yield (prev, cur)
        prev = cur


# ════════════════════════════════════════════════
# 08. 표준 라이브러리
# ════════════════════════════════════════════════

# === 문제 8.1: Counter 활용 → 3.5 의 top_words 재사용 ===


# === 문제 8.2: 디렉토리 통계 ===
def extension_stats(dirpath: Path) -> dict[str, int]:
    """확장자별 파일 개수 (확장자 없으면 '(확장자 없음)')."""
    counter = Counter(
        p.suffix.lower() if p.suffix else "(확장자 없음)"
        for p in dirpath.iterdir()
        if p.is_file()
    )
    return dict(counter)


# === 문제 8.3: grep CLI ===
def build_grep_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mygrep", description="미니 grep 도구")
    parser.add_argument("pattern", help="찾을 패턴")
    parser.add_argument("files", nargs="+", help="대상 파일들")
    parser.add_argument("-n", action="store_true", help="줄 번호 출력")
    parser.add_argument("-i", action="store_true", help="대소문자 무시")
    return parser


def my_grep(argv: list[str]) -> list[str]:
    """argparse 로 만든 grep — argv 를 받아 결과 리스트 반환 (테스트 용이)."""
    args = build_grep_parser().parse_args(argv)
    flags = re.IGNORECASE if args.i else 0
    results = []
    for filepath in args.files:
        with open(filepath, encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                if re.search(args.pattern, line, flags):
                    if args.n:
                        results.append(f"{filepath}:{lineno}:{line.rstrip()}")
                    else:
                        results.append(line.rstrip())
    return results


# === 문제 8.4: 파일 해시 ===
def sha256_of_dir(dirpath: Path) -> dict[str, str]:
    """디렉토리 내 모든 파일의 SHA-256 → {상대경로: 해시}."""
    hashes = {}
    for p in sorted(dirpath.rglob("*")):
        if p.is_file():
            hashes[str(p.relative_to(dirpath))] = hashlib.sha256(
                p.read_bytes()
            ).hexdigest()
    return hashes


# === 문제 8.5: 만년 달력 ===
def month_calendar(year: int, month: int) -> str:
    return calendar.month(year, month)


# ════════════════════════════════════════════════
# 종합 프로젝트 1: 간단한 블로그 시스템
# ════════════════════════════════════════════════


class SimpleBlog:
    """글 CRUD + 태그/검색 + JSON 파일 저장."""

    def __init__(self):
        self.posts: dict[int, dict] = {}
        self._next_id = 1

    def add_post(self, title: str, body: str, tags: list[str] | None = None) -> int:
        post_id = self._next_id
        self._next_id += 1
        self.posts[post_id] = {
            "id": post_id,
            "title": title,
            "body": body,
            "tags": list(tags or []),
        }
        return post_id

    def update_post(self, post_id: int, **fields) -> None:
        post = self._get(post_id)
        for key in ("title", "body", "tags"):
            if key in fields:
                post[key] = fields[key]

    def delete_post(self, post_id: int) -> None:
        self._get(post_id)
        del self.posts[post_id]

    def get(self, post_id: int) -> dict | None:
        return self.posts.get(post_id)

    def search(self, keyword: str) -> list[dict]:
        return [
            p
            for p in self.posts.values()
            if keyword in p["title"] or keyword in p["body"]
        ]

    def by_tag(self, tag: str) -> list[dict]:
        return [p for p in self.posts.values() if tag in p["tags"]]

    def save(self, path: Path) -> None:
        path.write_text(
            json.dumps(list(self.posts.values()), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @classmethod
    def load(cls, path: Path) -> "SimpleBlog":
        blog = cls()
        for post in json.loads(path.read_text(encoding="utf-8")):
            blog.posts[post["id"]] = post
            blog._next_id = max(blog._next_id, post["id"] + 1)
        return blog

    def _get(self, post_id: int) -> dict:
        if post_id not in self.posts:
            raise KeyError(f"글 없음: {post_id}")
        return self.posts[post_id]


# ════════════════════════════════════════════════
# 종합 프로젝트 2: 가계부
# ════════════════════════════════════════════════


class Ledger:
    """수입/지출 기록, 카테고리·월별 통계, ASCII 차트."""

    def __init__(self):
        self.entries: list[dict] = []

    def add(self, date_iso: str, kind: str, category: str, amount: int) -> None:
        if kind not in ("수입", "지출"):
            raise ValueError("kind 는 '수입' 또는 '지출'")
        self.entries.append(
            {"date": date_iso, "kind": kind, "category": category, "amount": amount}
        )

    def balance(self) -> int:
        total = sum(e["amount"] for e in self.entries if e["kind"] == "수입")
        total -= sum(e["amount"] for e in self.entries if e["kind"] == "지출")
        return total

    def by_category(self) -> dict[str, int]:
        """카테고리별 순액 (수입 − 지출)."""
        result: dict[str, int] = {}
        for e in self.entries:
            sign = 1 if e["kind"] == "수입" else -1
            result[e["category"]] = result.get(e["category"], 0) + sign * e["amount"]
        return result

    def monthly_report(self, year: int, month: int) -> dict[str, int]:
        prefix = f"{year:04d}-{month:02d}"
        income = sum(
            e["amount"]
            for e in self.entries
            if e["date"].startswith(prefix) and e["kind"] == "수입"
        )
        expense = sum(
            e["amount"]
            for e in self.entries
            if e["date"].startswith(prefix) and e["kind"] == "지출"
        )
        return {"수입": income, "지출": expense, "순액": income - expense}

    @staticmethod
    def bar_chart(totals: dict[str, int], width: int = 30) -> str:
        """값을 █ 막대로 그린 ASCII 차트 (matplotlib 대체)."""
        if not totals or max(abs(v) for v in totals.values()) == 0:
            return ""
        unit = max(abs(v) for v in totals.values()) / width
        lines = []
        for cat, value in totals.items():
            bars = "█" * max(1, round(abs(value) / unit)) if value else ""
            lines.append(f"{cat:>6} │{bars} {value:,}")
        return "\n".join(lines)


# ════════════════════════════════════════════════
# 종합 프로젝트 3: 텍스트 에디터
# ════════════════════════════════════════════════


class TextEditor:
    """CLI 편집 버퍼 — 열기/저장/검색/치환/실행 취소(스냅샷 방식)."""

    def __init__(self):
        self.lines: list[str] = []
        self._undo_stack: list[list[str]] = []

    def open(self, text: str) -> None:
        self.lines = text.splitlines() or [""]

    def text(self) -> str:
        return "\n".join(self.lines)

    def save(self, path: Path) -> None:
        path.write_text(self.text(), encoding="utf-8")

    def _snapshot(self) -> None:
        # 핵심 아이디어: 변경 전 상태를 스택에 복사해 두면 undo 는 pop 한 번
        self._undo_stack.append(self.lines.copy())

    def insert_line(self, index: int, text: str) -> None:
        self._snapshot()
        self.lines.insert(index, text)

    def delete_line(self, index: int) -> str:
        self._snapshot()
        return self.lines.pop(index)

    def replace(self, old: str, new: str) -> int:
        """old 를 new 로 치환하고 치환한 줄 수 반환."""
        self._snapshot()
        count = 0
        for i, line in enumerate(self.lines):
            if old in line:
                self.lines[i] = line.replace(old, new)
                count += 1
        return count

    def find(self, keyword: str) -> list[int]:
        """키워드가 포함된 줄 번호(1-based) 목록."""
        return [i for i, line in enumerate(self.lines, 1) if keyword in line]

    def undo(self) -> bool:
        if not self._undo_stack:
            return False
        self.lines = self._undo_stack.pop()
        return True


# ════════════════════════════════════════════════
# 검증 — python3 solutions.py 로 실행
# ════════════════════════════════════════════════
if __name__ == "__main__":
    # ── 01. 함수 심화 ──
    people = [
        {"name": "a", "age": 3},
        {"name": "b", "age": 1},
        {"name": "c", "age": 2},
    ]
    assert [p["age"] for p in sort_by(people, "age")] == [1, 2, 3]
    assert [p["age"] for p in sort_by(people, "age", reverse=True)] == [3, 2, 1]

    assert compose(lambda x: x + 1, lambda x: x * 2)(3) == 7  # f(g(3)) = 6 + 1

    counter = make_counter(10, 5)
    assert [counter(), counter(), counter()] == [10, 15, 20]
    default_counter = make_counter()
    assert [default_counter(), default_counter()] == [0, 1]

    memo_calls: list = []

    @memoize
    def square(x: int, offset: int = 0) -> int:
        memo_calls.append((x, offset))
        return x * x + offset

    assert square(4) == 16
    assert square(4) == 16  # 캐시 히트 → 재계산 없음
    assert len(memo_calls) == 1
    assert square(4, offset=1) == 17
    assert len(memo_calls) == 2

    assert even_square_sum([1, 2, 3, 4, 5]) == 20  # 4 + 16
    print("✅ 01. 함수 심화 (5 문제)")

    # ── 02. OOP ──
    acc = BankAccount("홍길동", 0)
    acc.deposit(1000)
    acc.withdraw(400)
    assert acc.balance == 600
    try:
        acc.withdraw(999)
        assert False, "InsufficientFundsError 발생해야 함"
    except InsufficientFundsError:
        pass
    try:
        acc.deposit(-100)
        assert False
    except ValueError:
        pass

    shapes_list: list[Shape] = [Rectangle(3, 4), Circle(1), Triangle(3, 4, 4, 5)]
    assert math.isclose(shapes_list[0].area(), 12)
    assert math.isclose(shapes_list[0].perimeter(), 14)
    assert math.isclose(shapes_list[1].area(), math.pi)
    assert math.isclose(shapes_list[1].perimeter(), 2 * math.pi)
    assert math.isclose(shapes_list[2].area(), 6)
    assert math.isclose(shapes_list[2].perimeter(), 12)

    v = Vector(3, 4)
    assert v + Vector(1, 1) == Vector(4, 5)
    assert v - Vector(1, 1) == Vector(2, 3)
    assert v * 2 == Vector(6, 8)
    assert v.dot(Vector(1, 1)) == 7
    assert math.isclose(v.magnitude, 5.0)
    n = v.normalize()
    assert math.isclose(n.magnitude, 1.0)
    assert math.isclose(n.x, 0.6) and math.isclose(n.y, 0.8)

    lib = Library()
    lib.add_book("파이썬", 2)
    lib.borrow("파이썬")
    assert lib.available("파이썬") == 1
    lib.borrow("파이썬")
    try:
        lib.borrow("파이썬")
        assert False
    except ValueError:
        pass
    lib.return_book("파이썬")
    assert lib.available("파이썬") == 1

    prods = [
        Product(name="콜라", price=1500, category="음료"),
        Product(name="과자", price=2000, category="식품"),
        Product(name="사탕", price=500, category="식품"),
    ]
    assert [p.name for p in products_sorted_by_price(prods)] == ["사탕", "콜라", "과자"]
    assert [p.name for p in products_in_category(prods, "식품")] == ["과자", "사탕"]
    print("✅ 02. OOP (5 문제)")

    # ── 03. 모듈 ──
    assert add(2, 3) == 5
    assert subtract(5, 2) == 3
    assert multiply(3, 4) == 12
    assert divide(10, 4) == 2.5
    try:
        divide(1, 0)
        assert False
    except ZeroDivisionError:
        pass

    # shapes 패키지를 실제로 만들어 `from shapes import Circle` 확인
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        build_shapes_package(tmp_path)
        sys.path.insert(0, str(tmp_path))
        try:
            shapes_mod = importlib.import_module("shapes")
            assert math.isclose(shapes_mod.Circle(2).area(), 4 * math.pi)
            assert shapes_mod.Rectangle(2, 3).area() == 6
        finally:
            sys.path.remove(str(tmp_path))
            for name in [m for m in sys.modules if m.split(".")[0] == "shapes"]:
                del sys.modules[name]
    print(f"   💡 3.3 가상 환경 절차:\n{VENV_GUIDE}")

    assert days_between(date(2026, 1, 1), date(2026, 3, 1)) == 59  # 31 + 28 평년
    td = time_diff(datetime(2026, 1, 1, 10, 0), datetime(2026, 1, 1, 9, 30))
    assert td == timedelta(minutes=30)

    sea_text = "바다 하늘 바다 산 바다 강"
    top = top_words(sea_text, 10)
    assert top[0] == ("바다", 3)
    assert len(top) <= 10
    print("✅ 03. 모듈 (5 문제)")

    # ── 04. 예외 처리 ──
    assert safe_divide("10", "2") == "5"
    assert "0 으로" in safe_divide("10", "0")
    assert "숫자" in safe_divide("abc", "2")

    ok, content, err = read_config("존재하지_않는_파일.txt")
    assert not ok and err == "파일이 없습니다"

    retry_attempts: list[int] = []

    @retry(times=3, delay=0)
    def flaky() -> str:
        retry_attempts.append(len(retry_attempts))
        if len(retry_attempts) < 3:
            raise ConnectionError("일시적 장애")
        return "성공"

    assert flaky() == "성공" and len(retry_attempts) == 3

    @retry(times=3, delay=0)
    def always_fails() -> None:
        raise ValueError("영구 장애")

    try:
        always_fails()
        assert False
    except RuntimeError:
        pass

    assert is_valid_email("hong@example.com")
    assert not is_valid_email("hong@@bad")
    assert is_valid_password("Abc123!@")
    assert not is_valid_password("abc123!@")   # 대문자 없음
    assert not is_valid_password("Sh0rt!@")    # 8자 미만
    assert is_valid_phone("010-1234-5678")
    assert not is_valid_phone("011-1234-5678")
    print("✅ 04. 예외 처리 (5 문제)")

    # ── 05. 파일 I/O ──
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        src = tmp_path / "source.txt"
        src.write_text("가\n나\n다\n", encoding="utf-8")
        dst = tmp_path / "copy.txt"
        assert copy_lines(src, dst) == 3
        assert dst.read_text(encoding="utf-8") == "가\n나\n다\n"

        text_file = tmp_path / "words.txt"
        text_file.write_text("Apple banana apple", encoding="utf-8")
        freq_file = tmp_path / "freq.json"
        freq = word_freq_to_json(text_file, freq_file)
        assert freq == {"apple": 2, "banana": 1}
        assert json.loads(freq_file.read_text(encoding="utf-8")) == freq

        csv_in = tmp_path / "scores.csv"
        csv_in.write_text(
            "name,score\n민수,90\n지연,60\n철수,85\n", encoding="utf-8"
        )
        csv_out = tmp_path / "passed.csv"
        assert filter_csv(csv_in, csv_out, lambda row: int(row["score"]) >= 80) == 2
        assert "민수" in csv_out.read_text(encoding="utf-8")
        assert "지연" not in csv_out.read_text(encoding="utf-8")

        (tmp_path / "file1.txt").write_text("1", encoding="utf-8")
        folder = tmp_path / "folder"
        folder.mkdir()
        (folder / "file2.txt").write_text("2", encoding="utf-8")
        (folder / "file3.py").write_text("#", encoding="utf-8")
        tree = tree_lines(tmp_path)
        assert any(line.endswith("file2.txt") and "│" in line for line in tree)

        target = tmp_path / "app.cfg"
        target.write_text("v1", encoding="utf-8")
        with opened_with_backup(target, "a") as f:
            f.write("v2")
        assert target.read_text(encoding="utf-8") == "v1v2"
        assert target.with_suffix(".cfg.bak").read_text(encoding="utf-8") == "v1"
    print("✅ 05. 파일 I/O (5 문제)")

    # ── 06. 정규표현식 ──
    phone_text = "연락처: 010-1234-5678, 대체: 010-0000-0001"
    assert extract_phones(phone_text) == ["010-1234-5678", "010-0000-0001"]

    assert mask_email("alice@example.com") == "a****@example.com"
    assert mask_email("bob@test.co.kr") == "b****@test.co.kr"

    assert convert_date("2026/05/12") == "2026-05-12"

    assert extract_numbers("abc 123 def 456") == [123, 456]

    assert PASSWORD_RE.match("Passw0rd!") is not None
    assert PASSWORD_RE.match("password") is None          # 대문자/숫자/특수 없음
    assert PASSWORD_RE.match("PASSWORD1!") is None        # 소문자 없음
    assert PASSWORD_RE.match("Pw1!" + "a" * 20) is None   # 20자 초과
    print("✅ 06. 정규표현식 (5 문제)")

    # ── 07. 컴프리헨션과 제너레이터 ──
    assert even_squares() == [4, 16, 36, 64, 100, 144, 196, 256, 324, 400]

    assert word_lengths(["apple", "kiwi"]) == {"apple": 5, "kiwi": 4}

    assert flatten([[1, 2], [3, 4], [5, 6]]) == [1, 2, 3, 4, 5, 6]

    assert list(islice(infinite_counter(5, 3), 3)) == [5, 8, 11]
    assert list(islice(infinite_counter(), 2)) == [0, 1]

    with tempfile.TemporaryDirectory() as tmp:
        log_path = Path(tmp) / "app.log"
        log_path.write_text(
            "INFO 시작\nERROR 실패\nWARN 주의\nERROR 재실패\n", encoding="utf-8"
        )
        matched = list(grep_lines(log_path, "ERROR"))
        assert matched == ["ERROR 실패", "ERROR 재실패"]

    assert list(pairwise([1, 2, 3, 4])) == [(1, 2), (2, 3), (3, 4)]
    assert list(pairwise([1])) == []
    print("✅ 07. 컴프리헨션과 제너레이터 (6 문제)")

    # ── 08. 표준 라이브러리 ──
    common = top_words("사과 바나나 사과 포도 사과 바나나 딸기 귤 사과 배", 5)
    assert common[0] == ("사과", 4)
    assert len(common) == 5

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        for filename in ("a.txt", "b.txt", "c.py", "d.md", "e.txt"):
            (tmp_path / filename).write_text("x", encoding="utf-8")
        stats = extension_stats(tmp_path)
        assert stats[".txt"] == 3 and stats[".py"] == 1 and stats[".md"] == 1

        data_file = tmp_path / "data.log"
        data_file.write_text(
            "INFO ok\nERROR boom\ninfo fine\nERROR again\n", encoding="utf-8"
        )
        assert my_grep(["-n", "ERROR", str(data_file)]) == [
            f"{data_file}:2:ERROR boom",
            f"{data_file}:4:ERROR again",
        ]
        assert len(my_grep(["-i", "info", str(data_file)])) == 2  # INFO + info

        hashes = sha256_of_dir(tmp_path)
        assert hashes["a.txt"] == hashlib.sha256(b"x").hexdigest()
        json.loads(json.dumps(hashes))  # JSON 직렬화 가능 확인

    august = month_calendar(2026, 8)
    assert "August 2026" in august
    assert "Mo Tu We Th Fr Sa Su" in august  # 기본 시작 요일은 월요일
    print("✅ 08. 표준 라이브러리 (5 문제)")

    # ── 종합 프로젝트 1: 블로그 시스템 ──
    blog = SimpleBlog()
    pid1 = blog.add_post("파이썬 입문", "기초 문법 배우기", tags=["python"])
    pid2 = blog.add_post("정규식 팁", "re 모듈 활용법", tags=["regexp", "python"])
    assert pid1 == 1 and pid2 == 2
    assert [p["id"] for p in blog.search("정규식")] == [2]
    assert [p["id"] for p in blog.by_tag("python")] == [1, 2]
    blog.update_post(pid1, title="파이썬 기초")
    assert blog.get(pid1)["title"] == "파이썬 기초"
    with tempfile.TemporaryDirectory() as tmp:
        save_path = Path(tmp) / "blog.json"
        blog.save(save_path)
        restored = SimpleBlog.load(save_path)
        assert restored.get(pid1) == blog.get(pid1)
    blog.delete_post(pid2)
    assert blog.get(pid2) is None
    print("✅ 프로젝트 1: 블로그 시스템")

    # ── 종합 프로젝트 2: 가계부 ──
    ledger = Ledger()
    ledger.add("2026-07-05", "수입", "급여", 2_000_000)
    ledger.add("2026-07-10", "지출", "식비", 300_000)
    ledger.add("2026-07-20", "지출", "교통", 80_000)
    ledger.add("2026-08-02", "지출", "식비", 250_000)
    ledger.add("2026-08-15", "수입", "용돈", 50_000)
    assert ledger.balance() == 2_000_000 + 50_000 - 300_000 - 80_000 - 250_000
    assert ledger.by_category()["식비"] == -(300_000 + 250_000)
    july = ledger.monthly_report(2026, 7)
    assert july == {"수입": 2_000_000, "지출": 380_000, "순액": 1_620_000}
    chart = Ledger.bar_chart(ledger.by_category())
    assert "█" in chart and "급여" in chart
    print(chart)
    print("✅ 프로젝트 2: 가계부")

    # ── 종합 프로젝트 3: 텍스트 에디터 ──
    editor = TextEditor()
    editor.open("one\ntwo\nthree")
    assert editor.find("t") == [2, 3]
    assert editor.replace("o", "0") == 2  # one, two 두 줄
    assert editor.text() == "0ne\ntw0\nthree"
    editor.insert_line(1, "inserted")
    assert editor.lines == ["0ne", "inserted", "tw0", "three"]
    removed = editor.delete_line(0)
    assert removed == "0ne"
    assert editor.undo() and editor.undo() and editor.undo()
    assert editor.text() == "one\ntwo\nthree"
    assert not editor.undo()  # 되돌릴 게 없음
    with tempfile.TemporaryDirectory() as tmp:
        save_path = Path(tmp) / "doc.txt"
        editor.save(save_path)
        assert save_path.read_text(encoding="utf-8") == "one\ntwo\nthree"
    print("✅ 프로젝트 3: 텍스트 에디터")

    print("\n🎉 모든 테스트 통과! (본문 41문제 + 프로젝트 3개)")
