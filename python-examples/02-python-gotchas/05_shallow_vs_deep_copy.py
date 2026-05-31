"""
05_shallow_vs_deep_copy.py - 🟠 얕은 복사 vs 깊은 복사

📌 핵심 개념:
    - 얕은 복사 (Shallow Copy): 최상위 객체만 복사, 내부 객체는 참조 공유
    - 깊은 복사 (Deep Copy): 모든 중첩 객체까지 재귀적으로 복사
    
    Python의 list[:], copy.copy()는 얕은 복사입니다!

🔄 다른 언어 비교:
    - Java: clone()은 얕은 복사, 깊은 복사는 직접 구현
    - Go: 슬라이스 복사는 얕은 복사, copy() 내장 함수
    - Kotlin: toMutableList()는 얕은 복사
    - Python: copy, deepcopy 모듈 제공

⚠️ 주의사항:
    중첩 리스트/딕셔너리를 복사할 때 특히 주의하세요!

📚 참고: https://docs.python.org/3/library/copy.html
"""

from __future__ import annotations

import copy
from typing import Any


# =============================================================================
# 1️⃣ 할당 vs 복사
# =============================================================================

def assignment_vs_copy_demo() -> None:
    """
    할당과 복사의 차이.
    
    💡 Java 개발자를 위한 팁:
        Java에서 참조 타입 할당은 참조 복사와 같습니다.
        Python도 마찬가지입니다.
    """
    # 할당 = 같은 객체 참조
    original = [1, 2, 3]
    assigned = original
    
    print("할당 (Assignment):")
    print(f"  original = {original}")
    print(f"  assigned = original")
    print(f"  original is assigned: {original is assigned}")  # True
    
    assigned.append(4)
    print(f"\n  assigned.append(4) 후:")
    print(f"  original = {original}")  # [1, 2, 3, 4]
    print(f"  assigned = {assigned}")  # [1, 2, 3, 4]
    
    # 얕은 복사 = 새 객체, 하지만 내부는 참조
    original = [1, 2, 3]
    copied = original.copy()  # 또는 original[:] 또는 list(original)
    
    print("\n얕은 복사 (Shallow Copy):")
    print(f"  original = {original}")
    print(f"  copied = original.copy()")
    print(f"  original is copied: {original is copied}")  # False
    
    copied.append(4)
    print(f"\n  copied.append(4) 후:")
    print(f"  original = {original}")  # [1, 2, 3]
    print(f"  copied = {copied}")  # [1, 2, 3, 4]


# =============================================================================
# 2️⃣ ⚠️ 얕은 복사의 함정
# =============================================================================

def shallow_copy_gotcha_demo() -> None:
    """
    얕은 복사의 함정 - 중첩 객체.
    """
    # 중첩 리스트
    original = [[1, 2], [3, 4], [5, 6]]
    shallow = original.copy()  # 얕은 복사
    
    print("⚠️ 중첩 리스트의 얕은 복사:")
    print(f"  original = {original}")
    print(f"  shallow = original.copy()")
    print(f"  original is shallow: {original is shallow}")  # False
    print(f"  original[0] is shallow[0]: {original[0] is shallow[0]}")  # True!
    
    # 내부 리스트 수정
    shallow[0].append(999)
    print(f"\n  shallow[0].append(999) 후:")
    print(f"  original = {original}")  # [[1, 2, 999], ...]!
    print(f"  shallow = {shallow}")
    
    print("""
    ⚠️ 왜 이런 일이?
    - 얕은 복사는 최상위 리스트만 새로 생성
    - 내부 리스트 [1, 2]는 여전히 같은 객체를 참조
    """)


# =============================================================================
# 3️⃣ ✅ 깊은 복사
# =============================================================================

def deep_copy_demo() -> None:
    """
    깊은 복사로 문제 해결.
    """
    original = [[1, 2], [3, 4], [5, 6]]
    deep = copy.deepcopy(original)  # 깊은 복사
    
    print("✅ 깊은 복사:")
    print(f"  original = {original}")
    print(f"  deep = copy.deepcopy(original)")
    print(f"  original is deep: {original is deep}")  # False
    print(f"  original[0] is deep[0]: {original[0] is deep[0]}")  # False!
    
    # 내부 리스트 수정
    deep[0].append(999)
    print(f"\n  deep[0].append(999) 후:")
    print(f"  original = {original}")  # [[1, 2], ...] - 변경 없음!
    print(f"  deep = {deep}")  # [[1, 2, 999], ...]


# =============================================================================
# 4️⃣ 딕셔너리 복사
# =============================================================================

def dict_copy_demo() -> None:
    """
    딕셔너리 복사도 같은 문제.
    """
    # 중첩 딕셔너리
    original: dict[str, Any] = {
        "user": {"name": "Kim", "age": 30},
        "settings": {"theme": "dark"}
    }
    
    # 얕은 복사
    shallow = original.copy()  # 또는 dict(original) 또는 {**original}
    
    print("딕셔너리 얕은 복사:")
    shallow["user"]["age"] = 31
    print(f"  shallow['user']['age'] = 31 후:")
    print(f"  original['user']['age'] = {original['user']['age']}")  # 31!
    
    # 깊은 복사
    original["user"]["age"] = 30  # 원복
    deep = copy.deepcopy(original)
    
    print("\n딕셔너리 깊은 복사:")
    deep["user"]["age"] = 31
    print(f"  deep['user']['age'] = 31 후:")
    print(f"  original['user']['age'] = {original['user']['age']}")  # 30


# =============================================================================
# 5️⃣ 다양한 복사 방법
# =============================================================================

def copy_methods_demo() -> None:
    """
    다양한 복사 방법 비교.
    """
    original = [1, 2, [3, 4]]
    
    print("다양한 얕은 복사 방법:")
    methods = [
        ("list.copy()", original.copy()),
        ("list[:]", original[:]),
        ("list(original)", list(original)),
        ("copy.copy()", copy.copy(original)),
    ]
    
    for name, copied in methods:
        print(f"  {name}: {copied}")
        print(f"    is original: {copied is original}")
        print(f"    [2] is original[2]: {copied[2] is original[2]}")
    
    print("\n깊은 복사:")
    deep = copy.deepcopy(original)
    print(f"  copy.deepcopy(): {deep}")
    print(f"    is original: {deep is original}")
    print(f"    [2] is original[2]: {deep[2] is original[2]}")


# =============================================================================
# 6️⃣ 커스텀 객체의 복사
# =============================================================================

def custom_object_copy_demo() -> None:
    """
    커스텀 객체의 복사.
    """
    class Node:
        def __init__(self, value: int, children: list["Node"] | None = None) -> None:
            self.value = value
            self.children = children or []
        
        def __repr__(self) -> str:
            return f"Node({self.value}, children={len(self.children)})"
    
    # 트리 구조
    child1 = Node(2)
    child2 = Node(3)
    root = Node(1, [child1, child2])
    
    print("커스텀 객체 복사:")
    print(f"  root = {root}")
    
    # 얕은 복사
    shallow_root = copy.copy(root)
    print(f"\n  얕은 복사 후:")
    print(f"  shallow_root is root: {shallow_root is root}")
    print(f"  shallow_root.children[0] is root.children[0]: "
          f"{shallow_root.children[0] is root.children[0]}")
    
    # 깊은 복사
    deep_root = copy.deepcopy(root)
    print(f"\n  깊은 복사 후:")
    print(f"  deep_root is root: {deep_root is root}")
    print(f"  deep_root.children[0] is root.children[0]: "
          f"{deep_root.children[0] is root.children[0]}")


# =============================================================================
# 7️⃣ 요약
# =============================================================================

def summary() -> None:
    """
    복사 방법 요약.
    """
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║              🟠 얕은 복사 vs 깊은 복사 정리                    ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║                                                               ║
    ║  할당 (Assignment):                                           ║
    ║    b = a  → 같은 객체 참조                                    ║
    ║                                                               ║
    ║  얕은 복사 (Shallow Copy):                                    ║
    ║    - list.copy(), list[:], dict.copy(), {**d}                ║
    ║    - copy.copy(obj)                                           ║
    ║    - 최상위만 복사, 내부 객체는 참조 공유                     ║
    ║                                                               ║
    ║  깊은 복사 (Deep Copy):                                       ║
    ║    - copy.deepcopy(obj)                                       ║
    ║    - 모든 중첩 객체까지 재귀적 복사                           ║
    ║                                                               ║
    ║  ⚠️ 주의:                                                      ║
    ║    - 중첩 리스트/딕셔너리는 deepcopy 필요                     ║
    ║    - deepcopy는 느리므로 필요할 때만 사용                     ║
    ║    - 순환 참조가 있으면 deepcopy가 처리함                     ║
    ║                                                               ║
    ║  💡 선택 가이드:                                               ║
    ║    - 단순 리스트 (중첩 없음): 얕은 복사 OK                    ║
    ║    - 중첩 구조: deepcopy 사용                                 ║
    ║    - 성능 중요: 필요한 부분만 직접 복사                       ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)


# =============================================================================
# 메인 실행
# =============================================================================

def main() -> None:
    """예제 실행."""
    demos = [
        ("1️⃣ 할당 vs 복사", assignment_vs_copy_demo),
        ("2️⃣ 얕은 복사 함정", shallow_copy_gotcha_demo),
        ("3️⃣ 깊은 복사", deep_copy_demo),
        ("4️⃣ 딕셔너리 복사", dict_copy_demo),
        ("5️⃣ 복사 방법", copy_methods_demo),
        ("6️⃣ 커스텀 객체", custom_object_copy_demo),
        ("7️⃣ 요약", summary),
    ]
    
    print("=" * 60)
    print("🟠 얕은 복사 vs 깊은 복사")
    print("=" * 60)
    print()
    
    for title, demo_func in demos:
        print("-" * 60)
        print(f"📌 {title}")
        print("-" * 60)
        demo_func()
        print()


if __name__ == "__main__":
    main()

