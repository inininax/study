"""
01_reference_counting.py - 참조 카운팅 이해

📌 핵심 개념:
    CPython은 참조 카운팅으로 메모리를 관리합니다.
    객체의 참조 수가 0이 되면 즉시 해제됩니다.

🔄 다른 언어 비교:
    - Java/Go: 지연된 GC (Mark & Sweep)
    - Python: 즉시 해제 (참조 카운팅)

📚 참고: https://docs.python.org/3/c-api/intro.html#reference-counts
"""

from __future__ import annotations

import gc
import sys


def reference_count_demo() -> None:
    """참조 카운팅 시연."""
    print("📌 참조 카운팅 기본")
    print("=" * 50)
    
    # 객체 생성
    obj = [1, 2, 3]
    # getrefcount는 인자로 전달할 때 +1되므로 1을 빼서 출력
    print(f"생성 직후: {sys.getrefcount(obj) - 1}")
    
    # 참조 추가
    ref1 = obj
    print(f"ref1 = obj 후: {sys.getrefcount(obj) - 1}")
    
    ref2 = obj
    print(f"ref2 = obj 후: {sys.getrefcount(obj) - 1}")
    
    # 리스트에 추가
    container = [obj]
    print(f"리스트에 추가 후: {sys.getrefcount(obj) - 1}")
    
    # 참조 제거
    del ref1
    print(f"del ref1 후: {sys.getrefcount(obj) - 1}")
    
    del ref2
    print(f"del ref2 후: {sys.getrefcount(obj) - 1}")
    
    container.clear()
    print(f"container.clear() 후: {sys.getrefcount(obj) - 1}")


def destructor_timing_demo() -> None:
    """소멸자 호출 시점 시연."""
    print("\n📌 소멸자 호출 시점")
    print("=" * 50)
    
    class Resource:
        def __init__(self, name: str) -> None:
            self.name = name
            print(f"  {name} 생성")
        
        def __del__(self) -> None:
            print(f"  {self.name} 소멸")
    
    print("순환 참조 없는 경우:")
    r = Resource("Resource1")
    del r  # 즉시 소멸
    print("  del r 완료")
    
    print("\n순환 참조 있는 경우:")
    
    class Node:
        def __init__(self, name: str) -> None:
            self.name = name
            self.partner: Node | None = None
        
        def __del__(self) -> None:
            print(f"  {self.name} 소멸")
    
    a = Node("A")
    b = Node("B")
    a.partner = b
    b.partner = a  # 순환!
    
    del a
    del b
    print("  del a, b 완료 - 아직 소멸 안 됨!")
    
    gc.collect()  # 순환 GC 실행
    print("  gc.collect() 완료")


def gc_stats_demo() -> None:
    """GC 통계 확인."""
    print("\n📌 GC 통계")
    print("=" * 50)
    
    gc.collect()
    
    print(f"gc.get_count(): {gc.get_count()}")
    print("  (각 세대의 할당 - 해제 횟수)")
    
    print(f"\ngc.get_threshold(): {gc.get_threshold()}")
    print("  (각 세대의 GC 트리거 임계값)")
    
    print("\n세대별 통계:")
    for i, stat in enumerate(gc.get_stats()):
        print(f"  Generation {i}:")
        print(f"    collections: {stat['collections']}")
        print(f"    collected: {stat['collected']}")
        print(f"    uncollectable: {stat['uncollectable']}")


def main() -> None:
    """메인 실행."""
    reference_count_demo()
    destructor_timing_demo()
    gc_stats_demo()


if __name__ == "__main__":
    main()

