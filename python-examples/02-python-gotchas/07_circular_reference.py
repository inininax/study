"""
07_circular_reference.py - 🟡 순환 참조와 메모리

📌 핵심 개념:
    Python은 참조 카운팅 + 순환 GC로 메모리를 관리합니다.
    순환 참조가 있으면 참조 카운팅만으로 해제되지 않습니다.
    __del__ 메서드가 있으면 순환 GC도 제대로 동작하지 않을 수 있습니다.

🔄 다른 언어 비교:
    - Java: Mark & Sweep GC로 순환 참조 처리
    - Go: Mark & Sweep GC로 순환 참조 처리
    - Python: 참조 카운팅 + 순환 GC 조합

⚠️ 주의사항:
    - __del__ 사용 시 순환 참조 주의
    - weakref로 순환 참조 방지 가능
    - 명시적으로 참조 해제하는 것이 안전

📚 참고: https://docs.python.org/3/library/gc.html
"""

from __future__ import annotations

import gc
import weakref
from typing import Any


# =============================================================================
# 1️⃣ 참조 카운팅 기본
# =============================================================================

def reference_counting_demo() -> None:
    """
    Python의 참조 카운팅.
    
    💡 Java/Go 개발자를 위한 팁:
        Java/Go는 지연된 GC를 사용합니다.
        Python은 참조 카운트가 0이 되면 즉시 해제합니다.
    """
    import sys
    
    print("참조 카운팅:")
    
    # 객체 생성
    obj = [1, 2, 3]
    print(f"  생성 직후 참조 수: {sys.getrefcount(obj) - 1}")  # -1은 getrefcount 인자
    
    # 참조 추가
    ref1 = obj
    print(f"  ref1 = obj 후: {sys.getrefcount(obj) - 1}")
    
    ref2 = obj
    print(f"  ref2 = obj 후: {sys.getrefcount(obj) - 1}")
    
    # 참조 제거
    del ref2
    print(f"  del ref2 후: {sys.getrefcount(obj) - 1}")
    
    del ref1
    print(f"  del ref1 후: {sys.getrefcount(obj) - 1}")
    
    # obj가 마지막 참조 - del obj 하면 즉시 해제됨


# =============================================================================
# 2️⃣ 순환 참조 문제
# =============================================================================

def circular_reference_demo() -> None:
    """
    순환 참조가 발생하는 경우.
    """
    print("순환 참조:")
    
    class Node:
        def __init__(self, name: str) -> None:
            self.name = name
            self.partner: Node | None = None
        
        def __del__(self) -> None:
            print(f"    {self.name} 해제됨")
    
    # 순환 참조 없이
    print("\n  순환 참조 없는 경우:")
    a = Node("A")
    del a  # 즉시 해제
    
    # 순환 참조 발생
    print("\n  순환 참조 발생:")
    x = Node("X")
    y = Node("Y")
    x.partner = y  # X → Y
    y.partner = x  # Y → X (순환!)
    
    print("    del x, y 실행...")
    del x
    del y
    # __del__이 호출되지 않을 수 있음!
    
    print("    gc.collect() 실행...")
    gc.collect()  # 순환 GC 강제 실행


# =============================================================================
# 3️⃣ 실제 예시: 부모-자식 관계
# =============================================================================

def parent_child_demo() -> None:
    """
    부모-자식 관계에서의 순환 참조.
    """
    print("부모-자식 순환 참조:")
    
    # ❌ 순환 참조 발생
    class Parent:
        def __init__(self, name: str) -> None:
            self.name = name
            self.children: list[Child] = []
        
        def add_child(self, child: "Child") -> None:
            self.children.append(child)
            child.parent = self  # 순환!
    
    class Child:
        def __init__(self, name: str) -> None:
            self.name = name
            self.parent: Parent | None = None
    
    parent = Parent("Parent")
    child1 = Child("Child1")
    child2 = Child("Child2")
    
    parent.add_child(child1)
    parent.add_child(child2)
    
    print(f"  parent.children: {[c.name for c in parent.children]}")
    print(f"  child1.parent: {child1.parent.name if child1.parent else None}")
    
    # 순환: parent → children → child → parent
    print("  ⚠️ 순환 참조 발생: parent → children → child → parent")


# =============================================================================
# 4️⃣ ✅ weakref로 해결
# =============================================================================

def weakref_solution_demo() -> None:
    """
    weakref를 사용하여 순환 참조 방지.
    """
    print("weakref로 순환 참조 방지:")
    
    class Parent:
        def __init__(self, name: str) -> None:
            self.name = name
            self.children: list["Child"] = []
        
        def add_child(self, child: "Child") -> None:
            self.children.append(child)
            child.parent = weakref.ref(self)  # 약한 참조!
        
        def __del__(self) -> None:
            print(f"    Parent '{self.name}' 해제됨")
    
    class Child:
        def __init__(self, name: str) -> None:
            self.name = name
            self.parent: weakref.ref[Parent] | None = None
        
        def get_parent(self) -> Parent | None:
            if self.parent:
                return self.parent()  # weakref 역참조
            return None
        
        def __del__(self) -> None:
            print(f"    Child '{self.name}' 해제됨")
    
    print("\n  객체 생성:")
    parent = Parent("Parent")
    child = Child("Child")
    parent.add_child(child)
    
    print(f"  child.get_parent(): {child.get_parent()}")
    
    print("\n  del parent 실행:")
    del parent
    
    # 부모가 해제된 후 자식에서 접근
    print(f"  child.get_parent() (부모 해제 후): {child.get_parent()}")
    
    print("\n  del child 실행:")
    del child


# =============================================================================
# 5️⃣ weakref 패턴
# =============================================================================

def weakref_patterns_demo() -> None:
    """
    weakref 활용 패턴.
    """
    print("weakref 패턴:")
    
    # 1. 캐시 (WeakValueDictionary)
    print("\n  1. 캐시 (WeakValueDictionary):")
    
    class ExpensiveObject:
        def __init__(self, id: int) -> None:
            self.id = id
            print(f"    ExpensiveObject({id}) 생성")
        
        def __del__(self) -> None:
            print(f"    ExpensiveObject({self.id}) 해제")
    
    cache: weakref.WeakValueDictionary[int, ExpensiveObject] = weakref.WeakValueDictionary()
    
    # 캐시에 저장
    obj1 = ExpensiveObject(1)
    cache[1] = obj1
    print(f"    cache[1]: {cache.get(1)}")
    
    # obj1 참조 해제
    del obj1
    gc.collect()
    print(f"    del obj1 후 cache[1]: {cache.get(1)}")  # None
    
    # 2. 콜백 (weakref.finalize)
    print("\n  2. 정리 콜백 (weakref.finalize):")
    
    class Resource:
        def __init__(self, name: str) -> None:
            self.name = name
            # __del__ 대신 finalize 사용
            self._finalizer = weakref.finalize(
                self, 
                lambda n: print(f"    Resource '{n}' 정리됨"),
                name
            )
    
    res = Resource("MyResource")
    del res
    gc.collect()


# =============================================================================
# 6️⃣ gc 모듈 활용
# =============================================================================

def gc_module_demo() -> None:
    """
    gc 모듈로 순환 참조 탐지.
    """
    print("gc 모듈 활용:")
    
    # 순환 참조 생성
    class Node:
        def __init__(self) -> None:
            self.ref: Node | None = None
    
    # 순환 참조 생성
    gc.collect()  # 기존 가비지 정리
    gc.set_debug(0)  # 디버그 출력 비활성화
    
    nodes = []
    for i in range(5):
        n1 = Node()
        n2 = Node()
        n1.ref = n2
        n2.ref = n1
        nodes.append((n1, n2))
    
    # 참조 해제
    del nodes
    
    # 순환 참조 수집 전
    unreachable_before = gc.collect()
    print(f"  수집된 순환 참조 객체 수: {unreachable_before}")
    
    # gc 통계
    print(f"\n  gc.get_stats():")
    for i, stat in enumerate(gc.get_stats()):
        print(f"    Generation {i}: collections={stat['collections']}, collected={stat['collected']}")


# =============================================================================
# 7️⃣ 요약
# =============================================================================

def summary() -> None:
    """
    순환 참조 요약.
    """
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                  🟡 순환 참조 관리 규칙                        ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║                                                               ║
    ║  Python 메모리 관리:                                          ║
    ║    1. 참조 카운팅 - 즉시 해제                                 ║
    ║    2. 순환 GC - 주기적으로 순환 참조 수집                     ║
    ║                                                               ║
    ║  순환 참조가 문제되는 경우:                                   ║
    ║    - __del__ 메서드가 있을 때                                 ║
    ║    - 파일 핸들, 네트워크 연결 등 리소스 보유                  ║
    ║    - 대용량 데이터를 참조할 때                                ║
    ║                                                               ║
    ║  ✅ 해결책:                                                    ║
    ║                                                               ║
    ║    1. weakref 사용                                            ║
    ║       parent = weakref.ref(obj)                               ║
    ║                                                               ║
    ║    2. 명시적 정리 메서드                                      ║
    ║       def close(self):                                        ║
    ║           self.parent = None                                  ║
    ║                                                               ║
    ║    3. Context Manager 사용                                    ║
    ║       with Resource() as r:                                   ║
    ║           ...                                                 ║
    ║                                                               ║
    ║    4. weakref.finalize 사용 (__del__ 대신)                    ║
    ║                                                               ║
    ║  💡 권장 사항:                                                 ║
    ║    - __del__ 사용 최소화                                      ║
    ║    - 양방향 참조 시 한쪽은 weakref                            ║
    ║    - 리소스는 Context Manager로 관리                          ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)


# =============================================================================
# 메인 실행
# =============================================================================

def main() -> None:
    """예제 실행."""
    demos = [
        ("1️⃣ 참조 카운팅", reference_counting_demo),
        ("2️⃣ 순환 참조", circular_reference_demo),
        ("3️⃣ 부모-자식 관계", parent_child_demo),
        ("4️⃣ weakref 해결책", weakref_solution_demo),
        ("5️⃣ weakref 패턴", weakref_patterns_demo),
        ("6️⃣ gc 모듈", gc_module_demo),
        ("7️⃣ 요약", summary),
    ]
    
    print("=" * 60)
    print("🟡 순환 참조와 메모리")
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

