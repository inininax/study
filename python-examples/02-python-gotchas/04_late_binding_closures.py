"""
04_late_binding_closures.py - 🟠 Late Binding Closures

📌 핵심 개념:
    Python 클로저는 변수의 값이 아닌 변수 자체를 캡처합니다.
    루프 안에서 람다를 생성하면, 모든 람다가 마지막 값을 참조합니다.

🔄 다른 언어 비교:
    - Java: 람다는 effectively final 변수만 캡처 (이 문제 없음)
    - Go: 같은 문제 있음! 변수를 루프 내부에서 복사해야 함
    - JavaScript: var는 같은 문제, let은 블록 스코프로 해결
    - Python: 기본적으로 late binding (지연 바인딩)

⚠️ 주의사항:
    이벤트 핸들러, 콜백 함수를 루프에서 생성할 때 특히 주의하세요!

📚 참고: https://docs.python.org/3/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-values-all-return-the-same-result
"""

from __future__ import annotations

from typing import Callable


# =============================================================================
# 1️⃣ ❌ 잘못된 패턴 - Late Binding 문제
# =============================================================================

def late_binding_problem_demo() -> None:
    """
    ❌ Late Binding 문제 시연.
    
    💡 Java 개발자를 위한 팁:
        Java에서는 이 문제가 발생하지 않습니다!
        Java 람다는 effectively final 변수만 캡처합니다.
        
        Java (이 문제 없음):
            List<Runnable> actions = new ArrayList<>();
            for (int i = 0; i < 5; i++) {
                int captured = i;  // effectively final
                actions.add(() -> System.out.println(captured));
            }
            
    💡 Go 개발자를 위한 팁:
        Go도 같은 문제가 있습니다!
        
        Go (문제 있음):
            for i := 0; i < 5; i++ {
                funcs = append(funcs, func() { fmt.Println(i) })
            }
            // 모든 함수가 5를 출력
    """
    # ❌ 잘못된 패턴
    functions: list[Callable[[], int]] = []
    
    for i in range(5):
        # 람다가 변수 i를 캡처, 하지만 값이 아닌 변수 자체!
        functions.append(lambda: i)
    
    print("❌ Late Binding 문제:")
    print("  기대값: 0, 1, 2, 3, 4")
    print(f"  실제값: {[f() for f in functions]}")  # [4, 4, 4, 4, 4]
    
    print("""
    ⚠️ 왜 이런 일이?
    - 람다는 변수 i의 '값'이 아닌 '변수 자체'를 캡처
    - 람다가 실행될 때 i의 현재 값을 찾음
    - 루프 종료 후 i는 4이므로, 모든 람다가 4를 반환
    """)


# =============================================================================
# 2️⃣ ✅ 해결책 1: 기본 인자로 값 캡처
# =============================================================================

def solution_default_argument_demo() -> None:
    """
    ✅ 해결책 1: 기본 인자로 현재 값 캡처.
    """
    functions: list[Callable[[], int]] = []
    
    for i in range(5):
        # 기본 인자로 현재 i 값을 캡처!
        functions.append(lambda x=i: x)
    
    print("✅ 기본 인자 해결책:")
    print(f"  결과: {[f() for f in functions]}")  # [0, 1, 2, 3, 4]
    
    print("""
    💡 왜 동작하는가?
    - 기본 인자는 함수 정의 시점에 평가됨
    - 각 루프에서 현재 i 값이 기본값으로 바인딩됨
    """)


# =============================================================================
# 3️⃣ ✅ 해결책 2: 클로저 팩토리
# =============================================================================

def solution_closure_factory_demo() -> None:
    """
    ✅ 해결책 2: 클로저 팩토리 함수 사용.
    """
    def make_func(x: int) -> Callable[[], int]:
        """x 값을 반환하는 함수를 생성."""
        return lambda: x
    
    functions = [make_func(i) for i in range(5)]
    
    print("✅ 클로저 팩토리 해결책:")
    print(f"  결과: {[f() for f in functions]}")  # [0, 1, 2, 3, 4]
    
    print("""
    💡 왜 동작하는가?
    - make_func가 호출될 때 x는 지역 변수
    - 각 클로저는 자신만의 x를 가짐
    """)


# =============================================================================
# 4️⃣ ✅ 해결책 3: functools.partial
# =============================================================================

def solution_partial_demo() -> None:
    """
    ✅ 해결책 3: functools.partial 사용.
    """
    from functools import partial
    
    def print_value(x: int) -> int:
        return x
    
    functions = [partial(print_value, i) for i in range(5)]
    
    print("✅ partial 해결책:")
    print(f"  결과: {[f() for f in functions]}")  # [0, 1, 2, 3, 4]


# =============================================================================
# 5️⃣ 실제 예시: 버튼 이벤트 핸들러
# =============================================================================

def button_handler_demo() -> None:
    """
    실제 예시: GUI 버튼 이벤트 핸들러.
    """
    class Button:
        """간단한 버튼 시뮬레이션."""
        def __init__(self, label: str) -> None:
            self.label = label
            self.on_click: Callable[[], None] | None = None
        
        def click(self) -> None:
            if self.on_click:
                self.on_click()
    
    buttons: list[Button] = []
    button_names = ["Save", "Load", "Exit"]
    
    # ❌ 잘못된 패턴
    print("❌ 잘못된 버튼 핸들러:")
    for name in button_names:
        btn = Button(name)
        btn.on_click = lambda: print(f"  Clicked: {name}")
        buttons.append(btn)
    
    for btn in buttons:
        print(f"  {btn.label} 버튼 클릭 →", end=" ")
        btn.click()  # 모두 "Exit" 출력!
    
    # ✅ 올바른 패턴
    print("\n✅ 올바른 버튼 핸들러:")
    buttons = []
    for name in button_names:
        btn = Button(name)
        btn.on_click = lambda n=name: print(f"  Clicked: {n}")
        buttons.append(btn)
    
    for btn in buttons:
        print(f"  {btn.label} 버튼 클릭 →", end=" ")
        btn.click()


# =============================================================================
# 6️⃣ 실제 예시: 딕셔너리에 함수 저장
# =============================================================================

def dict_functions_demo() -> None:
    """
    딕셔너리에 함수를 저장하는 패턴.
    """
    # ❌ 잘못된 패턴
    operations: dict[str, Callable[[int], int]] = {}
    
    for op_name, multiplier in [("double", 2), ("triple", 3), ("quadruple", 4)]:
        operations[op_name] = lambda x: x * multiplier
    
    print("❌ 잘못된 딕셔너리 함수:")
    for name, func in operations.items():
        print(f"  {name}(10) = {func(10)}")  # 모두 40!
    
    # ✅ 올바른 패턴
    operations = {}
    
    for op_name, multiplier in [("double", 2), ("triple", 3), ("quadruple", 4)]:
        operations[op_name] = lambda x, m=multiplier: x * m
    
    print("\n✅ 올바른 딕셔너리 함수:")
    for name, func in operations.items():
        print(f"  {name}(10) = {func(10)}")


# =============================================================================
# 7️⃣ 요약
# =============================================================================

def summary() -> None:
    """
    Late Binding 요약.
    """
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                 🟠 Late Binding Closures 규칙                  ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║                                                               ║
    ║  ❌ 문제가 되는 패턴:                                          ║
    ║                                                               ║
    ║     funcs = []                                                ║
    ║     for i in range(5):                                        ║
    ║         funcs.append(lambda: i)  # 모두 마지막 값!            ║
    ║                                                               ║
    ║  ✅ 해결책 1: 기본 인자                                        ║
    ║                                                               ║
    ║     funcs.append(lambda x=i: x)  # 현재 값 캡처               ║
    ║                                                               ║
    ║  ✅ 해결책 2: 클로저 팩토리                                    ║
    ║                                                               ║
    ║     def make_func(x):                                         ║
    ║         return lambda: x                                      ║
    ║     funcs.append(make_func(i))                                ║
    ║                                                               ║
    ║  ✅ 해결책 3: functools.partial                                ║
    ║                                                               ║
    ║     from functools import partial                             ║
    ║     funcs.append(partial(func, i))                            ║
    ║                                                               ║
    ║  💡 기억하세요:                                                ║
    ║     클로저는 변수의 '값'이 아닌 '변수 자체'를 캡처합니다!     ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)


# =============================================================================
# 메인 실행
# =============================================================================

def main() -> None:
    """예제 실행."""
    demos = [
        ("1️⃣ Late Binding 문제", late_binding_problem_demo),
        ("2️⃣ 해결책: 기본 인자", solution_default_argument_demo),
        ("3️⃣ 해결책: 클로저 팩토리", solution_closure_factory_demo),
        ("4️⃣ 해결책: partial", solution_partial_demo),
        ("5️⃣ 버튼 핸들러 예시", button_handler_demo),
        ("6️⃣ 딕셔너리 함수 예시", dict_functions_demo),
        ("7️⃣ 요약", summary),
    ]
    
    print("=" * 60)
    print("🟠 Late Binding Closures")
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

