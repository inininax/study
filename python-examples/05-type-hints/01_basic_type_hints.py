"""
01_basic_type_hints.py - 기본 타입 힌트

📌 핵심 개념:
    Python 타입 힌트는 정적 분석과 IDE 지원을 위한 어노테이션입니다.
    런타임에는 강제되지 않습니다!

🔄 다른 언어 비교:
    - Java: 컴파일 타임에 타입 강제
    - Python: mypy 같은 도구로 별도 검사

📚 참고: https://docs.python.org/3/library/typing.html
"""

from __future__ import annotations

from typing import Any, Final, Literal, TypeAlias, TypedDict


# =============================================================================
# 기본 타입 힌트
# =============================================================================

def basic_types_demo() -> None:
    """기본 타입 힌트."""
    print("📌 기본 타입 힌트")
    print("=" * 50)
    
    # 기본 타입
    name: str = "Kim"
    age: int = 30
    height: float = 175.5
    is_active: bool = True
    
    # None 타입
    value: None = None
    
    # Optional (Union with None)
    optional_name: str | None = None
    
    print(f"name: {name} ({type(name).__name__})")
    print(f"age: {age} ({type(age).__name__})")
    print(f"optional_name: {optional_name}")


def collection_types_demo() -> None:
    """컬렉션 타입 힌트."""
    print("\n📌 컬렉션 타입 힌트")
    print("=" * 50)
    
    # Python 3.9+ 내장 타입으로 Generic 가능
    numbers: list[int] = [1, 2, 3]
    mapping: dict[str, int] = {"a": 1, "b": 2}
    unique: set[str] = {"x", "y", "z"}
    point: tuple[int, int] = (10, 20)
    
    # 가변 길이 튜플
    coords: tuple[float, ...] = (1.0, 2.0, 3.0, 4.0)
    
    print(f"list[int]: {numbers}")
    print(f"dict[str, int]: {mapping}")
    print(f"set[str]: {unique}")
    print(f"tuple[int, int]: {point}")
    print(f"tuple[float, ...]: {coords}")


def function_types_demo() -> None:
    """함수 타입 힌트."""
    print("\n📌 함수 타입 힌트")
    print("=" * 50)
    
    def greet(name: str, greeting: str = "Hello") -> str:
        """기본값이 있는 함수."""
        return f"{greeting}, {name}!"
    
    def process_items(items: list[str]) -> list[str]:
        """리스트 반환 함수."""
        return [item.upper() for item in items]
    
    def no_return() -> None:
        """반환값 없는 함수."""
        print("  이 함수는 반환값이 없습니다")
    
    print(f"greet('Kim'): {greet('Kim')}")
    print(f"process_items(['a', 'b']): {process_items(['a', 'b'])}")
    no_return()


def union_types_demo() -> None:
    """Union 타입."""
    print("\n📌 Union 타입")
    print("=" * 50)
    
    # Python 3.10+ | 문법
    def process(value: int | str) -> str:
        if isinstance(value, int):
            return f"정수: {value}"
        return f"문자열: {value}"
    
    print(f"process(42): {process(42)}")
    print(f"process('hello'): {process('hello')}")


def literal_final_demo() -> None:
    """Literal과 Final."""
    print("\n📌 Literal과 Final")
    print("=" * 50)
    
    # Literal - 특정 값만 허용
    def set_mode(mode: Literal["read", "write", "append"]) -> str:
        return f"Mode: {mode}"
    
    # Final - 상수 (재할당 불가 표시)
    MAX_SIZE: Final = 100
    API_VERSION: Final[str] = "v1"
    
    print(f"set_mode('read'): {set_mode('read')}")
    print(f"MAX_SIZE: {MAX_SIZE}")
    print(f"API_VERSION: {API_VERSION}")


def typeddict_demo() -> None:
    """TypedDict - 딕셔너리 스키마."""
    print("\n📌 TypedDict")
    print("=" * 50)
    
    class UserDict(TypedDict):
        name: str
        age: int
        email: str
    
    user: UserDict = {
        "name": "Kim",
        "age": 30,
        "email": "kim@example.com"
    }
    
    print(f"UserDict: {user}")


def type_alias_demo() -> None:
    """타입 별칭."""
    print("\n📌 타입 별칭")
    print("=" * 50)
    
    # Python 3.10+ TypeAlias
    UserId: TypeAlias = int
    UserDict: TypeAlias = dict[str, Any]
    
    def get_user(user_id: UserId) -> UserDict:
        return {"id": user_id, "name": "Kim"}
    
    print(f"get_user(1): {get_user(1)}")


def main() -> None:
    """메인 실행."""
    basic_types_demo()
    collection_types_demo()
    function_types_demo()
    union_types_demo()
    literal_final_demo()
    typeddict_demo()
    type_alias_demo()
    
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                   타입 힌트 정리                               ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║                                                               ║
    ║  기본 타입:                                                   ║
    ║    str, int, float, bool, None                                ║
    ║                                                               ║
    ║  컬렉션 (Python 3.9+):                                        ║
    ║    list[T], dict[K, V], set[T], tuple[T, ...]                ║
    ║                                                               ║
    ║  Union (Python 3.10+):                                        ║
    ║    int | str  (이전: Union[int, str])                         ║
    ║    str | None (이전: Optional[str])                           ║
    ║                                                               ║
    ║  특수:                                                        ║
    ║    Any, Literal, Final, TypedDict                             ║
    ║                                                               ║
    ║  💡 mypy로 타입 체크:                                          ║
    ║    mypy your_file.py --strict                                 ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    main()

